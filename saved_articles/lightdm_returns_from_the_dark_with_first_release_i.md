# LightDM returns from the dark with first release in 4 years

[LightDM](https://en.wikipedia.org/wiki/LightDM), Ubuntu’s former display manager, has had its first new release in four years – and the first under a new set of maintainers.

[LightDM v1.33.0](https://github.com/ubuntu/lightdm/releases/tag/1.33.0) is a ‘catch up’ release that adds Qt6 support (Qt5 still works, don’t worry) and clears a backlog of fixes that had built up since the previous release in 2022. There shouldn’t be any breaking changes either, per the release notes.

While it might sound like a sudden revival of a legacy effort, LightDM is still widely used by Linux distributions and desktops.

## LightDM: what is it?

LightDM is a backend that handles logging in to user sessions. A GUI ‘greeter’ sits on top for user interaction. Ubuntu used the unity-greeter, but other distros and desktops roll their own. [Linux Mint switched to LightDM](https://www.omgubuntu.co.uk/2017/04/linux-mint-adopts-lightdm-slick-greeter) in 2017 with slick-greeter as the login screen.

Canonical built LightDM to replace GDM – it [made its debut in Ubuntu 11.10](https://www.omgubuntu.co.uk/2011/08/ubuntu-11-10-lightdm-login-screen-turned) – as a nimble, desktop-agnostic alternative that was easily adaptable.

Ubuntu stopped using LightDM in 2017, when it switched back to GNOME Shell and GDM. Others didn’t, including various Ubuntu flavours. LightDM’s code stayed under Canonical’s auspices but, per original maintainer Robert Ancell, was ‘essentially unmaintained’.

It’s last release was in 2022, and most development activity (reviewing merge requests) stopped in in 2024.

Fast forward to 2026. Questions over its future [were raised by Fedora’s Neal Gompa](https://discourse.ubuntu.com/t/current-status-of-lightdm/29048/13?u=d0od) (as various Fedora spins use LightDM to power their login screens). Cutting a long story short, people keen to continue it stepped up and, with blessing from Ancell, a handover happened.

LightDM is now a community-maintained effort by *Joshua Peisach* and *Neal Gompa*, and contributors no longer need to sign the (contentious) Canonical Contributor License Agreement (CLA). The repo itself remains under the Ubuntu GitHub family.

Canonical’s drawn plenty of flack over the years for going it alone with Unity, Mir, Snap, etc. LightDM’s enduring appeal some 15 years after its debut suggests that, contrary to some narratives, its instincts aren’t always wrong.

*(via [LWN](https://lwn.net/Articles/1087759/))*

---
**Source URL:** https://www.omgubuntu.co.uk/2026/08/lightdm-new-release-new-maintainers