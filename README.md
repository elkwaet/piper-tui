# Piper TUI

![Screenshot](assets/piper-tui-zero.png)

A modern, terminal-based User Interface (TUI) for managing [Piper TTS](https://github.com/rhasspy/piper) on Linux.

## Features
- **Dual Mode Architecture**: 
  - `piper-tui`: A rich, asynchronous, Python-powered TUI (using the `textual` framework) for a modern experience.
  - `piper-tui-lite`: A minimalist, legacy bash version powered by `whiptail` for environments with strict dependency constraints.
- Automatically installs the Piper Text-to-Speech engine.
- Browse, download, and switch between high-quality French voice models natively via the HuggingFace API.
- Generates a `read-selection.sh` script to dictate selected text from any app.
- **Global Keyboard Shortcut Manager**: Configure, update, or remove your global shortcut directly from the TUI (Supports GNOME, Cinnamon, MATE, XFCE, KDE, LXQt).

## Requirements
- `wget`
- `xsel` (for X11) or `wl-clipboard` (for Wayland)
- `alsa-utils` (for audio playback)
- `python3` (for the main `piper-tui` app)
- `whiptail` (only if you use `piper-tui-lite`)

## Installation & Usage

```bash
# Clone this repository (or download the source)
git clone https://github.com/elkwaet/piper-tui.git
cd piper-tui/package

# Install globally (creates symlinks in ~/.local/bin)
./install.sh

# You can now run the modern Python TUI from anywhere

# To uninstall
./uninstall.sh (automatically setups a venv)
./piper-tui

# OR run the lightweight bash version
./piper-tui-lite
```

> **Note:** For advanced shortcut configuration and Window Managers setup, please consult the [WIKI](WIKI.md).

## Authors
- **elkwaet** - *Initial work* - [elkwaet](https://github.com/elkwaet)

## Licence
This project is licensed under the MIT License.
