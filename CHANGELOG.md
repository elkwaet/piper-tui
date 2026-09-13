# Changelog

All notable changes to this project will be documented in this file.

## [v0.3.0] - 2026-09-13
### Added
- Complete automated global shortcut support for all major Linux Desktop Environments (KDE Plasma, XFCE, Cinnamon, MATE, LXQt, Pantheon, GNOME/Zorin).
- Added Wiki documentation for standalone Window Managers configuration (i3, Sway, Openbox, bspwm).
- Dynamic DE detection and specific UI prompts matching the user's active desktop environment capabilities.

## [v0.2.1] - 2026-09-13
### Added
- Shortcut presets (`<Super><Shift>s`, `<Primary><Alt>s`, `<Primary>Escape`, etc.) in the TUI to avoid manual chevron input.
- Detailed syntax helper box explaining GNOME modifier names (`<Primary>` = Ctrl, `<Super>` = Windows).
- Direct shortcut action to launch the desktop GUI Settings (`gnome-control-center keyboard`).

## [v0.2.0] - 2026-09-13
### Added
- Automated global keyboard shortcut manager for GNOME / Zorin OS / Ubuntu environments via `gsettings`.
- Dedicated voices storage in `~/.piper/voices/` with local installation indicators `[✓ Installé]`.
- Clean terminal download progress bar.
- Dynamic active voice name indicator in the main menu.

## [v0.1.0] - 2026-09-13
### Added
- Initial release of the Piper TUI.
- Bash script using `whiptail` for terminal interaction.
- Automatic download of the Piper Text-to-Speech engine.
- Interactive menu to browse, download, and switch between French voices (Siwis, Gilles).
- Generation of the `read-selection.sh` integration script.
- Saved state and settings in `~/.config/piper-tui/config.env`.
