import math
import ctypes
import random
import string
import os
import sys
import time
import psutil
import keyboard
import Cheat.utils as utils
from Cheat.triggerbot import TriggerBot
from Cheat.config import cfg
from random import uniform
from win32gui import GetWindowText, GetForegroundWindow
from pynput.mouse import Controller, Button
from Cheat.aimbot import Aimbot
from Cheat.mouse_utils import move_mouse_relative_sendinput, mouse_click_sendinput

try:
    import win32api
except ImportError:
    print("[Aimbot] Warning: win32api not available, mouse button detection may not work")
    win32api = None





user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
ntdll = ctypes.windll.ntdll
pm = utils.get_pyMeow()
rq = utils.get_requests()




class Offsets:
    pass


class Colors:
    green = pm.get_color("#00FF00")
    orange = pm.fade_color(pm.get_color("#FFA500"), 0.3)
    black = pm.get_color("black")
    cyan = pm.fade_color(pm.get_color("#00F6F6"), 0.3)
    white = pm.get_color("white")
    grey = pm.fade_color(pm.get_color("#242625"), 0.7)
    red = pm.get_color("#FF0000")  


def is_key_code_pressed(key_code):
    try:
        if win32api and key_code is not None and isinstance(key_code, int):
            if key_code == 0:
                print("[Keybind] Warning: key_code is 0 (not set)")
            if not hasattr(is_key_code_pressed, '_printed_codes'):
                is_key_code_pressed._printed_codes = set()
            if key_code not in is_key_code_pressed._printed_codes:
                print(f"[Keybind] Checking key_code: {key_code}")
                is_key_code_pressed._printed_codes.add(key_code)
            return win32api.GetAsyncKeyState(key_code) < 0
    except Exception as e:
        print(f"[Keybind] Exception in is_key_code_pressed: {e}")
    return False


class Entity:

    def __init__(self, ptr, pawn_ptr, proc, cheat_instance=None):
        self.ptr = ptr
        self.pawn_ptr = pawn_ptr
        self.proc = proc
        self.cheat = cheat_instance
        self._valid = ptr and pawn_ptr and ptr > 0x1000 and pawn_ptr > 0x1000

    @property
    def name(self):
        if not self._valid:
            return "Invalid"
        try:
            name = pm.r_string(self.proc, self.ptr + Offsets.m_iszPlayerName)
            return name if name else "Unknown"
        except:
            return "Error"

    @property
    def health(self):
        if not self._valid:
            return 0
        try:
            health = pm.r_int(self.proc, self.pawn_ptr + Offsets.m_iHealth)
            if isinstance(health, int) and 0 <= health <= 200:
                return health
            return 0
        except:
            return 0

    @property
    def team(self):
        if not self._valid:
            return 0
        try:
            team = pm.r_int(self.proc, self.pawn_ptr + Offsets.m_iTeamNum)
            if isinstance(team, int) and team in [0, 1, 2, 3]:
                return team
            return 0
        except:
            return 0

    @property
    def pos(self):
        if not self._valid:
            return {"x": 0, "y": 0, "z": 0}
        try:
            pos = pm.r_vec3(self.proc, self.pawn_ptr + Offsets.m_vOldOrigin)
            if pos and all(isinstance(pos.get(k), (int, float)) for k in ['x', 'y', 'z']):
                return pos
            return {"x": 0, "y": 0, "z": 0}
        except:
            return {"x": 0, "y": 0, "z": 0}
    
    @property
    def dormant(self):
        if not self._valid:
            return True
        try:
            dormant = pm.r_bool(self.proc, self.pawn_ptr + Offsets.m_bDormant)
            return bool(dormant)
        except:
            return True

    @property
    def spotted(self):
        if not self._valid:
            return False
        try:
            spotted_mask = pm.r_int(self.proc, self.pawn_ptr + Offsets.m_entitySpottedState + Offsets.m_bSpottedByMask)
            
            if (self.cheat and hasattr(self.cheat, '_cached_local_index') and 
                self.cheat._cached_local_index is not None):
                local_player_bit = 1 << self.cheat._cached_local_index
                return bool(spotted_mask & local_player_bit)
            
            for slot in [0, 1, 2, 3]:
                test_bit = 1 << slot
                if spotted_mask & test_bit:
                    if slot == 0:
                        return True
            
            return bool(spotted_mask & 1)
                
        except:
            return False

    @property
    def weaponIndex(self):
        if not self._valid:
            return 0
        try:
            currentWeapon = pm.r_int64(self.proc, self.pawn_ptr + Offsets.m_pClippingWeapon)
            if not currentWeapon or currentWeapon < 0x1000:
                return 0
            weaponIndex = pm.r_int(self.proc, currentWeapon + Offsets.m_AttributeManager + Offsets.m_Item + Offsets.m_iItemDefinitionIndex)
            if isinstance(weaponIndex, int) and 0 <= weaponIndex <= 100:
                return weaponIndex
            return 0
        except:
            return 0
    
    def get_weapon_name(self):
        try:
            weapon_index = self.weaponIndex
            return weapon_names.get(weapon_index, "Unknown")
        except:
            return "Unknown"
        
    def get_distance(self, localPos):
        if not self._valid or not localPos:
            return float('inf')
        try:
            current_pos = self.pos  
            if not current_pos:
                return float('inf')
                
            dx = current_pos["x"] - localPos["x"]
            dy = current_pos["y"] - localPos["y"]
            dz = current_pos["z"] - localPos["z"]
            distance = int(math.sqrt(dx * dx + dy * dy + dz * dz) / 100)
            
            if 0 <= distance <= 1000:
                return distance
            return float('inf')
        except:
            return float('inf')

    def bone_pos(self, bone):
        if not self._valid:
            return {"x": 0, "y": 0, "z": 0}
        try:
            game_scene = pm.r_int64(self.proc, self.pawn_ptr + Offsets.m_pGameSceneNode)
            if not game_scene or game_scene < 0x1000:
                return {"x": 0, "y": 0, "z": 0}
                
            bone_array_ptr = pm.r_int64(self.proc, game_scene + Offsets.m_pBoneArray)
            if not bone_array_ptr or bone_array_ptr < 0x1000:
                return {"x": 0, "y": 0, "z": 0}
                
            bone_pos = pm.r_vec3(self.proc, bone_array_ptr + bone * 32)
            if bone_pos and all(isinstance(bone_pos.get(k), (int, float)) for k in ['x', 'y', 'z']):
                return bone_pos
            return {"x": 0, "y": 0, "z": 0}
        except:
            return {"x": 0, "y": 0, "z": 0}
    
    def wts(self, view_matrix):
        if not self._valid or not view_matrix:
            print(f"[WTS DEBUG] Invalid entity or view_matrix: valid={self._valid}, view_matrix={view_matrix}")
            return False
        try:
            head_pos = self.bone_pos(6)  
            feet_pos = self.pos.copy()  
            if not head_pos or not feet_pos:
                print(f"[WTS DEBUG] Invalid head_pos or feet_pos: head_pos={head_pos}, feet_pos={feet_pos}")
                return False
            feet_pos["z"] -= 10  


            pos2d = pm.world_to_screen(view_matrix, self.pos, 1)
            head_pos2d = pm.world_to_screen(view_matrix, head_pos, 1)
            feet_pos2d = pm.world_to_screen(view_matrix, feet_pos, 1)


            if not (pos2d and head_pos2d and feet_pos2d):
                print(f"[WTS DEBUG] Invalid 2D positions: pos2d={pos2d}, head_pos2d={head_pos2d}, feet_pos2d={feet_pos2d}")
                return False
            self.pos2d = pos2d
            self.head_pos2d = head_pos2d
            self.feet_pos2d = feet_pos2d
            return all(pos.get("x") and pos.get("y") for pos in [pos2d, head_pos2d, feet_pos2d])
        except Exception as e:
            print(f"[WTS DEBUG] Exception: {e}")
            return False

