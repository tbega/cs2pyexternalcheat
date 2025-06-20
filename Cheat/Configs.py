import json
import os

class ESP:
    show_box = True
    show_filled_box = True
    show_cornered_box = False
    show_line = True
    show_health = True
    show_health_text = False
    show_distance = False
    show_weapon = False
    show_weapon_icon = False
    show_skeleton = False
    show_name = False
    show_head_circle = False
    show_teammates = True  
    visible_only = False  # Only show ESP for visible enemies
    visible_color_change = True  # Change colors based on visibility
    max_distance = 25
    line_position = "Center"  
    box_style = "Regular"
    box_color = [1.0, 1.0, 1.0, 1.0]  
    box_fill_color = [1.0, 1.0, 1.0, 0.3]  
    line_color = [1.0, 1.0, 1.0, 1.0]  
    skeleton_color = [1.0, 0.0, 1.0, 1.0]
    # Visible/Spotted colors
    visible_box_color = [0.0, 1.0, 0.0, 1.0]  # Green for visible
    visible_skeleton_color = [0.0, 1.0, 0.0, 1.0]  # Green for visible
    skeleton_shadow = True
    skeleton_thickness = 1.5
    weapon_icon_size = 32

class TRIGGERBOT:
    enabled = False
    delay_min = 0.2  
    delay_max = 0.4  
    trigger_key = "shift"
    shoot_teammates = False
    check_interval = 0.01 

class AIMBOT:
    enabled = True  # Enable aimbot by default for testing
    aim_key = "e"  # Key to activate aimbot (matches what's being used)
    aim_fov = 150.0  # Field of view for aimbot targeting (increased for better targeting)
    smoothness = 2.5  # How smooth the mouse movement should be (higher = smoother)
    target_bone = 6  # Bone to target (6 = head, 4 = chest, 2 = body)
    auto_shoot = False  # Automatically shoot when target is acquired
    show_fov_circle = True  # Show the FOV circle on screen
    target_teammates = False  # Whether to target teammates
    max_distance = 30.0  # Maximum distance to target enemies
    # Advanced settings
    dynamic_fov = False  # Adjust FOV based on distance
    min_fov = 30.0  # Minimum FOV for dynamic mode
    max_fov = 90.0  # Maximum FOV for dynamic mode
    
    # Flick settings
    flick_mode = False  # Instant snap to target
    flick_smoothness = 1.0  # Smoothness for flick mode
    
    # Target priority
    prefer_head = True  # Prefer headshots
    prefer_closest = False  # Target closest enemy instead of best FOV
    
    # Safety features
    visible_check = True  # Only target visible enemies

class MISC:
    always_on_top = True
    overlay_fps = 120
    show_bomb_timer = True
    show_spectator_list = True
    stream_proof = False  # Hide cheat elements when streaming

class ConfigManager:
    CONFIG_FILE = "config.json"
    
    @staticmethod
    def save_config():
        """Save current configuration to file"""
        try:
            config_data = {
                "ESP": {
                    "show_box": ESP.show_box,
                    "show_filled_box": ESP.show_filled_box,
                    "show_cornered_box": ESP.show_cornered_box,
                    "show_line": ESP.show_line,
                    "show_health": ESP.show_health,
                    "show_health_text": ESP.show_health_text,
                    "show_distance": ESP.show_distance,
                    "show_weapon": ESP.show_weapon,
                    "show_weapon_icon": ESP.show_weapon_icon,
                    "show_skeleton": ESP.show_skeleton,                    "show_name": ESP.show_name,
                    "show_head_circle": ESP.show_head_circle,
                    "show_teammates": ESP.show_teammates,
                    "visible_only": ESP.visible_only,
                    "visible_color_change": ESP.visible_color_change,
                    "max_distance": ESP.max_distance,
                    "line_position": ESP.line_position,
                    "box_style": ESP.box_style,
                    "box_color": ESP.box_color,
                    "box_fill_color": ESP.box_fill_color,
                    "line_color": ESP.line_color,
                    "skeleton_color": ESP.skeleton_color,
                    "visible_box_color": ESP.visible_box_color,
                    "visible_skeleton_color": ESP.visible_skeleton_color,
                    "skeleton_shadow": ESP.skeleton_shadow,
                    "skeleton_thickness": ESP.skeleton_thickness,

                },
                "TRIGGERBOT": {
                    "enabled": TRIGGERBOT.enabled,
                    "delay_min": TRIGGERBOT.delay_min,
                    "delay_max": TRIGGERBOT.delay_max,
                    "trigger_key": TRIGGERBOT.trigger_key,
                    "shoot_teammates": TRIGGERBOT.shoot_teammates,
                    "check_interval": TRIGGERBOT.check_interval
                },
                "AIMBOT": {
                    "enabled": AIMBOT.enabled,
                    "aim_key": AIMBOT.aim_key,
                    "aim_fov": AIMBOT.aim_fov,
                    "smoothness": AIMBOT.smoothness,
                    "target_bone": AIMBOT.target_bone,
                    "auto_shoot": AIMBOT.auto_shoot,
                    "show_fov_circle": AIMBOT.show_fov_circle,
                    "target_teammates": AIMBOT.target_teammates,
                    "max_distance": AIMBOT.max_distance,
                    "dynamic_fov": AIMBOT.dynamic_fov,
                    "min_fov": AIMBOT.min_fov,
                    "max_fov": AIMBOT.max_fov,
                    "flick_mode": AIMBOT.flick_mode,
                    "flick_smoothness": AIMBOT.flick_smoothness,
                    "prefer_head": AIMBOT.prefer_head,
                    "prefer_closest": AIMBOT.prefer_closest,
                    "visible_check": AIMBOT.visible_check,
                },                "MISC": {
                    "always_on_top": MISC.always_on_top,
                    "overlay_fps": MISC.overlay_fps,
                    "show_bomb_timer": MISC.show_bomb_timer,
                    "stream_proof": MISC.stream_proof
                }
            }
            
            with open(ConfigManager.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
            return True
            
        except Exception as e:
            print(f"[Config] Failed to save configuration: {e}")
            return False
    
    @staticmethod
    def load_config():
        try:
            if not os.path.exists(ConfigManager.CONFIG_FILE):
                print(f"[Config] No config file found, using defaults")
                return True
                
            with open(ConfigManager.CONFIG_FILE, 'r') as f:
                config_data = json.load(f)

            if "ESP" in config_data:
                esp_data = config_data["ESP"]
                for key, value in esp_data.items():
                    if hasattr(ESP, key):
                        setattr(ESP, key, value)

            if "TRIGGERBOT" in config_data:
                triggerbot_data = config_data["TRIGGERBOT"]
                for key, value in triggerbot_data.items():
                    if hasattr(TRIGGERBOT, key):
                        setattr(TRIGGERBOT, key, value)

            if "AIMBOT" in config_data:
                aimbot_data = config_data["AIMBOT"]
                for key, value in aimbot_data.items():
                    if hasattr(AIMBOT, key):
                        setattr(AIMBOT, key, value)

            if "MISC" in config_data:
                misc_data = config_data["MISC"]
                for key, value in misc_data.items():
                    if hasattr(MISC, key):
                        setattr(MISC, key, value)
            return True
        
            
        except Exception as e:
            print(f"[Config] Failed to load configuration: {e}")
            return False

ConfigManager.load_config()