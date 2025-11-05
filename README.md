# RA Config Editor

RA Config Editor is a small graphical application to create and edit Remote Admin (RemoteAdmin) configuration files for SCP: Secret Laboratory servers. It provides a friendly GUI for managing users, roles, permissions, ban templates and other RemoteAdmin settings and exports them as YAML/text files compatible with server setups.

The app is built with Python and PyQt6 and uses PyYAML for reading/writing configuration files.

## Features

- Visual editor for Members, Roles, Permissions, Ban Templates and other settings
- Load and save RemoteAdmin config files (YAML / TXT)
- Preview generated YAML in-app
- Add/remove roles and users and tweak role badges, colors and kick powers

## Install

You can either **download a ready-to-use release** from the [Releases](../../releases) page
or **clone the repository** and run it manually:

```bash
git clone https://github.com/MollyIO/ra_config_editor.git
cd ra_config_editor
pip install -r requirements.txt
python main.py
```

---

Enjoy and happy server administrating!
