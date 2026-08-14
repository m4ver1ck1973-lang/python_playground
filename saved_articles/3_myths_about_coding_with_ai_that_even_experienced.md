# 3 myths about coding with AI that even experienced developers still believe

It has been four years since large language models first became publicly accessible, and in that relatively short time, [AI has found its way into more workflows](https://www.xda-developers.com/the-ai-automation-tool-nobody-talks-about-just-replaced-my-entire-workflow-setup/) than most of us could've anticipated. Few fields have embraced it quite as enthusiastically as software development, where it has become a fairly ordinary part of the development process. 

There's little doubt that AI has augmented countless tasks for developers, but its rapid adoption has also created a number of assumptions about what AI-assisted programming *can*, and perhaps more importantly, *cannot do*. Some of these myths are easy to dismiss, while the others are so compelling that even experienced developers continue to believe them. Here are some myths about [AI in coding](https://www.xda-developers.com/cant-believe-how-good-ai-coding-model-is-it-isnt-from-openai-or-anthropic/) which are in need of some serious myth-busting. 

## "AI coding makes developers more productive"

### Time saved writing code can just be spent verifying code instead

[AI coding](https://www.howtogeek.com/this-is-what-ai-coding-actually-excels-atand-its-not-what-you-think/) assistants like Claude Code, Cursor, and IDEs like Google Antigravity have made it easier than ever to offload the menial and mechanical parts of software development. The prevalent assumption is that, if AI can handle much of the code writing, developers will have more time to focus on parts of their work that require their higher order thinking skills. And sure enough, most of it sounds reasonable. After all, frontier models are now faster and better at writing code, and with these models aiding the development process, it should naturally translate into [greater productivity](https://www.xda-developers.com/built-ai-powered-learning-system-best-thing-ive-ever-done-for-my-productivity/). 

It was this very assumption that [recent research from the University of Auckland](https://arxiv.org/abs/2605.23135) challenged. The study suggests that the relationship between AI assistance and productivity is more complicated than it appears. In a longitudinal study of professional software engineers, the research found that 82% spent less time writing code, yet their work had broadly shifted from creation toward verifying, evaluating, and correcting AI output.

Although 84% of surveyed engineers continued to report that AI improved their productivity, the share reporting a worsened developer experience in at least one dimension nearly doubled, going from 14% up to 27%. The decline concentrated in flow state and cognitive load, both of which suggest that writing less code does not necessarily mean doing less work. It also implies that the time AI frees up doesn't simply disappear into higher-order work.

## "AI is good enough at code review to catch the problems humans miss"

### AI can simply choose to focus on the wrong problems to solve

The premise behind introducing AI tools into secure coding revolves around a rather intuitive assumption. If AI can process code quicker than the human eye, it should also be better at spotting security vulnerabilities that developers might overlook. It is a compelling proposition, certainly. After all, who can argue that not having a second set of eyes scrutinizing every line of code doesn't sound useful?

A September 2025 [research evaluating GitHub Copilot's Code Review](https://arxiv.org/abs/2509.13650) feature seems to suggest that those eyes may not be looking in the right places.

Researchers from the Department of Computer Science at Toronto Metropolitan University tested the Copilot against a curated set of vulnerable code samples drawn from open-source projects and found that it frequently failed to identify critical vulnerabilities, such as SQL injection, cross-site scripting and insecure deserialization. Its feedback, instead, was more likely to focus on issues like coding style and typographical errors. The authors themselves stress upon retaining manual code audits to ensure software security, and the evidence makes a pretty compelling case for it.

## "AI coding is still just sophisticated autocomplete"

### This attitude understates what agentic coding is capable of

AI coding has come a long way from suggesting or predicting the next line of code, and yet, in most developer discourses across subreddits and tech forums, the perception that these tools are just sophisticated autocomplete remains persistent. To be fair, this was a reasonable characterization of early AI coding assistants, but modern, agentic coding does considerably more than just complete snippets.

Claude Code and OpenAI's Codex CLI can already reason through tasks, modify multiple files, run tests, and iterate on their own work with limited human intervention. In a recent benchmark jointly developed by Epoch AI and nonprofit METR, Claude Opus 4.6 was able to [autonomously reimplement a bioinformatics toolkit](https://epoch.ai/publications/mirrorcode-preliminary-results) with roughly 16,000 lines of Go and more than 40 commands without access to its source code by inferring the program's behavior, developing its own implementation, and satisfying 2,001 end-to-end tests.

This is a task that the researchers believed would take about 2 to 17 weeks of a human engineer's time, although they did not publish a measured human baseline or wall-clock time taken by Opus 4.6. Instead, the benchmark reported token usage metrics and the tests passed. It does, however, evidence that an AI agent can sustain an autonomous software engineering process over a task that the researchers estimate would take a human weeks to complete.

### The industry is moving faster than the narrative around technology

AI-augmented coding seems to have clearly moved beyond the prevalent assumptions surrounding it, and there's no doubt about it seeing as how the industry has been moving at a breakneck pace. That, however, doesn't mean that every perceived benefit survives scrutiny. If anything, the research seems to suggest that AI is changing software development in more complex ways than the prevailing narrative surrounding the technology implies.

---
**Source URL:** https://www.xda-developers.com/x-myths-about-coding-with-ai-that-even-experienced-developers-still-believe/