class Render:
    @staticmethod
    def get_color_from_config(color_value):
        color_map = {
            "Red": "#FF0000",
            "Green": "#00FF00",
            "Blue": "#0000FF",
            "Yellow": "#FFFF00",
            "Magenta": "#FF00FF",
            "Cyan": "#00FFFF",
            "White": "#FFFFFF",
            "Orange": "#FFA500",
            "Purple": "#800080",
            "Pink": "#FFC0CB"
        }
        if isinstance(color_value, str):
            hex_color = color_map.get(color_value, color_value)
            return pm.get_color(hex_color)
        if isinstance(color_value, (list, tuple)) and len(color_value) >= 3:
            r, g, b = color_value[:3]
            if all(0 <= c <= 1 for c in (r, g, b)):
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
            else:
                r, g, b = int(r), int(g), int(b)
            hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
            return pm.get_color(hex_color)
        return pm.get_color("#FFFFFF")

    @staticmethod
    def draw_smooth_line(x1, y1, x2, y2, color, thickness=1.0, anti_aliased=True):
        if anti_aliased and thickness > 2.0:
            pm.draw_line(x1 + 0.5, y1 + 0.5, x2 + 0.5, y2 + 0.5, pm.fade_color(color, 0.3), thickness * 0.8)
        pm.draw_line(x1, y1, x2, y2, color, thickness)

    @staticmethod
    def draw_smooth_rectangle_lines(x, y, width, height, color, thickness=1.0):
        """Draw smooth rectangle outline with minimal performance impact"""
        
        pm.draw_rectangle_lines(x, y, width, height, color, thickness)

    @staticmethod
    def draw_esp_line(local_x, local_y, target_x, target_y, color, thickness=2.0):
        line_position = getattr(cfg.ESP, "line_position", "Bottom")
        if line_position == "Top":
            local_y = int(local_y * 0.25)
        elif line_position == "Center":
            pass
        elif line_position == "Bottom":
            local_y = int(local_y * 0.75)
        pm.draw_line(local_x, local_y, target_x, target_y, color, thickness)

    @staticmethod
    def calculate_accurate_box(entity, distance):
        if not (entity.head_pos2d and entity.feet_pos2d):
            return None, None, None, None
            
        
        raw_height = abs(entity.feet_pos2d["y"] - entity.head_pos2d["y"])
        box_height = raw_height * 0.95  
        
       
        if distance > 30:
            
            box_width = box_height * 0.35
        elif distance > 15:
            
            box_width = box_height * 0.4
        else:
           
            box_width = box_height * 0.45
            
       
        min_box_size = 8
        box_width = max(min_box_size, box_width)
        box_height = max(min_box_size, box_height)
        
        
        box_x = entity.head_pos2d["x"] - box_width / 2
        
        height_reduction = raw_height * 0.15
        box_y = entity.head_pos2d["y"] + (height_reduction * 0.2)  
        
        return box_x, box_y, box_width, box_height

    @staticmethod
    def draw_health(max, current, PosX, PosY, width, height):
        if cfg.ESP.show_health:
            Proportion = current / max
            Height = height * Proportion
            offsetY = height * (max - current) / max
            
            health_percentage = current / max
            if health_percentage > 0.7:
                health_color = pm.get_color("#00FF00")  
            elif health_percentage > 0.4:
                health_color = pm.get_color("#FFFF00")  
            elif health_percentage > 0.2:
                health_color = pm.get_color("#FFA500")  
            else:
                health_color = pm.get_color("#FF0000")  

            pm.draw_rectangle(PosX + 1, PosY + 1 + offsetY, width / 2, Height, health_color)
            pm.draw_rectangle_lines(PosX, PosY, width, height, Colors.black)
            
           
            if cfg.ESP.show_health_text:
                font_size = 14  
                text_x = PosX + width / 2 + 2
                text_y = PosY + height / 2 - font_size / 2
                pm.draw_text(f"{current}", text_x + 1, text_y + 1, font_size, Colors.black)
                pm.draw_text(f"{current}", text_x, text_y, font_size, Colors.red)
        
        
        return PosX, PosY, width, height

    @staticmethod
    def draw_box(entity, distance, team_color):
        if not cfg.ESP.show_box:
            print("[DEBUG] draw_box: show_box is False, skipping.")
            return
        box_coords = Render.calculate_accurate_box(entity, distance)
        if not box_coords or not all(coord is not None for coord in box_coords):
            print("[DEBUG] draw_box: Invalid box_coords, skipping.")
            return
        box_x, box_y, box_width, box_height = box_coords

        # --- FIX: Use visible color if enabled and entity is spotted ---
        if getattr(cfg.ESP, "visible_color_change", False) and getattr(entity, "spotted", False):
            box_color = Render.get_color_from_config(cfg.ESP.visible_box_color)
        else:
            box_color = Render.get_color_from_config(cfg.ESP.box_color)
        # -------------------------------------------------------------

        box_style = getattr(cfg.ESP, "box_style", "Regular")
        if box_style == "Cornered":
            l = min(box_width, box_height) // 3
            t = 2.0
            pm.draw_line(box_x, box_y, box_x + l, box_y, box_color, t)
            pm.draw_line(box_x, box_y, box_x, box_y + l, box_color, t)
            pm.draw_line(box_x + box_width - l, box_y, box_x + box_width, box_y, box_color, t)
            pm.draw_line(box_x + box_width, box_y, box_x + box_width, box_y + l, box_color, t)
            pm.draw_line(box_x, box_y + box_height - l, box_x, box_y + box_height, box_color, t)
            pm.draw_line(box_x, box_y + box_height, box_x + l, box_y + box_height, box_color, t)
            pm.draw_line(box_x + box_width - l, box_y + box_height, box_x + box_width, box_y + box_height, box_color, t)
            pm.draw_line(box_x + box_width, box_y + box_height - l, box_x + box_width, box_y + box_height, box_color, t)
        else:
            pm.draw_rectangle_lines(box_x, box_y, box_width, box_height, box_color, 2.0)

    @staticmethod
    def draw_skeleton(entity, view_matrix, distance):
        if not cfg.ESP.show_skeleton:
            print("[DEBUG] draw_skeleton: show_skeleton is False, skipping.")
            return

        # --- FIX: Use visible color if enabled and entity is spotted ---
        if getattr(cfg.ESP, "visible_color_change", False) and getattr(entity, "spotted", False):
            skeleton_color = Render.get_color_from_config(cfg.ESP.visible_skeleton_color)
        else:
            skeleton_color = Render.get_color_from_config(cfg.ESP.skeleton_color)
        # -------------------------------------------------------------

        base_thickness = 2.0
        thickness = base_thickness if distance <= 20 else min(base_thickness * 1.1, 2.5)
        if distance > 25:
            bone_connections = [
                (6, 5), (5, 4), (4, 2), (2, 0),
                (4, 8), (8, 10),
                (4, 13), (13, 15),
                (0, 22), (22, 24),
                (0, 25), (25, 27),
            ]
        else:
            bone_connections = [
                (6, 5), (5, 4), (4, 2), (2, 0),
                (4, 8), (8, 9), (9, 10), (10, 11),
                (4, 13), (13, 14), (14, 15), (15, 16),
                (0, 22), (22, 23), (23, 24),
                (0, 25), (25, 26), (26, 27),
            ]
        try:
            for bone1, bone2 in bone_connections:
                bone1_pos = entity.bone_pos(bone1)
                bone2_pos = entity.bone_pos(bone2)
                bone1_2d = pm.world_to_screen(view_matrix, bone1_pos, 1)
                bone2_2d = pm.world_to_screen(view_matrix, bone2_pos, 1)
                if bone1_2d and bone2_2d:
                    pm.draw_line(bone1_2d["x"], bone1_2d["y"], bone2_2d["x"], bone2_2d["y"], skeleton_color, thickness)
        except Exception as e:
            print(f"[DEBUG] draw_skeleton: Exception: {e}")
            pass

    @staticmethod
    def draw_head_circle(entity, view_matrix, local_pos, distance):
        if not cfg.ESP.show_head_circle:
            return
            
        if cfg.ESP.visible_color_change and entity.spotted:
            color_value = cfg.ESP.visible_skeleton_color
        else:
            color_value = cfg.ESP.skeleton_color
        head_color = Render.get_color_from_config(color_value)
        
        try:
            
            head_pos = entity.bone_pos(6)
            head_2d = pm.world_to_screen(view_matrix, head_pos, 1)
            
            if head_2d:
                
                if distance > 25:
                    radius = max(5, 60 / distance)
                else:
                    radius = max(4, 40 / distance)
                radius = min(radius, 10)
                
               
                segments = 12 if distance > 20 else 16
                thickness = cfg.ESP.skeleton_thickness
                
                
                circle_points = []
                for i in range(segments):
                    angle = (i * 2 * math.pi) / segments
                    x = head_2d["x"] + radius * math.cos(angle)
                    y = head_2d["y"] + radius * math.sin(angle)
                    circle_points.append((x, y))
                
                
                for i in range(segments):
                    x1, y1 = circle_points[i]
                    x2, y2 = circle_points[(i + 1) % segments]
                   
                    if cfg.ESP.skeleton_shadow and distance < 15:
                        pm.draw_line(x1 + 1, y1 + 1, x2 + 1, y2 + 1, Colors.black, thickness * 0.8)
                   
                    pm.draw_line(x1, y1, x2, y2, head_color, thickness)
                    
        except:
            pass

