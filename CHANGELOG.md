# Changelog

All notable changes to this project will be documented in this file.

## [v1.2.0] - 2026-09-15
### Added
- **Worldwide Voices Support**: Removed artificial FR/EN limitations, unlocking 170+ official Piper voices across 30+ international languages.
- **Intelligent Quality Sorting**: Voices within each language category are now automatically sorted by engine quality (`high` > `medium` > `low` > `x-low`).
- **Progressive Disclosure**: Clean UX default showing FR/EN voices first, with a dynamic button to unfold the full international catalog on demand.
- **"Installed Only" Quick Filter**: Checkbox toggle to immediately isolate and manage already downloaded voices without scrolling or typing.
- **Theme Persistence**: Dark/Light mode toggle (`d`) is now permanently remembered across restarts via `~/.config/piper-tui/config.env`.
- **Floating Widget Persistence**: Position coordinates of the floating playback widget are automatically preserved upon drag-and-drop (`~/.config/piper-tui/widget_pos.txt`).
- **Ergonomic Drag Grip**: Added a 4px safety border around playback buttons with a `fleur` cursor, preventing accidental clicks on Play/Pause while moving the widget.

### Fixed
- **Debounced Search**: Added a 200ms debounce on the catalog search bar, preventing unnecessary DOM rebuilds and restoring smooth UI performance.
- **Localization**: Ensured all dynamic labels (including international expansion button) adhere to the active locale (`fr` / `en`).

## [v1.1.1] - 2026-09-14
### Changed
- Automated CI/CD mirror pipeline to sync Git tags and release notes directly to GitHub Releases.

## [v1.1.0] - 2026-09-14
### Added
- Native Tkinter floating playback widget with Play, Pause, and Stop controls floating over desktop applications.
- Playback queue synchronization ensuring the widget waits for `aplay` audio buffers to flush before terminating.

### Fixed
- Fixed process termination edge-cases (`pkill -x` preventing shell subshell PID collisions and `SIGKILL` override).

## [v1.0.0] - 2026-09-14
### Added
- Python Textual TUI interface alongside the original lightweight Bash implementation.
- Dynamic Hugging Face voice catalog download and management.
- Multi-language support (English & French) with automatic locale detection.
- Cross-Desktop Environment global shortcut configurator (GNOME, KDE, XFCE, Cinnamon, MATE, LXQt, etc.).

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
