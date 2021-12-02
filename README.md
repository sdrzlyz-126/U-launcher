[![Build Status](https://travis-ci.org/Ulauncher/Ulauncher.svg?branch=dev)](https://travis-ci.org/Ulauncher/Ulauncher)


[Application Launcher for Linux 🐧](https://ulauncher.io)
================================

Ulauncher is a fast application launcher for Linux. It's is written in Python, using GTK+, and features: App Search (fuzzy matching), Calculator, [Extensions](https://ext.ulauncher.io/), Shortcuts, File browser mode and [Custom Color Themes](https://docs.ulauncher.io/en/latest/themes/themes.html)

| App Search | File Browser | Color Themes |
---|---|---
|![screenshot](https://i.imgur.com/8FpJLGG.png?1)|![screenshot](https://i.imgur.com/wJvXSmP.png?1)|![screenshot](https://i.imgur.com/2a4GCW7.png?1)|

For more info or download links see [ulauncher.io](https://ulauncher.io)


### Run Ulauncher on startup

If your distribution uses [Systemd](https://www.freedesktop.org/wiki/Software/systemd/) and the packages includes [ulauncher.service](ulauncher.service), then you can run `ulauncher` on startup by running:

```
systemctl --user enable --now ulauncher
```

If not, then you can open Ulauncher and enable "Launch at Login" in the preferences.


### Known Issues and workarounds

* If you get a black box or border a border around the Ulauncher window, it's likely because your compositor or desktop environment doesn't support shadows. Try turning them off from the settings. For Sway in particular you may need to follow [these instructions](https://github.com/Ulauncher/Ulauncher/issues/230#issuecomment-570736422)
* [Can't map the keys to ALT+SPACE](https://github.com/Ulauncher/Ulauncher/issues/100)
* [Hotkey doesn't work in Wayland when is triggered from certain apps](https://github.com/Ulauncher/Ulauncher/issues/183)
* [Pass custom environment variable to Ulauncher](https://github.com/Ulauncher/Ulauncher/issues/780#issuecomment-912982174)


### Code Contribution


| Project | Contributor-friendly Issues |
---|---
| Ulauncher App | [![GitHub issues by-label](https://img.shields.io/github/issues/Ulauncher/Ulauncher/contributor-friendly.svg?color=3cf014&label=All%20contributor-friendly&style=for-the-badge)](https://github.com/Ulauncher/Ulauncher/labels/contributor-friendly) <br> [![GitHub issues by-label](https://img.shields.io/github/issues/Ulauncher/Ulauncher/Python.svg?color=5319e7&label=Python&style=for-the-badge)](https://github.com/Ulauncher/Ulauncher/labels/Python) <br> [![GitHub issues by-label](https://img.shields.io/github/issues/Ulauncher/Ulauncher/VueJS.svg?color=a553cc&label=VueJS&style=for-the-badge)](https://github.com/Ulauncher/Ulauncher/labels/VueJS) <br> [![GitHub issues by-label](https://img.shields.io/github/issues/Ulauncher/Ulauncher/Linux.svg?color=0e035e&label=Linux&style=for-the-badge)](https://github.com/Ulauncher/Ulauncher/labels/Linux)|
| [Frontend for extensions website](https://github.com/Ulauncher/ext.ulauncher.io) <br> Uses ReactJS | [![GitHub issues by-label](https://img.shields.io/github/issues/Ulauncher/ext.ulauncher.io/contributor-friendly.svg?color=3cf014&label=contributor-friendly&style=for-the-badge)](https://github.com/Ulauncher/ext.ulauncher.io/labels/contributor-friendly)|
| [API for extensions website](https://github.com/Ulauncher/ext-api.ulauncher.io) <br> Uses Python and bottle library | [![GitHub issues by-label](https://img.shields.io/github/issues/Ulauncher/ext-api.ulauncher.io/contributor-friendly.svg?color=3cf014&label=contributor-friendly&style=for-the-badge)](https://github.com/Ulauncher/ext-api.ulauncher.io/labels/contributor-friendly)|

Contributions are appreciated, but before you put a the work in please ensure that it's a feature or improvement we want by creating an [issue](https://github.com/Ulauncher/Ulauncher/issues) for it if there isn't one already. Be aware that we might still not accept the PR depending on the implementation. Issues with the [contributor-friendly](https://github.com/Ulauncher/Ulauncher/labels/contributor-friendly) label are more straight forward to implement without in depth knowledge of the Ulauncher architecture.

### Setup Development Environment

You need the the following:

* [Yarn](https://classic.yarnpkg.com/en/docs/install)
* python3-setuptools (if you have pip, you have it already)
* Application runtime dependencies (if you already installed Ulauncher you should have these)

#### Distro specific instructions

<details>
  <summary>Ubuntu/Debian</summary>

  Install the dependencies

  ```
  sudo apt-get update && sudo apt-get install \
    yarnpkg gobject-introspection libgtk-3-0 libkeybinder-3.0-0 \
    gir1.2-{gtk-3.0,keybinder-3.0,webkit2-4.0,glib-2.0,gdkpixbuf-2.0,notify-0.7,ayatanaappindicator3-0.1} \
    python3-{setuptools,all,gi,dbus,levenshtein}
  ```

</details>

### How to build, run and contribute
1. Fork the repo and clone your fork locally.
1. Create a new branch for your PR
1. Make your changes to the code
1. If you have Ulauncher installed, make sure you stop the background process (`systemctl --user stop ulauncher.service`)
1. `./bin/ulauncher -v` runs the app from the git root directory (`-v` turns on verbose logging), so you can test it.
1. Create a pull request (provide the relevant information suggested by the template)

For GTK-related issues you may want to check out [Useful Resources for a Python GTK Developer](https://github.com/Ulauncher/Ulauncher/wiki/Resources-for-a-Python-GTK-Developer).

If you have any questions, feel free to ask in a Github issue.

There are more developer and maintainer commands provided by the `ul` wrapper. `./ul` lists all of these (note that most of them are only useful to the maintainers and/or requires docker/podman).


### License

See the [LICENSE](LICENSE) file for license rights and limitations (GNU GPL v3.0).
