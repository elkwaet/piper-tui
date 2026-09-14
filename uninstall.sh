#!/bin/bash
set -e

# Default to English
MSG_START="🗑️ Uninstalling Piper TUI..."
MSG_SYMLINKS_RM="🔗 Removing symlinks from"
MSG_PROMPT_PURGE="❓ Do you also want to delete downloaded voices, the Piper engine, and configuration files? (y/N) "
MSG_PURGE_DONE="🧹 Configuration and engine files removed."
MSG_PURGE_SKIP="⏩ Configuration and engine files kept."
MSG_DONE="✅ Uninstallation complete!"

# Override with French if detected
if [[ "$LANG" == fr* ]]; then
    MSG_START="🗑️ Désinstallation de Piper TUI..."
    MSG_SYMLINKS_RM="🔗 Suppression des liens symboliques dans"
    MSG_PROMPT_PURGE="❓ Voulez-vous également supprimer les voix téléchargées, le moteur Piper et les fichiers de configuration ? (o/N) "
    MSG_PURGE_DONE="🧹 Fichiers de configuration et moteur supprimés."
    MSG_PURGE_SKIP="⏩ Fichiers de configuration et moteur conservés."
    MSG_DONE="✅ Désinstallation terminée !"
fi

echo "$MSG_START"

LOCAL_BIN="$HOME/.local/bin"

if [ -L "$LOCAL_BIN/piper-tui" ]; then
    rm -f "$LOCAL_BIN/piper-tui"
fi
if [ -L "$LOCAL_BIN/piper-tui-lite" ]; then
    rm -f "$LOCAL_BIN/piper-tui-lite"
fi

echo "$MSG_SYMLINKS_RM $LOCAL_BIN"

read -p "$MSG_PROMPT_PURGE" choice
case "$choice" in 
  y|Y|o|O|yes|oui ) 
    rm -rf "$HOME/.config/piper-tui"
    rm -rf "$HOME/.piper"
    echo "$MSG_PURGE_DONE"
    ;;
  * )
    echo "$MSG_PURGE_SKIP"
    ;;
esac

echo "$MSG_DONE"
