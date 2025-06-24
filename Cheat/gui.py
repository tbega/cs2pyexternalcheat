import os
os.environ["QT_LOGGING_RULES"] = "qt.qpa.*=false"
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QCheckBox, QLabel, QGroupBox, QSlider, QPushButton, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect, QTabBar, QColorDialog, QToolButton, QButtonGroup, QDialog, QGridLayout, QLineEdit
)
from PySide6.QtGui import QFont, QColor, QPalette, QPainter, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from Cheat.config import cfg, ConfigManager
PASTEL_BG = QColor(34, 34, 59)
PASTEL_ACCENT = QColor(201, 173, 167)
PASTEL_HEADER = QColor(154, 140, 152)
PASTEL_CHECK = QColor(163, 230, 53)
class AnimatedCheckBox(QCheckBox):
    def __init__(self, label):
        super().__init__(label)
        self.setFont(QFont("Segoe UI", 13))
        self.setStyleSheet(
            "QCheckBox { color: white; spacing: 12px; } "
            "QCheckBox::indicator { width: 24px; height: 24px; border-radius: 9px; border: 2.5px solid #C9ADA7; background: #5E5A80; } "
            "QCheckBox::indicator:unchecked { border: 2.5px solid #C9ADA7; background: #5E5A80; } "
            "QCheckBox::indicator:checked { border: 3px solid #A3E635; background: #5E5A80; } "
            "QCheckBox::indicator:hover { border: 2.5px solid #9A8C98; background: #726D99; } "
            "QCheckBox::indicator:checked:hover { border: 3px solid #A3E635; background: #726D99; } "
            "QCheckBox::indicator:checked:disabled { background: #B8B8D1; } "
            "QCheckBox::indicator:unchecked:disabled { background: #B8B8D1; } "
        )
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(163, 230, 53, 120))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        self.stateChanged.connect(self.animate_glow)
        self.stateChanged.connect(self.update_bold)
        self._default_font = QFont("Segoe UI", 13)
        self._bold_font = QFont("Segoe UI", 13, QFont.Bold)
        self._default_size = 24
        self._large_size = 28
        self._anim_size = None
    def animate_glow(self, state):
        anim = QPropertyAnimation(self.shadow, b"blurRadius")
        anim.setDuration(220)
        if state:
            anim.setStartValue(0)
            anim.setEndValue(18)
        else:
            anim.setStartValue(self.shadow.blurRadius())
            anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        self._anim = anim  
        self.set_indicator_size(self._large_size if state else self._default_size)
    def set_indicator_size(self, value):
        size = int(value)
        self.setStyleSheet(
            f"QCheckBox {{ color: {'#A3E635' if self.isChecked() else 'white'}; font-weight: {'bold' if self.isChecked() else 'normal'}; spacing: 12px; }} "
            f"QCheckBox::indicator {{ width: {size}px; height: {size}px; border-radius: 9px; border: 2.5px solid {'#A3E635' if self.isChecked() else '#C9ADA7'}; background: #5E5A80; }} "
            f"QCheckBox::indicator:unchecked {{ border: 2.5px solid #C9ADA7; background: #5E5A80; }} "
            f"QCheckBox::indicator:checked {{ border: 3px solid #A3E635; background: #5E5A80; }} "
            f"QCheckBox::indicator:hover {{ border: 2.5px solid #9A8C98; background: #726D99; }} "
            f"QCheckBox::indicator:checked:hover {{ border: 3px solid #A3E635; background: #726D99; }} "
            f"QCheckBox::indicator:checked:disabled {{ background: #B8B8D1; }} "
            f"QCheckBox::indicator:unchecked:disabled {{ background: #B8B8D1; }} "
        )
    def update_bold(self, state):
        self.setFont(self._bold_font if state else self._default_font)
        self.setStyleSheet(
            f"QCheckBox {{ color: {'#A3E635' if state else 'white'}; font-weight: {'bold' if state else 'normal'}; spacing: 12px; }} "
            f"QCheckBox::indicator {{ width: {self._large_size if state else self._default_size}px; height: {self._large_size if state else self._default_size}px; border-radius: 9px; border: 2.5px solid {'#A3E635' if state else '#C9ADA7'}; background: #5E5A80; }} "
            f"QCheckBox::indicator:unchecked {{ border: 2.5px solid #C9ADA7; background: #5E5A80; }} "
            f"QCheckBox::indicator:checked {{ border: 3px solid #A3E635; background: #5E5A80; }} "
            f"QCheckBox::indicator:hover {{ border: 2.5px solid #9A8C98; background: #726D99; }} "
            f"QCheckBox::indicator:checked:hover {{ border: 3px solid #A3E635; background: #726D99; }} "
            f"QCheckBox::indicator:checked:disabled {{ background: #B8B8D1; }} "
            f"QCheckBox::indicator:unchecked:disabled {{ background: #B8B8D1; }} "
        )
class ESPTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(18)
        accent = QLabel()
        accent.setFixedHeight(6)
        accent.setStyleSheet("background: #A3E635; border-radius: 3px;")
        layout.addWidget(accent)
        header = QLabel("ESP Visual Features")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: white;")
        header.setAlignment(Qt.AlignHCenter)
        layout.addWidget(header)
        subtitle = QLabel("Customize your ESP experience")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #C9ADA7;")
        subtitle.setAlignment(Qt.AlignHCenter)
        layout.addWidget(subtitle)
        card = QGroupBox()
        card.setStyleSheet(
            "QGroupBox { background: #4A4E69; border: 2px solid #C9ADA7; border-radius: 16px; margin-top: 18px; }"
        )
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)
        self.main_toggle = QToolButton()
        self.main_toggle.setText("Main")
        self.main_toggle.setCheckable(True)
        self.main_toggle.setChecked(True)
        self.main_toggle.setArrowType(Qt.DownArrow)
        self.main_toggle.setStyleSheet("color: white; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.main_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 0, 0, 0)
        self.box_cb = AnimatedCheckBox("Show Box")
        self.line_cb = AnimatedCheckBox("Show Line")
        self.head_cb = AnimatedCheckBox("Head Circle")
        self.skeleton_cb = AnimatedCheckBox("Skeleton")
        self.visible_cb = AnimatedCheckBox("Visible Only")
        self.box_cb.setChecked(cfg.ESP.show_box)
        self.line_cb.setChecked(cfg.ESP.show_line)
        self.head_cb.setChecked(cfg.ESP.show_head_circle)
        self.skeleton_cb.setChecked(cfg.ESP.show_skeleton)
        self.visible_cb.setChecked(getattr(cfg.ESP, "visible_only", False))
        self.box_cb.stateChanged.connect(lambda state: (setattr(cfg.ESP, "show_box", bool(state)), ConfigManager.save_config()))
        self.line_cb.stateChanged.connect(lambda state: (setattr(cfg.ESP, "show_line", bool(state)), ConfigManager.save_config()))
        self.head_cb.stateChanged.connect(lambda state: (setattr(cfg.ESP, "show_head_circle", bool(state)), ConfigManager.save_config()))
        self.skeleton_cb.stateChanged.connect(lambda state: (setattr(cfg.ESP, "show_skeleton", bool(state)), ConfigManager.save_config()))
        self.visible_cb.stateChanged.connect(lambda state: (setattr(cfg.ESP, "visible_only", bool(state)), ConfigManager.save_config()))
        for cb in [self.box_cb, self.line_cb, self.head_cb, self.skeleton_cb, self.visible_cb]:
            main_layout.addWidget(cb)
        self.main_widget.setLayout(main_layout)
        self.main_widget.setVisible(True)
        def toggle_main():
            expanded = self.main_toggle.isChecked()
            self.main_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.main_widget.setVisible(expanded)
        self.main_toggle.clicked.connect(toggle_main)
        self.info_toggle = QToolButton()
        self.info_toggle.setText("Info")
        self.info_toggle.setCheckable(True)
        self.info_toggle.setChecked(False)
        self.info_toggle.setArrowType(Qt.RightArrow)
        self.info_toggle.setStyleSheet("color: #A3E635; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.info_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.info_widget = QWidget()
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(24, 0, 0, 0)
        self.info_distance = AnimatedCheckBox("Distance")
        self.info_name = AnimatedCheckBox("Name")
        self.info_weapon = AnimatedCheckBox("Weapon")
        self.info_health = AnimatedCheckBox("Health Text")
        self.info_distance.setChecked(cfg.ESP.show_distance)
        self.info_name.setChecked(cfg.ESP.show_name)
        self.info_weapon.setChecked(cfg.ESP.show_weapon)
        self.info_health.setChecked(cfg.ESP.show_health_text)
        for cb, attr in zip([self.info_distance, self.info_name, self.info_weapon, self.info_health],
                            ["show_distance", "show_name", "show_weapon", "show_health_text"]):
            def make_handler(cb, attr):
                def handler(state):
                    setattr(cfg.ESP, attr, bool(state))
                    ConfigManager.save_config()
                return handler
            cb.stateChanged.connect(make_handler(cb, attr))
        for cb in [self.info_distance, self.info_name, self.info_weapon, self.info_health]:
            info_layout.addWidget(cb)
        self.info_widget.setLayout(info_layout)
        self.info_widget.setVisible(False)
        def toggle_info():
            expanded = self.info_toggle.isChecked()
            self.info_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.info_widget.setVisible(expanded)
        self.info_toggle.clicked.connect(toggle_info)
        self.styles_toggle = QToolButton()
        self.styles_toggle.setText("Styles")
        self.styles_toggle.setCheckable(True)
        self.styles_toggle.setChecked(False)
        self.styles_toggle.setArrowType(Qt.RightArrow)
        self.styles_toggle.setStyleSheet("color: #F76C6C; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.styles_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.styles_widget = QWidget()
        styles_layout = QVBoxLayout()
        styles_layout.setContentsMargins(24, 0, 0, 0)
        self.box_style_options = ["Regular", "Cornered"]
        self.box_style_idx = self.box_style_options.index(getattr(cfg.ESP, "box_style", "Regular")) if hasattr(cfg.ESP, "box_style") else 0
        self.box_style_btn = QPushButton(f"Box: {self.box_style_options[self.box_style_idx]}")
        self.box_style_btn.setStyleSheet("background: #F6E7CB; color: #726D99; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
        def cycle_box_style():
            self.box_style_idx = (self.box_style_idx + 1) % len(self.box_style_options)
            self.box_style_btn.setText(f"Box: {self.box_style_options[self.box_style_idx]}")
            cfg.ESP.box_style = self.box_style_options[self.box_style_idx]
            ConfigManager.save_config()
        self.box_style_btn.clicked.connect(cycle_box_style)
        styles_layout.addWidget(self.box_style_btn)
        self.line_pos_options = ["Center", "Top", "Bottom"]
        self.line_pos_idx = self.line_pos_options.index(getattr(cfg.ESP, "line_position", "Bottom")) if hasattr(cfg.ESP, "line_position") else 0
        self.line_pos_btn = QPushButton(f"Line: {self.line_pos_options[self.line_pos_idx]}")
        self.line_pos_btn.setStyleSheet("background: #F6E7CB; color: #726D99; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
        def cycle_line_pos():
            self.line_pos_idx = (self.line_pos_idx + 1) % len(self.line_pos_options)
            self.line_pos_btn.setText(f"Line: {self.line_pos_options[self.line_pos_idx]}")
            cfg.ESP.line_position = self.line_pos_options[self.line_pos_idx]
            ConfigManager.save_config()
        self.line_pos_btn.clicked.connect(cycle_line_pos)
        styles_layout.addWidget(self.line_pos_btn)
        self.styles_widget.setLayout(styles_layout)
        self.styles_widget.setVisible(False)
        def toggle_styles():
            expanded = self.styles_toggle.isChecked()
            self.styles_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.styles_widget.setVisible(expanded)
        self.styles_toggle.clicked.connect(toggle_styles)
        self.colors_toggle = QToolButton()
        self.colors_toggle.setText("Colors")
        self.colors_toggle.setCheckable(True)
        self.colors_toggle.setChecked(False)
        self.colors_toggle.setArrowType(Qt.RightArrow)
        self.colors_toggle.setStyleSheet("color: #B8B8D1; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.colors_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.colors_widget = QWidget()
        colors_layout = QVBoxLayout()
        colors_layout.setContentsMargins(24, 0, 0, 0)
        self.box_color_btn = QPushButton("Box Color")
        self.box_color = QColor(*cfg.ESP.box_color)
        self.box_color_btn.setStyleSheet(f"background: {self.box_color.name()}; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
        def pick_box_color():
            dlg = PastelColorDialog(self, self.box_color)
            if dlg.exec():
                self.box_color = dlg.getColor()
                self.box_color_btn.setStyleSheet(f"background: {self.box_color.name()}; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
                cfg.ESP.box_color = [self.box_color.red(), self.box_color.green(), self.box_color.blue(), self.box_color.alpha()]
                ConfigManager.save_config()
        self.box_color_btn.clicked.connect(pick_box_color)
        colors_layout.addWidget(self.box_color_btn)
        self.line_color_btn = QPushButton("Line Color")
        self.line_color_btn.setStyleSheet("background: #C9ADA7; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
        self.line_color = QColor(*cfg.ESP.line_color)
        def pick_line_color():
            dlg = PastelColorDialog(self, self.line_color)
            if dlg.exec():
                self.line_color = dlg.getColor()
                self.line_color_btn.setStyleSheet(f"background: {self.line_color.name()}; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
                cfg.ESP.line_color = [self.line_color.red(), self.line_color.green(), self.line_color.blue(), self.line_color.alpha()]
                ConfigManager.save_config()
        self.line_color_btn.clicked.connect(pick_line_color)
        colors_layout.addWidget(self.line_color_btn)
        self.skel_color_btn = QPushButton("Skeleton Color")
        self.skel_color_btn.setStyleSheet("background: #9A8C98; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
        self.skel_color = QColor(*cfg.ESP.skeleton_color)
        def pick_skel_color():
            dlg = PastelColorDialog(self, self.skel_color)
            if dlg.exec():
                self.skel_color = dlg.getColor()
                self.skel_color_btn.setStyleSheet(f"background: {self.skel_color.name()}; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
                cfg.ESP.skeleton_color = [self.skel_color.red(), self.skel_color.green(), self.skel_color.blue(), self.skel_color.alpha()]
                ConfigManager.save_config()
        self.skel_color_btn.clicked.connect(pick_skel_color)
        colors_layout.addWidget(self.skel_color_btn)
        self.vis_box_color_btn = QPushButton("Visible Box Color")
        self.vis_box_color_btn.setStyleSheet("background: #F7B2AD; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
        self.vis_box_color = QColor(*cfg.ESP.visible_box_color)
        def pick_vis_box_color():
            dlg = PastelColorDialog(self, self.vis_box_color)
            if dlg.exec():
                self.vis_box_color = dlg.getColor()
                self.vis_box_color_btn.setStyleSheet(f"background: {self.vis_box_color.name()}; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
                cfg.ESP.visible_box_color = [self.vis_box_color.red(), self.vis_box_color.green(), self.vis_box_color.blue(), self.vis_box_color.alpha()]
                ConfigManager.save_config()
        self.vis_box_color_btn.clicked.connect(pick_vis_box_color)
        colors_layout.addWidget(self.vis_box_color_btn)
        self.vis_skel_color_btn = QPushButton("Visible Skeleton Color")
        self.vis_skel_color_btn.setStyleSheet("background: #B5EAD7; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
        self.vis_skel_color = QColor(*cfg.ESP.visible_skeleton_color)
        def pick_vis_skel_color():
            dlg = PastelColorDialog(self, self.vis_skel_color)
            if dlg.exec():
                self.vis_skel_color = dlg.getColor()
                self.vis_skel_color_btn.setStyleSheet(f"background: {self.vis_skel_color.name()}; color: #22223B; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
                cfg.ESP.visible_skeleton_color = [self.vis_skel_color.red(), self.vis_skel_color.green(), self.vis_skel_color.blue(), self.vis_skel_color.alpha()]
                ConfigManager.save_config()
        self.vis_skel_color_btn.clicked.connect(pick_vis_skel_color)
        colors_layout.addWidget(self.vis_skel_color_btn)
        self.colors_widget.setLayout(colors_layout)
        self.colors_widget.setVisible(False)
        def toggle_colors():
            expanded = self.colors_toggle.isChecked()
            self.colors_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.colors_widget.setVisible(expanded)
        self.colors_toggle.clicked.connect(toggle_colors)
        self.addons_toggle = QToolButton()
        self.addons_toggle.setText("Addons")
        self.addons_toggle.setCheckable(True)
        self.addons_toggle.setChecked(False)
        self.addons_toggle.setArrowType(Qt.RightArrow)
        self.addons_toggle.setStyleSheet("color: #B39DDB; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.addons_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addons_widget = QWidget()
        addons_layout = QVBoxLayout()
        addons_layout.setContentsMargins(24, 0, 0, 0)
        self.addon_distance_slider = PastelSlider(5, 50, cfg.ESP.esp_distance, "ESP Distance", float_mode=False, step=1, suffix=" m")
        self.addon_distance_slider.slider.valueChanged.connect(lambda v: (setattr(cfg.ESP, "esp_distance", v), ConfigManager.save_config()))
        addons_layout.addWidget(self.addon_distance_slider)
        self.addon_skel_slider = PastelSlider(1.0, 5.0, cfg.ESP.skeleton_width, "Skeleton Width", float_mode=True, step=0.1, suffix="")
        self.addon_skel_slider.slider.valueChanged.connect(lambda v: (setattr(cfg.ESP, "skeleton_width", self.addon_skel_slider.value()), ConfigManager.save_config()))
        addons_layout.addWidget(self.addon_skel_slider)
        self.addon_shadow = AnimatedCheckBox("Shadow")
        self.addon_shadow.setChecked(cfg.ESP.skeleton_shadow)
        self.addon_shadow.stateChanged.connect(lambda state: (setattr(cfg.ESP, "skeleton_shadow", bool(state)), ConfigManager.save_config()))
        addons_layout.addWidget(self.addon_shadow)
        self.addons_widget.setLayout(addons_layout)
        self.addons_widget.setVisible(False)
        def toggle_addons():
            expanded = self.addons_toggle.isChecked()
            self.addons_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.addons_widget.setVisible(expanded)
        self.addons_toggle.clicked.connect(toggle_addons)
        card_layout.addWidget(self.main_toggle)
        card_layout.addWidget(self.main_widget)
        card_layout.addWidget(self.info_toggle)
        card_layout.addWidget(self.info_widget)
        card_layout.addWidget(self.styles_toggle)
        card_layout.addWidget(self.styles_widget)
        card_layout.addWidget(self.colors_toggle)
        card_layout.addWidget(self.colors_widget)
        card_layout.addWidget(self.addons_toggle)
        card_layout.addWidget(self.addons_widget)
        card.setLayout(card_layout)
        layout.addWidget(card)
        layout.addStretch(1)
        self.setLayout(layout)
class AssistTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(18)
        accent = QLabel()
        accent.setFixedHeight(6)
        accent.setStyleSheet("background: #A3E635; border-radius: 3px;")
        layout.addWidget(accent)
        header = QLabel("Assist Features")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: white;")
        header.setAlignment(Qt.AlignHCenter)
        layout.addWidget(header)
        subtitle = QLabel("Configure your assist tools")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #C9ADA7;")
        subtitle.setAlignment(Qt.AlignHCenter)
        layout.addWidget(subtitle)
        card = QGroupBox()
        card.setStyleSheet(
            "QGroupBox { background: #4A4E69; border: 2px solid #C9ADA7; border-radius: 16px; margin-top: 18px; }"
        )
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)
        self.trig_toggle = QToolButton()
        self.trig_toggle.setText("Triggerbot")
        self.trig_toggle.setCheckable(True)
        self.trig_toggle.setChecked(True)
        self.trig_toggle.setArrowType(Qt.DownArrow)
        self.trig_toggle.setStyleSheet("color: white; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.trig_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.trig_widget = QWidget()
        trig_layout = QVBoxLayout()
        trig_layout.setContentsMargins(24, 0, 0, 0)
        key_row = QHBoxLayout()
        key_label = QLabel("Set key:")
        key_label.setStyleSheet("color: #C9ADA7; font-size: 15px; font-weight: 600;")
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("e.g. Mouse5")
        self.key_input.setStyleSheet("background: #726D99; color: white; border-radius: 8px; padding: 4px 12px; font-size: 15px; min-width: 80px;")
        self.key_input.setText(str(cfg.TRIGGERBOT.trigger_key))
        self.key_input.textChanged.connect(lambda val: (setattr(cfg.TRIGGERBOT, "trigger_key", val), ConfigManager.save_config()))
        key_row.addWidget(key_label)
        key_row.addWidget(self.key_input)
        trig_layout.addLayout(key_row)
        self.shoot_team_cb = AnimatedCheckBox("Shoot teammates")
        self.shoot_team_cb.setChecked(cfg.TRIGGERBOT.shoot_teammates)
        self.shoot_team_cb.stateChanged.connect(lambda state: (setattr(cfg.TRIGGERBOT, "shoot_teammates", bool(state)), ConfigManager.save_config()))
        trig_layout.addWidget(self.shoot_team_cb)
        self.enable_cb = AnimatedCheckBox("Enable")
        self.enable_cb.setChecked(cfg.TRIGGERBOT.enabled)
        self.enable_cb.stateChanged.connect(lambda state: (setattr(cfg.TRIGGERBOT, "enabled", bool(state)), ConfigManager.save_config()))
        trig_layout.addWidget(self.enable_cb)
        self.sticky_cb = AnimatedCheckBox("Sticky mode")
        self.sticky_cb.setChecked(cfg.TRIGGERBOT.sticky_mode)
        self.sticky_cb.stateChanged.connect(lambda state: (setattr(cfg.TRIGGERBOT, "sticky_mode", bool(state)), ConfigManager.save_config()))
        trig_layout.addWidget(self.sticky_cb)
        self.trig_widget.setLayout(trig_layout)
        self.trig_widget.setVisible(True)
        def toggle_trig():
            expanded = self.trig_toggle.isChecked()
            self.trig_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.trig_widget.setVisible(expanded)
        self.trig_toggle.clicked.connect(toggle_trig)
        self.delays_toggle = QToolButton()
        self.delays_toggle.setText("Delays")
        self.delays_toggle.setCheckable(True)
        self.delays_toggle.setChecked(False)
        self.delays_toggle.setArrowType(Qt.RightArrow)
        self.delays_toggle.setStyleSheet("color: #F76C6C; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.delays_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.delays_widget = QWidget()
        delays_layout = QVBoxLayout()
        delays_layout.setContentsMargins(24, 0, 0, 0)
        self.min_delay_slider = PastelSlider(0, 400, cfg.TRIGGERBOT.delay_min, "Min delay", float_mode=False, step=1, suffix=" ms")
        self.min_delay_slider.slider.valueChanged.connect(lambda v: (setattr(cfg.TRIGGERBOT, "delay_min", v), ConfigManager.save_config()))
        delays_layout.addWidget(self.min_delay_slider)
        self.max_delay_slider = PastelSlider(0, 400, cfg.TRIGGERBOT.delay_max, "Max delay", float_mode=False, step=1, suffix=" ms")
        self.max_delay_slider.slider.valueChanged.connect(lambda v: (setattr(cfg.TRIGGERBOT, "delay_max", v), ConfigManager.save_config()))
        delays_layout.addWidget(self.max_delay_slider)
        self.delays_widget.setLayout(delays_layout)
        self.delays_widget.setVisible(False)
        def toggle_delays():
            expanded = self.delays_toggle.isChecked()
            self.delays_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.delays_widget.setVisible(expanded)
        self.delays_toggle.clicked.connect(toggle_delays)
        card_layout.addWidget(self.trig_toggle)
        card_layout.addWidget(self.trig_widget)
        card_layout.addWidget(self.delays_toggle)
        card_layout.addWidget(self.delays_widget)
        card.setLayout(card_layout)
        layout.addWidget(card)
        layout.addStretch(1)
        self.setLayout(layout)

class GlowTabBar(QTabBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setExpanding(False)
        self.setUsesScrollButtons(False)
        self.setStyleSheet(
            "QTabBar::tab { height: 38px; min-width: 120px; padding: 0 28px; font-weight: 600; color: white; background: #726D99; border-radius: 14px; margin: 6px; font-size: 16px; letter-spacing: 1px; } "
            "QTabBar::tab:selected { background: #C9ADA7; color: #22223B; font-size: 18px; font-weight: bold; } "
            "QTabBar::tab:hover { background: #9A8C98; color: #fff; } "
            "QTabBar::tab:!selected { margin-top: 8px; } "
        )

    def update_tab_effects(self, idx):
        pass

    def paintEvent(self, event):
        super().paintEvent(event)

class AimbotTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(18)
        accent = QLabel()
        accent.setFixedHeight(6)
        accent.setStyleSheet("background: #A3E635; border-radius: 3px;")
        layout.addWidget(accent)
        header = QLabel("Aimbot Features")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: white;")
        header.setAlignment(Qt.AlignHCenter)
        layout.addWidget(header)
        subtitle = QLabel("Configure your aimbot")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #C9ADA7;")
        subtitle.setAlignment(Qt.AlignHCenter)
        layout.addWidget(subtitle)
        card = QGroupBox()
        card.setStyleSheet(
            "QGroupBox { background: #4A4E69; border: 2px solid #C9ADA7; border-radius: 16px; margin-top: 18px; }"
        )
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)
        self.aimbot_toggle = QToolButton()
        self.aimbot_toggle.setText("Aimbot")
        self.aimbot_toggle.setCheckable(True)
        self.aimbot_toggle.setChecked(True)
        self.aimbot_toggle.setArrowType(Qt.DownArrow)
        self.aimbot_toggle.setStyleSheet("color: white; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.aimbot_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.aimbot_widget = QWidget()
        aimbot_layout = QVBoxLayout()
        aimbot_layout.setContentsMargins(24, 0, 0, 0)
        self.aimbot_enable_cb = AnimatedCheckBox("Enable")
        self.aimbot_enable_cb.setChecked(cfg.AIMBOT.enabled)
        self.aimbot_enable_cb.stateChanged.connect(lambda state: (setattr(cfg.AIMBOT, "enabled", bool(state)), ConfigManager.save_config()))
        aimbot_layout.addWidget(self.aimbot_enable_cb)
        aimkey_row = QHBoxLayout()
        aimkey_label = QLabel("Aim Key:")
        aimkey_label.setStyleSheet("color: #C9ADA7; font-size: 15px; font-weight: 600;")
        self.aimkey_input = QLineEdit()
        self.aimkey_input.setPlaceholderText("e.g. Mouse4")
        self.aimkey_input.setStyleSheet("background: #726D99; color: white; border-radius: 8px; padding: 4px 12px; font-size: 15px; min-width: 80px;")
        self.aimkey_input.setText(str(cfg.AIMBOT.aim_key))
        self.aimkey_input.textChanged.connect(lambda val: (setattr(cfg.AIMBOT, "aim_key", val), ConfigManager.save_config()))
        aimkey_row.addWidget(aimkey_label)
        aimkey_row.addWidget(self.aimkey_input)
        aimbot_layout.addLayout(aimkey_row)
        bones_label = QLabel("Target bones:")
        bones_label.setStyleSheet("color: #C9ADA7; font-size: 15px; font-weight: 600; margin-bottom: 2px;")
        aimbot_layout.addWidget(bones_label)
        self.bone_buttons = []
        bones_row = QHBoxLayout()
        bone_names = ["head", "neck", "chest", "body"]
        for bone in bone_names:
            btn = QPushButton(bone.capitalize())
            btn.setCheckable(True)
            btn.setStyleSheet("QPushButton { background: #F6E7CB; color: #726D99; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 6px 18px; margin-right: 8px; } QPushButton:checked { background: #A3E635; color: #22223B; }")
            btn.setChecked(bone in cfg.AIMBOT.target_bones)
            def make_bone_handler(bone, btn):
                def handler(checked):
                    bones = set(cfg.AIMBOT.target_bones)
                    if checked:
                        bones.add(bone)
                    else:
                        bones.discard(bone)
                    cfg.AIMBOT.target_bones = list(bones)
                    ConfigManager.save_config()
                return handler
            btn.toggled.connect(make_bone_handler(bone, btn))
            bones_row.addWidget(btn)
            self.bone_buttons.append(btn)
        bones_row.addStretch(1)
        aimbot_layout.addLayout(bones_row)
        self.aimbot_widget.setLayout(aimbot_layout)
        self.aimbot_widget.setVisible(True)
        def toggle_aimbot():
            expanded = self.aimbot_toggle.isChecked()
            self.aimbot_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.aimbot_widget.setVisible(expanded)
        self.aimbot_toggle.clicked.connect(toggle_aimbot)
        self.fov_slider = PastelSlider(5, 150, cfg.AIMBOT.aim_fov, "Aim FOV", float_mode=False, step=1, suffix=" px")
        self.fov_slider.slider.valueChanged.connect(lambda v: (setattr(cfg.AIMBOT, "aim_fov", v), ConfigManager.save_config()))
        self.smooth_slider = PastelSlider(1, 100, cfg.AIMBOT.smoothness, "Smoothness", float_mode=True, step=1, suffix=" %")
        self.smooth_slider.slider.valueChanged.connect(lambda v: (setattr(cfg.AIMBOT, "smoothness", self.smooth_slider.value()), ConfigManager.save_config()))
        self.maxdist_slider = PastelSlider(1, 100, cfg.AIMBOT.max_distance, "Max Distance", float_mode=False, step=1, suffix=" m")
        self.maxdist_slider.slider.valueChanged.connect(lambda v: (setattr(cfg.AIMBOT, "max_distance", v), ConfigManager.save_config()))
        self.settings_toggle = QToolButton()
        self.settings_toggle.setText("Settings")
        self.settings_toggle.setCheckable(True)
        self.settings_toggle.setChecked(False)
        self.settings_toggle.setArrowType(Qt.RightArrow)
        self.settings_toggle.setStyleSheet("color: #A3E635; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.settings_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.settings_widget = QWidget()
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(24, 0, 0, 0)
        settings_layout.addWidget(self.fov_slider)
        settings_layout.addWidget(self.smooth_slider)
        settings_layout.addWidget(self.maxdist_slider)
        self.settings_widget.setLayout(settings_layout)
        self.settings_widget.setVisible(False)
        def toggle_settings():
            expanded = self.settings_toggle.isChecked()
            self.settings_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.settings_widget.setVisible(expanded)
        self.settings_toggle.clicked.connect(toggle_settings)
        self.addons_toggle = QToolButton()
        self.addons_toggle.setText("Addons")
        self.addons_toggle.setCheckable(True)
        self.addons_toggle.setChecked(False)
        self.addons_toggle.setArrowType(Qt.RightArrow)
        self.addons_toggle.setStyleSheet("color: #F76C6C; font-weight: bold; background: transparent; border: none; font-size: 16px;")
        self.addons_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addons_widget = QWidget()
        addons_layout = QVBoxLayout()
        addons_layout.setContentsMargins(24, 0, 0, 0)
        self.curve_options = ["Linear", "SLinear", "RLinear", "Beziercurve"]
        self.curve_idx = self.curve_options.index(cfg.AIMBOT.curve) if cfg.AIMBOT.curve in self.curve_options else 0
        self.curve_btn = QPushButton(f"Curve: {self.curve_options[self.curve_idx]}")
        self.curve_btn.setStyleSheet("background: #F6E7CB; color: #726D99; border-radius: 10px; font-weight: 600; font-size: 15px; padding: 8px 18px;")
        def cycle_curve():
            self.curve_idx = (self.curve_idx + 1) % len(self.curve_options)
            self.curve_btn.setText(f"Curve: {self.curve_options[self.curve_idx]}")
            cfg.AIMBOT.curve = self.curve_options[self.curve_idx]
            ConfigManager.save_config()
        self.curve_btn.clicked.connect(cycle_curve)
        self.visible_only_cb = AnimatedCheckBox("Visible only")
        self.visible_only_cb.setChecked(cfg.AIMBOT.visible_check)
        self.visible_only_cb.stateChanged.connect(lambda state: (setattr(cfg.AIMBOT, "visible_check", bool(state)), ConfigManager.save_config()))
        addons_layout.addWidget(self.curve_btn)
        addons_layout.addWidget(self.visible_only_cb)
        self.addons_widget.setLayout(addons_layout)
        self.addons_widget.setVisible(False)
        def toggle_addons():
            expanded = self.addons_toggle.isChecked()
            self.addons_toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.addons_widget.setVisible(expanded)
        self.addons_toggle.clicked.connect(toggle_addons)
        card_layout.addWidget(self.aimbot_toggle)
        card_layout.addWidget(self.aimbot_widget)
        card_layout.addWidget(self.settings_toggle)
        card_layout.addWidget(self.settings_widget)
        card_layout.addWidget(self.addons_toggle)
        card_layout.addWidget(self.addons_widget)
        card.setLayout(card_layout)
        layout.addWidget(card)
        layout.addStretch(1)
        self.setLayout(layout)

class MiscTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(18)
        accent = QLabel()
        accent.setFixedHeight(6)
        accent.setStyleSheet("background: #A3E635; border-radius: 3px;")
        layout.addWidget(accent)
        header = QLabel("Miscellaneous")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: white;")
        header.setAlignment(Qt.AlignHCenter)
        layout.addWidget(header)
        subtitle = QLabel("Other features")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #C9ADA7;")
        subtitle.setAlignment(Qt.AlignHCenter)
        layout.addWidget(subtitle)
        card = QGroupBox()
        card.setStyleSheet(
            "QGroupBox { background: #4A4E69; border: 2px solid #C9ADA7; border-radius: 16px; margin-top: 18px; }"
        )
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)
        self.fps_slider = PastelSlider(30, 360, cfg.MISC.overlay_fps, "FPS", float_mode=False, step=1, suffix="")
        self.fps_slider.slider.valueChanged.connect(lambda v: (setattr(cfg.MISC, "overlay_fps", v), ConfigManager.save_config()))
        card_layout.addWidget(self.fps_slider)
        self.bomb_timer_cb = AnimatedCheckBox("Bomb timer")
        self.bomb_timer_cb.setChecked(cfg.MISC.bomb_timer)
        self.bomb_timer_cb.stateChanged.connect(lambda state: (setattr(cfg.MISC, "bomb_timer", bool(state)), ConfigManager.save_config()))
        card_layout.addWidget(self.bomb_timer_cb)
        self.streamproof_cb = AnimatedCheckBox("Streamproof")
        self.streamproof_cb.setChecked(cfg.MISC.streamproof)
        self.streamproof_cb.stateChanged.connect(lambda state: (setattr(cfg.MISC, "streamproof", bool(state)), ConfigManager.save_config()))
        card_layout.addWidget(self.streamproof_cb)
        card.setLayout(card_layout)
        layout.addWidget(card)
        layout.addStretch(1)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS2 External Cheat")
        self.resize(600, 400)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        pal = self.palette()
        pal.setColor(QPalette.Window, PASTEL_BG)
        self.setPalette(pal)
        tabs = QTabWidget()
        tabs.setFont(QFont("Segoe UI", 11))
        tabs.setTabBar(GlowTabBar())
        self.esp_tab = ESPTab()
        tabs.addTab(self.esp_tab, QIcon("icons/esp.png"), "ESP")
        self.assist_tab = AssistTab()
        tabs.addTab(self.assist_tab, QIcon("icons/assist.png"), "Assist")
        self.aimbot_tab = AimbotTab()
        tabs.addTab(self.aimbot_tab, QIcon("icons/aimbot.png"), "Aimbot")
        self.misc_tab = MiscTab()
        tabs.addTab(self.misc_tab, QIcon("icons/misc.png"), "Misc")
        self.setCentralWidget(tabs)

class PastelSegmentedControl(QWidget):
    def __init__(self, labels, default=0):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.buttons = []
        self.group = QButtonGroup(self)
        pastel_bg = "#F6E7CB"
        pastel_sel = "#A3E635"
        pastel_txt = "#22223B"
        pastel_un = "#726D99"
        pastel_border = "#E0D6F6"
        for i, label in enumerate(labels):
            btn = QPushButton(label)
            btn.setCheckable(True)
            if i == 0:
                radius = "20px 0 0 20px"
            elif i == len(labels)-1:
                radius = "0 20px 20px 0"
            else:
                radius = "0"
            border_left = "1.5px solid {}".format(pastel_border) if i == 0 else "0"
            border_right = "1.5px solid {}".format(pastel_border) if i == len(labels)-1 else "0"
            btn.setStyleSheet(f"QPushButton {{ background: {pastel_bg}; color: {pastel_un}; border-top: 1.5px solid {pastel_border}; border-bottom: 1.5px solid {pastel_border}; border-left: {border_left}; border-right: {border_right}; border-radius: {radius}; padding: 10px 28px; font-weight: 600; font-size: 16px; min-width: 80px; min-height: 38px; }} "
                f"QPushButton:checked {{ background: {pastel_sel}; color: {pastel_txt}; border-top: 2.5px solid {pastel_sel}; border-bottom: 2.5px solid {pastel_sel}; border-left: {border_left}; border-right: {border_right}; }} "
                f"QPushButton:hover {{ background: #FFF5E1; color: {pastel_txt}; }}")
            self.layout.addWidget(btn)
            self.group.addButton(btn, i)
            self.buttons.append(btn)
        self.setLayout(self.layout)
        self.setStyleSheet(f"background: {pastel_bg}; border-radius: 20px; border: 1.5px solid {pastel_border}; padding: 4px 2px 4px 2px; margin-bottom: 10px;")
        self.group.button(default).setChecked(True)
    def selected(self):
        return self.group.checkedId()
    def set_selected(self, idx):
        self.group.button(idx).setChecked(True)

class PastelColorDialog(QDialog):
    def __init__(self, parent=None, initial=QColor("#A3E635")):
        super().__init__(parent)
        self.setWindowTitle("Pick Color")
        self.setFixedSize(340, 220)
        self.setStyleSheet("background: #22223B; border-radius: 16px;")
        layout = QVBoxLayout()
        palette = [
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#FFFF00",
            "#FFA500",
            "#800080",
            "#FFFFFF",
            "#000000",
            "#808080",
            "#00FFFF",
            "#FFC0CB",
            "#A52A2A",
        ]
        grid = QGridLayout()
        self.selected_color = initial
        self.color_buttons = []
        for i, color in enumerate(palette):
            btn = QPushButton()
            btn.setFixedSize(38,38)
            btn.setStyleSheet(f"background: {color}; border-radius: 19px; border: 3px solid #fff;")
            btn.clicked.connect(lambda _, c=color: self.pick(c))
            grid.addWidget(btn, i//6, i%6)
            self.color_buttons.append(btn)
        layout.addLayout(grid)
        self.hex_input = QLineEdit(initial.name())
        self.hex_input.setStyleSheet("background: #726D99; color: white; border-radius: 8px; padding: 4px 12px; font-size: 15px;")
        layout.addWidget(self.hex_input)
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet("background: #A3E635; color: #22223B; border-radius: 8px; font-weight: 600; padding: 6px 18px; font-size: 15px;")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)
        self.setLayout(layout)
    def pick(self, color):
        self.selected_color = QColor(color)
        self.hex_input.setText(color)
    def getColor(self):
        if QColor(self.hex_input.text()).isValid():
            return QColor(self.hex_input.text())
        return self.selected_color

class PastelSlider(QWidget):
    def __init__(self, minval, maxval, value, label, float_mode=False, step=1, suffix=""):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(10)
        self.label = QLabel(label)
        self.label.setStyleSheet("color: #C9ADA7; font-size: 15px; font-weight: 600; padding-right: 8px;")
        self.slider = QSlider(Qt.Horizontal)
        self.float_mode = float_mode
        self.suffix = suffix
        if float_mode:
            self.slider.setMinimum(0)
            self.slider.setMaximum(int((maxval-minval)/step))
            self._min = minval
            self._max = maxval
            self._step = step
            self.slider.setValue(int((value-minval)/step))
        else:
            self.slider.setMinimum(minval)
            self.slider.setMaximum(maxval)
            self.slider.setValue(value)
        self.slider.setStyleSheet("QSlider::groove:horizontal { background: #726D99; height: 12px; border-radius: 6px; } QSlider::handle:horizontal { background: #A3E635; width: 28px; border-radius: 14px; border: 2px solid #C9ADA7; } QSlider::sub-page:horizontal { background: #A3E635; border-radius: 6px; } QSlider::add-page:horizontal { background: #4A4E69; border-radius: 6px; } QSlider:focus { outline: none; border: none; } QSlider::handle:focus { outline: none; border: 2px solid #C9ADA7; }")
        self.value_label = QLabel()
        self.value_label.setStyleSheet("color: #A3E635; font-size: 15px; font-weight: bold; min-width: 48px;")
        def update_label(v):
            if self.float_mode:
                val = self._min + v * self._step
                self.value_label.setText(f"{val:.1f}{self.suffix}")
            else:
                self.value_label.setText(f"{v}{self.suffix}")
        self.slider.valueChanged.connect(update_label)
        update_label(self.slider.value())
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.value_label)
        self.setLayout(layout)
    def value(self):
        if self.float_mode:
            return self._min + self.slider.value() * self._step
        return self.slider.value()
    def setValue(self, v):
        if self.float_mode:
            self.slider.setValue(int((v-self._min)/self._step))
        else:
            self.slider.setValue(v)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
