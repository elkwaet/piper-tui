#!/bin/bash
set -e

echo "🚀 Téléchargement et installation de Piper TUI..."

INSTALL_DIR="$HOME/.piper-tui-app"
TMP_TAR="/tmp/piper-tui-latest.tar.gz"

echo "📁 Préparation du dossier $INSTALL_DIR..."
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

echo "⬇️  Téléchargement de la dernière version..."
# Téléchargement de l'archive de la branche principale depuis le miroir public GitHub
curl -sSL "https://github.com/elkwaet/piper-tui/archive/refs/heads/main.tar.gz" -o "$TMP_TAR"

echo "📦 Extraction des fichiers..."
tar -xzf "$TMP_TAR" -C "$INSTALL_DIR" --strip-components=1
rm -f "$TMP_TAR"

echo "⚙️  Lancement du script d'intégration système..."
cd "$INSTALL_DIR"
bash install.sh

echo ""
echo "✨ Terminé ! L'application est installée dans $INSTALL_DIR"
