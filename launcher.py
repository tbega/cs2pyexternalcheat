import sys
import os
import subprocess
import ctypes
import json
from pathlib import Path
import psutil
import threading
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QProgressBar,
                           QFrame, QGraphicsDropShadowEffect, QMessageBox,
                           QSystemTrayIcon, QMenu, QSpacerItem, QSizePolicy,
                           QLineEdit)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPalette, QColor, QLinearGradient, QPainter


class WorkerThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, operation, *args):
        super().__init__()
        self.operation = operation
        self.args = args
    
    def run(self):
        try:
            if self.operation == "install_deps":
                self.install_dependencies()
            elif self.operation == "launch_cheat":
                self.launch_cheat()
        except Exception as e:
            self.finished.emit(False, str(e))
    
    def install_dependencies(self):
        self.progress.emit("Upgrading pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      capture_output=True, text=True)
        
        self.progress.emit("Installing dependencies...")
        requirements_file = Path(__file__).parent / "requirements.txt"
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            self.finished.emit(True, "Dependencies installed successfully!")
        else:
            self.finished.emit(False, f"Installation failed: {result.stderr}")
    
    def launch_cheat(self):
        self.progress.emit("Launching CS2 External Cheat...")
        script_dir = Path(__file__).parent
        main_script = script_dir / "main.py"
        
        try:
            subprocess.Popen([sys.executable, str(main_script)], cwd=str(script_dir))
            self.finished.emit(True, "Cheat launched successfully!")
        except Exception as e:
            self.finished.emit(False, f"Launch failed: {e}")


class StatusCard(QFrame):
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.is_hovered = False
        self.current_status = "loading"
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        self.setFixedHeight(62)  
        self.setStyleSheet("""
            QFrame {
                background: rgba(40, 40, 45, 0.92);
                border: none;
                border-radius: 14px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 8, 22, 8)
        layout.setSpacing(18)

        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.status_dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_dot.setFixedSize(32, 32)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.title_label = QLabel(self.title)
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #fff; background: transparent;")

        self.status_label = QLabel("Checking...")
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setStyleSheet("color: #B0B0B0; background: transparent;")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.status_label)

        layout.addWidget(self.status_dot)
        layout.addSpacing(8)
        layout.addLayout(text_layout)
        layout.addStretch()

    def setup_animations(self):
        pass  
    
    def enterEvent(self, event):
        super().enterEvent(event)
        self.is_hovered = True
    
    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.is_hovered = False
    
    def set_status(self, status, message, color):
        self.current_status = status
        self.status_dot.setStyleSheet(f"color: {color}; background: transparent;")
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: 500; background: transparent;")


class PremiumButton(QPushButton):
    """Premium button with glassmorphism and animations"""
    
    def __init__(self, text, button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        self.setMinimumHeight(50)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        
        if self.button_type == "primary":
            self.setStyleSheet("""
                PremiumButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #4CAF50, stop:1 #45a049);
                    border: none;
                    border-radius: 12px;
                    color: white;
                    padding: 0 20px;
                }
                PremiumButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #5CBF60, stop:1 #55b059);
                }
                PremiumButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #3CAF40, stop:1 #35a039);
                }
                PremiumButton:disabled {
                    background: rgba(76, 175, 80, 0.5);
                    color: rgba(255, 255, 255, 0.6);
                }
            """)
        elif self.button_type == "secondary":
            self.setStyleSheet("""
                PremiumButton {
                    background: rgba(33, 150, 243, 0.9);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    color: white;
                    padding: 0 15px;
                }
                PremiumButton:hover {
                    background: rgba(33, 150, 243, 1.0);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                PremiumButton:pressed {
                    background: rgba(23, 140, 233, 0.9);
                }
            """)
        
       
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
    
    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)


class LoadingWindow(QMainWindow):
    loading_complete = pyqtSignal()
    
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setup_ui()
        self.start_loading_sequence()
        
    def setup_ui(self):
        self.setWindowTitle("CS2 External - Loading")
        self.setFixedSize(500, 350)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        main_widget = QWidget()
        main_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(25, 25, 35, 0.95), 
                    stop:0.5 rgba(35, 35, 45, 0.95),
                    stop:1 rgba(30, 30, 40, 0.95));
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        self.setCentralWidget(main_widget)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        main_widget.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.welcome_label = QLabel(f"Welcome back, {self.username}!")
        self.welcome_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.welcome_label.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4CAF50, stop:1 #2196F3);
        """)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.welcome_label)
        
        ring_layout = QHBoxLayout()
        ring_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ring_layout.setSpacing(8)
        
        self.ring_dots = []
        for i in range(8):
            dot = QLabel("●")
            dot.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            dot.setStyleSheet("color: rgba(255, 255, 255, 0.2); border: none; outline: none;")
            dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dot.setFixedSize(16, 16)
            ring_layout.addWidget(dot)
            self.ring_dots.append(dot)
        
        layout.addLayout(ring_layout)
        
        self.status_label = QLabel("Initializing components...")
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); border: none; outline: none;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.loading_progress = QProgressBar()
        self.loading_progress.setRange(0, 100)
        self.loading_progress.setValue(0)
        self.loading_progress.setFixedHeight(6)
        self.loading_progress.setTextVisible(False)
        self.loading_progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 3px;
                background: rgba(255, 255, 255, 0.1);
                text-align: center;
                outline: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2196F3);
                border-radius: 3px;
                border: none;
                outline: none;
            }
        """)
        layout.addWidget(self.loading_progress)
    
    def start_loading_sequence(self):
        self.ring_timer = QTimer()
        self.ring_timer.timeout.connect(self.animate_ring)
        self.current_ring_dot = 0
        self.ring_timer.start(120)
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.progress_timer.start(40)
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_step = 0
        self.status_messages = [
            "Starting CS2 External",
            "Preparing",
            "Verifying",
            "Loading components",
            "Done"
        ]
        self.status_timer.start(700)
    
    def animate_ring(self):
        for i, dot in enumerate(self.ring_dots):
            if i == self.current_ring_dot:
                dot.setStyleSheet("color: #4CAF50; border: none; outline: none;")
            elif i == (self.current_ring_dot - 1) % len(self.ring_dots):
                dot.setStyleSheet("color: rgba(76, 175, 80, 0.6); border: none; outline: none;")
            elif i == (self.current_ring_dot - 2) % len(self.ring_dots):
                dot.setStyleSheet("color: rgba(76, 175, 80, 0.3); border: none; outline: none;")
            else:
                dot.setStyleSheet("color: rgba(255, 255, 255, 0.2); border: none; outline: none;")
        
        self.current_ring_dot = (self.current_ring_dot + 1) % len(self.ring_dots)
    
    def update_progress(self):
        self.progress_value += 1.5
        self.loading_progress.setValue(int(min(self.progress_value, 100)))
        
        if self.progress_value >= 100:
            self.progress_timer.stop()
            self.ring_timer.stop()
            self.status_timer.stop()
            QTimer.singleShot(400, self.loading_complete.emit)
            QTimer.singleShot(500, self.close)
    
    def update_status(self):
        if self.status_step < len(self.status_messages):
            self.status_label.setText(self.status_messages[self.status_step])
            self.status_step += 1

class LoginWindow(QMainWindow):
    login_success = pyqtSignal(str, bool) 
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_saved_username()
        
    def setup_ui(self):
        self.setWindowTitle("CS2 External - Login")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        main_widget = QWidget()
        main_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(25, 25, 35, 0.95), 
                    stop:0.5 rgba(35, 35, 45, 0.95),
                    stop:1 rgba(30, 30, 40, 0.95));
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        self.setCentralWidget(main_widget)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        main_widget.setGraphicsEffect(shadow)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        title = QLabel("ENTER USERNAME")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4CAF50, stop:1 #2196F3);
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Your username...")
        self.username_field.setStyleSheet("""
            QLineEdit {
                background: rgba(40, 40, 45, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 15px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        layout.addWidget(self.username_field)
        remember_layout = QHBoxLayout()
        remember_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.remember_checkbox = QPushButton("☐ Remember me")
        self.remember_checkbox.setCheckable(True)
        self.remember_checkbox.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                padding: 5px;
            }
            QPushButton:checked {
                color: #4CAF50;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        self.remember_checkbox.clicked.connect(self.toggle_remember)
        remember_layout.addWidget(self.remember_checkbox)
        layout.addLayout(remember_layout)
        
        login_btn = PremiumButton("CONTINUE", "primary")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        self.username_field.returnPressed.connect(self.handle_login)
        
        self.username_field.setFocus()
    
    def toggle_remember(self):
        if self.remember_checkbox.isChecked():
            self.remember_checkbox.setText("☑ Remember me")
        else:
            self.remember_checkbox.setText("☐ Remember me")
    
    def load_saved_username(self):
        try:
            config_file = Path(__file__).parent / "user_config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if config.get('remember_me') and config.get('username'):
                        self.username_field.setText(config['username'])
                        self.remember_checkbox.setChecked(True)
                        self.toggle_remember()
        except Exception:
            pass
    
    def save_username(self, username, remember):
        try:
            config_file = Path(__file__).parent / "user_config.json"
            config = {'username': username if remember else '', 'remember_me': remember}
            with open(config_file, 'w') as f:
                json.dump(config, f)
        except Exception:
            pass
        
    def handle_login(self):
        username = self.username_field.text().strip()
        remember = self.remember_checkbox.isChecked()
        
        if username:
            self.save_username(username, remember)
            self.login_success.emit(username, remember)
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Please enter a username.")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.drag_start_position)
                self.drag_start_position = event.globalPosition().toPoint()

class CustomMessageBox(QWidget):
    def __init__(self, parent, title, message, msg_type="info"):
        super().__init__(parent)
        self.msg_type = msg_type
        self.setup_ui(title, message)
        self.show_animation()
    
    def setup_ui(self, title, message):
        self.setFixedSize(350, 150)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(35, 35, 45, 0.95), 
                    stop:1 rgba(45, 45, 55, 0.95));
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        if self.msg_type == "success":
            title_label.setStyleSheet("color: #4CAF50;")
        elif self.msg_type == "error":
            title_label.setStyleSheet("color: #F44336;")
        else:
            title_label.setStyleSheet("color: #2196F3;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        msg_label = QLabel(message)
        msg_label.setFont(QFont("Segoe UI", 11))
        msg_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label)
        if self.parent():
            parent_rect = self.parent().geometry()
            self.move(
                parent_rect.width() // 2 - self.width() // 2,
                parent_rect.height() // 2 - self.height() // 2
            )
    
    def show_animation(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        start_rect = self.geometry()
        start_rect.moveTop(start_rect.top() - 50)
        end_rect = self.geometry()
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        QTimer.singleShot(3000, self.close_animation)
    
    def close_animation(self):
        self.close_anim = QPropertyAnimation(self, b"geometry")
        self.close_anim.setDuration(200)
        self.close_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        
        start_rect = self.geometry()
        end_rect = start_rect
        end_rect.moveTop(end_rect.top() - 30)
        
        self.close_anim.setStartValue(start_rect)
        self.close_anim.setEndValue(end_rect)
        self.close_anim.finished.connect(self.deleteLater)
        self.close_anim.start()

class CS2LauncherGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_dir = Path(__file__).parent.absolute()
        self.main_script = self.script_dir / "main.py"
        self.requirements_file = self.script_dir / "requirements.txt"
        self.is_running = False
        self.username = ""
        self.is_admin = self.check_admin_privileges()
        self.setup_ui()
        self.setup_system_tray()
        self.setup_timers()
        self.setup_status_animations()
        self.update_all_status()
        self.check_saved_user()
    
    def check_saved_user(self):
        try:
            config_file = Path(__file__).parent / "user_config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if config.get('remember_me') and config.get('username'):
                        self.username = config['username']
                        self.show_loading()
                        return
        except Exception:
            pass
        
        self.hide()
        self.show_login()
    
    def on_login_success(self, username, remember_me):
        self.username = username
        self.show_loading()

    def show_login(self):
        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.on_login_success)
        screen = QApplication.primaryScreen().geometry()
        window = self.login_window.geometry()
        self.login_window.move(
            (screen.width() - window.width()) // 2,
            (screen.height() - window.height()) // 2
        )
        
        self.login_window.show()
    
    def show_loading(self):
        self.loading_window = LoadingWindow(self.username)
        self.loading_window.loading_complete.connect(self.on_loading_complete)
        screen = QApplication.primaryScreen().geometry()
        window = self.loading_window.geometry()
        self.loading_window.move(
            (screen.width() - window.width()) // 2,
            (screen.height() - window.height()) // 2
        )
        
        self.loading_window.show()
    
    def on_loading_complete(self):
        self.show()
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        self.move(
            (screen.width() - window.width()) // 2,
            (screen.height() - window.height()) // 2
        )
        
        # Update header with username
        self.update_header_with_username()
    
    def update_header_with_username(self):
        # Find the title label and update it
        title_label = self.centralWidget().findChild(QLabel)
        if title_label and "CS2 EXTERNAL" in title_label.text():
            welcome_text = f"Welcome back, {self.username}!"
            subtitle = self.centralWidget().findChildren(QLabel)[1]  
            subtitle.setText(welcome_text)
            subtitle.setStyleSheet("color: #4CAF50; margin: 0px; padding: 0px; font-weight: bold;")

    def setup_ui(self):
        self.setWindowTitle("CS2 External Cheat - Premium Launcher")
        self.setFixedSize(660, 820)  
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        main_widget = QWidget()
        main_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(25, 25, 35, 0.95), 
                    stop:0.5 rgba(35, 35, 45, 0.95),
                    stop:1 rgba(30, 30, 40, 0.95));
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        self.setCentralWidget(main_widget)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        main_widget.setGraphicsEffect(shadow)
        







        # setup the main layout
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(25) 
        self.create_header(layout)
        self.create_status_section(layout)
        layout.addSpacing(80)       
        self.create_progress_section(layout)
        self.create_controls_section(layout)

    def create_header(self, layout):
        # Change quit button to properly close console
        quit_btn = QPushButton("Quit")
        quit_btn.setFixedSize(60, 28)
        quit_btn.setStyleSheet("""
            QPushButton {
                background: rgba(220, 50, 50, 0.8);
                border: none;
                border-radius: 14px;
                color: white;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: rgba(240, 70, 70, 0.9);
            }
        """)
        quit_btn.clicked.connect(self.quit_application)
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(quit_btn)
        layout.addLayout(close_layout)
        header_frame = QFrame()
        header_frame.setStyleSheet("background: transparent; border: none;")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(0, 10, 0, 20)
        title = QLabel("CS2 EXTERNAL")
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4CAF50, stop:1 #2196F3);
            margin: 0px;
            padding: 0px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Launcher")  
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); margin: 0px; padding: 0px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_frame)
    
    def create_status_section(self, layout):
        """Create the status monitoring section with better spacing"""
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background: rgba(20, 20, 25, 0.7);
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.06);
            }
        """)
        status_frame.setMinimumHeight(320)  
        status_frame.setMaximumHeight(320)  
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(22, 20, 22, 20) 
        status_layout.setSpacing(0)
        title = QLabel("SYSTEM STATUS")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("""
            color: #FFFFFF;
            margin-bottom: 0px;
            padding: 0px 0px 8px 0px;
            border: none;
            background: transparent;
        """)
        status_layout.addWidget(title)
        status_layout.addSpacing(12)  
        self.admin_card = StatusCard("Admin Privileges")
        self.cs2_card = StatusCard("CS2 Running")
        self.deps_card = StatusCard("Dependencies")
        self.files_card = StatusCard("Required Files")

        cards = [self.admin_card, self.cs2_card, self.deps_card, self.files_card]
        for i, card in enumerate(cards):
            status_layout.addWidget(card)
            if i < len(cards) - 1:
                status_layout.addSpacing(15) 

        layout.addWidget(status_frame)
    
    def create_progress_section(self, layout):
        progress_container = QWidget()
        progress_container.setFixedHeight(30)
        progress_container_layout = QVBoxLayout(progress_container)
        progress_container_layout.setContentsMargins(0, 10, 0, 10)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 3px;
                background: rgba(255, 255, 255, 0.08);
                outline: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2196F3);
                border-radius: 3px;
                border: none;
                outline: none;
            }
        """)
        self.progress_bar.setVisible(False)
        progress_container_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_container)
    
    def create_controls_section(self, layout):
        self.launch_btn = PremiumButton("🚀 LAUNCH CS2 CHEAT", "primary")
        self.launch_btn.setMinimumHeight(55)
        self.launch_btn.clicked.connect(self.launch_cheat)
        layout.addWidget(self.launch_btn)
        
        # Utility buttons
        util_layout = QHBoxLayout()
        util_layout.setSpacing(12)
        
        self.install_btn = PremiumButton("📦 Install Dependencies", "secondary")
        self.install_btn.clicked.connect(self.install_dependencies)
        
        self.refresh_btn = PremiumButton("🔄 Refresh Status", "secondary")
        self.refresh_btn.clicked.connect(self.update_all_status)
        
        util_layout.addWidget(self.install_btn)
        util_layout.addWidget(self.refresh_btn)
        layout.addLayout(util_layout)
    
    def setup_system_tray(self):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
            
            tray_menu = QMenu()
            show_action = tray_menu.addAction("Show Launcher")
            show_action.triggered.connect(self.show)
            quit_action = tray_menu.addAction("Quit")
            quit_action.triggered.connect(self.close)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
    
    def setup_timers(self):
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_all_status)
        self.status_timer.start(30000)  # you kinda have to update every 30 seconds \ user might be dumb and not know how to refresh
    
    def check_admin_privileges(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def restart_as_admin(self):
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{__file__}"', None, 1
            )
            self.close()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to restart as administrator:\n{e}")
            return False
    
    def check_cs2_running(self):
        for process in psutil.process_iter(['name']):
            try:
                if 'cs2' in process.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    
    def check_files_exist(self):
        return (self.main_script.exists() and 
                self.requirements_file.exists() and
                (self.script_dir / "Cheat").exists())
    
    def check_dependencies(self): # this is buggy?? why
        required_packages = {
            'psutil': 'psutil',
            'pywin32': 'win32api',
            'requests': 'requests',
            'pyMeow': 'pyMeow',
            'dearpygui': 'dearpygui',
            'keyboard': 'keyboard',
            'pynput': 'pynput'
        }
        
        for package_name, import_name in required_packages.items():
            try:
                __import__(import_name)
            except ImportError:
                return False
        return True
    
    def update_all_status(self): 
        cards = [self.admin_card, self.cs2_card, self.deps_card, self.files_card]
        for card in cards:
            card.status_dot.setStyleSheet("color: white; background: transparent;")
            card.status_label.setText("Refreshing...")
            card.status_label.setStyleSheet("color: white; font-weight: 500; background: transparent;")
        # works
        
        QTimer.singleShot(500, self.perform_status_update)
    
    def perform_status_update(self):
        if self.is_admin:
            self.admin_card.set_status("success", "Running with admin privileges", "#4CAF50")
        else:
            self.admin_card.set_status("warning", "Not running as admin", "#FF9800")

        if self.check_cs2_running():
            self.cs2_card.set_status("success", "Running and detected", "#4CAF50")
        else:
            self.cs2_card.set_status("error", "Not running", "#F44336")

        if self.check_dependencies():
            self.deps_card.set_status("success", "All packages installed", "#4CAF50")
        else:
            self.deps_card.set_status("error", "Missing packages", "#F44336")

        if self.check_files_exist():
            self.files_card.set_status("success", "All required files found", "#4CAF50")
        else:
            self.files_card.set_status("error", "Missing required files", "#F44336")

    def install_dependencies(self):
        if self.is_running:
            return
        
        self.is_running = True
        self.install_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  
        self.worker = WorkerThread("install_deps")
        self.worker.finished.connect(self.on_install_finished)
        self.worker.start()
    
    def on_install_finished(self, success, message):
        self.is_running = False
        self.install_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        # this doesnt work... okay!
        if success:
            CustomMessageBox(self, "Success", message, "success")
        else:
            CustomMessageBox(self, "Error", message, "error")
        
        self.update_all_status()

    def quit_application(self):
        import os
        import sys

        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        
        QApplication.quit()
              
        if sys.platform == "win32":
            try:
                os._exit(0)
            except:
                pass

    def launch_cheat(self):
        if self.is_running:
            return
        
        if not self.is_admin:
            reply = QMessageBox.question(
                self, "Administrator Required",
                "This application works best with administrator privileges.\n\n"
                "Would you like to restart as administrator?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                if self.restart_as_admin():
                    return
        
        if not self.check_files_exist():
            QMessageBox.critical(self, "Error", "Required files are missing! Please check your installation.")
            return
        
        if not self.check_dependencies():
            reply = QMessageBox.question(
                self, "Missing Dependencies",
                "Some dependencies are missing. Would you like to install them now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.install_dependencies()
                return
        
        if not self.check_cs2_running():
            reply = QMessageBox.question(
                self, "CS2 Not Running",
                "Counter-Strike 2 is not currently running.\n\n"
                "The cheat requires CS2 to be running. Continue anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        self.start_enhanced_launch_animation()
        self.is_running = True
        self.launch_btn.setEnabled(False)
        self.launch_btn.setText("🔄 LAUNCHING...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        self.worker = WorkerThread("launch_cheat")
        self.worker.finished.connect(self.on_launch_finished)
        self.worker.start()
    
    def start_enhanced_launch_animation(self):
        self.pulse_animation = QPropertyAnimation(self, b"geometry")
        self.pulse_animation.setDuration(300)
        self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        current_rect = self.geometry()
        pulse_rect = QRect(
            current_rect.x() - 5,
            current_rect.y() - 5,
            current_rect.width() + 10,
            current_rect.height() + 10
        )
        
        self.pulse_animation.setStartValue(current_rect)
        self.pulse_animation.setEndValue(pulse_rect)
        self.pulse_animation.finished.connect(self.reverse_pulse_animation)
        self.button_animation = QPropertyAnimation(self.launch_btn, b"geometry")
        self.button_animation.setDuration(150)
        self.button_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        btn_rect = self.launch_btn.geometry()
        smaller_btn = QRect(
            btn_rect.x() + 5,
            btn_rect.y() + 2,
            btn_rect.width() - 10,
            btn_rect.height() - 4
        )
        
        self.button_animation.setStartValue(btn_rect)
        self.button_animation.setEndValue(smaller_btn)
        self.pulse_animation.start()
        self.button_animation.start()
    
    def reverse_pulse_animation(self):
        self.pulse_reverse = QPropertyAnimation(self, b"geometry")
        self.pulse_reverse.setDuration(300)
        self.pulse_reverse.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        current_rect = self.geometry()
        original_rect = QRect(
            current_rect.x() + 5,
            current_rect.y() + 5,
            current_rect.width() - 10,
            current_rect.height() - 10
        )
        
        self.pulse_reverse.setStartValue(current_rect)
        self.pulse_reverse.setEndValue(original_rect)
        self.pulse_reverse.start()

    def on_launch_finished(self, success, message):
        self.is_running = False
        self.launch_btn.setEnabled(True)
        self.launch_btn.setText("🚀 LAUNCH CS2 CHEAT")
        self.progress_bar.setVisible(False)
        
        if success:
            CustomMessageBox(self, "Launch Successful", 
                           "CS2 External Cheat launched successfully!\nLauncher will close in 2 seconds.", 
                           "success")
            QTimer.singleShot(2500, self.quit_application)
        else:
            CustomMessageBox(self, "Launch Error", f"Failed to launch cheat:\n{message}", "error")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.drag_start_position)
                self.drag_start_position = event.globalPosition().toPoint()
    
    def setup_status_animations(self):
        self.entrance_timer = QTimer()
        self.entrance_timer.setSingleShot(True)
        self.entrance_timer.timeout.connect(self.animate_cards_entrance)
        self.entrance_timer.start(300)
    
    def animate_cards_entrance(self):
        cards = [self.admin_card, self.cs2_card, self.deps_card, self.files_card]
        
        for i, card in enumerate(cards):
            entrance_animation = QPropertyAnimation(card, b"geometry")
            entrance_animation.setDuration(350)
            entrance_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            current_rect = card.geometry()
            start_rect = QRect(
                current_rect.x() - 15,
                current_rect.y(),
                current_rect.width(),
                current_rect.height()
            )
            
            entrance_animation.setStartValue(start_rect)
            entrance_animation.setEndValue(current_rect)
            QTimer.singleShot(i * 80, entrance_animation.start)

def main():
    import ctypes
    if sys.platform == "win32":
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)  
    app.setApplicationName("CS2 External Cheat Launcher")
    app.setApplicationVersion("2.0")
    
    launcher = CS2LauncherGUI()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()