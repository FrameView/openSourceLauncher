import os
import sys
import shutil
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QLabel, QFileDialog, QListWidget, QMessageBox)

#Global variables
path = ""
instances = ["1.21.8 (Latest)", "1.20.6", "1.19.4", "1.18.2", "1.17.1", "1.16.5", "1.15.2", "1.14.4", "1.13.2", "1.12.2"]

class MinecraftLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        #Launcher variables
        self.version_label = QLabel("Select a MC version:")
        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems([i for i in instances])
        self.mods_label = QLabel("Add mods:")
        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        self.launch_button = QPushButton("Launch")
        self.mods_list = QListWidget()
        self.container = QWidget()

        #Layout Management
        layout = QVBoxLayout()
        layout.addWidget(self.version_label)
        layout.addWidget(self.version_dropdown)
        layout.addWidget(self.mods_label)
        layout.addWidget(self.mods_list)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.launch_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  
        layout.setSpacing(10) 

        #UI Management
        self.container.setLayout(layout)
        self.setWindowTitle("Sushi Launcher")
        self.setGeometry(100, 100, 300, 300)
        self.setCentralWidget(self.container)

        #Link buttons to specific actions
        self.launch_button.clicked.connect(self.launch_minecraft)
        self.add_button.clicked.connect(self.add_mod)
        self.remove_button.clicked.connect(self.remove_mod)
        self.version_dropdown.currentTextChanged.connect(self.load_mods)

    def launch_minecraft(self):
        selected_version = self.version_dropdown.currentText()
        print(f"Launching Minecraft {selected_version}")
        for i in instances:
            if selected_version == i:
                path = f"./instances/{i if selected_version != instances[0] else "1.21.8"}"
                break
        try:
            subprocess.Popen(f'cd "{path}" && gradlew runClient', shell=True)
        except Exception as e:
            print(f"Failed to launch: {e}")


    def add_mod(self):  
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "JAR Files (*.jar);;All Files (*)")
        if not file_path:  
            return
        
        try:
            selected_version = self.version_dropdown.currentText()
            mods_folder = f"./instances/{selected_version if selected_version != instances[0] else "1.21.8"}/run/mods"
            
            os.makedirs(mods_folder, exist_ok=True)
            mod_filename = os.path.basename(file_path)
            destination_path = os.path.join(mods_folder, mod_filename)
            
            shutil.copy2(file_path, destination_path)
            self.mods_list.addItem(mod_filename)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add mod:\n{e}")

    def remove_mod(self):   
        selected_item = self.mods_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select a mod to remove.")
            return
        
        mod_filename = selected_item.text()
        selected_version = self.version_dropdown.currentText()
        mods_folder = f"./instances/{selected_version if selected_version != instances[0] else "1.21.8"}/run/mods"
        mod_file_path = os.path.join(mods_folder, mod_filename)
        
        try:
            if os.path.exists(mod_file_path):
                os.remove(mod_file_path)
                self.mods_list.takeItem(self.mods_list.row(selected_item))
            else:
                self.mods_list.takeItem(self.mods_list.row(selected_item))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to remove mod:\n{e}")

    def load_mods(self):
        selected_version = self.version_dropdown.currentText()
        self.mods_list.clear()
        mods_folder = f"./instances/{selected_version if selected_version != instances[0] else "1.21.8"}/run/mods"
        if os.path.exists(mods_folder):
            for mod_file in os.listdir(mods_folder):
                if mod_file.endswith('.jar'):
                    self.mods_list.addItem(mod_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = MinecraftLauncher()
    launcher.show()
    sys.exit(app.exec())