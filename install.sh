#!/bin/bash
set -e

# Default to English
MSG_START="🚀 Installing Piper TUI..."
MSG_DIR_DETECTED="📁 Installation directory detected:"
MSG_SYMLINKS="🔗 Symlinks created in"
MSG_NOT_IN_PATH="⚠️  %s is not in your current PATH.\n"
MSG_ADDING_PATH="🔧 Attempting to add to shell configuration..."
MSG_ADDED_TO="✅ Added to"
MSG_DONE_RESTART="🎉 Installation complete! Please restart your terminal or run:"
MSG_DONE_ALREADY="🎉 Installation complete! %s seems to be already configured.\n"
MSG_DONE_READY="🎉 Installation complete! You can now type 'piper-tui' from anywhere."

# Override with French if detected
if [[ "$LANG" == fr* ]]; then
    MSG_START="🚀 Installation de Piper TUI..."
    MSG_DIR_DETECTED="📁 Répertoire d'installation détecté :"
    MSG_SYMLINKS="🔗 Liens symboliques créés dans"
    MSG_NOT_IN_PATH="⚠️  %s n'est pas dans votre PATH actuel.\n"
    MSG_ADDING_PATH="🔧 Tentative d'ajout au shell..."
    MSG_ADDED_TO="✅ Ajouté à"
    MSG_DONE_RESTART="🎉 Installation terminée ! Veuillez redémarrer votre terminal ou taper :"
    MSG_DONE_ALREADY="🎉 Installation terminée ! %s semble déjà être configuré.\n"
    MSG_DONE_READY="🎉 Installation terminée ! Vous pouvez maintenant taper 'piper-tui' depuis n'importe où."
fi

echo "$MSG_START"

# 1. Résolution du chemin absolu du dossier d'installation
INSTALL_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
echo "$MSG_DIR_DETECTED $INSTALL_DIR"

# Rendre les scripts exécutables au cas où
chmod +x "$INSTALL_DIR/piper-tui"
chmod +x "$INSTALL_DIR/piper-tui-lite"

# 2. Création des liens symboliques dans ~/.local/bin
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"

ln -sf "$INSTALL_DIR/piper-tui" "$LOCAL_BIN/piper-tui"
ln -sf "$INSTALL_DIR/piper-tui-lite" "$LOCAL_BIN/piper-tui-lite"
echo "$MSG_SYMLINKS $LOCAL_BIN"

# 3. Vérification du PATH
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    printf "$MSG_NOT_IN_PATH" "$LOCAL_BIN"
    echo "$MSG_ADDING_PATH"
    
    BASH_RC="$HOME/.bashrc"
    ZSH_RC="$HOME/.zshrc"
    
    ADDED=false
    # Vérification bash
    if [ -n "$BASH_VERSION" ] || [ -f "$BASH_RC" ]; then
        if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$BASH_RC" 2>/dev/null; then
            echo -e '\n# Piper TUI: Ajout de ~/.local/bin au PATH\nexport PATH="$HOME/.local/bin:$PATH"' >> "$BASH_RC"
            echo "$MSG_ADDED_TO $BASH_RC"
            ADDED=true
        fi
    fi
    # Vérification zsh
    if [ -n "$ZSH_VERSION" ] || [ -f "$ZSH_RC" ]; then
        if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$ZSH_RC" 2>/dev/null; then
            echo -e '\n# Piper TUI: Ajout de ~/.local/bin au PATH\nexport PATH="$HOME/.local/bin:$PATH"' >> "$ZSH_RC"
            echo "$MSG_ADDED_TO $ZSH_RC"
            ADDED=true
        fi
    fi
    
    if [ "$ADDED" = true ]; then
        echo "$MSG_DONE_RESTART"
        echo "   source ~/.bashrc  (ou source ~/.zshrc)"
    else
        printf "$MSG_DONE_ALREADY" "$LOCAL_BIN"
    fi
else
    echo "$MSG_DONE_READY"
fi
