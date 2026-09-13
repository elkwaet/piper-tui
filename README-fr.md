# Piper TUI

Une interface utilisateur légère en terminal (TUI) pour gérer [Piper TTS](https://github.com/rhasspy/piper) sous Linux.

## Fonctionnalités
- Interface terminal minimaliste propulsée par `whiptail`.
- Installe automatiquement le moteur Text-to-Speech Piper.
- Parcourez, téléchargez et basculez facilement entre des modèles vocaux français de haute qualité.
- Génère automatiquement le script `read-selection.sh` pour lire à voix haute le texte sélectionné depuis n'importe quelle application.
- **Gestionnaire de raccourci clavier global** : Configurez, modifiez ou supprimez votre raccourci système directement depuis l'interface (GNOME, Zorin OS, Ubuntu).

## Prérequis
- `whiptail`
- `wget`
- `xsel` (pour X11) ou `wl-clipboard` (pour Wayland)
- `alsa-utils` (pour la lecture audio)
- `gsettings` (pour l'intégration automatique sous GNOME/Zorin)

## Installation & Utilisation

```bash
# Cloner le dépôt (ou télécharger le script)
git clone https://github.com/VOTRE_GITHUB/piper-tui.git
cd piper-tui/package

# Rendre le script exécutable
chmod +x piper-tui.sh

# Lancer l'interface
./piper-tui.sh
```

## Configuration du raccourci clavier global

Vous pouvez configurer le raccourci global directement via **l'Option 4** dans le menu du TUI.

Alternativement, pour une configuration manuelle :
1. Ouvrez les **Paramètres** de votre système > **Clavier** > **Raccourcis personnalisés**.
2. Ajoutez un nouveau raccourci :
   - **Nom :** Lire la sélection (Piper)
   - **Commande :** `/home/VOTRE_NOM_UTILISATEUR/.piper/read-selection.sh` *(remplacez `VOTRE_NOM_UTILISATEUR` par votre vrai nom d'utilisateur Linux)*
   - **Raccourci :** `Super + Shift + S` (ou la combinaison de votre choix)
3. Sélectionnez n'importe quel texte à l'écran (navigateur, document, terminal) et appuyez sur votre raccourci pour l'écouter !

## Fichiers de configuration

Les paramètres sont sauvegardés dans `~/.config/piper-tui/config.env`.
Les voix téléchargées sont stockées dans `~/.piper/voices/`.
