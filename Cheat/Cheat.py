import math
import ctypes
import random
import string
import os
import sys
import time
import psutil
import keyboard
import Utils
import Configs as cfg
from random import uniform
from win32gui import GetWindowText, GetForegroundWindow
from pynput.mouse import Controller, Button

# Add win32api import for mouse button detection
try:
    import win32api
except ImportError:
    print("[Aimbot] Warning: win32api not available, mouse button detection may not work")
    win32api = None





user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
ntdll = ctypes.windll.ntdll
pm = Utils.get_pyMeow()
rq = Utils.get_requests()






class SecurityUtils:
    @staticmethod
    def generate_random_title():
        legitimate_titles = [
            "Microsoft Office Word",
            "Windows Security",
            "System Configuration",
            "Windows Update",
            "Task Manager",
            "Calculator",
            "Notepad",
            "Windows Explorer",
            "Control Panel",
            "Registry Editor",
            "System Information",
            "Windows Defender",
            "Network Configuration",
            "Device Manager",
            "Windows Settings"
        ]
        base_title = random.choice(legitimate_titles)
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        return f"{base_title} - {random_suffix}"
    
    @staticmethod
    def hide_from_process_list():
        try:
            current_process = kernel32.GetCurrentProcess()
            hwnd = user32.GetConsoleWindow()
            if hwnd:
                user32.ShowWindow(hwnd, 0) 
            kernel32.SetPriorityClass(current_process, 0x40)  
            return True
        except:
            return False
    
    @staticmethod
    def rename_process():
        try:
            process_name = "winlogon.exe\x00"
            process_name_bytes = process_name.encode('utf-16le')
            current_process = kernel32.GetCurrentProcess()
            return True
        except:
            return False
    
    @staticmethod
    def enable_debug_privileges():
        try:
            TOKEN_ADJUST_PRIVILEGES = 0x0020
            TOKEN_QUERY = 0x0008
            SE_DEBUG_PRIVILEGE = 20
            
            token = ctypes.c_void_p()
            luid = ctypes.c_uint64()

            if not ctypes.windll.advapi32.OpenProcessToken(
                kernel32.GetCurrentProcess(),
                TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
                ctypes.byref(token)
            ):
                return False
                
            if not ctypes.windll.advapi32.LookupPrivilegeValueW(
                None,
                "SeDebugPrivilege",
                ctypes.byref(luid)
            ):
                return False
                
            class TOKEN_PRIVILEGES(ctypes.Structure):
                _fields_ = [
                    ("PrivilegeCount", ctypes.c_uint32),
                    ("Luid", ctypes.c_uint64),
                    ("Attributes", ctypes.c_uint32)
                ]
            
            tp = TOKEN_PRIVILEGES()
            tp.PrivilegeCount = 1
            tp.Luid = luid.value
            tp.Attributes = 0x00000002  
            
            return ctypes.windll.advapi32.AdjustTokenPrivileges(
                token,
                False,
                ctypes.byref(tp),
                ctypes.sizeof(tp),
                None,
                None
            )
        except:
            return False
    
    @staticmethod
    def anti_debug_check():
        try:
            if kernel32.IsDebuggerPresent():
                return False
            
            import psutil
            suspicious_processes = [
                'ollydbg.exe', 'ida.exe', 'ida64.exe', 'windbg.exe',
                'x32dbg.exe', 'x64dbg.exe', 'cheatengine.exe',
                'processhacker.exe', 'procmon.exe', 'procexp.exe'
            ]
            
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() in suspicious_processes:
                        return False
                except:
                    continue
            
            return True
        except:
            return True  
    
    @staticmethod
    def set_overlay_title(title):
        try:
            try:
                import pygetwindow as gw
                windows = gw.getAllWindows()
                overlay_window = None
                for window in windows:
                    if (
                        (window.title == "" or 
                        "OpenGL" in window.title or 
                        "pygame" in window.title or
                        window.title.startswith("SDL") or
                        "pyMeow" in window.title.lower()) and
                        ("counter-strike" not in window.title.lower() and "cs2" not in window.title.lower())
                    ):
                        overlay_window = window
                        break
                if overlay_window:
                    hwnd = overlay_window._hWnd
                    user32.SetWindowTextW(hwnd, title)
                    return True
            except ImportError:
                pass 

            def enum_windows_callback(hwnd, lParam):
                try:
                    title_buffer = ctypes.create_unicode_buffer(256)
                    user32.GetWindowTextW(hwnd, title_buffer, 256)
                    window_title = title_buffer.value
                    
                    class_buffer = ctypes.create_unicode_buffer(256)
                    user32.GetClassNameW(hwnd, class_buffer, 256)
                    class_name = class_buffer.value
                    
                    
                    if (
                        (window_title == "" or 
                        "OpenGL" in window_title or
                        "SDL" in class_name or
                        "pyMeow" in window_title.lower()) and
                        ("counter-strike" not in window_title.lower() and 
                         "cs2" not in window_title.lower() and
                         "cheat menu" not in window_title.lower())  # Don't rename GUI window
                    ):
                        user32.SetWindowTextW(hwnd, title)
                        return False  
                except:
                    pass
                return True  
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
            user32.EnumWindows(EnumWindowsProc(enum_windows_callback), 0)
            return True
        except Exception as e:
            return False

    @staticmethod
    def obfuscate_gui_title(new_title):
        """Separate function to obfuscate the GUI window title"""
        try:
            hwnd = user32.FindWindowW(None, "Cheat Menu")
            if hwnd:
                user32.SetWindowTextW(hwnd, new_title)
                return True
            else:
                return False
        except Exception as e:
            print(f"[Security] Failed to obfuscate GUI title: {e}")
            return False

class Offsets:
    # Dynamic offsets will be populated from online sources during initialization
    # No static fallbacks to avoid using outdated offsets
    pass


class Colors:
    green = pm.get_color("#00FF00")
    orange = pm.fade_color(pm.get_color("#FFA500"), 0.3)
    black = pm.get_color("black")
    cyan = pm.fade_color(pm.get_color("#00F6F6"), 0.3)
    white = pm.get_color("white")
    grey = pm.fade_color(pm.get_color("#242625"), 0.7)
    red = pm.get_color("#FF0000")  


class TriggerBot:
    def __init__(self):
        self.mouse = Controller()
        self.last_shot_time = 0
        self.next_shot_delay = 0
        self.can_shoot = True
        self.last_check_time = 0
        self.first_shot = True  
        
    def shoot(self):
        """Execute a mouse click and set next shot delay"""
        current_time = time.time()
        
       
        if self.first_shot:
            self.last_shot_time = current_time
            self.next_shot_delay = uniform(cfg.TRIGGERBOT.delay_min, cfg.TRIGGERBOT.delay_max)
            self.first_shot = False
            if self.next_shot_delay <= 0.0:
                self.mouse.click(Button.left)
                return True
            return False  
        
        
        if current_time >= self.last_shot_time + self.next_shot_delay:
            self.mouse.click(Button.left)
            self.last_shot_time = current_time
            self.next_shot_delay = uniform(cfg.TRIGGERBOT.delay_min, cfg.TRIGGERBOT.delay_max)
            return True
        return False
        
    def check_and_shoot(self, process, module):
        current_time = time.time()
        
        if current_time - self.last_check_time < cfg.TRIGGERBOT.check_interval:
            return False
        
        self.last_check_time = current_time
        
        try:
            # Check if we're in CS2 window (using flexible matching)
            current_window = GetWindowText(GetForegroundWindow()).lower()
            cs2_window_keywords = ["counter-strike", "cs2", "csgo"]
            
            if not any(keyword in current_window for keyword in cs2_window_keywords):
                return False
                
            
            if not keyboard.is_pressed(cfg.TRIGGERBOT.trigger_key):
                self.first_shot = True
                return False
                
            
            local_pawn = pm.r_int64(process, module + Offsets.dwLocalPlayerPawn)
            if not local_pawn:
                return False
                
           
            entity_id = pm.r_int(process, local_pawn + Offsets.m_iIDEntIndex)
            if entity_id <= 0:
                return False
                
          
            entity_list = pm.r_int64(process, module + Offsets.dwEntityList)
            entry_ptr = pm.r_int64(process, entity_list + 0x8 * (entity_id >> 9) + 0x10)
            entity_ptr = pm.r_int64(process, entry_ptr + 120 * (entity_id & 0x1FF))
            
            if not entity_ptr:
                return False
                
            
            target_health = pm.r_int(process, entity_ptr + Offsets.m_iHealth)
            target_team = pm.r_int(process, entity_ptr + Offsets.m_iTeamNum)
            local_team = pm.r_int(process, local_pawn + Offsets.m_iTeamNum)
            
            
            if target_health > 0 and target_team != 0:
                if cfg.TRIGGERBOT.shoot_teammates or (target_team != local_team):
                    return self.shoot()  # This now returns True/False based on timing
                    
        except Exception as e:
            pass
            
        return False

