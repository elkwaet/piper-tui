#!/bin/bash
set -e

# Default to English messages
MSG_START="🚀 Downloading and installing Piper TUI..."
MSG_PREP="📁 Preparing directory"
MSG_DL="⬇️  Downloading latest version..."
MSG_EXTRACT="📦 Extracting files..."
MSG_INTEGRATION="⚙️  Running system integration script..."
MSG_DONE="✨ Done! Application installed in"

# Override with French if detected
if [[ "$LANG" == fr* ]]; then
    MSG_START="🚀 Téléchargement et installation de Piper TUI..."
    MSG_PREP="📁 Préparation du dossier"
    MSG_DL="⬇️  Téléchargement de la dernière version..."
    MSG_EXTRACT="📦 Extraction des fichiers..."
    MSG_INTEGRATION="⚙️  Lancement du script d'intégration système..."
    MSG_DONE="✨ Terminé ! L'application est installée dans"
fi

echo "$MSG_START"

INSTALL_DIR="$HOME/.piper-tui-app"
TMP_TAR="/tmp/piper-tui-latest.tar.gz"

echo "$MSG_PREP $INSTALL_DIR..."
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

echo "$MSG_DL"
curl -sSL "https://github.com/elkwaet/piper-tui/archive/refs/heads/main.tar.gz" -o "$TMP_TAR"

echo "$MSG_EXTRACT"
tar -xzf "$TMP_TAR" -C "$INSTALL_DIR" --strip-components=1
rm -f "$TMP_TAR"

echo "$MSG_INTEGRATION"
cd "$INSTALL_DIR"
bash install.sh

echo ""
echo "$MSG_DONE $INSTALL_DIR"
