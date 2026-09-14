import os
import locale
from pathlib import Path

CONFIG_FILE = Path.home() / ".config" / "piper-tui" / "config.env"

MESSAGES = {
    "en": {
        "engine_installed": "✅ Installed",
        "engine_not_installed": "❌ Not installed",
        "status_active_voice": "- Active voice: ",
        "status_engine": "- Engine: ",
        "status_shortcut": "- Shortcut: (See shortcut section)",
        "voice_none": "None",
        "status_tag_active": " 🟢 [Active]",
        "status_tag_installed": " ✔️ [Installed]",
        "dl_voice": "Downloading {}...",
        "voice_activated": "Voice {} activated!",
        "voice_deleted": "Voice {} uninstalled.",
        "dl_voice_ok": "✅ Voice {} installed and activated!",
        "dl_voice_err": "❌ Error: {}",
        "engine_already_installed": "Engine is already installed!",
        "engine_dl_ok": "✅ Piper Engine installed successfully!",
        "copy_err_tools": "wl-copy, xsel or xclip not found. Copy manually.",
        "copy_err": "Error during copy: {}",
        "bind_quit": "Quit",
        "bind_theme": "Toggle Dark Mode",
        "info_title": "Info",
        "search_placeholder": "Search voice (ex: FR, Amy)...",


        "btn_home": "Home",
        "btn_catalogue": "Voice Catalog",
        "btn_engine": "Install Piper Engine",
        "btn_test": "Test Active Voice",
        "btn_shortcut": "Global Shortcut",
        "btn_quit": "Quit",
        "menu_title": "MAIN MENU",
        "welcome_title": "Welcome to Piper TUI",
        "welcome_subtitle": "Select an option from the sidebar to begin.",
        "config_title": "\nCurrent configuration:",
        "loading": "Loading...",
        "catalogue_title": "Voice Catalog (HuggingFace)",
        "catalogue_loading": "Fetching list...",
        "downloading": "Downloading...",
        "modal_subtitle": "This voice is already installed on your system.",
        "loading_shortcut": "Loading current shortcut...",
        "shortcut_manual_hint": "\nIf you configure manually (via GUI), use this exact command:",
        "shortcut_auto_hint": "\nOr automatically create the shortcut (e.g. <Super><Shift>s):",
        "err_network": "❌ Network error or no voice found.",
        "err_no_engine": "Please install the engine first.",
        "err_title": "Error",
        "err_no_voice": "Please download a voice first.",
        "test_playing": "Playing audio test...",
        "test_title": "Audio Test",
        "engine_install_title": "⚙️ Piper Engine Installation",
        "engine_extracting": "Extracting tar.gz archive...",
        "engine_installed_ok": "Engine installation complete!",
        "success_title": "Success",
        "engine_installed_err": "Error installing engine. Check logs.",
        "voice_ready": "ready!",

        "btn_install_engine": "Install Piper Engine",
        "btn_test_voice": "Test active voice",
        "btn_shortcut": "Global Shortcut",
        "btn_quit": "Quit",
        "title_catalog": "Voice Catalog",
        "lbl_active_voice": "Active Voice: ",
        "lbl_no_voice": "None",
        "shortcut_title": "⌨️ Global Shortcut Configuration",
        "shortcut_desktop": "Detected desktop: ",
        "shortcut_current": "🟢 Active Shortcut: ",
        "shortcut_none": "🔴 No shortcut configured.",
        "btn_delete": "Delete",
        "btn_gui": "GUI Settings",
        "btn_copy": "Copy Command",
        "btn_save": "Save",
        "msg_copied": "Command copied to clipboard!",
        "voice_installed": "Installed",
        "voice_download": "Download",
        "modal_activate": "Activate Voice",
        "modal_delete": "Delete Voice",
        "modal_cancel": "Cancel",
    },
    "fr": {
        "engine_installed": "✅ Installé",
        "engine_not_installed": "❌ Non installé",
        "status_active_voice": "- Voix active : ",
        "status_engine": "- Moteur : ",
        "status_shortcut": "- Raccourci : (Voir section raccourci)",
        "voice_none": "Aucune",
        "status_tag_active": " 🟢 [Active]",
        "status_tag_installed": " ✔️ [Installée]",
        "dl_voice": "Téléchargement de {}...",
        "voice_activated": "Voix {} activée !",
        "voice_deleted": "Voix {} désinstallée.",
        "dl_voice_ok": "✅ Voix {} installée et activée !",
        "dl_voice_err": "❌ Erreur : {}",
        "engine_already_installed": "Le moteur est déjà installé !",
        "engine_dl_ok": "✅ Moteur Piper installé avec succès !",
        "copy_err_tools": "wl-copy, xsel ou xclip introuvables. Copiez manuellement.",
        "copy_err": "Erreur lors de la copie : {}",
        "bind_quit": "Quitter",
        "bind_theme": "Mode Sombre",
        "info_title": "Info",
        "search_placeholder": "Rechercher une voix (ex: FR, Amy)...",


        "btn_home": "Accueil",
        "btn_catalogue": "Catalogue Voix",
        "btn_engine": "Installer Moteur Piper",
        "btn_test": "Tester Voix Active",
        "btn_shortcut": "Raccourci Global",
        "btn_quit": "Quitter",
        "menu_title": "MENU PRINCIPAL",
        "welcome_title": "Bienvenue dans Piper TUI",
        "welcome_subtitle": "Sélectionnez une option dans le menu latéral pour commencer.",
        "config_title": "\nConfiguration actuelle :",
        "loading": "Chargement...",
        "catalogue_title": "Catalogue des Voix (HuggingFace)",
        "catalogue_loading": "Récupération de la liste en cours...",
        "downloading": "Téléchargement...",
        "modal_subtitle": "Cette voix est déjà installée sur votre système.",
        "loading_shortcut": "Chargement du raccourci actuel...",
        "shortcut_manual_hint": "\nSi vous configurez manuellement (via GUI), utilisez cette commande exacte :",
        "shortcut_auto_hint": "\nOu créer automatiquement le raccourci (ex: <Super><Shift>s) :",
        "err_network": "❌ Erreur réseau ou aucune voix trouvée.",
        "err_no_engine": "Veuillez installer le moteur d'abord.",
        "err_title": "Erreur",
        "err_no_voice": "Veuillez télécharger une voix d'abord.",
        "test_playing": "Lecture du test audio en cours...",
        "test_title": "Test Audio",
        "engine_install_title": "⚙️ Installation du Moteur Piper",
        "engine_extracting": "Extraction de l'archive tar.gz...",
        "engine_installed_ok": "Installation du moteur terminée !",
        "success_title": "Succès",
        "engine_installed_err": "Erreur lors de l'installation du moteur. Consultez les logs.",
        "voice_ready": "prête !",

        "btn_install_engine": "Installer Moteur Piper",
        "btn_test_voice": "Tester la voix active",
        "btn_shortcut": "Raccourci Global",
        "btn_quit": "Quitter",
        "title_catalog": "Catalogue des Voix",
        "lbl_active_voice": "Voix Active : ",
        "lbl_no_voice": "Aucune",
        "shortcut_title": "⌨️ Configuration du Raccourci Global",
        "shortcut_desktop": "Bureau détecté : ",
        "shortcut_current": "🟢 Raccourci Actif : ",
        "shortcut_none": "🔴 Aucun raccourci configuré.",
        "btn_delete": "Supprimer",
        "btn_gui": "Paramètres GUI",
        "btn_copy": "Copier la Commande",
        "btn_save": "Enregistrer",
        "msg_copied": "Commande copiée dans le presse-papiers !",
        "voice_installed": "Installée",
        "voice_download": "Télécharger",
        "modal_activate": "Activer cette voix",
        "modal_delete": "Supprimer la voix",
        "modal_cancel": "Annuler",
    }
}

def get_system_lang():
    # 1. Check config.env
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                if line.startswith("APP_LANG="):
                    return line.strip().split("=")[1].strip('"')
    
    # 2. Check system LANG
    system_lang = os.environ.get("LANG", "")
    if system_lang.startswith("fr"):
        return "fr"
    return "en"

CURRENT_LANG = get_system_lang()

def _(key):
    lang_dict = MESSAGES.get(CURRENT_LANG, MESSAGES["en"])
    return lang_dict.get(key, MESSAGES["en"].get(key, key))
