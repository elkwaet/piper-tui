# Piper TUI

![Screenshot](assets/piper-tui-zero.png)

Une interface moderne en terminal (TUI) pour gérer [Piper TTS](https://github.com/rhasspy/piper) sous Linux. Ce petit outil permet aux utilisateurs de lire à voix haute n'importe quelle sélection de texte, grâce à un raccourci clavier que vous aurez défini. Vous pouvez lire à voix haute n'importe quelle sélection de texte dans les interfaces de divers applis (navigateur, terminal, IDE, lecteur de documents, suites bureautiques).

## Fonctionnalités
- **Architecture Dual Mode** : 
  - `piper-tui` : L'interface principale, riche et asynchrone (Textual/Python).
  - `piper-tui-lite` : La version bash legacy, propulsée par `whiptail` pour les environnements minimaux.
- Installe automatiquement le moteur Text-to-Speech Piper.
- Parcourez, téléchargez et basculez facilement entre des modèles vocaux français de haute qualité depuis HuggingFace.
- Génère automatiquement le script `read-selection.sh` pour lire à voix haute le texte sélectionné depuis n'importe quelle application.
- **Gestionnaire de raccourci clavier global** : Configurez, modifiez ou supprimez votre raccourci système directement depuis l'interface (Support GNOME, Cinnamon, MATE, XFCE, KDE, LXQt).

## Prérequis
- `wget`
- `xsel` (pour X11) ou `wl-clipboard` (pour Wayland)
- `alsa-utils` (pour la lecture audio)
- `python3` (pour l'application `piper-tui`)
- `whiptail` (uniquement pour `piper-tui-lite`)

## Installation & Utilisation

```bash
# Cloner le dépôt (ou télécharger le code)
git clone https://github.com/elkwaet/piper-tui.git
cd piper-tui/package

# Installer globalement (crée des liens symboliques dans ~/.local/bin)
./install.sh

# Vous pouvez maintenant lancer la version Python moderne de n'importe où
./piper-tui

# Pour désinstaller
./uninstall.sh ('création automatique du venv')


# OU lancer la version bash allégée
./piper-tui-lite
```

> **Note :** Pour la configuration manuelle des raccourcis claviers et l'intégration dans les Window Managers (i3, sway, bspwm...), veuillez consulter le [WIKI](WIKI.md) , anglais seulement.

## Fichiers de configuration

Les paramètres sont sauvegardés dans `~/.config/piper-tui/config.env`.
Les voix téléchargées sont stockées dans `~/.piper/voices/`.

## Auteurs
- **elkwaet** - *Développement initial* - [elkwaet](https://gitlab.com/elkwaet)

## Licence
Ce projet est sous  [Licence MIT](LICENSE).