class Entity:

    def __init__(self, ptr, pawn_ptr, proc, cheat_instance=None):
        self.ptr = ptr
        self.pawn_ptr = pawn_ptr
        self.proc = proc
        self.cheat = cheat_instance  # Reference to cheat instance for local player info
        self._valid = ptr and pawn_ptr and ptr > 0x1000 and pawn_ptr > 0x1000

    @property
    def name(self):
        # always read fresh from memory with validation
        if not self._valid:
            return "Invalid"
        try:
            name = pm.r_string(self.proc, self.ptr + Offsets.m_iszPlayerName)
            return name if name else "Unknown"
        except:
            return "Error"

    @property
    def health(self):
        # always read fresh from memory with validation
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
        # always read fresh from memory with validation
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
        # always read fresh from memory with validation
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
        # always read fresh from memory with validation
        if not self._valid:
            return True
        try:
            dormant = pm.r_bool(self.proc, self.pawn_ptr + Offsets.m_bDormant)
            return bool(dormant)
        except:
            return True

    @property
    def spotted(self):
        # Fast visibility check - only check local player's bit in spotted mask
        if not self._valid:
            return False
        try:
            # Direct read of spotted mask (faster than multiple reads)
            spotted_mask = pm.r_int(self.proc, self.pawn_ptr + Offsets.m_entitySpottedState + Offsets.m_bSpottedByMask)
            
            # Use cached local player index if available
            if (self.cheat and hasattr(self.cheat, '_cached_local_index') and 
                self.cheat._cached_local_index is not None):
                # Fast path: use cached index
                local_player_bit = 1 << self.cheat._cached_local_index
                return bool(spotted_mask & local_player_bit)
            
            # Slower path: try to determine local player index
            # For most servers, local player is usually in slots 0-7
            # Check common slots first for speed
            for slot in [0, 1, 2, 3]:  # Check first 4 slots (most common)
                test_bit = 1 << slot
                if spotted_mask & test_bit:
                    # This might be the local player's spot
                    # We'll use slot 0 as the most likely candidate
                    if slot == 0:
                        return True
            
            # Fallback: assume local player is first available bit
            return bool(spotted_mask & 1)  # Check bit 0
                
        except:
            return False

    @property
    def weaponIndex(self):
        if not self._valid:
            return 0
        try:
            # always read fresh from memory
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
            # always get fresh weapon index
            weapon_index = self.weaponIndex
            return weapon_names.get(weapon_index, "Unknown")
        except:
            return "Unknown"
        
    def get_distance(self, localPos):
        # always calculate fresh distance with validation
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
        # always read fresh bone data with validation
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
            return False
        try:
            head_pos = self.bone_pos(6)  
            feet_pos = self.pos.copy()  
            if not head_pos or not feet_pos:
                return False
                
            feet_pos["z"] -= 10  
            
            pos2d = pm.world_to_screen(view_matrix, self.pos, 1)
            head_pos2d = pm.world_to_screen(view_matrix, head_pos, 1)
            feet_pos2d = pm.world_to_screen(view_matrix, feet_pos, 1)
            
            # Validate 2D positions
            if not (pos2d and head_pos2d and feet_pos2d):
                return False
                
            self.pos2d = pos2d
            self.head_pos2d = head_pos2d
            self.feet_pos2d = feet_pos2d
            
            return all(pos.get("x") and pos.get("y") for pos in [pos2d, head_pos2d, feet_pos2d])
        except:
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
            hex_color = color_map.get(color_value, "#FFFFFF")
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
                pm.draw_text(f"{current}", text_x + 1, text_y + 1, font_size, Colors.black)  # Shadow
                pm.draw_text(f"{current}", text_x, text_y, font_size, Colors.red)  # Red text
        
        
        return PosX, PosY, width, height

    @staticmethod
    def draw_box(entity, distance, team_color):
        if not cfg.ESP.show_box:
            return
            
        box_coords = Render.calculate_accurate_box(entity, distance)
        if not all(coord is not None for coord in box_coords):
            return
            
        box_x, box_y, box_width, box_height = box_coords
        
        # Choose color based on visibility if enabled
        if cfg.ESP.visible_color_change and entity.spotted:
            box_color = Render.get_color_from_config(cfg.ESP.visible_box_color)
        else:
            box_color = Render.get_color_from_config(cfg.ESP.box_color)
        
        box_fill_color = Render.get_color_from_config(cfg.ESP.box_fill_color)
        
        
        if cfg.ESP.box_style == "Filled":
            pm.draw_rectangle(box_x, box_y, box_width, box_height, box_fill_color)
           
            Render.draw_smooth_rectangle_lines(box_x, box_y, box_width, box_height, box_color, 1.2)
        elif cfg.ESP.box_style == "Cornered":
            Render.draw_cornered_box_improved(box_x, box_y, box_width, box_height, box_color, distance, False)
        elif cfg.ESP.box_style == "Cornered + Filled":
            Render.draw_cornered_box_improved(box_x, box_y, box_width, box_height, box_color, distance, True, box_fill_color)
        else:  
            
            pm.draw_rectangle_lines(box_x + 1, box_y + 1, box_width, box_height, Colors.black, 0.8)
            
            Render.draw_smooth_rectangle_lines(box_x, box_y, box_width, box_height, box_color, 1.2)

    @staticmethod
    def draw_cornered_box_improved(x, y, width, height, color, distance, filled=False, fill_color=None):
        corner_length = min(width, height) * 0.25
        corner_length = max(corner_length, 6)
        
        thickness = 1.5
        
        
        if filled and fill_color:
            pm.draw_rectangle(x, y, width, height, fill_color)
        
        
        corners = [
            # Top-left
            [(x, y, x + corner_length, y), (x, y, x, y + corner_length)],
            # Top-right  
            [(x + width - corner_length, y, x + width, y), (x + width, y, x + width, y + corner_length)],
            # Bottom-left
            [(x, y + height - corner_length, x, y + height), (x, y + height, x + corner_length, y + height)],
            # Bottom-right
            [(x + width, y + height - corner_length, x + width, y + height), (x + width - corner_length, y + height, x + width, y + height)]
        ]
        
        for corner_lines in corners:
            for line in corner_lines:
                x1, y1, x2, y2 = line
                pm.draw_line(x1, y1, x2, y2, color, thickness)

    @staticmethod
    def draw_skeleton(entity, view_matrix, distance):
        if not cfg.ESP.show_skeleton:
            return

        # Choose color based on visibility if enabled
        if cfg.ESP.visible_color_change and entity.spotted:
            color_value = cfg.ESP.visible_skeleton_color
        else:
            color_value = cfg.ESP.skeleton_color
        skeleton_color = Render.get_color_from_config(color_value)
        
        
        base_thickness = cfg.ESP.skeleton_thickness
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
                # Get fresh bone positions for each connection
                bone1_pos = entity.bone_pos(bone1)
                bone2_pos = entity.bone_pos(bone2)
                
                bone1_2d = pm.world_to_screen(view_matrix, bone1_pos, 1)
                bone2_2d = pm.world_to_screen(view_matrix, bone2_pos, 1)
                
                if bone1_2d and bone2_2d:
                    if cfg.ESP.skeleton_shadow and distance < 15:
                        pm.draw_line(bone1_2d["x"] + 1, bone1_2d["y"] + 1, 
                                   bone2_2d["x"] + 1, bone2_2d["y"] + 1, 
                                   Colors.black, thickness * 0.8)
                    
                    
                    pm.draw_line(bone1_2d["x"], bone1_2d["y"], 
                               bone2_2d["x"], bone2_2d["y"], 
                               skeleton_color, thickness)
                
        except Exception as e:
            pass

    @staticmethod
    def draw_head_circle(entity, view_matrix, local_pos, distance):
        if not cfg.ESP.show_head_circle:
            return
            
        # Choose color based on visibility if enabled
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
                   
                    # Simple shadow only for close targets
                    if cfg.ESP.skeleton_shadow and distance < 15:
                        pm.draw_line(x1 + 1, y1 + 1, x2 + 1, y2 + 1, Colors.black, thickness * 0.8)
                   
                    # Main circle line
                    pm.draw_line(x1, y1, x2, y2, head_color, thickness)
                    
        except:
            pass

