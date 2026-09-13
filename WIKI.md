# Piper TUI - Wiki

Welcome to the Piper TUI Wiki!

## Global Keyboard Shortcuts Configuration

For supported Desktop Environments (GNOME, Zorin, Ubuntu, Cinnamon, MATE, XFCE, KDE Plasma, LXQt, Pantheon), the Piper TUI script handles the global shortcut configuration automatically via **Option 4** in the menu.

### Window Managers (i3, Sway, Openbox, bspwm)

If you are using a standalone Window Manager (WM), there is no unified CLI standard to inject shortcuts automatically. You must manually add the shortcut to your WM configuration file.

The script to execute is always located at:
`/home/YOUR_USERNAME/.piper/read-selection.sh`

#### i3wm / Sway
Open your config file (`~/.config/i3/config` or `~/.config/sway/config`) and add the following line:
```text
bindsym $mod+Shift+s exec /home/YOUR_USERNAME/.piper/read-selection.sh
```
Reload your configuration:
- i3: `$mod+Shift+c`
- Sway: `$mod+Shift+c`

#### Openbox
Open `~/.config/openbox/rc.xml` and add inside the `<keyboard>` section:
```xml
<keybind key="W-S-s">
  <action name="Execute">
    <command>/home/YOUR_USERNAME/.piper/read-selection.sh</command>
  </action>
</keybind>
```
Reload Openbox: `openbox --reconfigure`

#### bspwm (via sxhkd)
Open `~/.config/sxhkd/sxhkdrc` and add:
```text
super + shift + s
    /home/YOUR_USERNAME/.piper/read-selection.sh
```
Reload sxhkd: `pkill -USR1 -x sxhkd`
