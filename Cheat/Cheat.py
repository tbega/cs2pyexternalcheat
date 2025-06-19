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
    m_pBoneArray = 496


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
            if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
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

    def __init__(self, ptr, pawn_ptr, proc):
        self.ptr = ptr
        self.pawn_ptr = pawn_ptr
        self.proc = proc
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
            raise Exception(f"Could not find client.dll module in CS2 process: {e}")

        try:
            offsets_name = ["dwViewMatrix", "dwEntityList", "dwLocalPlayerController", "dwLocalPlayerPawn"]
            rq = Utils.get_requests()
            offsets = rq.get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json").json()
            [setattr(Offsets, k, offsets["client.dll"][k]) for k in offsets_name]
            
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

                "m_AttributeManager": "C_EconEntity",
                "m_Item": "C_AttributeContainer",
                "m_iItemDefinitionIndex": "C_EconItemView"
            }
            clientDll = rq.get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json").json()
            [setattr(Offsets, k, clientDll["client.dll"]["classes"][client_dll_name[k]]["fields"][k]) for k in client_dll_name]
            print("[Cheat] Offsets downloaded and applied successfully")
            
        except Exception as e:
            raise Exception(f"Failed to download or apply offsets: {e}")
        
        
        self.overlay_initialized = False
        
        
        self.triggerbot = TriggerBot()
        
       
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
                        
                yield Entity(controller_ptr, pawn_ptr, self.proc)
                
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
        
        while pm.overlay_loop():
            current_frame_time = time.time()
            frame_start = current_frame_time
            
            try:
                # Run triggerbot if enabled
                if cfg.TRIGGERBOT.enabled:
                    try:
                        self.triggerbot.check_and_shoot(self.proc, self.mod)
                    except:
                        pass  # Silently ignore triggerbot errors
                
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
                        self.render_entities_optimized(entities_to_render, view_matrix, local_pos, local_team)
                    else:
                        # Show helpful message when no entities are found
                        pm.draw_text("No players detected", 50, 80, 14, pm.get_color("#808080"))
                        
                except Exception as e:
                    print(f"[Cheat] Error rendering entities: {e}")
                
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
