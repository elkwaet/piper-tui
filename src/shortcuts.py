import os
import subprocess
from pathlib import Path
import configparser

HOME_DIR = Path.home()
SCRIPT_PATH = HOME_DIR / ".piper" / "read-selection.sh"

def run_cmd(cmd):
    """Exécute une commande shell et retourne la sortie."""
    try:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def detect_desktop():
    """Détecte l'environnement de bureau courant."""
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if not desktop:
        desktop = os.environ.get("DESKTOP_SESSION", "").lower()
    
    if "gnome" in desktop or "pantheon" in desktop:
        return "gnome"
    elif "cinnamon" in desktop:
        return "cinnamon"
    elif "mate" in desktop:
        return "mate"
    elif "xfce" in desktop:
        return "xfce"
    elif "kde" in desktop or "plasma" in desktop:
        return "kde"
    elif "lxqt" in desktop:
        return "lxqt"
    return "unknown"

class ShortcutManager:
    """Gestionnaire unifié des raccourcis claviers Linux."""
    
    @staticmethod
    def _find_gsettings_path(schema: str, custom_schema: str, list_key: str):
        """Boucle comme le Bash pour trouver le chemin exact du custom-keybinding."""
        current_list = run_cmd(f"gsettings get {schema} {list_key}")
        if not current_list or current_list == "@as []":
            return None, current_list
            
        paths = current_list.replace("[", "").replace("]", "").replace("'", "").split(", ")
        for p in paths:
            if p:
                cmd = run_cmd(f"gsettings get {custom_schema}:{p} command").strip("'")
                if cmd == str(SCRIPT_PATH):
                    return p, current_list
        return None, current_list

    @staticmethod
    def _apply_gsettings(schema: str, custom_schema: str, list_key: str, shortcut: str, base_path: str):
        existing_path, current_list = ShortcutManager._find_gsettings_path(schema, custom_schema, list_key)
        
        if existing_path:
            path_to_use = existing_path
        else:
            import time
            path_to_use = f"{base_path}custom{int(time.time())}/"
            if current_list == "@as []" or not current_list:
                new_list = f"['{path_to_use}']"
            else:
                new_list = current_list.replace("]", f", '{path_to_use}']")
            run_cmd(f"gsettings set {schema} {list_key} \"{new_list}\"")
            
        run_cmd(f"gsettings set {custom_schema}:{path_to_use} name 'Piper TTS'")
        run_cmd(f"gsettings set {custom_schema}:{path_to_use} command '{SCRIPT_PATH}'")
        run_cmd(f"gsettings set {custom_schema}:{path_to_use} binding '{shortcut}'")
        return True

    @staticmethod
    def _remove_gsettings(schema: str, custom_schema: str, list_key: str):
        existing_path, current_list = ShortcutManager._find_gsettings_path(schema, custom_schema, list_key)
        if existing_path:
            # Enlever le path du tableau
            paths = [p for p in current_list.replace("[", "").replace("]", "").replace("'", "").split(", ") if p and p != existing_path]
            if not paths:
                new_list = "@as []"
            else:
                new_list = "['" + "', '".join(paths) + "']"
            run_cmd(f"gsettings set {schema} {list_key} \"{new_list}\"")
            
            # Reset des propriétés
            run_cmd(f"gsettings reset {custom_schema}:{existing_path} name")
            run_cmd(f"gsettings reset {custom_schema}:{existing_path} command")
            run_cmd(f"gsettings reset {custom_schema}:{existing_path} binding")
        return True

    @staticmethod
    def get_gnome():
        p, _ = ShortcutManager._find_gsettings_path("org.gnome.settings-daemon.plugins.media-keys", "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding", "custom-keybindings")
        if p: return run_cmd(f"gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:{p} binding").strip("'")
        return None
        
    @staticmethod
    def apply_gnome(shortcut: str):
        return ShortcutManager._apply_gsettings("org.gnome.settings-daemon.plugins.media-keys", "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding", "custom-keybindings", shortcut, "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/")
        
    @staticmethod
    def remove_gnome():
        return ShortcutManager._remove_gsettings("org.gnome.settings-daemon.plugins.media-keys", "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding", "custom-keybindings")

    @staticmethod
    def get_cinnamon():
        p, _ = ShortcutManager._find_gsettings_path("org.cinnamon.desktop.keybindings", "org.cinnamon.desktop.keybindings.custom-keybinding", "custom-list")
        if p: return run_cmd(f"gsettings get org.cinnamon.desktop.keybindings.custom-keybinding:{p} binding").strip("'")
        return None

    @staticmethod
    def apply_cinnamon(shortcut: str):
        return ShortcutManager._apply_gsettings("org.cinnamon.desktop.keybindings", "org.cinnamon.desktop.keybindings.custom-keybinding", "custom-list", shortcut, "/org/cinnamon/desktop/keybindings/custom-keybindings/")
        
    @staticmethod
    def remove_cinnamon():
        return ShortcutManager._remove_gsettings("org.cinnamon.desktop.keybindings", "org.cinnamon.desktop.keybindings.custom-keybinding", "custom-list")

    @staticmethod
    def get_mate():
        p, _ = ShortcutManager._find_gsettings_path("org.mate.SettingsDaemon.plugins.media-keys", "org.mate.SettingsDaemon.plugins.media-keys.custom-keybinding", "custom-keybindings")
        if p: return run_cmd(f"gsettings get org.mate.SettingsDaemon.plugins.media-keys.custom-keybinding:{p} binding").strip("'")
        return None

    @staticmethod
    def apply_mate(shortcut: str):
        return ShortcutManager._apply_gsettings("org.mate.SettingsDaemon.plugins.media-keys", "org.mate.SettingsDaemon.plugins.media-keys.custom-keybinding", "custom-keybindings", shortcut, "/org/mate/settings-daemon/plugins/media-keys/custom-keybindings/")

    @staticmethod
    def remove_mate():
        return ShortcutManager._remove_gsettings("org.mate.SettingsDaemon.plugins.media-keys", "org.mate.SettingsDaemon.plugins.media-keys.custom-keybinding", "custom-keybindings")

    @staticmethod
    def get_xfce():
        props = run_cmd("xfconf-query -c xfce4-keyboard-shortcuts -p /commands/custom -l").splitlines()
        for prop in props:
            val = run_cmd(f"xfconf-query -c xfce4-keyboard-shortcuts -p '{prop}'")
            if val == str(SCRIPT_PATH):
                return prop.replace('/commands/custom/', '')
        return None

    @staticmethod
    def apply_xfce(shortcut: str):
        cmd_create = f"xfconf-query -c xfce4-keyboard-shortcuts -p /commands/custom/{shortcut} -n -t string -s '{SCRIPT_PATH}'"
        subprocess.run(cmd_create, shell=True)
        return True
        
    @staticmethod
    def remove_xfce():
        b = ShortcutManager.get_xfce()
        if b:
            subprocess.run(f"xfconf-query -c xfce4-keyboard-shortcuts -p '/commands/custom/{b}' -r", shell=True)
        return True

    @staticmethod
    def get_kde():
        kread = "kreadconfig5" if not subprocess.run("command -v kreadconfig6", shell=True, capture_output=True).returncode else "kreadconfig6"
        res = run_cmd(f"{kread} --file kglobalshortcutsrc --group 'piper-tts.desktop' --key '_launch'")
        if res and "none,none" not in res:
            return res.split(",")[0]
        return None

    @staticmethod
    def apply_kde(shortcut: str):
        desktop_dir = HOME_DIR / ".local" / "share" / "applications"
        desktop_dir.mkdir(parents=True, exist_ok=True)
        desktop_file = desktop_dir / "piper-tts.desktop"
        
        content = f"[Desktop Entry]\nType=Application\nName=Piper TTS\nExec={SCRIPT_PATH}\nTerminal=false\nHidden=true\n"
        with open(desktop_file, "w") as f:
            f.write(content)
            
        kwrite = "kwriteconfig5" if not subprocess.run("command -v kwriteconfig6", shell=True, capture_output=True).returncode else "kwriteconfig6"
        run_cmd(f"{kwrite} --file kglobalshortcutsrc --group 'piper-tts.desktop' --key '_launch' '{shortcut},none,Piper TTS'")
        
        qdbus = "qdbus" if not subprocess.run("command -v qdbus6", shell=True, capture_output=True).returncode else "qdbus6"
        run_cmd(f"{qdbus} org.kde.kglobalaccel /component/piper_tts_desktop invokeShortcut _launch")
        return True
        
    @staticmethod
    def remove_kde():
        desktop_file = HOME_DIR / ".local" / "share" / "applications" / "piper-tts.desktop"
        if desktop_file.exists():
            desktop_file.unlink()
        kwrite = "kwriteconfig5" if not subprocess.run("command -v kwriteconfig6", shell=True, capture_output=True).returncode else "kwriteconfig6"
        run_cmd(f"{kwrite} --file kglobalshortcutsrc --group 'piper-tts.desktop' --key '_launch' --delete")
        qdbus = "qdbus" if not subprocess.run("command -v qdbus6", shell=True, capture_output=True).returncode else "qdbus6"
        run_cmd(f"{qdbus} org.kde.kglobalaccel /kglobalaccel org.kde.KGlobalAccel.reparseConfiguration")
        return True

    @staticmethod
    def get_lxqt():
        conf_file = HOME_DIR / ".config" / "lxqt" / "globalkeyshortcuts.conf"
        if not conf_file.exists(): return None
        with open(conf_file, "r") as f:
            content = f.read()
        if "PiperTTS" in content:
            for line in content.splitlines():
                if line.startswith("Shortcut="):
                    return line.split("=")[1]
        return None

    @staticmethod
    def apply_lxqt(shortcut: str):
        conf_file = HOME_DIR / ".config" / "lxqt" / "globalkeyshortcuts.conf"
        if conf_file.exists():
            ShortcutManager.remove_lxqt()
            with open(conf_file, "a") as f:
                f.write(f"\n[PiperTTS]\nComment=Piper TTS\nExec={SCRIPT_PATH}\nShortcut={shortcut}\n")
            run_cmd("killall lxqt-globalkeysd && lxqt-globalkeysd &")
        return True
        
    @staticmethod
    def remove_lxqt():
        conf_file = HOME_DIR / ".config" / "lxqt" / "globalkeyshortcuts.conf"
        if conf_file.exists():
            run_cmd(f"sed -i '/\\[PiperTTS\\]/,/Shortcut=/d' '{conf_file}'")
            run_cmd("killall lxqt-globalkeysd && lxqt-globalkeysd &")
        return True

