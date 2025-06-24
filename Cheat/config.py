import json
import os

class ESPConfig:
    def __init__(self):
        self.show_box = True
        self.show_line = True
        self.show_health = True
        self.show_teammates = True
        self.show_distance = True
        self.show_weapon = True
        self.show_name = True
        self.show_health_text = True
        self.show_skeleton = True
        self.show_head_circle = True
        self.skeleton_shadow = False
        self.box_color = [163, 230, 53, 255]
        self.line_color = [201, 173, 167, 255]
        self.skeleton_color = [154, 140, 152, 255]
        self.visible_box_color = [247, 178, 173, 255]
        self.visible_skeleton_color = [181, 234, 215, 255]
        self.esp_distance = 20
        self.skeleton_width = 2.0
        self.max_distance = 100
        self.box_style = "Regular"
        self.line_position = "Bottom"
        self.visible_only = False

    @property
    def skeleton_thickness(self):
        return self.skeleton_width

    @skeleton_thickness.setter
    def skeleton_thickness(self, value):
        self.skeleton_width = value

class AimbotConfig:
    def __init__(self):
        self.enabled = False
        self.aim_key = "Mouse4"
        self.target_bones = ["head"]
        self.aim_fov = 30
        self.smoothness = 50
        self.max_distance = 50
        self.curve = "Linear"
        self.visible_check = True
        self.show_fov_circle = True

class TriggerbotConfig:
    def __init__(self):
        self.enabled = False
        self.trigger_key = "Mouse5"
        self.shoot_teammates = False
        self.sticky_mode = False
        self.delay_min = 0
        self.delay_max = 0

class MiscConfig:
    def __init__(self):
        self.overlay_fps = 144
        self.bomb_timer = False
        self.streamproof = False

class ConfigManager:
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
    @classmethod
    def load_config(cls):
        if os.path.exists(cls.CONFIG_PATH):
            with open(cls.CONFIG_PATH, "r") as f:
                data = json.load(f)
            for section, obj in [("ESP", cfg.ESP), ("AIMBOT", cfg. AIMBOT), ("TRIGGERBOT", cfg.TRIGGERBOT), ("MISC", cfg.MISC)]:
                if section in data:
                    for k, v in data[section].items():
                        setattr(obj, k, v)
    @classmethod
    def save_config(cls):
        data = {
            "ESP": vars(cfg.ESP),
            "AIMBOT": vars(cfg.AIMBOT),
            "TRIGGERBOT": vars(cfg.TRIGGERBOT),
            "MISC": vars(cfg.MISC),
        }
        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=2)

class Config:
    def __init__(self):
        self.ESP = ESPConfig()
        self.AIMBOT = AimbotConfig()
        self.TRIGGERBOT = TriggerbotConfig()
        self.MISC = MiscConfig()
        self.ConfigManager = ConfigManager

cfg = Config()
ConfigManager.load_config()
