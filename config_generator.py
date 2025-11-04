import yaml
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QListWidget, QLineEdit, 
                             QComboBox, QCheckBox, QSpinBox, QTextEdit, QPushButton,
                             QLabel, QMessageBox, QSplitter, QTableWidget,
                             QTableWidgetItem, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
import os

from add_role_dialog import AddRoleDialog

class ConfigGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_data = self.get_default_config()
        self.init_ui()
        
    def get_default_config(self):
        return {
            'Members': [],
            'enable_staff_access': False,
            'enable_manager_access': True,
            'enable_banteam_access': True,
            'enable_banteam_reserved_slots': True,
            'enable_banteam_bypass_geoblocking': True,
            'Roles': ['owner', 'admin', 'moderator'],
            'Permissions': {
                'KickingAndShortTermBanning': ['owner', 'admin', 'moderator'],
                'BanningUpToDay': ['owner', 'admin', 'moderator'],
                'LongTermBanning': ['owner', 'admin'],
                'ForceclassSelf': ['owner', 'admin', 'moderator'],
                'ForceclassToSpectator': ['owner', 'admin', 'moderator'],
                'ForceclassWithoutRestrictions': ['owner', 'admin'],
                'GivingItems': ['owner', 'admin'],
                'WarheadEvents': ['owner', 'admin', 'moderator'],
                'RespawnEvents': ['owner', 'admin'],
                'RoundEvents': ['owner', 'admin', 'moderator'],
                'SetGroup': ['owner'],
                'GameplayData': ['owner', 'admin'],
                'Overwatch': ['owner', 'admin', 'moderator'],
                'FacilityManagement': ['owner', 'admin', 'moderator'],
                'PlayersManagement': ['owner', 'admin'],
                'PermissionsManagement': ['owner'],
                'ServerConsoleCommands': [],
                'ViewHiddenBadges': ['owner', 'admin', 'moderator'],
                'ServerConfigs': ['owner'],
                'Broadcasting': ['owner', 'admin', 'moderator'],
                'PlayerSensitiveDataAccess': ['owner', 'admin', 'moderator'],
                'Noclip': ['owner', 'admin'],
                'AFKImmunity': ['owner', 'admin'],
                'AdminChat': ['owner', 'admin', 'moderator'],
                'ViewHiddenGlobalBadges': ['owner', 'admin', 'moderator'],
                'Announcer': ['owner', 'admin'],
                'Effects': ['owner', 'admin'],
                'FriendlyFireDetectorImmunity': ['owner', 'admin', 'moderator'],
                'FriendlyFireDetectorTempDisable': ['owner', 'admin'],
                'ServerLogLiveFeed': ['owner', 'admin'],
                'ExecuteAs': ['owner'],
                'Vanish': ['owner']
            },
            'override_password': 'none',
            'override_password_role': 'owner',
            'allow_central_server_commands_as_ServerConsoleCommands': False,
            'enable_predefined_ban_templates': True,
            'PredefinedBanTemplates': [
                [0, 'Consider this a warning!'],
                [3600, 'Mic Spamming'],
                [86400, 'Team Killing (Minor Offence)'],
                [604800, 'Team Killing (Major Offence)'],
                [1577000000, 'Abusing Exploits']
            ]
        }

    def init_ui(self):
        self.setWindowTitle("RemoteAdmin Config Editor")
        self.setGeometry(100, 100, 1200, 700)
        self.set_window_icon()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        tabs = QTabWidget()
        
        tabs.addTab(self.create_members_tab(), "Users")
        tabs.addTab(self.create_access_tab(), "Access")
        tabs.addTab(self.create_roles_tab(), "Roles")
        tabs.addTab(self.create_permissions_tab(), "Permissions")
        tabs.addTab(self.create_ban_templates_tab(), "Ban Templates")
        tabs.addTab(self.create_other_tab(), "Other Settings")
        
        layout.addWidget(tabs)
        
        button_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load Config")
        load_btn.clicked.connect(self.load_config)
        
        save_btn = QPushButton("Save Config")
        save_btn.clicked.connect(self.save_config)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_config)
        
        button_layout.addWidget(load_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)

    def create_members_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("SteamId64@steam or DiscordUserID@discord")
        controls_layout.addWidget(QLabel("UserID:"))
        controls_layout.addWidget(self.user_id_input)
        
        self.role_combo = QComboBox()
        controls_layout.addWidget(QLabel("Role:"))
        controls_layout.addWidget(self.role_combo)
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_member)
        controls_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_member)
        controls_layout.addWidget(remove_btn)
        
        layout.addLayout(controls_layout)
        
        # Members list
        self.members_list = QListWidget()
        layout.addWidget(self.members_list)
        
        return widget

    def create_access_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.staff_access = QCheckBox("Enable Secret Lab staff access")
        self.manager_access = QCheckBox("Enable Secret Lab manager access")
        self.banteam_access = QCheckBox("Enable ban team access")
        self.banteam_slots = QCheckBox("Enable reserved slots for ban team")
        self.banteam_geo = QCheckBox("Allow ban team to bypass geoblocking")
        
        for checkbox in [self.staff_access, self.manager_access, self.banteam_access, self.banteam_slots, self.banteam_geo]:
            layout.addWidget(checkbox)
        
        layout.addStretch()
        return widget

    def create_roles_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        controls_layout = QHBoxLayout()
        add_role_btn = QPushButton("Add Role")
        add_role_btn.clicked.connect(self.add_new_role)
        
        remove_role_btn = QPushButton("Remove Role")
        remove_role_btn.clicked.connect(self.remove_role)
        
        controls_layout.addWidget(add_role_btn)
        controls_layout.addWidget(remove_role_btn)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.roles_list = QListWidget()
        self.roles_list.currentItemChanged.connect(self.on_role_selected)
        splitter.addWidget(self.roles_list)
        
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        
        self.role_badge = QLineEdit()
        self.role_color = QComboBox()
        self.role_color.addItems(["red", "blue", "green", "yellow", "purple", "orange", "silver", "none"])
        self.role_cover = QCheckBox("Cover (overrides global badges)")
        self.role_hidden = QCheckBox("Hidden (hidden badge)")
        self.role_kick_power = QSpinBox()
        self.role_kick_power.setRange(0, 255)
        self.role_required_kick = QSpinBox()
        self.role_required_kick.setRange(0, 255)
        
        editor_layout.addWidget(QLabel("Badge:"))
        editor_layout.addWidget(self.role_badge)
        editor_layout.addWidget(QLabel("Color:"))
        editor_layout.addWidget(self.role_color)
        editor_layout.addWidget(self.role_cover)
        editor_layout.addWidget(self.role_hidden)
        editor_layout.addWidget(QLabel("Kick Power:"))
        editor_layout.addWidget(self.role_kick_power)
        editor_layout.addWidget(QLabel("Required Kick Power:"))
        editor_layout.addWidget(self.role_required_kick)
        
        save_role_btn = QPushButton("Save Changes")
        save_role_btn.clicked.connect(self.save_role_changes)
        editor_layout.addWidget(save_role_btn)
        
        editor_layout.addStretch()
        splitter.addWidget(editor_widget)
        
        layout.addWidget(splitter)
        return widget

    def create_permissions_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.permissions_table = QTableWidget()
        layout.addWidget(self.permissions_table)
        
        return widget

    def create_ban_templates_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        controls_layout = QHBoxLayout()
        
        self.ban_duration = QSpinBox()
        self.ban_duration.setRange(0, 999999999)
        self.ban_duration.setSuffix(" seconds")
        
        self.ban_reason = QLineEdit()
        self.ban_reason.setPlaceholderText("Ban reason")
        
        add_ban_btn = QPushButton("Add Template")
        add_ban_btn.clicked.connect(self.add_ban_template)
        
        remove_ban_btn = QPushButton("Remove Template")
        remove_ban_btn.clicked.connect(self.remove_ban_template)
        
        controls_layout.addWidget(QLabel("Duration:"))
        controls_layout.addWidget(self.ban_duration)
        controls_layout.addWidget(QLabel("Reason:"))
        controls_layout.addWidget(self.ban_reason)
        controls_layout.addWidget(add_ban_btn)
        controls_layout.addWidget(remove_ban_btn)
        
        layout.addLayout(controls_layout)
        
        self.ban_table = QTableWidget()
        self.ban_table.setColumnCount(2)
        self.ban_table.setHorizontalHeaderLabels(["Duration (sec)", "Reason"])
        layout.addWidget(self.ban_table)
        
        return widget

    def create_other_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password (not recommended):"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("none to disable")
        password_layout.addWidget(self.password_input)
        
        password_layout.addWidget(QLabel("Password role:"))
        self.password_role = QComboBox()
        password_layout.addWidget(self.password_role)
        layout.addLayout(password_layout)
        
        self.central_commands = QCheckBox("Allow central server commands")
        self.predefined_bans = QCheckBox("Enable ban templates")
        
        for checkbox in [self.central_commands, self.predefined_bans]:
            layout.addWidget(checkbox)
        
        layout.addWidget(QLabel("Config Preview:"))
        self.config_preview = QTextEdit()
        self.config_preview.setFont(QFont("Consolas", 9))
        layout.addWidget(self.config_preview)
        
        return widget

    def update_ui_from_config(self):
        self.members_list.clear()
        for member in self.config_data.get('Members', []):
            user_id, role = self._extract_member_pair(member)
            self.members_list.addItem(f"{user_id}: {role}")
        
        self.staff_access.setChecked(self.config_data['enable_staff_access'])
        self.manager_access.setChecked(self.config_data['enable_manager_access'])
        self.banteam_access.setChecked(self.config_data['enable_banteam_access'])
        self.banteam_slots.setChecked(self.config_data['enable_banteam_reserved_slots'])
        self.banteam_geo.setChecked(self.config_data['enable_banteam_bypass_geoblocking'])
        
        self.update_roles_list()
        
        self.update_permissions_table()
        
        self.update_ban_templates()
        
        self.password_input.setText(self.config_data['override_password'])
        self.central_commands.setChecked(self.config_data['allow_central_server_commands_as_ServerConsoleCommands'])
        self.predefined_bans.setChecked(self.config_data['enable_predefined_ban_templates'])
        
        self.update_config_preview()

    def update_roles_list(self):
        self.roles_list.clear()
        self.role_combo.clear()
        self.password_role.clear()
        
        for role in self.config_data['Roles']:
            self.roles_list.addItem(role)
            self.role_combo.addItem(role)
            self.password_role.addItem(role)

    def update_permissions_table(self):
        permissions = self.config_data['Permissions']
        roles = self.config_data['Roles']
        
        self.permissions_table.setRowCount(len(permissions))
        self.permissions_table.setColumnCount(len(roles))
        self.permissions_table.setHorizontalHeaderLabels(roles)
        
        row = 0
        for perm_name, perm_roles in permissions.items():
            self.permissions_table.setVerticalHeaderItem(row, QTableWidgetItem(perm_name))
            
            for col, role in enumerate(roles):
                checkbox = QCheckBox()
                checkbox.setChecked(role in perm_roles)
                checkbox.stateChanged.connect(lambda state, p=perm_name, r=role: 
                                            self.update_permission(p, r, state))
                self.permissions_table.setCellWidget(row, col, checkbox)
            row += 1

    def update_ban_templates(self):
        templates = self.config_data['PredefinedBanTemplates']
        self.ban_table.setRowCount(len(templates))
        
        for row, template in enumerate(templates):
            self.ban_table.setItem(row, 0, QTableWidgetItem(str(template[0])))
            self.ban_table.setItem(row, 1, QTableWidgetItem(template[1]))

    def update_config_preview(self):
        try:
            yaml_output = yaml.dump(self.config_data, default_flow_style=False, allow_unicode=True)
            self.config_preview.setPlainText(yaml_output)
        except Exception as e:
            self.config_preview.setPlainText(f"YAML generation error: {str(e)}")

    def add_member(self):
        user_id = self.user_id_input.text().strip()
        role = self.role_combo.currentText()
        
        if user_id and role:
            self.config_data['Members'].append({user_id: role})
            self.update_ui_from_config()
            self.user_id_input.clear()

    def _extract_member_pair(self, member):
        """Return (user_id, role) for a member entry.

        Supported input formats:
        - dict: {user_id: role}
        - list/tuple: [user_id, role]
        - str: user_id (role will be empty string)
        - any: stringified as user_id with empty role
        """
        if isinstance(member, dict):
            # take first key/value pair
            try:
                k = next(iter(member))
                return str(k), member[k]
            except StopIteration:
                return ("", "")
        if isinstance(member, (list, tuple)) and len(member) >= 2:
            return str(member[0]), member[1]
        if isinstance(member, str):
            return member, ""
        return str(member), ""

    def remove_member(self):
        current_row = self.members_list.currentRow()
        if current_row >= 0:
            self.config_data['Members'].pop(current_row)
            self.update_ui_from_config()

    def add_new_role(self):
        dialog = AddRoleDialog(self)
        if dialog.exec():
            role_data = dialog.get_role_data()
            if role_data['name'] and role_data['badge']:
                if role_data['name'] not in self.config_data['Roles']:
                    self.config_data['Roles'].append(role_data['name'])
                
                role_key = f"{role_data['name']}_badge"
                self.config_data[role_key] = role_data['badge']
                self.config_data[f"{role_data['name']}_color"] = role_data['color']
                self.config_data[f"{role_data['name']}_cover"] = True
                self.config_data[f"{role_data['name']}_hidden"] = False
                self.config_data[f"{role_data['name']}_kick_power"] = 1
                self.config_data[f"{role_data['name']}_required_kick_power"] = 1
                
                self.update_ui_from_config()

    def remove_role(self):
        current_item = self.roles_list.currentItem()
        if current_item:
            role_name = current_item.text()
            
            self.config_data['Roles'].remove(role_name)
            
            for key in ['_badge', '_color', '_cover', '_hidden', '_kick_power', '_required_kick_power']:
                self.config_data.pop(f"{role_name}{key}", None)
            
            for perm in self.config_data['Permissions']:
                if role_name in self.config_data['Permissions'][perm]:
                    self.config_data['Permissions'][perm].remove(role_name)
            
            self.update_ui_from_config()

    def on_role_selected(self, current):
        if current:
            role_name = current.text()
            self.role_badge.setText(self.config_data.get(f"{role_name}_badge", ""))
            self.role_color.setCurrentText(self.config_data.get(f"{role_name}_color", "none"))
            self.role_cover.setChecked(self.config_data.get(f"{role_name}_cover", False))
            self.role_hidden.setChecked(self.config_data.get(f"{role_name}_hidden", False))
            self.role_kick_power.setValue(self.config_data.get(f"{role_name}_kick_power", 0))
            self.role_required_kick.setValue(self.config_data.get(f"{role_name}_required_kick_power", 0))

    def save_role_changes(self):
        current_item = self.roles_list.currentItem()
        if current_item:
            role_name = current_item.text()
            self.config_data[f"{role_name}_badge"] = self.role_badge.text()
            self.config_data[f"{role_name}_color"] = self.role_color.currentText()
            self.config_data[f"{role_name}_cover"] = self.role_cover.isChecked()
            self.config_data[f"{role_name}_hidden"] = self.role_hidden.isChecked()
            self.config_data[f"{role_name}_kick_power"] = self.role_kick_power.value()
            self.config_data[f"{role_name}_required_kick_power"] = self.role_required_kick.value()
            
            self.update_ui_from_config()

    def update_permission(self, permission, role, state):
        if state == Qt.CheckState.Checked.value:
            if role not in self.config_data['Permissions'][permission]:
                self.config_data['Permissions'][permission].append(role)
        else:
            if role in self.config_data['Permissions'][permission]:
                self.config_data['Permissions'][permission].remove(role)

    def add_ban_template(self):
        duration = self.ban_duration.value()
        reason = self.ban_reason.text().strip()
        
        if reason:
            self.config_data['PredefinedBanTemplates'].append([duration, reason])
            self.update_ui_from_config()
            self.ban_reason.clear()

    def remove_ban_template(self):
        current_row = self.ban_table.currentRow()
        if current_row >= 0:
            self.config_data['PredefinedBanTemplates'].pop(current_row)
            self.update_ui_from_config()

    def load_config(self):
        """Load config from YAML file"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Load Config File",
                "",
                "TXT Files (*.txt);;All Files (*)"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as file:
                    loaded_data = yaml.safe_load(file)
                
                if loaded_data:
                    if self.validate_config_structure(loaded_data):
                        if 'Members' in loaded_data:
                            normalized_members = []
                            for m in loaded_data['Members']:
                                if isinstance(m, dict):
                                    normalized_members.append(m)
                                elif isinstance(m, (list, tuple)) and len(m) >= 2:
                                    normalized_members.append({str(m[0]): m[1]})
                                elif isinstance(m, str):
                                    normalized_members.append({m: ""})
                                else:
                                    normalized_members.append({str(m): ""})
                            loaded_data['Members'] = normalized_members

                        self.config_data = loaded_data
                        self.update_ui_from_config()
                        QMessageBox.information(self, "Success", f"Config loaded from:\n{filename}")
                    else:
                        QMessageBox.warning(self, "Warning", "Loaded file has invalid structure. Using default config.")
                else:
                    QMessageBox.warning(self, "Warning", "Failed to load config file. Using default config.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading config:\n{str(e)}")

    def save_config(self):
        """Save config to YAML file"""
        try:
            self.update_config_from_ui()
            
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Config File",
                "remoteadmin_config.yml",
                "YAML Files (*.yml *.yaml);;All Files (*)"
            )
            
            if filename:
                if not filename.lower().endswith(('.yml', '.yaml')):
                    filename += '.yml'
                
                with open(filename, 'w', encoding='utf-8') as file:
                    yaml.dump(
                        self.config_data, 
                        file, 
                        default_flow_style=False, 
                        allow_unicode=True,
                        sort_keys=False,
                        indent=2
                    )
                
                QMessageBox.information(self, "Success", f"Config saved to:\n{filename}")
                self.update_config_preview()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving config:\n{str(e)}")

    def update_config_from_ui(self):
        """Update config data from all UI elements"""
        self.config_data['enable_staff_access'] = self.staff_access.isChecked()
        self.config_data['enable_manager_access'] = self.manager_access.isChecked()
        self.config_data['enable_banteam_access'] = self.banteam_access.isChecked()
        self.config_data['enable_banteam_reserved_slots'] = self.banteam_slots.isChecked()
        self.config_data['enable_banteam_bypass_geoblocking'] = self.banteam_geo.isChecked()
        
        self.config_data['override_password'] = self.password_input.text() or 'none'
        self.config_data['override_password_role'] = self.password_role.currentText()
        self.config_data['allow_central_server_commands_as_ServerConsoleCommands'] = self.central_commands.isChecked()
        self.config_data['enable_predefined_ban_templates'] = self.predefined_bans.isChecked()

    def validate_config_structure(self, config):
        """Basic validation of config structure"""
        required_keys = ['Members', 'Roles', 'Permissions']
        return all(key in config for key in required_keys)

    def set_window_icon(self):
        """Set icon for the main window"""
        
        if os.path.exists("icon.png"):
            self.setWindowIcon(QIcon("icon.png"))
            return
        
        app_icon = QApplication.instance().windowIcon()
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)
        else:
            print("Warning: No icon file found")

    def reset_config(self):
        self.config_data = self.get_default_config()
        self.update_ui_from_config()