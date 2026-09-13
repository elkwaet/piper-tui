#!/bin/bash
set -e

CONFIG_DIR="$HOME/.config/piper-tui"
CONFIG_FILE="$CONFIG_DIR/config.env"
PIPER_DIR="$HOME/.piper"
VOICES_DIR="$PIPER_DIR/voices"
READ_SCRIPT="$PIPER_DIR/read-selection.sh"
DESKTOP_FILE="$HOME/.local/share/applications/piper-tts.desktop"

mkdir -p "$CONFIG_DIR"
mkdir -p "$PIPER_DIR"
mkdir -p "$VOICES_DIR"

if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    ACTIVE_VOICE="Aucune"
    VOICE_FILE=""
    SAMPLE_RATE=16000
    echo "ACTIVE_VOICE=\"$ACTIVE_VOICE\"" > "$CONFIG_FILE"
    echo "VOICE_FILE=\"$VOICE_FILE\"" >> "$CONFIG_FILE"
    echo "SAMPLE_RATE=$SAMPLE_RATE" >> "$CONFIG_FILE"
fi

update_read_script() {
    cat << EOF > "$READ_SCRIPT"
#!/bin/bash
if [ "\$XDG_SESSION_TYPE" = "wayland" ]; then
    TEXT=\$(wl-paste --primary)
else
    TEXT=\$(xsel -o)
fi

if [ ! -z "\$TEXT" ]; then
    if pkill -f "piper/piper" ; then
        exit 0
    fi
    echo "\$TEXT" | $PIPER_DIR/piper/piper \\
        --model $VOICE_FILE \\
        --output_raw | aplay -r $SAMPLE_RATE -f S16_LE -t raw
fi
EOF
    chmod +x "$READ_SCRIPT"
}

download_voice() {
    local name="$1"
    local url="$2"
    local rate="$3"
    local filename="$4"
    local local_file="$VOICES_DIR/$filename"
    
    clear
    echo "================================================="
    echo "📥 Téléchargement de la voix : $name"
    echo "================================================="
    
    if [ ! -f "$local_file" ]; then
        wget -q --show-progress -O "$local_file" "$url"
        wget -q -O "${local_file}.json" "${url}.json"
    else
        echo "✅ La voix $name est déjà présente sur la machine."
        sleep 1
    fi
    
    ACTIVE_VOICE="$name"
    VOICE_FILE="$local_file"
    SAMPLE_RATE="$rate"
    
    echo "ACTIVE_VOICE=\"$ACTIVE_VOICE\"" > "$CONFIG_FILE"
    echo "VOICE_FILE=\"$VOICE_FILE\"" >> "$CONFIG_FILE"
    echo "SAMPLE_RATE=$SAMPLE_RATE" >> "$CONFIG_FILE"
    
    update_read_script
    
    echo ""
    echo "🎉 Voix $name configurée avec succès !"
    read -p "Appuyez sur Entrée pour retourner au menu..."
}

select_or_input_binding() {
    local default_val="$1"
    local de="$2"
    
    # Syntaxe spécifique selon le bureau
    local ex_super="<Super>"
    local ex_ctrl="<Primary>"
    if [ "$de" = "KDE" ]; then
        ex_super="Meta+"
        ex_ctrl="Ctrl+"
    elif [ "$de" = "MATE" ]; then
        ex_super="<Mod4>"
    fi
    
    CHOICE_BIND=$(whiptail --title "Combinaison de touches ($de)" --menu \
"💡 Aide syntaxe : $ex_ctrl = Ctrl, $ex_super = Touche Windows/Super.
Choisissez une combinaison prête à l'emploi ou saisissez-en une personnalisée :" 18 78 5 \
        "1" "$ex_super${ex_ctrl/Ctrl+/}Shift+S (Super + Maj + S)" \
        "2" "$ex_ctrl$ex_super S (Ctrl + Alt + S)" \
        "3" "$ex_ctrl$ex_super L (Ctrl + Alt + L)" \
        "4" "$ex_ctrl Escape (Ctrl + Échap)" \
        "5" "Saisie personnalisée (Entrée manuelle précise)" 3>&1 1>&2 2>&3)

    case $CHOICE_BIND in
        1)
            if [ "$de" = "KDE" ]; then echo "Meta+Shift+S"; elif [ "$de" = "MATE" ]; then echo "<Mod4><Shift>s"; else echo "<Super><Shift>s"; fi ;;
        2)
            if [ "$de" = "KDE" ]; then echo "Ctrl+Alt+S"; else echo "<Primary><Alt>s"; fi ;;
        3)
            if [ "$de" = "KDE" ]; then echo "Ctrl+Alt+L"; else echo "<Primary><Alt>l"; fi ;;
        4)
            if [ "$de" = "KDE" ]; then echo "Ctrl+Esc"; else echo "<Primary>Escape"; fi ;;
        5)
            CUSTOM_INPUT=$(whiptail --title "Saisie personnalisée" --inputbox "Entrez votre combinaison selon la syntaxe de votre bureau :" 10 65 "$default_val" 3>&1 1>&2 2>&3)
            echo "$CUSTOM_INPUT"
            ;;
        *)
            echo ""
            ;;
    esac
}

