# Piper TUI

![Screenshot](assets/piper-tui-zero.png)

A modern, terminal-based User Interface (TUI) for managing [Piper TTS](https://github.com/rhasspy/piper) on Linux. This little tool allows users to read any selected text aloud using a keyboard shortcut that you define. You can read aloud any selected text in UI of various apps (web browsers, terminals, IDEs, document readers, and office suites) of your Linux Desktop.

## Features
- **Dual Mode Architecture**: 
  - `piper-tui`: A rich, asynchronous, Python-powered TUI (using the `textual` framework) for a modern experience.
  - `piper-tui-lite`: A minimalist, legacy bash version powered by `whiptail` for environments with strict dependency constraints.
- Automatically installs and sets up the Piper Text-to-Speech engine.
- Browse, download, and switch between high-quality French and English voice models natively via the HuggingFace API.
- Generates a `read-selection.sh` script to dictate selected text from any application.
- **Floating Playback Controller**: Minimalist on-screen widget allowing you to play, pause, or kill current playback at any moment.
- **Global Keyboard Shortcut Manager**: Configure, update, or remove your global shortcut directly from the TUI (Supports GNOME, Cinnamon, MATE, XFCE, KDE, LXQt).

## Requirements
- `wget`
- `xsel` (for X11) or `wl-clipboard` (for Wayland)
- `alsa-utils` (for audio playback)
- `python3` (for the main `piper-tui` app)
- `whiptail` (only if you use `piper-tui-lite`)

### Hardware Requirements
- **CPU**: Any modern 64-bit processor (Highly optimized ONNX runtime, runs smoothly even on older hardware).
- **GPU**: **None required** (100% CPU inference).
- **RAM**: < 100 MB during active playback.
- **Storage**: ~30 MB for the engine + ~15-25 MB per voice model.

## Installation

Choose your preferred installation method:

### 1. One-Liner (Recommended)
Run our automated installation script:
```bash
curl -sSL https://raw.githubusercontent.com/elkwaet/piper-tui/main/net-install.sh | bash
```
> **Tip:** Once installed, restart your terminal (or run `source ~/.bashrc` / `source ~/.zshrc`), then launch with `piper-tui`.

### 2. Manual Archive Download (.tar.gz)
For users preferring not to pipe directly into bash:
```bash
# Download and extract the archive
mkdir -p ~/.piper-tui-app && cd ~/.piper-tui-app
curl -sSL https://github.com/elkwaet/piper-tui/archive/refs/heads/main.tar.gz | tar -xz --strip-components=1

# Install symlinks into ~/.local/bin
./install.sh
```

### 3. From Git
```bash
# Clone the repository
git clone https://github.com/elkwaet/piper-tui.git
cd piper-tui

# Install symlinks into ~/.local/bin
./install.sh
```

## Usage

```bash
# Launch the modern Python TUI
# (Automatically configures an isolated virtual environment on first run)
piper-tui

# Or launch the lightweight bash version
piper-tui-lite

# To uninstall
./uninstall.sh
```

> **Note:** For advanced shortcut configuration and Window Managers setup, please consult the [WIKI](WIKI.md).

## Acknowledgments
This project stands on the shoulders of open-source giants. Massive thanks to:
- **Michael Hansen & the Open Home Foundation** for developing the blazing fast [Piper TTS](https://github.com/OHF-Voice/piper1-gpl) engine.
- **Rhasspy Project & the HuggingFace Community** for training and hosting the incredible [open voice models](https://huggingface.co/rhasspy/piper-voices).

## Authors
- **elkwaet** - *Initial work* - [elkwaet](https://gitlab.com/elkwaet)

## Licence
This project is licensed under the [GNU GPL v3.0](LICENSE).
