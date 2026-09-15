from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static, Label, ListView, ListItem, LoadingIndicator, ProgressBar, Input, Checkbox
from textual.binding import Binding
from textual.screen import ModalScreen
from huggingface import HuggingFaceAPI
import piper_engine
import shortcuts
import asyncio
import i18n
from i18n import _
import subprocess
import logging
from pathlib import Path

# Configuration des logs
LOG_FILE = Path.home() / ".config" / "piper-tui" / "app.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class VoiceActionModal(ModalScreen[str]):
    """Modal demandant à l'utilisateur s'il veut activer ou supprimer une voix déjà installée."""
    def __init__(self, voice_data):
        super().__init__()
        self.voice_data = voice_data
        
    def compose(self) -> ComposeResult:
        with Vertical(id="modal-dialog"):
            yield Label(f"Voix : {self.voice_data['name']}", id="modal-title")
            yield Label(_("modal_subtitle"), id="modal-subtitle")
            yield Button(_("modal_activate"), id="btn_modal_activate", variant="success")
            yield Button(_("modal_delete"), id="btn_modal_delete", variant="error")
            yield Button(_("modal_cancel"), id="btn_modal_cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id)

class Sidebar(Vertical):
    """Menu latéral de l'application."""
    def compose(self) -> ComposeResult:
        yield Label(_("menu_title"), id="menu-title")
        yield Button(_("btn_home"), id="btn_home")
        yield Button(_("btn_catalogue"), id="btn_catalogue", variant="primary")
        yield Button(_("btn_engine"), id="btn_engine")
        yield Button(_("btn_test"), id="btn_test")
        yield Button(_("btn_shortcut"), id="btn_shortcut")
        yield Button(_("btn_quit"), id="btn_quit", variant="error")

class WelcomeScreen(Static):
    """Écran d'accueil principal."""
    def compose(self) -> ComposeResult:
        yield Label(_("welcome_title"), id="welcome-title")
        yield Label(_("welcome_subtitle"), id="welcome-subtitle")
        yield Label(_("config_title"), id="config-title")
        yield Label(_("loading"), id="config-status")
        
    def on_mount(self) -> None:
        self.refresh_config()
        
    def refresh_config(self) -> None:
        conf = piper_engine.get_current_config()
        est_installe = piper_engine.is_engine_installed()
        moteur_ok = _("engine_installed") if est_installe else _("engine_not_installed")
        v_act = conf.get("ACTIVE_VOICE") or _("voice_none")
        txt = f"{_('status_active_voice')}{v_act}\n{_('status_engine')}{moteur_ok}\n{_('status_shortcut')}"
        self.query_one("#config-status", Label).update(txt)
        
        try:
            self.app.query_one("#btn_engine", Button).disabled = est_installe
        except:
            pass

class CatalogueScreen(Static):
    """Écran affichant le catalogue dynamique de voix depuis HuggingFace."""
    def compose(self) -> ComposeResult:
        yield Label(_("catalogue_title"), id="catalogue-title")
        yield Label(_("catalogue_loading"), id="catalogue-loading")
        with Horizontal(id="search-container", classes="hidden"):
            yield Input(placeholder=_("search_placeholder"), id="search-bar")
            yield Checkbox(_("filter_installed"), id="chk-installed")
        yield ListView(id="catalogue-list", classes="hidden")
        yield Vertical(
            Label(_("downloading"), id="dl-label"),
            ProgressBar(id="dl-progress", total=100, show_eta=False),
            id="dl-container",
            classes="hidden"
        )

    async def on_mount(self) -> None:
        self.show_all_voices = False
        logging.info("Récupération du catalogue HuggingFace.")
        self.voices = await HuggingFaceAPI.fetch_catalog_voices()
        
        loading_label = self.query_one("#catalogue-loading", Label)
        list_view = self.query_one("#catalogue-list", ListView)
        search_container = self.query_one("#search-container")
        
        loading_label.display = False
        
        if not self.voices:
            list_view.remove_class("hidden")
            logging.error("Aucune voix trouvée ou erreur réseau.")
            list_view.append(ListItem(Label(_("err_network"))))
            return
            
        search_container.remove_class("hidden")
        list_view.remove_class("hidden")
        self.refresh_list()
        

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search-bar":
            try:
                self._search_timer.stop()
            except AttributeError:
                pass
            self._search_timer = self.set_timer(0.2, lambda: self.refresh_list(event.value))

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id == "chk-installed":
            search_val = ""
            try:
                search_val = self.query_one("#search-bar", Input).value
            except:
                pass
            self.refresh_list(search_val)
            
    def refresh_list(self, filter_text: str = "") -> None:
        list_view = self.query_one("#catalogue-list", ListView)
        list_view.clear()
        
        installed_files = piper_engine.get_installed_voices()
        conf = piper_engine.get_current_config()
        active_file = conf.get("VOICE_FILE", "")
        
        filter_text = filter_text.lower()
        has_hidden_voices = False
        
        filter_installed_only = False
        try:
            filter_installed_only = self.query_one("#chk-installed", Checkbox).value
        except:
            pass
        
        for voice in self.voices:
            filename = voice['file_path'].split('/')[-1]
            
            # Filtre 'Installées uniquement'
            if filter_installed_only and filename not in installed_files:
                continue
                
            # Filtre de recherche
            if filter_text and filter_text not in voice['name'].lower() and filter_text not in voice['key'].lower():
                continue
                
            # Filtre "Progressive disclosure" si aucune recherche n'est active
            if not filter_text and not getattr(self, "show_all_voices", False) and not filter_installed_only:
                lang_code = voice.get("lang_code", "")
                if not (lang_code.startswith("FR") or lang_code.startswith("EN")):
                    has_hidden_voices = True
                    continue
                
            status = ""
            if active_file.endswith(filename):
                status = _("status_tag_active")
            elif filename in installed_files:
                status = _("status_tag_installed")
                
            list_item = ListItem(Label(f"🎙️ {voice['name']} - {voice['key']}{status}"))
            list_item.voice_data = voice
            list_view.append(list_item)
            
        if has_hidden_voices:
            expand_item = ListItem(Label(_("btn_show_all")))
            expand_item.is_expand_button = True
            list_view.append(expand_item)
            
    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        if getattr(event.item, "is_expand_button", False):
            self.show_all_voices = True
            search_val = ""
            try:
                search_val = self.query_one("#search-bar", Input).value
            except:
                pass
            self.refresh_list(search_val)
            return

        if not hasattr(event.item, "voice_data"):
            return
            
        voice = event.item.voice_data
        filename = voice['file_path'].split('/')[-1]
        installed_files = piper_engine.get_installed_voices()
        
        # Si la voix est déjà installée, on affiche le menu modale (Activation/Suppression)
        if filename in installed_files:
            def handle_modal_result(action: str):
                if action == "btn_modal_activate":
                    piper_engine.save_active_voice(voice["name"], str(piper_engine.VOICES_DIR / filename))
                    self.app.query_one("#view-welcome").refresh_config()
                    self.refresh_list()
                    self.notify(_("voice_activated").format(voice["name"]))
                elif action == "btn_modal_delete":
                    piper_engine.delete_voice(filename)
                    # Si c'était la voix active, on la désactive de l'affichage
                    conf = piper_engine.get_current_config()
                    if conf.get("VOICE_FILE", "").endswith(filename):
                        piper_engine.save_active_voice(_("voice_none"), "")
                    self.app.query_one("#view-welcome").refresh_config()
                    self.refresh_list()
                    self.notify(_("voice_deleted").format(voice["name"]), severity="warning")
                    
            self.app.push_screen(VoiceActionModal(voice), handle_modal_result)
            return

        # Si non installée, on procède au téléchargement (comportement normal)
        self.query_one("#catalogue-list").add_class("hidden")
        dl_container = self.query_one("#dl-container")
        dl_container.remove_class("hidden")
        dl_label = self.query_one("#dl-label")
        dl_label.update(_("dl_voice").format(voice["name"]))
        pb = self.query_one("#dl-progress")
        pb.progress = 0
        
        last_percent = 0
        def update_progress(downloaded, total):
            nonlocal last_percent
            if total > 0:
                percent = int((downloaded / total) * 100)
                if percent > last_percent:
                    last_percent = percent
                    pb.update(total=total, progress=downloaded)
                
        logging.info(f"Début du téléchargement de la voix {voice['name']}")
        try:
            await piper_engine.download_voice(voice, update_progress)
            dl_label.update(_("dl_voice_ok").format(voice["name"]))
            logging.info(f"Voix {voice['name']} installée avec succès.")
        except Exception as e:
            dl_label.update(_("dl_voice_err").format(e))
            logging.error(f"Erreur pendant le téléchargement de la voix {voice['name']}: {e}", exc_info=True)
            
        self.app.query_one("#view-welcome").refresh_config()
        self.refresh_list()
        
        await asyncio.sleep(2.5)
        dl_container.add_class("hidden")
        self.query_one("#catalogue-list").remove_class("hidden")

class ShortcutScreen(Static):
    """Écran de configuration des raccourcis."""
    def compose(self) -> ComposeResult:
        desktop = shortcuts.detect_desktop().upper()
        yield Label(_("shortcut_title"), id="shortcut-title")
        yield Label(f"{_('shortcut_desktop')} {desktop}", id="shortcut-desktop")
        
        yield Label(_("loading_shortcut"), id="shortcut-current")
        with Horizontal(id="shortcut-actions"):
            yield Button(_("btn_delete"), id="btn_delete_shortcut", variant="error", classes="hidden")
            yield Button(_("btn_gui"), id="btn_gui_settings", variant="primary")
            yield Button(_("btn_copy"), id="btn_copy_cmd")
        
        yield Label(_("shortcut_manual_hint"), id="shortcut-manual-hint")
        yield Label(f"➡️ {shortcuts.SCRIPT_PATH}", id="shortcut-manual-cmd")
        
        yield Label(_("shortcut_auto_hint"), id="shortcut-hint")
        yield Input(placeholder="<Super><Shift>s", id="shortcut-input")
        yield Button(_("btn_save"), id="btn_save_shortcut", variant="success")
        yield Label("", id="shortcut-status")

    def on_mount(self) -> None:
        self.refresh_shortcut()
        
    def refresh_shortcut(self) -> None:
        current = shortcuts.get_current_shortcut()
        if current:
            self.query_one("#shortcut-current", Label).update(f"{_('shortcut_current')} {current}")
            self.query_one("#btn_delete_shortcut", Button).remove_class("hidden")
        else:
            self.query_one("#shortcut-current", Label).update(_("shortcut_none"))
            self.query_one("#btn_delete_shortcut", Button).add_class("hidden")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_save_shortcut":
            val = self.query_one("#shortcut-input", Input).value
            if not val:
                return
            success, msg = shortcuts.apply_shortcut(val)
            self.query_one("#shortcut-status", Label).update(msg)
            self.refresh_shortcut()
            
        elif event.button.id == "btn_delete_shortcut":
            success, msg = shortcuts.remove_shortcut()
            self.query_one("#shortcut-status", Label).update(msg)
            self.refresh_shortcut()
            
        elif event.button.id == "btn_gui_settings":
            shortcuts.open_gui_settings()
            
        elif event.button.id == "btn_copy_cmd":
            cmd = str(shortcuts.SCRIPT_PATH)
            try:
                if subprocess.run("command -v wl-copy", shell=True, capture_output=True).returncode == 0:
                    subprocess.run(["wl-copy"], input=cmd.encode())
                    self.notify(_("msg_copied"), title="Succès")
                elif subprocess.run("command -v xsel", shell=True, capture_output=True).returncode == 0:
                    subprocess.run(["xsel", "-b", "-i"], input=cmd.encode())
                    self.notify(_("msg_copied"), title="Succès")
                elif subprocess.run("command -v xclip", shell=True, capture_output=True).returncode == 0:
                    subprocess.run(["xclip", "-selection", "clipboard"], input=cmd.encode())
                    self.notify(_("msg_copied"), title="Succès")
                else:
                    self.notify(_("copy_err_tools"), severity="warning")
            except Exception as e:
                self.notify(_("copy_err").format(e), severity="error")

class PiperTuiApp(App):
    """Application principale Textual."""
    
    CSS = """
    Screen { layout: horizontal; }
    Sidebar { width: 30; height: 100%; background: $boost; border-right: vkey $background; padding: 1 2; }
    #menu-title { text-align: center; text-style: bold; width: 100%; padding-bottom: 2; }
    Sidebar Button { width: 100%; margin-bottom: 1; }
    #main-content { width: 1fr; height: 100%; padding: 1 2; }
    #welcome-title, #catalogue-title, #shortcut-title, #engine-title { text-align: center; text-style: bold; color: $accent; padding: 1; }
    #welcome-subtitle { text-align: center; color: $text-muted; }
    .hidden { display: none; }
    #search-container { height: auto; }
    #search-bar { width: 1fr; }
    #chk-installed { width: auto; margin-left: 1; }
    #catalogue-list { height: 1fr; border: solid $accent; margin-top: 1; }
    #dl-container { align: center middle; height: 1fr; }
    #shortcut-hint { margin-top: 1; margin-bottom: 1; }
    #btn_save_shortcut { margin-top: 1; }
    #shortcut-status { margin-top: 1; color: $success; }
    #shortcut-actions { height: auto; margin-top: 1; }
    #shortcut-actions Button { margin-right: 1; }
    #shortcut-manual-hint { margin-top: 1; color: $text-muted; }
    #shortcut-manual-cmd { color: $accent; text-style: bold; margin-bottom: 1; }
    
    VoiceActionModal { align: center middle; background: $background 80%; }
    #modal-dialog { width: 50; height: auto; padding: 1 2; border: thick $accent; background: $surface; }
    #modal-title { text-align: center; text-style: bold; color: $accent; margin-bottom: 1; }
    #modal-subtitle { text-align: center; margin-bottom: 2; }
    #modal-dialog Button { width: 100%; margin-bottom: 1; }
    """

    BINDINGS = [
        Binding("q", "quit", _("bind_quit"), show=True),
        Binding("d", "toggle_dark", _("bind_theme"), show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            yield Sidebar()
            with Container(id="main-content"):
                yield WelcomeScreen(id="view-welcome")
                yield CatalogueScreen(id="view-catalogue", classes="hidden")
                yield ShortcutScreen(id="view-shortcut", classes="hidden")
                
                # Screen d'install moteur simple
                yield Vertical(
                    Label(_("engine_install_title"), id="engine-title"),
                    Label(_("downloading"), id="engine-dl-label"),
                    ProgressBar(id="engine-progress", total=100),
                    id="view-engine",
                    classes="hidden"
                )
        yield Footer()

    def switch_view(self, view_id: str) -> None:
        for view in self.query("#main-content > Static, #main-content > Vertical"):
            if view.id == view_id:
                view.remove_class("hidden")
            else:
                view.add_class("hidden")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        
        if button_id == "btn_quit":
            self.exit()
        elif button_id == "btn_home":
            self.switch_view("view-welcome")
        elif button_id == "btn_catalogue":
            self.switch_view("view-catalogue")
        elif button_id == "btn_engine":
            if piper_engine.is_engine_installed():
                self.notify(_("engine_already_installed"), title=_("info_title"))
                return
                
            self.switch_view("view-engine")
            pb = self.query_one("#engine-progress", ProgressBar)
            pb.progress = 0
            
            def update_progress(downloaded, total):
                if downloaded == -1:
                    self.query_one("#engine-dl-label", Label).update(_("engine_extracting"))
                elif total > 0:
                    pb.update(total=total, progress=downloaded)
                    
            await piper_engine.download_engine(update_progress)
            self.query_one("#engine-dl-label", Label).update(_("engine_dl_ok"))
            self.query_one("#view-welcome").refresh_config()
            await asyncio.sleep(2)
            self.switch_view("view-welcome")
            
        elif button_id == "btn_test":
            if not piper_engine.is_engine_installed():
                self.notify(_("err_no_engine"), title=_("err_title"), severity="error")
                return
            conf = piper_engine.get_current_config()
            voice = conf.get("VOICE_FILE")
            if not voice:
                self.notify(_("err_no_voice"), title=_("err_title"), severity="error")
                return
                
            self.notify(_("test_playing"), title=_("test_title"))
            sr = conf.get("SAMPLE_RATE", 16000)
            cmd = f'echo "Ceci est un test audio du moteur Piper. L\'interface graphique Python fonctionne à la perfection !" | {piper_engine.ENGINE_BIN} --model "{voice}" --output_raw | aplay -r {sr} -f S16_LE -t raw'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        elif button_id == "btn_shortcut":
            self.switch_view("view-shortcut")

    def on_mount(self) -> None:
        conf = piper_engine.get_current_config()
        self.dark = conf.get("DARK_MODE", "true").lower() == "true"
        self.switch_view("view-welcome")
        
    def action_toggle_dark(self) -> None:
        """Surcharge l'action native pour sauvegarder le choix."""
        self.dark = not self.dark
        piper_engine.update_config_key("DARK_MODE", str(self.dark).lower())

if __name__ == "__main__":
    app = PiperTuiApp()
    app.run()
