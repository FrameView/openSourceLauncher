import os
import sys
import shutil
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QLabel, QFileDialog, QListWidget, QMessageBox, QHBoxLayout



#Global variables
path = ""
instances = ["1.21.8 (Latest)", "1.20.6", "1.19.4", "1.18.2", "1.17.1", "1.16.5", "1.15.2", "1.14.4", "1.13.2", "1.12.2"]



#Main class
class MinecraftLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        #Launcher variables
        self.mods_list = QListWidget()
        self.container = QWidget()
        self.version_label = QLabel("Select a MC version:")
        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems([i for i in instances])
        self.mods_label = QLabel("Add mods:")
        
        #Buttons
        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        self.add_button.setFixedSize(40, 40)  
        self.remove_button.setFixedSize(40, 40)
        self.launch_button = QPushButton("Launch🚀")
        self.background_button = QPushButton("🎨")
        self.background_button.setFixedSize(40, 40) 
        self.background_button.setToolTip("Switch background")

        #Layouts
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.version_label)
        top_layout.addStretch()  
        top_layout.addWidget(self.background_button)
        
        mods_header_layout = QHBoxLayout()
        mods_header_layout.addWidget(self.mods_label)
        mods_header_layout.addWidget(self.add_button)
        mods_header_layout.addWidget(self.remove_button)
        mods_header_layout.addStretch()  # Push buttons to the left
        mods_header_layout.setSpacing(5)  
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)  
        main_layout.addWidget(self.version_dropdown)
        main_layout.addLayout(mods_header_layout)  
        main_layout.addWidget(self.mods_list)
        main_layout.addWidget(self.launch_button)  
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  
        main_layout.setSpacing(10) 

        #Global setup
        self.container.setLayout(main_layout)
        self.setWindowTitle("Sushi Launcher")
        self.setGeometry(100, 100, 1000, 500)
        self.setCentralWidget(self.container)

        #Link buttons to specific actions
        self.launch_button.clicked.connect(self.launch_minecraft)
        self.add_button.clicked.connect(self.add_mod)
        self.remove_button.clicked.connect(self.remove_mod)
        self.version_dropdown.currentTextChanged.connect(self.load_mods)
        self.background_button.clicked.connect(self.switch_background)



    #Launch the current instance
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



    #Add a mod to the current instance
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


            
    #Remove selected mod from the current instance
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



    #Load mods each time we switch instance accordingly
    def load_mods(self):
        selected_version = self.version_dropdown.currentText()
        self.mods_list.clear()
        mods_folder = f"./instances/{selected_version if selected_version != instances[0] else "1.21.8"}/run/mods"
        if os.path.exists(mods_folder):
            for mod_file in os.listdir(mods_folder):
                if mod_file.endswith('.jar'):
                    self.mods_list.addItem(mod_file)



    #Switch background
    def switch_background(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)")
        if not file_path:  
            return
        try:
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                QMessageBox.warning(self, "Error", "Failed to load the image file.")
                return
            
            self.container.setStyleSheet(f"""
                QWidget {{
                    background-image: url({file_path});
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                QLabel {{
                    background: transparent;
                    color: white;
                    font-weight: bold;
                    font-size: 14pt;
                }}
                QPushButton {{
                    background: transparent;
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 100);
                    border-radius: 5px;
                    padding: 6px;
                    font-weight: bold;
                    font-size: 16pt;
                }}
                QPushButton:hover {{
                    background: rgba(255, 255, 255, 30);
                    border: 1px solid rgba(255, 255, 255, 150);
                }}
                QPushButton:pressed {{
                    background: rgba(255, 255, 255, 50);
                }}
                QComboBox {{
                    background: transparent;
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 100);
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 12pt;
                }}
                QComboBox QAbstractItemView {{
                    background: rgba(0, 0, 0, 200);
                    color: white;
                    selection-background-color: rgba(100, 100, 100, 200);
                    font-size: 12pt;
                }}
                QComboBox::drop-down {{
                    border: none;
                    background: transparent;
                }}
                QListWidget {{
                    background: transparent;
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 100);
                    border-radius: 5px;
                    font-size: 12pt;
                }}
                QListWidget::item {{
                    background: transparent;
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 50);
                    border-radius: 3px;
                    margin: 2px;
                    padding: 5px;
                    font-size: 12pt;  
                }}
                QListWidget::item:selected {{
                    background: rgba(255, 255, 255, 50);
                    color: white;
                }}
                QListWidget::item:hover {{
                    background: rgba(255, 255, 255, 30);
                }}
            """)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to set background:\n{e}")



    #Resize event to maintain background scaling
    def resizeEvent(self, event): 
        current_palette = self.palette() # Reapply background when window is resized
        if current_palette.brush(QPalette.ColorRole.Window).texture().isNull():
            return
        super().resizeEvent(event)



#Software init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = MinecraftLauncher()
    launcher.show()
    sys.exit(app.exec())