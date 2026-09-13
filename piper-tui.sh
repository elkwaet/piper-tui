#!/bin/bash
set -e

CONFIG_DIR="$HOME/.config/piper-tui"
CONFIG_FILE="$CONFIG_DIR/config.env"
PIPER_DIR="$HOME/.piper"
VOICES_DIR="$PIPER_DIR/voices"
READ_SCRIPT="$PIPER_DIR/read-selection.sh"

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
    
    # Sortir de l'UI whiptail pour un téléchargement natif propre
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

while true; do
    CHOICE=$(whiptail --title "Piper TUI" --menu "Voix Active: $ACTIVE_VOICE" 15 60 4 \
        "1" "Sélectionner / Télécharger une voix" \
        "2" "Installer le moteur Piper (si manquant)" \
        "3" "Tester la voix active ($ACTIVE_VOICE)" \
        "4" "Quitter" 3>&1 1>&2 2>&3)

    case $CHOICE in
        1)
            # Détection des voix locales
            SIWIS_STATE=" (À télécharger)"
            GILLES_STATE=" (À télécharger)"
            
            if [ -f "$VOICES_DIR/siwis.onnx" ]; then SIWIS_STATE=" [✓ Installé]"; fi
            if [ -f "$VOICES_DIR/gilles.onnx" ]; then GILLES_STATE=" [✓ Installé]"; fi
            
            VOICE=$(whiptail --title "Catalogue des Voix" --menu "Choisis une voix française :" 15 70 2 \
                "Siwis" "Féminine, Naturelle, Haute qualité$SIWIS_STATE" \
                "Gilles" "Masculine, Basique$GILLES_STATE" 3>&1 1>&2 2>&3)
            
            case $VOICE in
                Siwis)
                    download_voice "Siwis (Medium)" "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx" 22050 "siwis.onnx"
                    ;;
                Gilles)
                    download_voice "Gilles (Low)" "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx" 16000 "gilles.onnx"
                    ;;
            esac
            ;;
        2)
            if [ -f "$PIPER_DIR/piper/piper" ]; then
                whiptail --msgbox "✅ Le moteur Piper est déjà installé !" 8 45
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
            clear
            exit 0
            ;;
        *)
            clear
            exit 0
            ;;
    esac
done
