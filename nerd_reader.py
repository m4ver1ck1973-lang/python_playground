# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "textual",
#   "feedparser",
#   "httpx",
#   "trafilatura",
# ]
# ///

import html
import json
import os
import re
import webbrowser
from pathlib import Path

import feedparser
import httpx
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Footer, Header, Markdown, Static, Tree


# ------------------------------------------------------------------------------
# Helper Functions, Configuration & History Loaders
# ------------------------------------------------------------------------------

def clean_html(raw_html: str) -> str:
    """Strip HTML tags and unescape entities for clean terminal rendering."""
    clean_text = re.sub(r"<[^>]+>", "", raw_html)
    return html.unescape(clean_text).strip()


CONFIG_PATH = Path("feeds.json")
HISTORY_PATH = Path("nerd_reader_history.json")

DEFAULT_FEEDS = {
    "Tech News & Mobile": {
        "XDA Developers": "https://www.xda-developers.com/feed/",
        "How-To Geek": "https://www.howtogeek.com/feed/",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index"
    },
    "Linux & Open Source": {
        "Phoronix": "https://www.phoronix.com/phoronix-rss.php",
        "OMG! Ubuntu!": "https://www.omgubuntu.co.uk/feed",
        "Techmint": "https://www.tecmint.com/feed/"
    },
    "Homelab & Self-Hosting": {
        "Self-Hosted Podcast": "https://selfhosted.show/rss",
        "Kube8s & DevOps (CNCF)": "https://www.cncf.io/feed/",
        "ServeTheHome": "https://www.servethehome.com/feed/"
    },
    "Python & Development": {
        "Real Python": "https://realpython.com/atom.xml",
        "Python Software Foundation": "https://blog.python.org/feeds/posts/default",
        "Talk Python To Me": "https://talkpython.fm/episodes/rss"
    },
    "Community & Aggregators": {
        "Hacker News": "https://news.ycombinator.com/rss"
    }
}


def load_feeds() -> dict[str, str]:
    """Load feeds from feeds.json, or create a default config file if missing."""
    if not CONFIG_PATH.exists():
        try:
            CONFIG_PATH.write_text(json.dumps(DEFAULT_FEEDS, indent=4), encoding="utf-8")
        except Exception:
            pass

    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        flat_feeds = {}
        if isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, dict):
                    for site_name, feed_url in val.items():
                        flat_feeds[site_name] = feed_url
                elif isinstance(val, str):
                    flat_feeds[key] = val
            
            if flat_feeds:
                return flat_feeds
    except Exception:
        pass

    fallback_flat = {}
    for key, val in DEFAULT_FEEDS.items():
        if isinstance(val, dict):
            for site_name, feed_url in val.items():
                fallback_flat[site_name] = feed_url
        else:
            fallback_flat[key] = val
    return fallback_flat


def load_history() -> set[str]:
    """Load the set of read article URLs from JSON history file."""
    if HISTORY_PATH.exists():
        try:
            data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return set(data)
        except Exception:
            pass
    return set()


def save_history(history: set[str]) -> None:
    """Save the set of read article URLs to JSON history file."""
    try:
        HISTORY_PATH.write_text(json.dumps(sorted(list(history)), indent=2), encoding="utf-8")
    except Exception:
        pass


# ------------------------------------------------------------------------------
# Application Class
# ------------------------------------------------------------------------------

