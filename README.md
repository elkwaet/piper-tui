# Piper TUI

A lightweight, terminal-based User Interface (TUI) for managing [Piper TTS](https://github.com/rhasspy/piper) on Linux.

## Features
- Minimalist terminal UI powered by `whiptail`.
- Automatically installs the Piper Text-to-Speech engine.
- Browse, download, and switch between high-quality French voice models.
- Generates a `read-selection.sh` script to dictate selected text from any app.
- **Global Keyboard Shortcut Manager**: Configure, update, or remove your global shortcut directly from the TUI (GNOME, Zorin OS, Ubuntu).

## Requirements
- `whiptail`
- `wget`
- `xsel` (for X11) or `wl-clipboard` (for Wayland)
- `alsa-utils` (for audio playback)
- `gsettings` (for automated shortcut integration on GNOME/Zorin)

## Installation & Usage

```bash
# Clone this repository (or download the script)
git clone https://github.com/YOUR_GITHUB/piper-tui.git
cd piper-tui/package

# Make the script executable
chmod +x piper-tui.sh

# Run the TUI
./piper-tui.sh
```

## Global Keyboard Shortcut Setup

You can configure the global shortcut directly via **Option 4** in the TUI menu.

Alternatively, for manual setup:
1. Open your system **Settings** > **Keyboard** > **Custom Shortcuts**.
2. Add a new shortcut:
   - **Name:** Read Selection (Piper)
   - **Command:** `/home/YOUR_USERNAME/.piper/read-selection.sh` *(replace `YOUR_USERNAME` with your actual Linux username)*
   - **Shortcut:** `Super + Shift + S` (or any combination you prefer)
3. Select any text on your screen (browser, document, terminal) and press your shortcut to hear it!

## Configuration

Settings are saved in `~/.config/piper-tui/config.env`.
Voices are stored in `~/.piper/voices/`.
 