class ProcessDetector:
    
    @staticmethod
    def find_cs2_by_name():
        try:
            pm = utils.get_pyMeow()
            possible_names = ["cs2.exe", "cs2", "Counter-Strike 2.exe", "CounterStrike2.exe"]
            
            for name in possible_names:
                try:
                    proc = pm.open_process(name)
                    if proc:
                        print(f"[ProcessDetector] Found CS2 by name: {name}")
                        return proc
                except Exception as e:
                    print(f"[ProcessDetector] Failed to find CS2 by name '{name}': {e}")
                    continue
                    
        except Exception as e:
            print(f"[ProcessDetector] Failed to find CS2 by name: {e}")
        return None
    
    @staticmethod
    def find_cs2_by_pid_scan():
        """Scan all processes to find CS2 by PID"""
        try:
            pm = utils.get_pyMeow()
            cs2_names = ["cs2.exe", "Counter-Strike 2.exe", "CounterStrike2.exe"]
            
            for process in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_name = process.info['name']
                    if proc_name and any(name.lower() in proc_name.lower() for name in cs2_names):
                        pid = process.info['pid']
                        print(f"[ProcessDetector] Found potential CS2 process: {proc_name} (PID: {pid})")
                        
                        
                        if hasattr(pm, 'open_process_by_pid'):
                            proc = pm.open_process_by_pid(pid)
                        else:
                           
                            proc = pm.open_process(proc_name)
                            
                        if proc:
                            print(f"[ProcessDetector] Successfully opened CS2 process: {proc_name} (PID: {pid})")
                            return proc
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                except Exception as e:
                    print(f"[ProcessDetector] Error checking process {process.info.get('name', 'unknown')}: {e}")
                    continue
                    
        except Exception as e:
            print(f"[ProcessDetector] Failed to scan processes by PID: {e}")
        return None
    
    @staticmethod
    def find_cs2_by_window_title():
        """Try to find CS2 by looking for game window titles"""
        try:
            import win32gui
            import win32process
            
            pm = utils.get_pyMeow()
            cs2_window_titles = [
                "Counter-Strike 2",
                "Counter Strike 2", 
                "CS2",
                "cs2"
            ]
            
            def enum_windows_callback(hwnd, windows):
                try:
                    window_title = win32gui.GetWindowText(hwnd)
                    if window_title and any(title.lower() in window_title.lower() for title in cs2_window_titles):
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        windows.append((window_title, pid))
                except:
                    pass
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            for title, pid in windows:
                print(f"[ProcessDetector] Found CS2 window: '{title}' (PID: {pid})")
                try:
                    
                    if hasattr(pm, 'open_process_by_pid'):
                        proc = pm.open_process_by_pid(pid)
                    else:
                       
                        try:
                            p = psutil.Process(pid)
                            proc_name = p.name()
                            proc = pm.open_process(proc_name)
                        except:
                            continue
                            
                    if proc:
                        print(f"[ProcessDetector] Successfully opened CS2 by window detection: {title} (PID: {pid})")
                        return proc
                except Exception as e:
                    print(f"[ProcessDetector] Failed to open process by window PID {pid}: {e}")
                    continue
                    
        except ImportError:
            print("[ProcessDetector] win32gui not available for window title search")
        except Exception as e:
            print(f"[ProcessDetector] Failed to find CS2 by window title: {e}")
        return None
    
    @staticmethod
    def find_cs2_by_common_paths():
        """Try to find CS2 by checking common installation paths"""
        try:
            pm = utils.get_pyMeow()
            common_paths = [
                r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
                r"C:\Program Files\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
                r"C:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    print(f"[ProcessDetector] Found CS2 executable at: {path}")
                    for process in psutil.process_iter(['pid', 'name', 'exe']):
                        try:
                            if process.info['exe'] and os.path.samefile(process.info['exe'], path):
                                pid = process.info['pid']
                                proc_name = process.info['name']
                                print(f"[ProcessDetector] Found running CS2 process at {path} (PID: {pid})")
                                
                                
                                if hasattr(pm, 'open_process_by_pid'):
                                    proc = pm.open_process_by_pid(pid)
                                else:
                                    
                                    proc = pm.open_process(proc_name)
                                    
                                if proc:
                                    return proc
                        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                            continue
                            
        except Exception as e:
            print(f"[ProcessDetector] Failed to find CS2 by common paths: {e}")
        return None
    
    @staticmethod
    def find_cs2_via_steam():
        """Try to find CS2 through Steam process monitoring"""
        try:
            pm = utils.get_pyMeow()
            
            
            steam_pids = []
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_name = process.info['name']
                    if proc_name and 'steam' in proc_name.lower():
                        steam_pids.append(process.info['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if steam_pids:
                print(f"[ProcessDetector] Found {len(steam_pids)} Steam processes")
                
                
                for process in psutil.process_iter(['pid', 'name', 'ppid', 'cmdline']):
                    try:
                        proc_name = process.info['name']
                        if proc_name and any(cs2_name.lower() in proc_name.lower() for cs2_name in ['cs2', 'counter-strike']):
                            pid = process.info['pid']
                            ppid = process.info.get('ppid', 0)
                            
                            print(f"[ProcessDetector] Found CS2-like process: {proc_name} (PID: {pid}, Parent: {ppid})")
                            
                            if hasattr(pm, 'open_process_by_pid'):
                                proc = pm.open_process_by_pid(pid)
                            else:
                                proc = pm.open_process(proc_name)
                                
                            if proc:
                                print(f"[ProcessDetector] Successfully opened CS2 via Steam detection: {proc_name}")
                                return proc
                                
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                        
        except Exception as e:
            print(f"[ProcessDetector] Failed to find CS2 via Steam: {e}")
        return None
    
    @staticmethod
    def find_cs2_with_retry(max_retries=5, retry_delay=2):
        
        
        methods = [
            ("exact name", ProcessDetector.find_cs2_by_name),
            ("PID scan", ProcessDetector.find_cs2_by_pid_scan),
            ("Steam detection", ProcessDetector.find_cs2_via_steam),
            ("window title", ProcessDetector.find_cs2_by_window_title),
            ("common paths", ProcessDetector.find_cs2_by_common_paths)
        ]
        
        for attempt in range(max_retries):
            
            for method_name, method in methods:
                proc = method()
                if proc:
                    return proc
                    
            if attempt < max_retries - 1:
                print(f"[ProcessDetector] All methods failed, waiting {retry_delay}s before retry...")
                time.sleep(retry_delay)
        
        print("[ProcessDetector] Failed to find CS2 process after all attempts")
        return None


class Cheat:
    def __init__(self):
        self.proc = ProcessDetector.find_cs2_with_retry()
        if not self.proc:
            raise Exception("Could not find CS2 process. Make sure Counter-Strike 2 is running.")
            
        
        try:
            pm = utils.get_pyMeow()
            self.mod = pm.get_module(self.proc, "client.dll")["base"]
        except Exception as e:
            raise Exception(f"Could not find client.dll module in CS2 process: {e}")
        try:
            print("[Cheat] Downloading latest offsets...")
            offsets_name = ["dwViewMatrix", "dwEntityList", "dwLocalPlayerController", "dwLocalPlayerPawn", "dwPlantedC4", "dwGameRules"]
            rq = utils.get_requests()
            
            offsets_response = rq.get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json")
            if offsets_response.status_code != 200:
                raise Exception(f"Failed to download offsets: HTTP {offsets_response.status_code}")
            
            offsets = offsets_response.json()
            for offset_name in offsets_name:
                if offset_name in offsets["client.dll"]:
                    setattr(Offsets, offset_name, offsets["client.dll"][offset_name])
                else:
                    if offset_name == "dwPlantedC4":
                        print(f"[Cheat] Warning: {offset_name} not found in offsets, bomb timer may not work")
                        setattr(Offsets, offset_name, 0)
                    else:
                        raise Exception(f"Missing critical offset: {offset_name}")
            
            client_dll_name = {
                "m_iIDEntIndex": "C_CSPlayerPawnBase",
                "m_hPlayerPawn": "CCSPlayerController",
                "m_fFlags": "C_BaseEntity",
                "m_iszPlayerName": "CBasePlayerController",
                "m_iHealth": "C_BaseEntity",
                "m_iTeamNum": "C_BaseEntity",
                "m_vOldOrigin": "C_BasePlayerPawn",
                "m_pGameSceneNode": "C_BaseEntity",
                "m_bDormant": "CGameSceneNode",
                "m_flFlashDuration": "C_CSPlayerPawnBase",
                "m_pClippingWeapon": "C_CSPlayerPawnBase",
                "m_iShotsFired": "C_CSPlayerPawn",
                "m_angEyeAngles": "C_CSPlayerPawnBase",
                "m_aimPunchAngle": "C_CSPlayerPawn",
                "m_entitySpottedState": "C_CSPlayerPawn",
                "m_bSpottedByMask": "EntitySpottedState_t",
                "m_AttributeManager": "C_EconEntity",
                "m_Item": "C_AttributeContainer",
                "m_iItemDefinitionIndex": "C_EconItemView",
                "m_pBoneArray": "CGameSceneNode",
                "m_flC4Blow": "C_PlantedC4",
                "m_flTimerLength": "C_PlantedC4",
                "m_flDefuseLength": "C_PlantedC4", 
                "m_flDefuseCountDown": "C_PlantedC4",
                "m_bBombTicking": "C_PlantedC4",
                "m_bBeingDefused": "C_PlantedC4",
                "m_hBombDefuser": "C_PlantedC4",
                "m_bBombDefused": "C_PlantedC4",
                "m_flNextBeep": "C_PlantedC4",
                "m_bBombPlanted": "C_CSGameRules",
                "m_pObserverServices": "C_BasePlayerPawn",
                "m_hObserverTarget": "CPlayerObserverServices",
                "m_hController": "C_BasePlayerPawn"
            }
            
            client_dll_response = rq.get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json")
            if client_dll_response.status_code != 200:
                raise Exception(f"Failed to download client_dll offsets: HTTP {client_dll_response.status_code}")
                
            clientDll = client_dll_response.json()
            
            missing_offsets = []
            for offset_name, class_name in client_dll_name.items():
                try:
                    offset_found = False
                    
                    if (class_name in clientDll["client.dll"]["classes"] and 
                        "fields" in clientDll["client.dll"]["classes"][class_name] and
                        offset_name in clientDll["client.dll"]["classes"][class_name]["fields"]):
                        
                        offset_value = clientDll["client.dll"]["classes"][class_name]["fields"][offset_name]
                        setattr(Offsets, offset_name, offset_value)
                        offset_found = True
                    
                    elif (class_name in clientDll["client.dll"]["classes"] and 
                          "fields" in clientDll["client.dll"]["classes"][class_name]):
                        
                        fields = clientDll["client.dll"]["classes"][class_name]["fields"]
                        if offset_name in fields:
                            field_value = fields[offset_name]
                            
                            if field_value is None or field_value == 0:
                                print(f"[Cheat] Warning: {offset_name} found but is null/zero, using fallback")
                                
                                if offset_name == "m_pBoneArray":
                                    Offsets.m_pBoneArray = 0x1F0
                                    print(f"[Cheat] Applied fallback for {offset_name}: 0x{Offsets.m_pBoneArray:X}")
                                    offset_found = True
                            else:
                                setattr(Offsets, offset_name, field_value)
                                offset_found = True
                    
                    if not offset_found and offset_name == "m_pBoneArray":
                        potential_classes = ["C_BaseEntity", "CBaseAnimating", "C_BaseAnimating", "CGameSceneNode"]
                        for potential_class in potential_classes:
                            if (potential_class in clientDll["client.dll"]["classes"] and 
                                "fields" in clientDll["client.dll"]["classes"][potential_class] and
                                offset_name in clientDll["client.dll"]["classes"][potential_class]["fields"]):
                                
                                offset_value = clientDll["client.dll"]["classes"][potential_class]["fields"][offset_name]
                                if offset_value and offset_value > 0:
                                    setattr(Offsets, offset_name, offset_value)
                                    offset_found = True
                                    break
                    
                    if not offset_found:
                        missing_offsets.append(f"{offset_name} (from {class_name})")
                        
                except Exception as e:
                    missing_offsets.append(f"{offset_name} (error: {e})")
            
            if missing_offsets:
                
                if not hasattr(Offsets, 'm_pBoneArray'):
                    Offsets.m_pBoneArray = 0x1F0
                    missing_offsets = [offset for offset in missing_offsets if not offset.startswith('m_pBoneArray')]
                
                if not hasattr(Offsets, 'm_hObserverTarget'):
                    Offsets.m_hObserverTarget = 0x44
                    missing_offsets = [offset for offset in missing_offsets if not offset.startswith('m_hObserverTarget')]
                
                if not hasattr(Offsets, 'm_pObserverServices'):
                    Offsets.m_pObserverServices = 0x11C0
                    missing_offsets = [offset for offset in missing_offsets if not offset.startswith('m_pObserverServices')]
                
                if not hasattr(Offsets, 'm_hController'):
                    Offsets.m_hController = 0x133C
                    missing_offsets = [offset for offset in missing_offsets if not offset.startswith('m_hController')]
                
                
               
                
                if missing_offsets:
                    print(f"[Cheat] Still missing offsets after fallbacks: {missing_offsets}")
                else:
                    print(f"[Cheat] All critical offsets available (with fallbacks applied)")
                
                
            print("[Cheat] Offset download completed successfully")
            
        except Exception as e:
            error_msg = f"Critical error: Failed to download current offsets: {e}"
            print(f"[Cheat] {error_msg}")
            print("[Cheat] The cheat cannot work without current offsets.")
            print("[Cheat] Please check your internet connection and try again.")
            print("[Cheat] If the problem persists, the offset source may be temporarily unavailable.")
            raise Exception(error_msg)
        
        
        self.overlay_initialized = False
        
        
        self.aimbot = Aimbot()
        self.triggerbot = TriggerBot(cheat_instance=self, offsets=Offsets)
        class BombTimer:
            def get_bomb_info(self, proc, mod):
                return None
            def draw_bomb_timer(self, bomb_info):
                pass
        self.bomb_timer = BombTimer()
        
       
        self.check_gpu_acceleration()
        
        self.last_frame_time = time.time()

    def check_gpu_acceleration(self):
        try:
            gpu_methods = [
                'set_vsync', 'enable_gpu_acceleration', 'set_render_mode',
                'enable_hardware_acceleration', 'set_opengl_mode'
            ]
            
            available_methods = []
            for method in gpu_methods:
                if hasattr(pm, method):
                    available_methods.append(method)
            
            if available_methods:
                print(f"[Cheat] GPU acceleration methods available: {available_methods}")
                
                
                if hasattr(pm, 'enable_gpu_acceleration'):
                    try:
                        pm.enable_gpu_acceleration(True)
                        print("[Cheat] GPU acceleration enabled")
                    except:
                        print("[Cheat] Failed to enable GPU acceleration")
                
                if hasattr(pm, 'set_vsync'):
                    try:
                        pm.set_vsync(True)
                        print("[Cheat] VSync enabled for smoother rendering")
                    except:
                        print("[Cheat] Failed to enable VSync")
                
                if hasattr(pm, 'set_render_mode'):
                    try:
                        pm.set_render_mode('hardware')  
                        print("[Cheat] Hardware render mode enabled")
                    except:
                        print("[Cheat] Failed to set hardware render mode")
                        
                
        except Exception as e:
            print(f"[Cheat] Error checking GPU acceleration: {e}")

    def update_overlay_fps(self, new_fps):
        """Update overlay FPS dynamically if possible"""
        if not self.overlay_initialized:
            print(f"[Cheat] Overlay not initialized yet, FPS will be applied on next start")
            return False
            
        try:
            pm = utils.get_pyMeow()
            if hasattr(pm, 'set_overlay_fps'):
                pm.set_overlay_fps(int(new_fps))
                print(f"[Cheat] Overlay FPS updated to {int(new_fps)}")
                return True
            elif hasattr(pm, 'overlay_set_fps'):
                pm.overlay_set_fps(int(new_fps))
                print(f"[Cheat] Overlay FPS updated to {int(new_fps)}")
                return True
            else:
                return False
        except Exception as e:
            print(f"[Cheat] Failed to update overlay FPS: {e}")
            return False

    def it_entities(self):
        ent_list = pm.r_int64(self.proc, self.mod + Offsets.dwEntityList)
        local = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerController)
        entity_count = 0
        now = time.time()
        if not hasattr(self, '_last_entity_debug') or now - self._last_entity_debug > 2.0:
            self._print_entity_debug = True
            self._last_entity_debug = now
        else:
            self._print_entity_debug = False
        for i in range(1, 65):
            try:
                entry_ptr = pm.r_int64(self.proc, ent_list + (8 * (i & 0x7FFF) >> 9) + 16)
                if not entry_ptr or entry_ptr < 0x1000:
                    continue
                controller_ptr = pm.r_int64(self.proc, entry_ptr + 120 * (i & 0x1FF))
                if not controller_ptr or controller_ptr < 0x1000 or controller_ptr == local:
                    continue
                controller_pawn_ptr = pm.r_int64(self.proc, controller_ptr + Offsets.m_hPlayerPawn)
                if not controller_pawn_ptr or controller_pawn_ptr < 0x1000:
                    continue
                list_entry_ptr = pm.r_int64(self.proc, ent_list + 0x8 * ((controller_pawn_ptr & 0x7FFF) >> 9) + 16)
                if not list_entry_ptr or list_entry_ptr < 0x1000:
                    continue
                pawn_ptr = pm.r_int64(self.proc, list_entry_ptr + 120 * (controller_pawn_ptr & 0x1FF))
                if not pawn_ptr or pawn_ptr < 0x1000:
                    continue
                if self._print_entity_debug:
                    print(f"[DEBUG] i={i}, controller_ptr=0x{controller_ptr:X}, pawn_ptr=0x{pawn_ptr:X}")
                yield Entity(controller_ptr, pawn_ptr, self.proc, self)
                entity_count += 1
            except Exception as e:
                continue
        if self._print_entity_debug:
            print(f"[DEBUG] Entities yielded: {entity_count}")

    def get_local_pawn(self):
        
        try:
            local_pawn = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerPawn)
            
            if local_pawn and local_pawn > 0x1000:
                return local_pawn
            return None
        except:
            return None

    def get_local_player_pos(self):
       
        try:
            local_pawn = self.get_local_pawn()
            if not local_pawn:
                return None
            pos = pm.r_vec3(self.proc, local_pawn + Offsets.m_vOldOrigin)
            if pos and all(isinstance(pos.get(k), (int, float)) for k in ['x', 'y', 'z']):
                return pos
            return None
        except:
            return None
    
    def get_local_player_team(self):
        try:
            local_pawn = self.get_local_pawn()
            if local_pawn:
                team = pm.r_int(self.proc, local_pawn + Offsets.m_iTeamNum)
                if team in [2, 3]:
                    return team
            return 0
        except:
            return 0

    def get_local_player_index(self):
        """Get the local player's index/slot for bitmask operations"""
        try:
            local_controller = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerController)
            if not local_controller or local_controller < 0x1000:
                return None
            
            local_index = pm.r_int(self.proc, local_controller + Offsets.m_iIDEntIndex)
            if 0 <= local_index <= 63:
                return local_index
            return None
        except:
            return None
    
    def update_local_player_index(self):
        """Update the cached local player index"""
        current_time = time.time()
        if (not hasattr(self, '_last_index_update') or 
            current_time - self._last_index_update > 2.0):
            
            self._cached_local_index = self.get_local_player_index()
            self._last_index_update = current_time
            
          
    
    _cached_local_index = None
    _last_index_update = 0

    def run(self):
        possible_titles = ["Counter-Strike 2", "cs2", "CS2", "Counter-Strike: Global Offensive"]
        game_window_title = None
        
        for title in possible_titles:
            try:
                
                hwnd = user32.FindWindowW(None, title)
                if hwnd:
                    game_window_title = title
                    break
            except:
                continue
        
        if not game_window_title:
           
            game_window_title = "Counter-Strike 2"
            print("[Security] Warning: Could not find CS2 window, using default title")
        
        pm.overlay_init(game_window_title, fps=cfg.MISC.overlay_fps)
        self.overlay_initialized = True
        
        self.optimize_overlay_rendering()
        
    
        
        frame_counter = 0
        title_change_interval = 5000
        
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        self.update_local_player_index()
        
        self._cached_local_index = None
        self._last_index_update = 0
        
        while pm.overlay_loop():
            current_frame_time = time.time()
            frame_start = current_frame_time
            
            try:
                self.update_local_player_index()
                
                if cfg.TRIGGERBOT.enabled:
                    try:
                        self.triggerbot.check_and_shoot(self.proc, self.mod)
                    except:
                        pass
                
                if cfg.AIMBOT.enabled:
                    try:
                        local_pawn = self.get_local_pawn()
                        if local_pawn and view_matrix:
                            pass
                    except:
                        pass
                
                frame_counter += 1
               
                
                try:
                    view_matrix = pm.r_floats(self.proc, self.mod + Offsets.dwViewMatrix, 16)
                    if not view_matrix or len(view_matrix) != 16:
                        continue
                except Exception as e:
                    consecutive_errors += 1
                    if consecutive_errors > max_consecutive_errors:
                        print("[Cheat] Too many consecutive errors, restarting...")
                        break
                    continue

                pm.begin_drawing()
                
                if hasattr(self, 'use_batched_rendering') and self.use_batched_rendering:
                    try:
                        pm.begin_batch()
                    except:
                        pass
                
                pm.draw_fps(0, 0)
                
                try:
                    local_pos = self.get_local_player_pos()
                    local_team = self.get_local_player_team()
                    
                    if not local_pos:
                        pm.draw_text("In Main Menu - Join a game to see ESP", 50, 50, 16, pm.get_color("#FFFF00"))
                        pm.end_drawing()
                        consecutive_errors = 0
                        continue
                except Exception as e:
                    pm.draw_text("Waiting for game data...", 50, 50, 16, pm.get_color("#FFA500"))
                    pm.end_drawing()
                    continue
                
                entities_to_render = []
                entity_count = 0
                max_entities_per_frame = 32
                debug_entity_infos = []
                for ent in self.it_entities():
                        if entity_count >= max_entities_per_frame:
                            break
                        try:
                            if not ent or not ent.ptr or not ent.pawn_ptr:
                                continue
                            try:
                                if ent.health <= 0:
                                    continue
                            except Exception as e:
                                continue
                            if not ent.wts(view_matrix):
                                continue
                            if ent.dormant:
                                continue
                            if cfg.ESP.visible_only and not ent.spotted:
                                continue
                            distance = ent.get_distance(local_pos)
                            if not distance or distance > esp_distance:
                                continue
                            if not cfg.ESP.show_teammates and ent.team == local_team:
                                continue
                            entities_to_render.append((ent, distance))
                            debug_entity_infos.append(f"ptr=0x{ent.ptr:X}, pawn=0x{ent.pawn_ptr:X}, health={ent.health}, team={ent.team}")
                            entity_count += 1
                        except Exception as e:
                            print(f"[FILTER] Skipped: Exception in entity loop ({e})")
                            continue
                    
                
                esp_distance = getattr(cfg.ESP, 'esp_distance', getattr(cfg.ESP, 'max_distance', 100))
                
                try:
                    if entities_to_render:
                        if cfg.AIMBOT.enabled:
                            self.aimbot.check_and_aim(entities_to_render, local_pos, local_team, self.proc, self.get_local_pawn(), view_matrix)
                        self.render_entities_optimized(entities_to_render, view_matrix, local_pos, local_team, esp_distance)
                    else:
                        pm.draw_text("No players detected", 50, 80, 14, pm.get_color("#808080"))
                except Exception as e:
                    print(f"[Cheat] Error rendering entities: {e}")
                
                try:
                    if cfg.AIMBOT.enabled and cfg.AIMBOT.show_fov_circle:
                        self.aimbot.draw_fov_circle()
                except Exception as e:
                    pass
                
                try:
                    if cfg.MISC.bomb_timer and not cfg.MISC.streamproof:
                        bomb_info = self.bomb_timer.get_bomb_info(self.proc, self.mod)
                        self.bomb_timer.draw_bomb_timer(bomb_info)
                except Exception as e:
                    print(f"[BombTimer] Error: {e}")
                
                if hasattr(self, 'use_batched_rendering') and self.use_batched_rendering:
                    try:
                        pm.end_batch()
                    except:
                        pass
                
                pm.end_drawing()
                
                consecutive_errors = 0
                
                frame_end = time.time()
                frame_duration = frame_end - frame_start
                
                if frame_duration > 0.1:
                
                
                 if frame_counter >= title_change_interval:
                    frame_counter = 0
                    
            except Exception as e:
                print(f"[Cheat] Critical error in main loop: {e}")
                consecutive_errors += 1
                if consecutive_errors > max_consecutive_errors:
                    print("[Cheat] Too many errors, exiting...")
                    break
                    
                try:
                    pm.end_drawing()
                except:
                    pass
                continue

    def optimize_overlay_rendering(self):
        """Apply rendering optimizations after overlay initialization"""
        try:
            optimization_methods = [
                ('set_blend_mode', 'alpha'),
                ('enable_antialiasing', False),
                ('set_line_smoothing', False),
                ('enable_texture_filtering', False),
                ('set_buffer_mode', 'double'),
                ('enable_fast_rendering', True),
                ('set_quality_mode', 'performance')
            ]
            
            for method_name, value in optimization_methods:
                if hasattr(pm, method_name):
                    try:
                        getattr(pm, method_name)(value)
                        print(f"[Cheat] Applied optimization: {method_name}({value})")
                    except Exception as e:
                        print(f"[Cheat] Failed to apply {method_name}: {e}")
            
            if hasattr(pm, 'begin_batch') and hasattr(pm, 'end_batch'):
                print("[Cheat] Batched rendering available - will use for better performance")
                self.use_batched_rendering = True
            else:
                self.use_batched_rendering = False
                
        except Exception as e:
            print(f"[Cheat] Error applying rendering optimizations: {e}")

    def render_entities_optimized(self, entities, view_matrix, local_pos, local_team, esp_distance):
        """Optimized rendering with no caching - fresh data every frame"""
        try:
            if cfg.ESP.show_line and entities:
                try:
                    line_color = Render.get_color_from_config(cfg.ESP.line_color)
                    screen_width = pm.get_screen_width()
                    screen_height = pm.get_screen_height()
                    
                    if cfg.ESP.line_position == "Top":
                        start_x, start_y = screen_width / 2, 0
                    elif cfg.ESP.line_position == "Bottom":
                        start_x, start_y = screen_width / 2, screen_height
                    else:
                        start_x, start_y = screen_width / 2, screen_height / 2
                    
                    for ent, distance in entities[:16]:
                        try:
                            end_x = ent.head_pos2d["x"]
                            end_y = ent.head_pos2d["y"]
                            pm.draw_line(start_x, start_y, end_x, end_y, line_color, 1.0)
                        except:
                            continue
                except Exception as e:
                    print(f"[Render] Error drawing lines: {e}")
            
            try:
                for ent, distance in entities:
                    try:
                        color = Colors.cyan if ent.team != 2 else Colors.orange
                        Render.draw_box(ent, distance, color)
                    except:
                        continue
            except Exception as e:
                print(f"[Render] Error drawing boxes: {e}")
            
            try:
                skeleton_count = 0
                for ent, distance in entities:
                    if skeleton_count >= 8:
                        break
                    if distance < 30:
                        try:
                            Render.draw_skeleton(ent, view_matrix, distance)
                            skeleton_count += 1
                        except:
                            continue
            except Exception as e:
                print(f"[Render] Error drawing skeletons: {e}")
            
            try:
                circle_count = 0
                for ent, distance in entities:
                    if circle_count >= 4:
                        break
                    if distance < 20:
                        try:
                            Render.draw_head_circle(ent, view_matrix, local_pos, distance)
                            circle_count += 1
                        except:
                            continue
            except Exception as e:
                print(f"[Render] Error drawing head circles: {e}")
            
            try:
                text_count = 0
                for ent, distance in entities:
                    if text_count >= 12:
                        break
                    try:
                        box_coords = Render.calculate_accurate_box(ent, distance)
                        if box_coords and all(coord is not None for coord in box_coords):
                            box_x, box_y, box_width, box_height = box_coords
                            
                            health_bar_x = box_x + box_width + 3
                            health_bar_y = box_y - 5
                            health_bar_width = max(3, 6 - distance // 10)
                            health_bar_height = box_height + 10
                            
                            Render.draw_health(100, ent.health, health_bar_x, health_bar_y, health_bar_width, health_bar_height)
                            
                            info_texts = []
                            if cfg.ESP.show_name and distance < 25:
                                info_texts.append(ent.name)
                            if cfg.ESP.show_distance:
                                info_texts.append(f"{distance}m")
                            if cfg.ESP.show_weapon and distance < 20:
                                weapon_name = ent.get_weapon_name()
                                if weapon_name and weapon_name != "Unknown":
                                    info_texts.append(weapon_name)
                            
                            info_texts = info_texts[:4]
                            
                            font_size = 12 if distance < 20 else 10
                            line_spacing = font_size + 4
                            total_height = len(info_texts) * line_spacing
                            text_start_y = box_y - total_height - 6;
                            
                            for idx, text in enumerate(info_texts):
                                text_width = font_size * 0.6 * len(text)
                                text_x = box_x + box_width / 2 - text_width / 2
                                text_y = text_start_y + idx * line_spacing
                                pm.draw_text(text, text_x, text_y, font_size, pm.get_color("#FFFFFF"))
                            
                            text_count += 1
                    except:
                        continue
            except Exception as e:
                print(f"[Render] Error drawing health/text: {e}")
                
        except Exception as e:
            print(f"[Render] Critical error in optimized rendering: {e}")

weapon_names = {
    1: "Desert Eagle",
    2: "Dual Berettas",
    3: "Five-SeveN",
    4: "Glock-18",
    7: "AK-47",
    8: "AUG",
    9: "AWP",
    10: "FAMAS",
    11: "G3SG1",
    13: "Galil AR",
    14: "M249",
    16: "M4A4",
    17: "MAC-10",
    19: "P90",
    23: "MP5-SD",
    24: "UMP-45",
    25: "XM1014",
    26: "PP-Bizon",
    27: "MAG-7",
    28: "Negev",
    29: "Sawed-Off",
    30: "Tec-9",
    31: "Zeus x27",
    32: "P2000",
    33: "MP7",
    34: "MP9",
    35: "Nova",
    36: "P250",
    38: "SCAR-20",
    39: "SG 553",
    40: "SSG 08",
    60: "M4A1-S",
    61: "USP-S",
    63: "CZ75-Auto",
    64: "R8 Revolver"
}