class ProcessDetector:
    
    @staticmethod
    def find_cs2_by_name():
        try:
            pm = Utils.get_pyMeow()
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
            pm = Utils.get_pyMeow()
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
            
            pm = Utils.get_pyMeow()
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
            pm = Utils.get_pyMeow()
            common_paths = [
                r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
                r"C:\Program Files\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
                r"C:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    print(f"[ProcessDetector] Found CS2 executable at: {path}")
                    # Check if this executable is currently running
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
            pm = Utils.get_pyMeow()
            
            
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
                            
                            # Try to open this process
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
            pm = Utils.get_pyMeow()
            self.mod = pm.get_module(self.proc, "client.dll")["base"]
        except Exception as e:
            raise Exception(f"Could not find client.dll module in CS2 process: {e}")        # Download fresh offsets - this is critical for the cheat to work
        try:
            print("[Cheat] Downloading latest offsets...")
            offsets_name = ["dwViewMatrix", "dwEntityList", "dwLocalPlayerController", "dwLocalPlayerPawn", "dwPlantedC4", "dwGameRules"]
            rq = Utils.get_requests()
            
            # Download main offsets
            offsets_response = rq.get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json")
            if offsets_response.status_code != 200:
                raise Exception(f"Failed to download offsets: HTTP {offsets_response.status_code}")
            
            offsets = offsets_response.json()
            for offset_name in offsets_name:
                if offset_name in offsets["client.dll"]:
                    setattr(Offsets, offset_name, offsets["client.dll"][offset_name])
                else:
                    # Allow dwPlantedC4 to be optional since it may not exist in all game states
                    if offset_name == "dwPlantedC4":
                        print(f"[Cheat] Warning: {offset_name} not found in offsets, bomb timer may not work")
                        setattr(Offsets, offset_name, 0)
                    else:
                        raise Exception(f"Missing critical offset: {offset_name}")
            
            # Download client.dll offsets
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
                # Bomb/C4 related offsets
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
                # Observer/Spectator related offsets
                "m_pObserverServices": "C_BasePlayerPawn",
                "m_hObserverTarget": "CPlayerObserverServices",
                "m_hController": "C_BasePlayerPawn"
            }
            
            clientDll_response = rq.get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json")
            if clientDll_response.status_code != 200:
                raise Exception(f"Failed to download client_dll offsets: HTTP {clientDll_response.status_code}")
                
            clientDll = clientDll_response.json()
            
            missing_offsets = []
            for offset_name, class_name in client_dll_name.items():
                try:
                    # Enhanced search logic for better offset detection
                    offset_found = False
                    
                    # Primary search: exact class and field match
                    if (class_name in clientDll["client.dll"]["classes"] and 
                        "fields" in clientDll["client.dll"]["classes"][class_name] and
                        offset_name in clientDll["client.dll"]["classes"][class_name]["fields"]):
                        
                        offset_value = clientDll["client.dll"]["classes"][class_name]["fields"][offset_name]
                        setattr(Offsets, offset_name, offset_value)
                        offset_found = True
                    
                    # Secondary search: check if field exists but is null (special handling for m_pBoneArray)
                    elif (class_name in clientDll["client.dll"]["classes"] and 
                          "fields" in clientDll["client.dll"]["classes"][class_name]):
                        
                        fields = clientDll["client.dll"]["classes"][class_name]["fields"]
                        if offset_name in fields:
                            field_value = fields[offset_name]
                            
                            # Check if the field is null or invalid
                            if field_value is None or field_value == 0:
                                print(f"[Cheat] Warning: {offset_name} found but is null/zero, using fallback")
                                
                                # Special handling for m_pBoneArray
                                if offset_name == "m_pBoneArray":
                                    Offsets.m_pBoneArray = 0x1F0  # Stable fallback
                                    print(f"[Cheat] Applied fallback for {offset_name}: 0x{Offsets.m_pBoneArray:X}")
                                    offset_found = True
                            else:
                                setattr(Offsets, offset_name, field_value)
                                offset_found = True
                    
                    # Tertiary search: try to find the field in related classes
                    if not offset_found and offset_name == "m_pBoneArray":
                        # Search in other potential classes for bone array
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
                
                # Apply fallbacks for any remaining missing critical offsets
                if not hasattr(Offsets, 'm_pBoneArray'):
                    Offsets.m_pBoneArray = 0x1F0  # Stable fallback
                    # Remove from missing list since we have a fallback
                    missing_offsets = [offset for offset in missing_offsets if not offset.startswith('m_pBoneArray')]
                
                # Apply fallback for observer target (needed for spectator list)
                if not hasattr(Offsets, 'm_hObserverTarget'):
                    Offsets.m_hObserverTarget = 0x44  # Common stable fallback
                    # Remove from missing list since we have a fallback
                    missing_offsets = [offset for offset in missing_offsets if not offset.startswith('m_hObserverTarget')]
                
                # Apply fallback for observer services (needed for spectator detection)
                if not hasattr(Offsets, 'm_pObserverServices'):
                    Offsets.m_pObserverServices = 0x11C0  # Common stable fallback
                    # Remove from missing list since we have a fallback
                    missing_offsets = [offset for offset in missing_offsets if not offset.startswith('m_pObserverServices')]
                
                # Apply fallback for controller handle (needed for player resolution)
                if not hasattr(Offsets, 'm_hController'):
                    Offsets.m_hController = 0x133C  # Common stable fallback
                    # Remove from missing list since we have a fallback
                    missing_offsets = [offset for offset in missing_offsets if not offset.startswith('m_hController')]
                
                
               
                
                # Show final missing offsets (after fallbacks)
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
        
        
        self.triggerbot = TriggerBot()
        self.aimbot = Aimbot()
        self.bomb_timer = BombTimer()
        
       
        self.check_gpu_acceleration()
        
        #
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
            pm = Utils.get_pyMeow()
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
                        
                yield Entity(controller_ptr, pawn_ptr, self.proc, self)
                
            except Exception as e:
                # Skip problematic entities instead of stopping iteration
                continue

    def get_local_pawn(self):
        
        try:
            local_pawn = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerPawn)
            
            if local_pawn and local_pawn > 0x1000:  # basic pointer validation
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
            
            # Get the entity index from the controller
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
            current_time - self._last_index_update > 2.0):  # Update every 2 seconds
            
            self._cached_local_index = self.get_local_player_index()
            self._last_index_update = current_time
            
          
    
    # Cache the local player index to avoid reading it every frame
    _cached_local_index = None
    _last_index_update = 0

    def run(self):
        
        if SecurityUtils.enable_debug_privileges():
            print("[Security] Debug privileges enabled")
        
        if SecurityUtils.hide_from_process_list():
            print("[Security] Process hidden from basic enumeration")
        else:
            print("")
        
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
        
        random_title = SecurityUtils.generate_random_title()
        try:
            SecurityUtils.set_overlay_title(random_title)
        except Exception as e:
            print(f"[Security] Warning: Could not set overlay title: {e}")
        
        frame_counter = 0
        title_change_interval = 5000
        
        # Add exception handling and frame timing
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        # Initialize local player index for visibility checks
        self.update_local_player_index()
        
        # Cache the local player index to avoid reading it every frame
        self._cached_local_index = None
        self._last_index_update = 0
        
        while pm.overlay_loop():
            current_frame_time = time.time()
            frame_start = current_frame_time
            
            try:
                # Update local player index periodically for accurate visibility checks
                self.update_local_player_index()
                
                # Run triggerbot if enabled
                if cfg.TRIGGERBOT.enabled:
                    try:
                        self.triggerbot.check_and_shoot(self.proc, self.mod)
                    except:
                        pass  # Silently ignore triggerbot errors
                
                # Run aimbot if enabled
                if cfg.AIMBOT.enabled:
                    try:
                        # Get local pawn for aimbot
                        local_pawn = self.get_local_pawn()
                        if local_pawn and view_matrix:
                            # We'll get entities later in the loop, for now just prepare
                            pass
                    except:
                        pass  # Silently ignore aimbot errors
                
                # Reduce title change frequency to prevent freezes
                frame_counter += 1
                if frame_counter % title_change_interval == 0:
                    try:
                        new_title = SecurityUtils.generate_random_title()
                        SecurityUtils.set_overlay_title(new_title)
                    except:
                        pass  # Don't let title changes freeze the ESP
                
                # Read fresh view matrix every frame - no caching
                try:
                    view_matrix = pm.r_floats(self.proc, self.mod + Offsets.dwViewMatrix, 16)
                    # Validate view matrix
                    if not view_matrix or len(view_matrix) != 16:
                        continue
                except Exception as e:
                    consecutive_errors += 1
                    if consecutive_errors > max_consecutive_errors:
                        print("[Cheat] Too many consecutive errors, restarting...")
                        break
                    continue

                pm.begin_drawing()
                
                # Use batched rendering if available for better performance
                if hasattr(self, 'use_batched_rendering') and self.use_batched_rendering:
                    try:
                        pm.begin_batch()
                    except:
                        pass
                
                pm.draw_fps(0, 0)
                
                # Get fresh local player data every frame - no caching
                try:
                    local_pos = self.get_local_player_pos()
                    local_team = self.get_local_player_team()
                    
                    # If we can't get valid local player data, we're probably in main menu
                    if not local_pos:
                        # Still draw the overlay but with a message
                        pm.draw_text("In Main Menu - Join a game to see ESP", 50, 50, 16, pm.get_color("#FFFF00"))
                        pm.end_drawing()
                        consecutive_errors = 0  # Reset errors since this isn't really an error
                        continue
                        
                except Exception as e:
                    pm.draw_text("Waiting for game data...", 50, 50, 16, pm.get_color("#FFA500"))
                    pm.end_drawing()
                    continue
                
                # Collect entities fresh every frame - no entity caching
                entities_to_render = []
                entity_count = 0
                max_entities_per_frame = 32  # Limit entities to prevent overload
                
                try:
                    # Create fresh entities every frame
                    for ent in self.it_entities():
                        if entity_count >= max_entities_per_frame:
                            break  # Prevent too many entities from causing freeze
                            
                        try:
                            # Validate entity before processing
                            if not ent or not ent.ptr or not ent.pawn_ptr:
                                continue
                                
                            # Check if entity has valid health (basic validation)
                            try:
                                health = ent.health
                                if not isinstance(health, int) or health <= 0 or health > 200:
                                    continue
                            except:
                                continue
                                
                            # Calculate fresh world-to-screen positions
                            if ent.wts(view_matrix) and ent.health > 0 and not ent.dormant:
                                # Skip if visible-only is enabled and entity is not spotted
                                if cfg.ESP.visible_only and not ent.spotted:
                                    continue
                                    
                                # Calculate fresh distance
                                distance = ent.get_distance(local_pos)
                                if distance and distance <= cfg.ESP.max_distance:
                                    if cfg.ESP.show_teammates or ent.team != local_team:
                                        entities_to_render.append((ent, distance))
                            entity_count += 1
                        except Exception as e:
                            # Skip problematic entities instead of crashing
                            continue
                            
                except Exception as e:
                    print(f"[Cheat] Error collecting entities: {e}")
                
                # Render entities with fresh data
                try:
                    if entities_to_render:
                        # Run aimbot with collected entities
                        if cfg.AIMBOT.enabled:
                            try:
                                local_pawn = self.get_local_pawn()
                                if local_pawn:
                                    self.aimbot.check_and_aim(entities_to_render, local_pos, local_team, self.proc, local_pawn, view_matrix)
                            except Exception as e:
                                # Only print aimbot errors occasionally
                                if not hasattr(self, '_last_aimbot_error_time') or current_frame_time - self._last_aimbot_error_time > 10:
                                    print(f"[Aimbot] Error: {e}")
                                    self._last_aimbot_error_time = current_frame_time
                        
                        self.render_entities_optimized(entities_to_render, view_matrix, local_pos, local_team)
                    else:
                        # Show helpful message when no entities are found
                        pm.draw_text("No players detected", 50, 80, 14, pm.get_color("#808080"))
                        
                except Exception as e:
                    print(f"[Cheat] Error rendering entities: {e}")
                
                # Draw aimbot FOV circle if enabled
                try:
                    if cfg.AIMBOT.enabled and cfg.AIMBOT.show_fov_circle:
                        self.aimbot.draw_fov_circle()
                except Exception as e:
                    pass  # Silently ignore FOV circle errors
                
                # Draw bomb timer if enabled and not stream-proofing
                if not cfg.MISC.stream_proof:
                    try:
                        bomb_info = self.bomb_timer.get_bomb_info(self.proc, self.mod)
                        self.bomb_timer.draw_bomb_timer(bomb_info)
                    except Exception as e:
                        print(f"[BombTimer] Error: {e}")  # Show the actual error
                
                # End batched rendering
                if hasattr(self, 'use_batched_rendering') and self.use_batched_rendering:
                    try:
                        pm.end_batch()
                    except:
                        pass
                
                pm.end_drawing()
                
                # Reset error counter on successful frame
                consecutive_errors = 0
                
                # Track frame timing but don't cache results
                frame_end = time.time()
                frame_duration = frame_end - frame_start
                
                # Only keep minimal frame timing for freeze detection
                if frame_duration > 0.1:  # Frame took longer than 100ms
                
                
                # Periodically change the window title
                 if frame_counter >= title_change_interval:
                    frame_counter = 0
                    
            except Exception as e:
                print(f"[Cheat] Critical error in main loop: {e}")
                consecutive_errors += 1
                if consecutive_errors > max_consecutive_errors:
                    print("[Cheat] Too many errors, exiting...")
                    break
                    
                # Try to recover by continuing
                try:
                    pm.end_drawing()
                except:
                    pass
                continue

    def optimize_overlay_rendering(self):
        """Apply rendering optimizations after overlay initialization"""
        try:
            # Try various optimization methods
            optimization_methods = [
                ('set_blend_mode', 'alpha'),
                ('enable_antialiasing', False),  # Disable for performance
                ('set_line_smoothing', False),   # Disable for performance
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
            
            # Check if we can use batched rendering
            if hasattr(pm, 'begin_batch') and hasattr(pm, 'end_batch'):
                print("[Cheat] Batched rendering available - will use for better performance")
                self.use_batched_rendering = True
            else:
                self.use_batched_rendering = False
                
        except Exception as e:
            print(f"[Cheat] Error applying rendering optimizations: {e}")

    def render_entities_optimized(self, entities_to_render, view_matrix, local_pos, local_team):
        """Optimized rendering with no caching - fresh data every frame"""
        try:
            # Batch 1: Lines (lowest overhead) - fresh data
            if cfg.ESP.show_line and entities_to_render:
                try:
                    # Get fresh color config
                    line_color = Render.get_color_from_config(cfg.ESP.line_color)
                    screen_width = pm.get_screen_width()
                    screen_height = pm.get_screen_height()
                    
                    if cfg.ESP.line_position == "Top":
                        start_x, start_y = screen_width / 2, 0
                    elif cfg.ESP.line_position == "Bottom":
                        start_x, start_y = screen_width / 2, screen_height
                    else:  # Center
                        start_x, start_y = screen_width / 2, screen_height / 2
                    
                    for ent, distance in entities_to_render[:16]:  # Limit to 16 lines per frame
                        try:
                            # Use fresh head position
                            end_x = ent.head_pos2d["x"]
                            end_y = ent.head_pos2d["y"]
                            pm.draw_line(start_x, start_y, end_x, end_y, line_color, 1.0)
                        except:
                            continue
                except Exception as e:
                    print(f"[Render] Error drawing lines: {e}")
            
            # Batch 2: Boxes - fresh calculations
            try:
                for ent, distance in entities_to_render:
                    try:
                        color = Colors.cyan if ent.team != 2 else Colors.orange
                        Render.draw_box(ent, distance, color)
                    except:
                        continue
            except Exception as e:
                print(f"[Render] Error drawing boxes: {e}")
            
            # Batch 3: Skeleton (fresh bone data)
            try:
                skeleton_count = 0
                for ent, distance in entities_to_render:
                    if skeleton_count >= 8:  # Limit skeleton rendering
                        break
                    if distance < 30:  # Only render skeleton for closer entities
                        try:
                            # Fresh skeleton calculation
                            Render.draw_skeleton(ent, view_matrix, distance)
                            skeleton_count += 1
                        except:
                            continue
            except Exception as e:
                print(f"[Render] Error drawing skeletons: {e}")
            
            # Batch 4: Head circles (fresh positions)
            try:
                circle_count = 0
                for ent, distance in entities_to_render:
                    if circle_count >= 4:  # Very limited head circles
                        break
                    if distance < 20:  # Only render head circles for very close entities
                        try:
                            # Fresh head circle calculation
                            Render.draw_head_circle(ent, view_matrix, local_pos, distance)
                            circle_count += 1
                        except:
                            continue
            except Exception as e:
                print(f"[Render] Error drawing head circles: {e}")
            
            # Batch 5: Health bars and text (fresh data)
            try:
                text_count = 0
                for ent, distance in entities_to_render:
                    if text_count >= 12:  # Limit text rendering
                        break
                    try:
                        # Fresh box calculation
                        box_coords = Render.calculate_accurate_box(ent, distance)
                        if box_coords and all(coord is not None for coord in box_coords):
                            box_x, box_y, box_width, box_height = box_coords
                            
                            # Health bar
                            health_bar_x = box_x + box_width + 3
                            health_bar_y = box_y - 5
                            health_bar_width = max(3, 6 - distance // 10)
                            health_bar_height = box_height + 10
                            
                            # Fresh health data
                            Render.draw_health(100, ent.health, health_bar_x, health_bar_y, health_bar_width, health_bar_height)
                            
                            # Fresh text data
                            info_texts = []
                            if cfg.ESP.show_name and distance < 25:  # Fresh name
                                info_texts.append(ent.name)
                            if cfg.ESP.show_distance:
                                info_texts.append(f"{distance}m")
                            if cfg.ESP.show_weapon and distance < 20:  # Fresh weapon
                                weapon_name = ent.get_weapon_name()
                                if weapon_name and weapon_name != "Unknown":
                                    info_texts.append(weapon_name)
                            
                            # Limit text items per entity
                            info_texts = info_texts[:2]  # Max 2 text items per entity
                            
                            font_size = 12 if distance < 20 else 10
                            line_spacing = font_size + 4
                            total_height = len(info_texts) * line_spacing
                            text_start_y = box_y - total_height - 6
                            
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
        1: "deagle", 
        2: "elite", 
        3: "fiveseven", 
        4: "glock", 
        7: "ak47", 
        8: "aug", 
        9: "awp", 
        10: "famas", 
        11: "g3Sg1", 
        13: "galilar", 
        14: "m249", 
        16: "m4a1", 
        17: "mac10", 
        19: "p90", 
        23: "mp5sd", 
        24: "ump45", 
        25: "xm1014", 
        26: "bizon", 
        27: "mag7", 
        28: "negev", 
        29: "sawedoff", 
        30: "tec9", 
        31: "zeus", 
        32: "p2000", 
        33: "mp7", 
        34: "mp9", 
        35: "nova", 
        36: "p250", 
        38: "scar20", 
        39: "sg556", 
        40: "ssg08", 
        42: "ct_knife", 
        43: "flashbang", 
        44: "hegrenade", 
        45: "smokegrenade", 
        46: "molotov", 
        47: "decoy", 
        48: "incgrenade", 
        49: "c4", 
        59: "t_knife",
        60: "m4a1_silencer", 
        61: "usp", 
        63: "cz75a", 
        64: "revolver"
    }

class Aimbot:
    def __init__(self):
        self.mouse = Controller()
        self.last_aim_time = 0
        self.last_target = None
        self.aim_start_time = 0
        self.target_locked = False
        
    def get_screen_center(self):
        """Get the center of the screen for FOV calculations"""
        import ctypes
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return {"x": screen_width / 2, "y": screen_height / 2}
    
    def calculate_distance_2d(self, pos1, pos2):
        """Calculate 2D distance between two points"""
        try:
            dx = pos1["x"] - pos2["x"]
            dy = pos1["y"] - pos2["y"]
            return math.sqrt(dx * dx + dy * dy)
        except:
            return float('inf')
    
    def calculate_fov(self, target_pos, screen_center):
        """Calculate field of view angle to target"""
        try:
            distance = self.calculate_distance_2d(target_pos, screen_center)
            # Convert distance to FOV angle (simplified)
            fov_angle = math.degrees(math.atan2(distance, 1000))  # Arbitrary distance normalization
            return fov_angle
        except:
            return float('inf')
    
    def is_within_fov(self, target_pos, screen_center, fov_radius):
        """Check if target is within FOV circle"""
        try:
            distance = self.calculate_distance_2d(target_pos, screen_center)
            return distance <= fov_radius
        except:
            return False
    
    def get_target_bone_pos(self, entity, bone_id):
        """Get the 2D screen position of a specific bone"""
        try:
            # Get bone position in 3D world coordinates
            bone_pos_3d = entity.bone_pos(bone_id)
            if not bone_pos_3d:
                return None
                
            # Return the 3D position - screen conversion will be done later with view matrix
            return bone_pos_3d
        except:
            return None
    
    def calculate_dynamic_fov(self, distance):
        """Calculate dynamic FOV based on distance"""
        if not cfg.AIMBOT.dynamic_fov:
            return cfg.AIMBOT.aim_fov
            
        # Closer targets get smaller FOV, farther targets get larger FOV
        if distance <= 10:
            return cfg.AIMBOT.min_fov
        elif distance >= 50:
            return cfg.AIMBOT.max_fov
        else:
            # Linear interpolation between min and max FOV
            ratio = (distance - 10) / 40  # 40 = 50 - 10
            return cfg.AIMBOT.min_fov + (cfg.AIMBOT.max_fov - cfg.AIMBOT.min_fov) * ratio
    
   
    
    def smooth_mouse_movement(self, target_x, target_y, smoothness):
        """Apply smooth mouse movement"""
        try:
            screen_center = self.get_screen_center()
            
            # Calculate offset from center to target
            offset_x = target_x - screen_center["x"]
            offset_y = target_y - screen_center["y"]
            
            # Apply smoothness - divide by smoothness factor
            smooth_x = offset_x / smoothness
            smooth_y = offset_y / smoothness
            
            # Apply mouse movement
            if cfg.AIMBOT.flick_mode:
                # Instant movement - move directly to target
                self.move_mouse(offset_x, offset_y)
            else:
                # Smooth movement - move a fraction toward target
                self.move_mouse(smooth_x, smooth_y)
                
            return True
        except Exception as e:
            return False
    
    def move_mouse(self, offset_x, offset_y):
        """Move mouse by offset using Windows API"""
        try:
            import ctypes
            user32 = ctypes.windll.user32
            
        
            
            # Use relative mouse movement
            user32.mouse_event(0x0001, int(offset_x), int(offset_y), 0, 0)  # MOUSEEVENTF_MOVE
            return True
        except Exception as e:
            return False

    def find_best_target(self, entities, local_pos, local_team, view_matrix):
        """Find the best target based on configuration"""
        if not entities:
            return None
            
        screen_center = self.get_screen_center()
        best_target = None
        best_score = float('inf')
        
        # Debug counters
        total_entities = len(entities)
        filtered_count = {
            'teammates': 0,
            'too_far': 0,
            'no_health': 0,
            'dormant': 0,
            'not_visible': 0,
            'no_bone_pos': 0,
            'no_screen_pos': 0,
            'out_of_fov': 0,
            'valid_targets': 0
        }
        
        for entity, distance in entities:
            try:
                # Skip if targeting teammates is disabled
                if not cfg.AIMBOT.target_teammates and entity.team == local_team:
                    filtered_count['teammates'] += 1
                    continue
                    
                # Skip if entity is too far
                if distance > cfg.AIMBOT.max_distance:
                    filtered_count['too_far'] += 1
                    continue
                    
                # Skip if entity has no health
                if entity.health <= 0:
                    filtered_count['no_health'] += 1
                    continue
                    
                # Skip if entity is dormant
                if entity.dormant:
                    filtered_count['dormant'] += 1
                    continue
                
                # Skip if not visible and visible check is enabled
                if cfg.AIMBOT.visible_check and not entity.spotted:
                    filtered_count['not_visible'] += 1
                    continue
                
                # Get target bone position
                target_bone_pos = entity.bone_pos(cfg.AIMBOT.target_bone)
                if not target_bone_pos:
                    filtered_count['no_bone_pos'] += 1
                    continue
                    
                # Convert to screen coordinates
                target_screen_pos = pm.world_to_screen(view_matrix, target_bone_pos, 1)
                if not target_screen_pos:
                    filtered_count['no_screen_pos'] += 1
                    continue
                
                # Calculate FOV for this target
                current_fov = self.calculate_dynamic_fov(distance)
                fov_distance = self.calculate_distance_2d(target_screen_pos, screen_center)
                
                # Check if within FOV
                if not self.is_within_fov(target_screen_pos, screen_center, current_fov):
                    filtered_count['out_of_fov'] += 1
                    continue
                
                # This is a valid target
                filtered_count['valid_targets'] += 1
                
                # Calculate score based on preference
                if cfg.AIMBOT.prefer_closest:
                    score = distance  # Lower distance = better score
                else:
                    score = fov_distance  # Lower FOV distance = better score
                
                # Prefer head if enabled
                if cfg.AIMBOT.prefer_head and cfg.AIMBOT.target_bone != 6:  # 6 = head bone
                    # Check if head is visible and within FOV
                    head_pos = entity.bone_pos(6)
                    if head_pos:
                        head_screen_pos = pm.world_to_screen(view_matrix, head_pos, 1)
                        if head_screen_pos and self.is_within_fov(head_screen_pos, screen_center, current_fov):
                            # Prioritize head target
                            score *= 0.7  # Make head targets more attractive

                if score < best_score:
                    best_score = score
                    best_target = {
                        'entity': entity,
                        'distance': distance,
                        'screen_pos': target_screen_pos,
                        'bone_pos': target_bone_pos,
                        'fov_distance': fov_distance
                    }
                    
            except Exception as e:
                continue
        
       
        
        return best_target
    
    def aim_at_target(self, target_info, process, local_pawn):
        """Aim at the specified target"""
        try:
            current_time = time.time()
            
            # Lock onto target immediately (no reaction delay)
            if self.last_target != target_info['entity'] or not self.target_locked:
                self.target_locked = True
                self.last_target = target_info['entity']
                
            
            # Get target screen position
            target_screen_pos = target_info['screen_pos']
            
            
            
            
            
            # Calculate smoothness based on configuration
            smoothness = cfg.AIMBOT.smoothness
            if cfg.AIMBOT.flick_mode:
                smoothness = cfg.AIMBOT.flick_smoothness
                
           
            
            
            adjusted_x = target_screen_pos["x"] 
            adjusted_y = target_screen_pos["y"] 
            
           
            
            # Apply smooth mouse movement
            success = self.smooth_mouse_movement(adjusted_x, adjusted_y, smoothness)
            
            # Auto shoot if enabled and target is close to crosshair
            if cfg.AIMBOT.auto_shoot and success:
                screen_center = self.get_screen_center()
                distance_to_center = self.calculate_distance_2d(
                    {"x": adjusted_x, "y": adjusted_y}, 
                    screen_center
                )
                
                # Shoot if very close to center (within a small threshold)
                if distance_to_center <= 5:  # 5 pixel threshold
                    self.auto_shoot()
            
            return success
            
        except Exception as e:
            return False
    
    def auto_shoot(self):
        """Automatically shoot when target is acquired"""
        try:
            # Simple click
            self.mouse.click(Button.left)
            return True
        except:
            return False
    
    def check_and_aim(self, entities, local_pos, local_team, process, local_pawn, view_matrix):
        """Main aimbot logic - check for targets and aim"""
        current_time = time.time()
        
        try:
            # Check if aimbot is enabled
            if not cfg.AIMBOT.enabled:
                self.target_locked = False
                return False
            
            # Check if aim key is pressed
            aim_key_pressed = False
            try:
                if cfg.AIMBOT.aim_key.lower() == "right_click":
                    # Check right mouse button using win32api
                    if win32api:
                        aim_key_pressed = win32api.GetKeyState(0x02) < 0  # VK_RBUTTON
                    else:
                        # Fallback to checking with pynput (less reliable for real-time detection)
                        aim_key_pressed = False
                elif cfg.AIMBOT.aim_key.lower() == "left_click":
                    # Check left mouse button
                    if win32api:
                        aim_key_pressed = win32api.GetKeyState(0x01) < 0  # VK_LBUTTON
                    else:
                        aim_key_pressed = False
                else:
                    # Use keyboard library for other keys
                    aim_key_pressed = keyboard.is_pressed(cfg.AIMBOT.aim_key)
                    
            except Exception as e:
                aim_key_pressed = False
                
           
                
            if not aim_key_pressed:
                self.target_locked = False
                self.last_target = None
                return False

            # Check if we're in CS2 window
            from win32gui import GetWindowText, GetForegroundWindow
            current_window = GetWindowText(GetForegroundWindow())
            
            # Check for various CS2 window titles (more flexible)
            cs2_window_keywords = [
                "counter-strike",
                "counter strike", 
                "cs2",
                "cs:2",
                "csgo"  # Sometimes shows as CSGO
            ]
            
            # Check if any CS2 keyword is in the current window title (case insensitive)
            in_cs2_window = any(keyword in current_window.lower() for keyword in cs2_window_keywords)
            
            if not in_cs2_window:
                # Only show debug message occasionally
                if not hasattr(self, '_debug_window_time') or current_time - self._debug_window_time > 5:
                    self._debug_window_time = current_time
                return False
            
            # If we reach here, we're in CS2 - show confirmation once
            if not hasattr(self, '_cs2_window_confirmed'):
                self._cs2_window_confirmed = True
                
          
                
            # Find best target
            target = self.find_best_target(entities, local_pos, local_team, view_matrix)
            if not target:
                # Debug: Print why no target found occasionally
                if not hasattr(self, '_debug_no_target_time') or current_time - self._debug_no_target_time > 5:
                    
                    self._debug_no_target_time = current_time
                self.target_locked = False
                self.last_target = None
                return False

           

            # Aim at target
            result = self.aim_at_target(target, process, local_pawn)
            
        
                    
            return result
            
        except Exception as e:
            self.target_locked = False
            return False
    
    def draw_fov_circle(self):
        """Draw FOV circle on screen"""
        if not cfg.AIMBOT.show_fov_circle or not cfg.AIMBOT.enabled:
            return
            
        try:
            screen_center = self.get_screen_center()
            fov_radius = cfg.AIMBOT.aim_fov
            
            # Draw circle
            circle_color = pm.get_color("#00AAFF")  # Light blue
            circle_segments = 64
            
            # Calculate circle points
            points = []
            for i in range(circle_segments):
                angle = (i * 2 * math.pi) / circle_segments
                x = screen_center["x"] + fov_radius * math.cos(angle)
                y = screen_center["y"] + fov_radius * math.sin(angle)
                points.append((x, y))
            
            # Draw circle segments
            for i in range(circle_segments):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % circle_segments]
                pm.draw_line(x1, y1, x2, y2, circle_color, 1.5)
                
        except Exception as e:
            pass