# --- FONCTIONS DE GESTION DES RACCOURCIS PAR BUREAU ---

manage_shortcut_gsettings() {
    local SCHEMA="$1"
    local CUSTOM_SCHEMA="$2"
    local LIST_KEY="$3"
    
    EXISTING=$(gsettings get $SCHEMA $LIST_KEY)
    FOUND_PATH=""
    CURRENT_BINDING=""
    
    PATHS=$(echo "$EXISTING" | tr -d "[]'" | tr ',' ' ')
    for p in $PATHS; do
        p_clean=$(echo "$p" | xargs)
        if [ -n "$p_clean" ]; then
            local cmd_val=""
            # Si le chemin commence par / on ajoute le custom_schema devant, sinon (Cinnamon) on ajoute le prefixe
            if [[ "$p_clean" == /* ]]; then
                cmd_val=$(gsettings get "$CUSTOM_SCHEMA:$p_clean" command 2>/dev/null | tr -d "'\"")
            else
                # Cinnamon
                cmd_val=$(gsettings get "$CUSTOM_SCHEMA:/org/cinnamon/desktop/keybindings/custom-keybindings/$p_clean/" command 2>/dev/null | tr -d "'\"")
            fi
            
            if [ "$cmd_val" = "$READ_SCRIPT" ]; then
                FOUND_PATH="$p_clean"
                if [[ "$p_clean" == /* ]]; then
                    CURRENT_BINDING=$(gsettings get "$CUSTOM_SCHEMA:$p_clean" binding 2>/dev/null | tr -d "'\"")
                else
                    CURRENT_BINDING=$(gsettings get "$CUSTOM_SCHEMA:/org/cinnamon/desktop/keybindings/custom-keybindings/$p_clean/" binding 2>/dev/null | tr -d "'\"")
                fi
                break
            fi
        fi
    done

    if [ -n "$FOUND_PATH" ]; then
        ACTION=$(whiptail --title "Raccourci Clavier Global" --menu "Raccourci actif : $CURRENT_BINDING" 15 65 3 \
            "1" "Modifier la combinaison de touches" \
            "2" "Ouvrir les Paramètres Système GUI" \
            "3" "Supprimer le raccourci global" 3>&1 1>&2 2>&3)
        
        case $ACTION in
            1)
                NEW_BINDING=$(select_or_input_binding "$CURRENT_BINDING" "GNOME")
                if [ -n "$NEW_BINDING" ]; then
                    if [[ "$FOUND_PATH" == /* ]]; then
                        gsettings set "$CUSTOM_SCHEMA:$FOUND_PATH" binding "$NEW_BINDING"
                    else
                        gsettings set "$CUSTOM_SCHEMA:/org/cinnamon/desktop/keybindings/custom-keybindings/$FOUND_PATH/" binding "$NEW_BINDING"
                    fi
                    whiptail --msgbox "✅ Raccourci mis à jour ($NEW_BINDING) !" 8 50
                fi
                ;;
            2)
                if command -v gnome-control-center &>/dev/null; then gnome-control-center keyboard &>/dev/null &
                elif command -v cinnamon-settings &>/dev/null; then cinnamon-settings keyboard &>/dev/null &
                elif command -v mate-keybinding-properties &>/dev/null; then mate-keybinding-properties &>/dev/null &
                fi
                whiptail --msgbox "⚙️ L'application Paramètres a été ouverte." 8 65
                ;;
            3)
                # Remove from list
                NEW_LIST=$(echo "$EXISTING" | sed "s|'$FOUND_PATH', ||; s|, '$FOUND_PATH'||; s|'$FOUND_PATH'||")
                if [ "$NEW_LIST" = "[]" ] || [ "$NEW_LIST" = "@as []" ]; then
                    gsettings set $SCHEMA $LIST_KEY "[]"
                else
                    gsettings set $SCHEMA $LIST_KEY "$NEW_LIST"
                fi
                whiptail --msgbox "🗑️ Raccourci supprimé avec succès !" 8 45
                ;;
        esac
    else
        ACTION=$(whiptail --title "Configurer Raccourci Clavier" --menu "Aucun raccourci configuré." 15 65 2 \
            "1" "Choisir une combinaison" \
            "2" "Ouvrir Paramètres GUI" 3>&1 1>&2 2>&3)
        
        if [ "$ACTION" = "1" ]; then
            BINDING=$(select_or_input_binding "<Super><Shift>s" "GNOME")
            if [ -n "$BINDING" ]; then
                IDX=0
                if [[ "$SCHEMA" == *"cinnamon"* ]]; then
                    while echo "$EXISTING" | grep -q "'custom$IDX'"; do IDX=$((IDX + 1)); done
                    NEW_PATH="custom$IDX"
                    FULL_PATH="$CUSTOM_SCHEMA:/org/cinnamon/desktop/keybindings/custom-keybindings/$NEW_PATH/"
                else
                    while echo "$EXISTING" | grep -q "/custom$IDX/"; do IDX=$((IDX + 1)); done
                    NEW_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom$IDX/"
                    if [[ "$SCHEMA" == *"mate"* ]]; then
                        NEW_PATH="/org/mate/settings-daemon/plugins/media-keys/custom-keybindings/custom$IDX/"
                    fi
                    FULL_PATH="$CUSTOM_SCHEMA:$NEW_PATH"
                fi
                
                gsettings set "$FULL_PATH" name 'Lire la sélection (Piper TTS)'
                gsettings set "$FULL_PATH" command "$READ_SCRIPT"
                gsettings set "$FULL_PATH" binding "$BINDING"
                
                if [ "$EXISTING" = "@as []" ] || [ "$EXISTING" = "[]" ]; then
                    gsettings set $SCHEMA $LIST_KEY "['$NEW_PATH']"
                else
                    UPDATED=$(echo "$EXISTING" | sed "s|\]|, '$NEW_PATH']|")
                    gsettings set $SCHEMA $LIST_KEY "$UPDATED"
                fi
                whiptail --msgbox "✅ Raccourci activé ($BINDING) !" 8 55
            fi
        elif [ "$ACTION" = "2" ]; then
            if command -v gnome-control-center &>/dev/null; then gnome-control-center keyboard &>/dev/null &
            elif command -v cinnamon-settings &>/dev/null; then cinnamon-settings keyboard &>/dev/null &
            fi
        fi
    fi
}

manage_shortcut_xfce() {
    # Check if shortcut already exists
    local existing_prop=""
    local current_binding=""
    for prop in $(xfconf-query -c xfce4-keyboard-shortcuts -p /commands/custom -l 2>/dev/null); do
        val=$(xfconf-query -c xfce4-keyboard-shortcuts -p "$prop" 2>/dev/null)
        if [ "$val" = "$READ_SCRIPT" ]; then
            existing_prop="$prop"
            current_binding=$(echo "$prop" | sed 's|/commands/custom/||')
            break
        fi
    done
    
    if [ -n "$existing_prop" ]; then
        ACTION=$(whiptail --title "Raccourci XFCE" --menu "Raccourci actif : $current_binding" 15 65 2 \
            "1" "Supprimer le raccourci" \
            "2" "Retour" 3>&1 1>&2 2>&3)
        if [ "$ACTION" = "1" ]; then
            xfconf-query -c xfce4-keyboard-shortcuts -p "$existing_prop" -r
            whiptail --msgbox "🗑️ Raccourci supprimé avec succès !" 8 45
        fi
    else
        BINDING=$(select_or_input_binding "<Super><Shift>s" "XFCE")
        if [ -n "$BINDING" ]; then
            xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/$BINDING" -n -t string -s "$READ_SCRIPT"
            whiptail --msgbox "✅ Raccourci activé ($BINDING) !" 8 55
        fi
    fi
}

manage_shortcut_kde() {
    # Setup .desktop file required by KDE
    mkdir -p ~/.local/share/applications
    cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Exec=$READ_SCRIPT
Name=Piper TTS Read Selection
Type=Application
EOF

    local kwrite="kwriteconfig5"
    local qdbus_cmd="qdbus"
    if command -v kwriteconfig6 &>/dev/null; then
        kwrite="kwriteconfig6"
        qdbus_cmd="qdbus6"
    fi

    # Read existing
    # format in kglobalshortcutsrc: _launch=Meta+Shift+S,none,Piper TTS Read Selection
    local existing=$(kreadconfig5 --file kglobalshortcutsrc --group "piper-tts.desktop" --key "_launch" 2>/dev/null || echo "")
    
    if [ -n "$existing" ] && [[ "$existing" != *"none,none"* ]]; then
        local current_binding=$(echo "$existing" | cut -d',' -f1)
        ACTION=$(whiptail --title "Raccourci KDE Plasma" --menu "Raccourci actif : $current_binding" 15 65 2 \
            "1" "Supprimer le raccourci" \
            "2" "Retour" 3>&1 1>&2 2>&3)
        if [ "$ACTION" = "1" ]; then
            $kwrite --file kglobalshortcutsrc --group "piper-tts.desktop" --key "_launch" --delete
            $qdbus_cmd org.kde.kglobalaccel /kglobalaccel org.kde.KGlobalAccel.reparseConfiguration &>/dev/null || true
            rm -f "$DESKTOP_FILE"
            whiptail --msgbox "🗑️ Raccourci supprimé avec succès !" 8 45
        fi
    else
        BINDING=$(select_or_input_binding "Meta+Shift+S" "KDE")
        if [ -n "$BINDING" ]; then
            $kwrite --file kglobalshortcutsrc --group "piper-tts.desktop" --key "_launch" "$BINDING,none,Piper TTS Read Selection"
            $qdbus_cmd org.kde.kglobalaccel /kglobalaccel org.kde.KGlobalAccel.reparseConfiguration &>/dev/null || true
            whiptail --msgbox "✅ Raccourci activé ($BINDING) !" 8 55
        fi
    fi
}

manage_shortcut_lxqt() {
    local CONF_FILE="$HOME/.config/lxqt/globalkeyshortcuts.conf"
    
    if grep -q "$READ_SCRIPT" "$CONF_FILE" 2>/dev/null; then
        ACTION=$(whiptail --title "Raccourci LXQt" --menu "Un raccourci existe dans globalkeyshortcuts.conf" 15 65 2 \
            "1" "Supprimer le raccourci" \
            "2" "Retour" 3>&1 1>&2 2>&3)
        if [ "$ACTION" = "1" ]; then
            sed -i '/\[.*Piper/,/path=/d' "$CONF_FILE" 2>/dev/null || true
            killall lxqt-globalkeysd && lxqt-globalkeysd &
            whiptail --msgbox "🗑️ Raccourci supprimé avec succès !" 8 45
        fi
    else
        BINDING=$(whiptail --title "Raccourci LXQt" --inputbox "Entrez la combinaison (ex: Meta+Shift+S) :" 10 65 "Meta+Shift+S" 3>&1 1>&2 2>&3)
        if [ -n "$BINDING" ]; then
            local escaped_binding=$(echo "$BINDING" | sed 's/+/%2B/g')
            cat <<EOF >> "$CONF_FILE"

[${escaped_binding}.Piper]
Comment=Piper TTS Read Selection
Enabled=true
path=$READ_SCRIPT
EOF
            killall lxqt-globalkeysd && lxqt-globalkeysd &
            whiptail --msgbox "✅ Raccourci activé ($BINDING) !" 8 55
        fi
    fi
}

# --- DISPATCHER ---
route_shortcut_manager() {
    local de="${XDG_CURRENT_DESKTOP:-Unknown}"
    
    if [[ "$de" == *"GNOME"* ]] || [[ "$de" == *"Pantheon"* ]] || [[ "$de" == *"ubuntu"* ]]; then
        manage_shortcut_gsettings "org.gnome.settings-daemon.plugins.media-keys" "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding" "custom-keybindings"
    elif [[ "$de" == *"Cinnamon"* ]]; then
        manage_shortcut_gsettings "org.cinnamon.desktop.keybindings" "org.cinnamon.desktop.keybindings.custom-keybinding" "custom-list"
    elif [[ "$de" == *"MATE"* ]]; then
        manage_shortcut_gsettings "org.mate.SettingsDaemon.plugins.media-keys" "org.mate.SettingsDaemon.plugins.media-keys.custom-keybinding" "custom-keybindings"
    elif [[ "$de" == *"XFCE"* ]]; then
        manage_shortcut_xfce
    elif [[ "$de" == *"KDE"* ]]; then
        manage_shortcut_kde
    elif [[ "$de" == *"LXQt"* ]]; then
        manage_shortcut_lxqt
    else
        whiptail --msgbox "Votre bureau ($de) ne dispose pas d'une API standardisée détectable par le script.\n\nConsultez le WIKI pour savoir comment ajouter manuellement le raccourci vers :\n$READ_SCRIPT" 12 70
    fi
}

while true; do
    CHOICE=$(whiptail --title "Piper TUI" --menu "Voix Active: $ACTIVE_VOICE" 16 65 5 \
        "1" "Sélectionner / Télécharger une voix" \
        "2" "Installer le moteur Piper (si manquant)" \
        "3" "Tester la voix active ($ACTIVE_VOICE)" \
        "4" "Configurer le raccourci global" \
        "5" "Quitter" 3>&1 1>&2 2>&3)

    case $CHOICE in
        1)
            SIWIS_STATE=" (À télécharger)"
            GILLES_STATE=" (À télécharger)"
            
            if [ -f "$VOICES_DIR/siwis.onnx" ]; then SIWIS_STATE=" [✓ Installé]"; fi
            if [ -f "$VOICES_DIR/gilles.onnx" ]; then GILLES_STATE=" [✓ Installé]"; fi
            
            VOICE=$(whiptail --title "Catalogue des Voix" --menu "Choisis une voix française :" 15 70 2 \
                "Siwis" "Féminine, Naturelle, Haute qualité$SIWIS_STATE" \
                "Gilles" "Masculine, Basique$GILLES_STATE" 3>&1 1>&2 2>&3)
            
            case $VOICE in
                Siwis) download_voice "Siwis (Medium)" "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx" 22050 "siwis.onnx" ;;
                Gilles) download_voice "Gilles (Low)" "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx" 16000 "gilles.onnx" ;;
            esac
            ;;
        2)
            if [ -f "$PIPER_DIR/piper/piper" ]; then whiptail --msgbox "✅ Le moteur Piper est déjà installé !" 8 45
            else
                clear
                echo "================================================="
                echo "📥 Téléchargement du moteur Piper..."
                echo "================================================="
                wget -q --show-progress -O /tmp/piper.tar.gz "https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz"
                tar -xzf /tmp/piper.tar.gz -C "$PIPER_DIR"
                rm /tmp/piper.tar.gz
                echo "🎉 Moteur Piper installé !"
                read -p "Appuyez sur Entrée pour retourner au menu..."
            fi
            ;;
        3)
            if [ ! -f "$VOICE_FILE" ] || [ ! -f "$PIPER_DIR/piper/piper" ]; then
                whiptail --msgbox "Erreur : Le moteur Piper ou la voix n'est pas installée !" 8 50
            else
                echo "Ceci est un test de la voix." | $PIPER_DIR/piper/piper --model "$VOICE_FILE" --output_raw | aplay -r $SAMPLE_RATE -f S16_LE -t raw &> /dev/null
            fi
            ;;
        4)
            route_shortcut_manager
            ;;
        5)
            clear
            exit 0
            ;;
        *)
            clear
            exit 0
            ;;
    esac
done
