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
    show_skeleton = False
    show_name = False
    show_head_circle = False
    show_teammates = True  
    max_distance = 25
    line_position = "Center"  
    box_style = "Regular"
    box_color = [1.0, 1.0, 1.0, 1.0]  
    box_fill_color = [1.0, 1.0, 1.0, 0.3]  
    line_color = [1.0, 1.0, 1.0, 1.0]  
    skeleton_color = [1.0, 0.0, 1.0, 1.0]  
    skeleton_shadow = True
    skeleton_thickness = 1.5

class TRIGGERBOT:
    enabled = False
    delay_min = 0.2  
    delay_max = 0.4  
    trigger_key = "shift"
    shoot_teammates = False
    check_interval = 0.01 

class MISC:
    always_on_top = True
    overlay_fps = 45

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
                    "show_health": ESP.show_health,                    "show_health_text": ESP.show_health_text,
                    "show_distance": ESP.show_distance,
                    "show_weapon": ESP.show_weapon,
                    "show_weapon_icon": ESP.show_weapon_icon,
                    "show_skeleton": ESP.show_skeleton,
                    "show_name": ESP.show_name,                    "show_head_circle": ESP.show_head_circle,
                    "show_teammates": ESP.show_teammates,
                    "max_distance": ESP.max_distance,
                    "line_position": ESP.line_position,
                    "box_style": ESP.box_style,
                    "box_color": ESP.box_color,
                    "box_fill_color": ESP.box_fill_color,
                    "line_color": ESP.line_color,
                    "skeleton_color": ESP.skeleton_color,
                    "skeleton_shadow": ESP.skeleton_shadow,
                    "skeleton_thickness": ESP.skeleton_thickness,
                    "weapon_icon_size": ESP.weapon_icon_size},
                "TRIGGERBOT": {
                    "enabled": TRIGGERBOT.enabled,
                    "delay_min": TRIGGERBOT.delay_min,
                    "delay_max": TRIGGERBOT.delay_max,
                    "trigger_key": TRIGGERBOT.trigger_key,
                    "shoot_teammates": TRIGGERBOT.shoot_teammates,
                    "check_interval": TRIGGERBOT.check_interval
                },
                "MISC": {                    "always_on_top": MISC.always_on_top,
                    "overlay_fps": MISC.overlay_fps
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