class NerdReader(App):
    """A TUI RSS Reader for nerd sites."""
    
    CSS = """
    #feed-tree {
        width: 45;  /* Set sidebar to 45 terminal characters wide */
    }

    #content-pane {
        width: 1fr; /* Takes up ALL remaining horizontal space */
    }
    
    #status-bar {
        background: $boost;
        color: $text;
        padding: 0 1;
        margin-bottom: 1;
        border-bottom: solid $accent;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("o", "open_in_browser", "Open Link"),
        ("s", "save_article", "Save Markdown"),
    ]

    # --- Layout & Lifecycle ---

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal():
            yield Tree("Feeds", id="feed-tree")
            
            with VerticalScroll(id="content-pane"):
                yield Static("Select an article to read.", id="status-bar")
                yield Markdown("Select an article from the left to read.", id="article-text")
        yield Footer()
    
    def on_mount(self) -> None:
        """Runs automatically when the app starts up."""
        self.read_urls = load_history()

        feed_tree = self.query_one("#feed-tree", Tree)
        root = feed_tree.root
        root.label = "Nerd Feeds"

        self.feeds = load_feeds()

        for site_name, feed_url in self.feeds.items():
            site_node = root.add(site_name, expand=False)
            self.fetch_feed(site_node, feed_url)

        # Periodically refresh feeds in background every 5 minutes (300s)
        self.set_interval(300, self.refresh_all_feeds)

    # --- Actions (Triggered via BINDINGS) ---

    def action_open_in_browser(self) -> None:
        """Opens the current article's link in your default desktop browser."""
        if hasattr(self, "active_link") and self.active_link:
            webbrowser.open(self.active_link)
            
    def action_save_article(self) -> None:
        """Saves the currently displayed article as a .md file."""
        if not hasattr(self, "active_article_md") or not self.active_article_md:
            self.notify("No article loaded to save!", severity="warning")
            return

        title_str = str(self.active_article_title)

        safe_title = re.sub(r"[^\w\s-]", "", title_str).strip()
        safe_title = re.sub(r"[-\s]+", "_", safe_title).lower()[:50]
        filename = f"{safe_title}.md"

        output_dir = Path("saved_articles")
        output_dir.mkdir(exist_ok=True)
        file_path = output_dir / filename

        try:
            file_path.write_text(self.active_article_md, encoding="utf-8")
            self.notify(f"Saved: {file_path}", title="Article Saved", severity="information")
        except Exception as e:
            self.notify(f"Failed to save: {e}", title="Error", severity="error")

    # --- Event Handlers ---

    def on_key(self, event) -> None:
        """Handle custom navigation keys for the Tree widget."""
        focused = self.focused

        if isinstance(focused, Tree) and focused.cursor_node:
            node = focused.cursor_node

            if event.key == "right":
                if node.children and not node.is_expanded:
                    node.expand()
                elif node.children and node.is_expanded:
                    focused.action_cursor_down()
                event.prevent_default()

            elif event.key == "left":
                if node.children and node.is_expanded:
                    node.collapse()
                elif node.parent:
                    focused.select_node(node.parent)
                event.prevent_default()

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        """Instantly show full untruncated title in the status bar on key nav."""
        node = event.node
        status_bar = self.query_one("#status-bar", Static)

        if node and node.label:
            title = node.data.get("raw_title", str(node.label)) if node.data else str(node.label)
            clean_title = re.sub(r"\[/?[^\]]+\]", "", str(title))
            status_bar.update(f"[bold lightgreen]📖 {clean_title}[/bold lightgreen]")
        else:
            status_bar.update("")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Called when a user clicks or presses Enter on a tree node."""
        node = event.node

        if node.data:
            link = node.data.get("link", "")
            raw_title = node.data.get("raw_title", str(node.label))

            if link and link not in self.read_urls:
                self.read_urls.add(link)
                save_history(self.read_urls)
                node.label = f"[dim]{raw_title}[/dim]"

            self.active_link = link
            article_widget = self.query_one("#article-text", Markdown)

            article_widget.update("*(Fetching full article...)*")

            if link:
                self.fetch_article_body(raw_title, link, node.data.get("summary", ""))

    # --- Async Background Workers ---

    @work(exclusive=False, thread=True)
    def refresh_all_feeds(self) -> None:
        """Background worker that periodically checks all feeds for new posts."""
        feed_tree = self.query_one("#feed-tree", Tree)
        for site_node in feed_tree.root.children:
            site_name = str(site_node.label)
            if site_name in self.feeds:
                self.fetch_feed(site_node, self.feeds[site_name], is_refresh=True)

    @work(exclusive=False, thread=True)
    def fetch_feed(self, site_node, feed_url: str, is_refresh: bool = False) -> None:
        """Background worker thread to fetch feeds without UI freezing."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        try:
            with httpx.Client(follow_redirects=True, timeout=10.0, headers=headers) as client:
                response = client.get(feed_url)
                if response.status_code == 200:
                    parsed_feed = feedparser.parse(response.text)
                else:
                    parsed_feed = feedparser.parse(feed_url)
        except Exception:
            parsed_feed = feedparser.parse(feed_url)

        if not parsed_feed.entries:
            if not is_refresh:
                self.call_from_thread(site_node.add_leaf, "[No posts found or feed blocked]", data={})
            return

        existing_links = set()
        if is_refresh:
            for child in site_node.children:
                if child.data and "link" in child.data:
                    existing_links.add(child.data["link"])

        for entry in parsed_feed.entries[:10]:  # Limit to 10 most recent entries
            link = entry.get("link", "")
            
            if is_refresh and link in existing_links:
                continue

            summary_text = entry.get("summary") or entry.get("description", "")
            raw_title = entry.title

            if link in self.read_urls:
                formatted_label = f"[dim #7f848e]{raw_title}[/dim #7f848e]"
            else:
                formatted_label = f"[bold #61afef]{raw_title}[/bold #61afef]"

            if is_refresh:
                self.call_from_thread(
                    site_node.add_leaf,
                    formatted_label,
                    data={"summary": summary_text, "link": link, "raw_title": raw_title},
                    at_index=0
                )
            else:
                self.call_from_thread(
                    site_node.add_leaf,
                    formatted_label,
                    data={"summary": summary_text, "link": link, "raw_title": raw_title}
                )

    @work(exclusive=False, thread=True)
    def fetch_article_body(self, title: str, link: str, summary: str) -> None:
        """Background worker to fetch full article text without UI stutter."""
        article_widget = self.query_one("#article-text", Markdown)
        
        try:
            import trafilatura
            
            downloaded = trafilatura.fetch_url(link)
            article_md = trafilatura.extract(
                downloaded, 
                output_format="markdown",
                include_links=True,
                include_images=False
            )

            if article_md:
                formatted_content = f"# {title}\n\n{article_md}\n\n---\n**Source URL:** {link}"
            else:
                formatted_content = f"# {title}\n\n{clean_html(summary)}\n\n---\n**Source URL:** {link}"

        except Exception as e:
            clean_sum = clean_html(summary)
            if not clean_sum or clean_sum.lower() == "comments":
                clean_sum = "*No summary provided by feed.*"
            formatted_content = f"*(Error fetching article: {e})*\n\n{clean_sum}\n\n---\n**Source URL:** {link}"

        self.active_article_title = str(title)
        self.active_article_md = formatted_content

        self.call_from_thread(article_widget.update, formatted_content)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = NerdReader()
    app.run()