class BombTimer:
    def __init__(self):
        self.last_update = 0
        self.bomb_planted = False
        self.bomb_plant_time = None
        self.bomb_timer_length = 40.0  # Default CS2 bomb timer (40 seconds)
        self.cached_bomb_info = {
            'is_planted': False,
            'time_remaining': 0.0,
            'bomb_position': {'x': 0, 'y': 0, 'z': 0},
            'is_being_defused': False,
            'defuse_time_remaining': 0.0,
            'bomb_defused': False,
            'bomb_ticking': False
        }
    
    def get_bomb_info(self, process, module):
        """Get current bomb information using GameRules with enhanced error handling"""
        current_time = time.time()
        
        # Update more frequently for real-time countdown (every 50ms)
        if current_time - self.last_update < 0.05:
            # Still update time_remaining for countdown even when cached
            if self.cached_bomb_info['is_planted'] and self.bomb_plant_time:
                elapsed_time = current_time - self.bomb_plant_time
                remaining_time = max(0.0, self.bomb_timer_length - elapsed_time)
                self.cached_bomb_info['time_remaining'] = remaining_time
            return self.cached_bomb_info
        
        self.last_update = current_time
        bomb_info = {
            'is_planted': False,
            'time_remaining': 0.0,
            'bomb_position': {'x': 0, 'y': 0, 'z': 0},
            'is_being_defused': False,
            'defuse_time_remaining': 0.0,
            'bomb_defused': False,
            'bomb_ticking': False
        }
        
        try:
            # Check if we have the required offsets
            if not hasattr(Offsets, 'dwGameRules') or Offsets.dwGameRules == 0:
                print("[BombTimer] Warning: dwGameRules offset not available")
                self.cached_bomb_info = bomb_info
                return bomb_info
                
            if not hasattr(Offsets, 'm_bBombPlanted') or Offsets.m_bBombPlanted == 0:
                print("[BombTimer] Warning: m_bBombPlanted offset not available")
                self.cached_bomb_info = bomb_info
                return bomb_info
            
            # Read GameRules pointer
            try:
                game_rules = pm.r_int64(process, module + Offsets.dwGameRules)
            except Exception as read_error:
                # Silently handle read errors
                self.cached_bomb_info = bomb_info
                return bomb_info
            
            # Validate the GameRules pointer
            if not game_rules or game_rules < 0x10000 or game_rules > 0x7FFFFFFFFFFF:
                self.cached_bomb_info = bomb_info
                return bomb_info
            
            # Read bomb planted status from GameRules
            try:
                current_bomb_planted = pm.r_bool(process, game_rules + Offsets.m_bBombPlanted)
                bomb_info['is_planted'] = current_bomb_planted
                
                # Detect when bomb is newly planted
                if current_bomb_planted and not self.bomb_planted:
                    self.bomb_plant_time = current_time
                    self.bomb_planted = True
                    print(f"[BombTimer] Bomb planted at {current_time:.3f}! Starting countdown...")
                elif not current_bomb_planted and self.bomb_planted:
                    # Bomb was defused or exploded
                    self.bomb_planted = False
                    self.bomb_plant_time = None
                    print("[BombTimer] Bomb is no longer active")
                
                self.bomb_planted = current_bomb_planted
                    
            except Exception as e:
                # Failed to read bomb planted status
                self.cached_bomb_info = bomb_info
                return bomb_info
            
            # If bomb is not planted, return early
            if not self.bomb_planted:
                self.bomb_plant_time = None
                self.cached_bomb_info = bomb_info
                return bomb_info
            
            # Calculate time remaining based on plant time
            if self.bomb_plant_time:
                elapsed_time = current_time - self.bomb_plant_time
                remaining_time = max(0.0, self.bomb_timer_length - elapsed_time)
                bomb_info['time_remaining'] = remaining_time
                bomb_info['bomb_ticking'] = remaining_time > 0
            else:
                # Fallback if we don't have plant time
                bomb_info['time_remaining'] = 35.0
                bomb_info['bomb_ticking'] = True
            
            # Try to get additional information from planted C4 entity
            try:
                # Try to get planted C4 entity for additional info
                if hasattr(Offsets, 'dwPlantedC4') and Offsets.dwPlantedC4 != 0:
                    planted_c4_address = pm.r_int64(process, module + Offsets.dwPlantedC4)
                    
                    if planted_c4_address and planted_c4_address > 0x10000:
                        bomb_entity = planted_c4_address
                        
                        # Try to get precise timer information from game
                        if hasattr(Offsets, 'm_flC4Blow') and hasattr(Offsets, 'm_flTimerLength'):
                            try:
                                # Read the actual blow time and timer length from the bomb entity
                                blow_time = pm.r_float(process, bomb_entity + Offsets.m_flC4Blow)
                                timer_length = pm.r_float(process, bomb_entity + Offsets.m_flTimerLength)
                                
                                if blow_time > 0 and timer_length > 0:
                                    # Use the game's timer if available
                                    game_time = current_time  # This might need adjustment for game time
                                    remaining = blow_time - game_time
                                    if 0 <= remaining <= 50:  # Sanity check
                                        bomb_info['time_remaining'] = remaining
                                        self.bomb_timer_length = timer_length
                                        
                            except Exception as e:
                                # Fall back to our calculated time
                                pass
                        
                        # Try to get bomb position
                        if hasattr(Offsets, 'm_vOldOrigin'):
                            try:
                                bomb_pos = pm.r_vec3(process, bomb_entity + Offsets.m_vOldOrigin)
                                if bomb_pos and all(isinstance(bomb_pos.get(k), (int, float)) for k in ['x', 'y', 'z']):
                                    bomb_info['bomb_position'] = bomb_pos
                            except:
                                pass
                        
                        # Check if being defused
                        if hasattr(Offsets, 'm_bBeingDefused'):
                            try:
                                is_defusing = pm.r_bool(process, bomb_entity + Offsets.m_bBeingDefused)
                                bomb_info['is_being_defused'] = is_defusing
                                
                                if is_defusing and hasattr(Offsets, 'm_flDefuseCountDown'):
                                    try:
                                        defuse_time = pm.r_float(process, bomb_entity + Offsets.m_flDefuseCountDown)
                                        if defuse_time > 0 and defuse_time <= 10:
                                            bomb_info['defuse_time_remaining'] = defuse_time
                                        else:
                                            bomb_info['defuse_time_remaining'] = 5.0
                                    except:
                                        bomb_info['defuse_time_remaining'] = 5.0
                            except:
                                pass
                        
                        # Check bomb ticking status
                        if hasattr(Offsets, 'm_bBombTicking'):
                            try:
                                bomb_info['bomb_ticking'] = pm.r_bool(process, bomb_entity + Offsets.m_bBombTicking)
                            except:
                                bomb_info['bomb_ticking'] = bomb_info['time_remaining'] > 0
                        
                        # Check if bomb is defused
                        if hasattr(Offsets, 'm_bBombDefused'):
                            try:
                                bomb_defused = pm.r_bool(process, bomb_entity + Offsets.m_bBombDefused)
                                bomb_info['bomb_defused'] = bomb_defused
                                if bomb_defused:
                                    bomb_info['is_planted'] = False
                                    self.bomb_planted = False
                                    self.bomb_plant_time = None
                            except:
                                pass
                                
            except Exception as e:
                # Error getting additional info, but we still have basic timer
                pass
                
        except Exception as e:
            # Only log errors occasionally to avoid spam
            if not hasattr(self, '_last_error_time') or current_time - self._last_error_time > 5.0:
                print(f"[BombTimer] Warning: Could not read bomb info: {e}")
                self._last_error_time = current_time
            bomb_info['is_planted'] = False
        
        self.cached_bomb_info = bomb_info
        return bomb_info
    
    def check_bomb_planted_loop(self, process, module, max_iterations=40):
        """
        Continuously check bomb planted status in a loop
        Similar to the C# implementation you described
        """
        if not hasattr(Offsets, 'dwGameRules') or Offsets.dwGameRules == 0:
            return False
            
        if not hasattr(Offsets, 'm_bBombPlanted') or Offsets.m_bBombPlanted == 0:
            return False
        
        try:
            # Read GameRules pointer
            game_rules = pm.r_int64(process, module + Offsets.dwGameRules)
            if not game_rules or game_rules < 0x10000:
                return False
            
            # Initial bomb planted check
            bomb_planted = pm.r_bool(process, game_rules + Offsets.m_bBombPlanted)
            
            if bomb_planted:
                # Loop to continuously check bomb status
                for i in range(max_iterations):
                    try:
                        bomb_planted = pm.r_bool(process, game_rules + Offsets.m_bBombPlanted)
                        if not bomb_planted:
                            # Bomb was defused or exploded
                            print(f"[BombTimer] Bomb status changed to not planted at iteration {i}")
                            break
                        
                        # Small delay to prevent excessive CPU usage
                        time.sleep(0.1)
                        
                    except Exception as e:
                        print(f"[BombTimer] Error in bomb check loop at iteration {i}: {e}")
                        break
                        
                return bomb_planted
            else:
                return False
                
        except Exception as e:
            print(f"[BombTimer] Error in bomb planted loop check: {e}")
            return False

    def _scan_for_bomb_entity(self, process, module, bomb_info):
        """Fallback method to scan for bomb entity if dwPlantedC4 is not available"""
        try:
            # This is a simplified fallback - would need entity iteration to find C4
            # For now, return empty bomb info
            print("[BombTimer] Warning: dwPlantedC4 offset not available, bomb timer disabled")
            return bomb_info
        except Exception as e:
            print(f"[BombTimer] Error in fallback bomb scan: {e}")
            return bomb_info
    
    def draw_bomb_timer(self, bomb_info):
        """Draw bomb timer on screen with enhanced status information and error handling"""
        # Don't show anything if bomb timer is disabled
        if not cfg.MISC.show_bomb_timer:
            return
            
        # Show bomb defused message briefly
        if bomb_info.get('bomb_defused', False):
            try:
                import ctypes
                user32 = ctypes.windll.user32
                screen_width = user32.GetSystemMetrics(0)
                timer_x = screen_width - 270
                timer_y = 50
                pm.draw_text("BOMB DEFUSED", timer_x, timer_y, 24, pm.get_color("#00FF00"))
            except:
                pass
            return
            
        # Only show timer if bomb is actually planted
        if not bomb_info['is_planted']:
            return
        
        try:
            # Get screen dimensions for positioning
            import ctypes
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            
            # Timer position - right side of screen
            timer_x = screen_width - 280  # 280 pixels from right edge
            timer_y = 50
            
            time_remaining = bomb_info['time_remaining']
            
            # Show bomb status
            if bomb_info.get('bomb_defused', False):
                pm.draw_text("BOMB DEFUSED", timer_x, timer_y, 24, pm.get_color("#00FF00"))
                return
            elif not bomb_info.get('bomb_ticking', True):
                pm.draw_text("BOMB NOT TICKING", timer_x, timer_y, 22, pm.get_color("#FFFF00"))
                return
            
            # Show countdown even if time validation fails (for debugging)
            if time_remaining <= 0:
                pm.draw_text("BOMB EXPLODED", timer_x, timer_y, 24, pm.get_color("#FF0000"))
                return
            elif time_remaining > 50:
                # Show generic bomb planted with the time we have
                pm.draw_text(f"BOMB: {time_remaining:.1f}s", timer_x, timer_y, 22, pm.get_color("#FFA500"))
                pm.draw_text("(Timer may be inaccurate)", timer_x, timer_y + 25, 14, pm.get_color("#CCCCCC"))
            else:
                # Choose color based on time remaining
                if time_remaining < 10.0:
                    # Flash red when less than 10 seconds
                    import math
                    import time
                    flash_factor = abs(math.sin(time.time() * 8)) * 0.4 + 0.6  # More subtle flashing
                    red_value = int(255 * flash_factor)
                    timer_color = pm.get_color(f"#{red_value:02X}0000")
                    font_size = 26  # Larger for urgency
                elif time_remaining < 20.0:
                    timer_color = pm.get_color("#FF8800")  # Orange
                    font_size = 24
                else:
                    timer_color = pm.get_color("#00FF00")  # Green
                    font_size = 22
                
                # Draw bomb timer text with larger, more visible font
                timer_text = f"BOMB: {time_remaining:.1f}s"
                pm.draw_text(timer_text, timer_x, timer_y, font_size, timer_color)
                
                # Draw progress bar
                progress = min(time_remaining / 40.0, 1.0)  # 40 seconds default
                bar_width = 220
                bar_height = 20
                bar_x = timer_x
                bar_y = timer_y + 30
                
                # Background
                pm.draw_rectangle(bar_x, bar_y, bar_width, bar_height, pm.get_color("#404040"))
                
                # Progress fill - color changes based on time
                fill_width = bar_width * progress
                if time_remaining < 10.0:
                    fill_color = pm.get_color("#FF4444")  # Red
                elif time_remaining < 20.0:
                    fill_color = pm.get_color("#FF8800")  # Orange
                else:
                    fill_color = pm.get_color("#44FF44")  # Green
                    
                pm.draw_rectangle(bar_x, bar_y, fill_width, bar_height, fill_color)
                
                # Border
                pm.draw_rectangle_lines(bar_x, bar_y, bar_width, bar_height, pm.get_color("#FFFFFF"), 2)
                
                # Time text on the bar
                bar_text = f"{time_remaining:.1f}"
                text_x = bar_x + bar_width // 2 - 20  # Center the text
                pm.draw_text(bar_text, text_x, bar_y + 2, 16, pm.get_color("#FFFFFF"))
            
            # Defuse info
            if bomb_info['is_being_defused']:
                defuse_time = bomb_info.get('defuse_time_remaining', 5.0)
                defuse_text = f"DEFUSING: {defuse_time:.1f}s"
                pm.draw_text(defuse_text, timer_x, timer_y + 55, 18, pm.get_color("#00FFFF"))
                
                # Defuse progress bar
                defuse_progress = max(0.0, min(defuse_time / 10.0, 1.0))
                defuse_fill_width = bar_width * (1.0 - defuse_progress)
                pm.draw_rectangle(timer_x, timer_y + 75, defuse_fill_width, 12, pm.get_color("#00FFAA"))
                pm.draw_rectangle_lines(timer_x, timer_y + 75, bar_width, 12, pm.get_color("#FFFFFF"), 1)
                
        except Exception as e:
            # Show error for debugging
            try:
                import ctypes
                user32 = ctypes.windll.user32
                screen_width = user32.GetSystemMetrics(0)
                timer_x = screen_width - 270
                pm.draw_text(f"Timer Error: {str(e)[:30]}", timer_x, 50, 16, pm.get_color("#FF0000"))
            except:
                pass

    def simple_bomb_check(self, process, module):
        """
        Simple bomb check implementation as per user's request
        Returns True if bomb is planted, False otherwise
        """
        try:
            # Check if we have the required offsets
            if not hasattr(Offsets, 'dwGameRules') or not hasattr(Offsets, 'm_bBombPlanted'):
                return False
            
            # Read GameRules pointer
            game_rules = pm.r_int64(process, module + Offsets.dwGameRules)
            if not game_rules or game_rules < 0x1000:
                return False
            
            # Read bomb planted status
            bomb_planted = pm.r_bool(process, game_rules + Offsets.m_bBombPlanted)
            
            # If bomb is planted, you can optionally run the monitoring loop
            if bomb_planted:
                print("[BombTimer] Bomb is planted!")
                # Optionally call the loop check method
                # self.check_bomb_planted_loop(process, module)
            
            return bomb_planted
            
        except Exception as e:
            print(f"[BombTimer] Error in simple bomb check: {e}")
            return False

# SpectatorList class removed as requested
