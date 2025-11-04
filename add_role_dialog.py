from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QComboBox, QLabel, QDialogButtonBox)
from PyQt6.QtCore import Qt

class AddRoleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Role")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        self.role_name = QLineEdit()
        self.role_name.setPlaceholderText("Role name (e.g.: senior_admin)")
        layout.addWidget(QLabel("Role Name:"))
        layout.addWidget(self.role_name)
        
        self.badge_name = QLineEdit()
        self.badge_name.setPlaceholderText("BADGE NAME")
        layout.addWidget(QLabel("Badge Name:"))
        layout.addWidget(self.badge_name)
        
        self.color_combo = QComboBox()
        self.color_combo.addItems(["red", "blue", "green", "yellow", "purple", "orange", "silver", "none"])
        layout.addWidget(QLabel("Color:"))
        layout.addWidget(self.color_combo)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_role_data(self):
        return {
            'name': self.role_name.text().strip(),
            'badge': self.badge_name.text().strip(),
            'color': self.color_combo.currentText()
        }