def open_gui_settings():
    """Ouvre les paramètres claviers du système courant."""
    desktop = detect_desktop()
    if desktop == "gnome":
        subprocess.Popen("gnome-control-center keyboard", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    elif desktop == "cinnamon":
        subprocess.Popen("cinnamon-settings keyboard", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    elif desktop == "mate":
        subprocess.Popen("mate-keybinding-properties", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    elif desktop == "xfce":
        subprocess.Popen("xfce4-keyboard-settings", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    elif desktop == "kde":
        subprocess.Popen("systemsettings kcm_keys", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    elif desktop == "lxqt":
        subprocess.Popen("lxqt-config-globalkeyshortcuts", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def get_current_shortcut() -> str:
    """Retourne le raccourci actuel ou None."""
    desktop = detect_desktop()
    if desktop == "gnome": return ShortcutManager.get_gnome()
    elif desktop == "cinnamon": return ShortcutManager.get_cinnamon()
    elif desktop == "mate": return ShortcutManager.get_mate()
    elif desktop == "xfce": return ShortcutManager.get_xfce()
    elif desktop == "kde": return ShortcutManager.get_kde()
    elif desktop == "lxqt": return ShortcutManager.get_lxqt()
    return None

def apply_shortcut(shortcut: str) -> tuple[bool, str]:
    """Applique le raccourci global selon le bureau. Retourne (Succès, Message)."""
    desktop = detect_desktop()
    
    if desktop == "gnome": res = ShortcutManager.apply_gnome(shortcut)
    elif desktop == "cinnamon": res = ShortcutManager.apply_cinnamon(shortcut)
    elif desktop == "mate": res = ShortcutManager.apply_mate(shortcut)
    elif desktop == "xfce": res = ShortcutManager.apply_xfce(shortcut)
    elif desktop == "kde": res = ShortcutManager.apply_kde(shortcut)
    elif desktop == "lxqt": res = ShortcutManager.apply_lxqt(shortcut)
    else: return False, f"Environnement non supporté: {os.environ.get('XDG_CURRENT_DESKTOP', 'Inconnu')}"
        
    if res:
        return True, f"Raccourci configuré avec succès pour {desktop.upper()} !"
    return False, "Erreur lors de la configuration."
    
def remove_shortcut() -> tuple[bool, str]:
    """Supprime le raccourci global."""
    desktop = detect_desktop()
    if desktop == "gnome": res = ShortcutManager.remove_gnome()
    elif desktop == "cinnamon": res = ShortcutManager.remove_cinnamon()
    elif desktop == "mate": res = ShortcutManager.remove_mate()
    elif desktop == "xfce": res = ShortcutManager.remove_xfce()
    elif desktop == "kde": res = ShortcutManager.remove_kde()
    elif desktop == "lxqt": res = ShortcutManager.remove_lxqt()
    else: return False, "Environnement non supporté."
    if res:
        return True, "Raccourci supprimé avec succès."
    return False, "Erreur de suppression."
