import math
import ctypes
import random
import string
import os
import sys
import time
import psutil
import Utils
import Configs as cfg





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
        """Hide process from basic process enumeration"""
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
                    if (window.title == "" or 
                        "OpenGL" in window.title or 
                        "pygame" in window.title or
                        window.title.startswith("SDL") or
                        "pyMeow" in window.title.lower()):
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
                    
                    
                    if (window_title == "" or 
                        "OpenGL" in window_title or
                        "SDL" in class_name or
                        "pyMeow" in window_title.lower()):
                       
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


class Entity:

    def __init__(self, ptr, pawn_ptr, proc):
        self.ptr = ptr
        self.pawn_ptr = pawn_ptr
        self.proc = proc
        self.pos2d = None
        self.head_pos2d = None

    @property
    def name(self):
        return pm.r_string(self.proc, self.ptr + Offsets.m_iszPlayerName)

    @property
    def health(self):
        return pm.r_int(self.proc, self.pawn_ptr + Offsets.m_iHealth)

    @property
    def team(self):
        return pm.r_int(self.proc, self.pawn_ptr + Offsets.m_iTeamNum)

    @property
    def pos(self):
        return pm.r_vec3(self.proc, self.pawn_ptr + Offsets.m_vOldOrigin)
    
    @property
    def dormant(self):
        return pm.r_bool(self.proc, self.pawn_ptr + Offsets.m_bDormant)

    @property
    def weaponIndex(self):
        try:
            currentWeapon = pm.r_int64(self.proc, self.pawn_ptr + Offsets.m_pClippingWeapon)
            if currentWeapon == 0:
                return 0
            weaponIndex = pm.r_int(self.proc, currentWeapon + Offsets.m_AttributeManager + Offsets.m_Item + Offsets.m_iItemDefinitionIndex)
            return weaponIndex
        except:
            return 0
    
    def get_weapon_name(self):
        try:
            weapon_index = self.weaponIndex
            return weapon_names.get(weapon_index, "Unknown")
        except:
            return "Unknown"
        
    def get_distance(self, localPos):
        dx = self.pos["x"] - localPos["x"]
        dy = self.pos["y"] - localPos["y"]
        dz = self.pos["z"] - localPos["z"]
        return int(math.sqrt(dx * dx + dy * dy + dz * dz) / 100)

    def bone_pos(self, bone):
        game_scene = pm.r_int64(self.proc, self.pawn_ptr + Offsets.m_pGameSceneNode)
        bone_array_ptr = pm.r_int64(self.proc, game_scene + Offsets.m_pBoneArray)
        return pm.r_vec3(self.proc, bone_array_ptr + bone * 32)
    
    def wts(self, view_matrix):
        try:
            self.pos2d = pm.world_to_screen(view_matrix, self.pos, 1)
            self.head_pos2d = pm.world_to_screen(view_matrix, self.bone_pos(6), 1)
        except:
            return False
        return True

class Render:
    @staticmethod
    def get_color_from_config(color_name):
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
        hex_color = color_map.get(color_name, "#FFFFFF")  # Default to white if not found
        return pm.get_color(hex_color)

    @staticmethod
    def draw_health(max, current, PosX, PosY, width, height):
        if cfg.ESP.show_health:
            Proportion = current / max
            Height = height * Proportion
            offsetY = height * (max - current) / max
            
            health_percentage = current / max
            if health_percentage > 0.7:
                health_color = pm.get_color("#00FF00")  # Green for high health
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
    def draw_box(PosX, PosY, width, height, filled_color):
        if not cfg.ESP.show_box:
            return
            
        box_color = Render.get_color_from_config(cfg.ESP.box_color)
        
        # Handle different box styles
        if cfg.ESP.box_style == "Filled":
            pm.draw_rectangle(PosX, PosY, width, height, filled_color)
            pm.draw_rectangle_lines(PosX + 1, PosY + 1, width, height, Colors.black, 1.2)   # Shadow
            pm.draw_rectangle_lines(PosX, PosY, width, height, box_color, 1.2)
        elif cfg.ESP.box_style == "Cornered":
            Render.draw_cornered_box_internal(PosX, PosY, width, height, filled_color, box_color)
        else:  # Regular box
            pm.draw_rectangle_lines(PosX + 1, PosY + 1, width, height, Colors.black, 1.2)   # Shadow
            pm.draw_rectangle_lines(PosX, PosY, width, height, box_color, 1.2)
    
    @staticmethod
    def draw_cornered_box_internal(PosX, PosY, width, height, filled_color, box_color):
        corner_length = min(width, height) * 0.25  # 25% of the smaller dimension
        
        if cfg.ESP.box_style == "Filled":
            pm.draw_rectangle(PosX, PosY, width, height, filled_color)
        
        # Draw corner lines with shadows
        # Top-left corner
        pm.draw_line(PosX + 1, PosY + 1, PosX + corner_length + 1, PosY + 1, Colors.black, 2.0)  # Shadow
        pm.draw_line(PosX, PosY, PosX + corner_length, PosY, box_color, 1.5)
        pm.draw_line(PosX + 1, PosY + 1, PosX + 1, PosY + corner_length + 1, Colors.black, 2.0)  # Shadow
        pm.draw_line(PosX, PosY, PosX, PosY + corner_length, box_color, 1.5)
        
        # Top-right corner
        pm.draw_line(PosX + width - corner_length + 1, PosY + 1, PosX + width + 1, PosY + 1, Colors.black, 2.0)  # Shadow
        pm.draw_line(PosX + width - corner_length, PosY, PosX + width, PosY, box_color, 1.5)
        pm.draw_line(PosX + width + 1, PosY + 1, PosX + width + 1, PosY + corner_length + 1, Colors.black, 2.0)  # Shadow
        pm.draw_line(PosX + width, PosY, PosX + width, PosY + corner_length, box_color, 1.5)
        
        # Bottom-left corner
        pm.draw_line(PosX + 1, PosY + height - corner_length + 1, PosX + 1, PosY + height + 1, Colors.black, 2.0)  # Shadow
        pm.draw_line(PosX, PosY + height - corner_length, PosX, PosY + height, box_color, 1.5)
        pm.draw_line(PosX + 1, PosY + height + 1, PosX + corner_length + 1, PosY + height + 1, Colors.black, 2.0)  # Shadow
        pm.draw_line(PosX, PosY + height, PosX + corner_length, PosY + height, box_color, 1.5)
        
        # Bottom-right corner
        pm.draw_line(PosX + width + 1, PosY + height - corner_length + 1, PosX + width + 1, PosY + height + 1, Colors.black, 2.0)  # Shadow
        pm.draw_line(PosX + width, PosY + height - corner_length, PosX + width, PosY + height, box_color, 1.5)
        pm.draw_line(PosX + width - corner_length + 1, PosY + height + 1, PosX + width + 1, PosY + height + 1, Colors.black, 2.0)  # Shadow
        pm.draw_line(PosX + width - corner_length, PosY + height, PosX + width, PosY + height, box_color, 1.5)

    @staticmethod
    def draw_distance(distance, health_bar_x, health_bar_y, health_bar_width, y_offset):
        text_x = health_bar_x + health_bar_width + 5
        text_y = health_bar_y + y_offset
        font_size = 12
        pm.draw_text(f"{distance}m", text_x + 1, text_y + 1, font_size, Colors.black)  # Shadow
        pm.draw_text(f"{distance}m", text_x, text_y, font_size, pm.get_color("#FF0000"))  # Red text

    @staticmethod
    def draw_weapon(weaponName, health_bar_x, health_bar_y, health_bar_width, y_offset):
        text_x = health_bar_x + health_bar_width + 5
        text_y = health_bar_y + y_offset
        font_size = 12
        pm.draw_text(f"{weaponName}", text_x + 1, text_y + 1, font_size, Colors.black)  # Shadow
        pm.draw_text(f"{weaponName}", text_x, text_y, font_size, pm.get_color("#FF0000"))  # Red text

    @staticmethod
    def draw_name(playerName, health_bar_x, health_bar_y, health_bar_width, y_offset):
        if not cfg.ESP.show_name:
            return
        text_x = health_bar_x + health_bar_width + 5
        text_y = health_bar_y + y_offset
        font_size = 12
        pm.draw_text(f"{playerName}", text_x + 1, text_y + 1, font_size, Colors.black)  # Shadow
        pm.draw_text(f"{playerName}", text_x, text_y, font_size, pm.get_color("#FF0000"))  # Red text

    @staticmethod
    def draw_skeleton(entity, view_matrix):
        if not cfg.ESP.show_skeleton:
            return
            



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
    



       
        color_name = cfg.ESP.skeleton_color
        hex_color = color_map.get(color_name, "#FF00FF")  # Default to magenta if not found
        skeleton_color = pm.get_color(hex_color)
        
        
        thickness = cfg.ESP.skeleton_thickness
            
       
        bone_connections = [
            # Head to neck
            (6, 5),   # Head to Neck
            # Spine
            (5, 4),   # Neck to Upper Chest
            (4, 2),   # Upper Chest to Lower Chest  
            (2, 0),   # Lower Chest to Pelvis
            # Left arm
            (4, 8),   # Upper Chest to Left Shoulder
            (8, 9),   # Left Shoulder to Left Upper Arm
            (9, 10),  # Left Upper Arm to Left Forearm
            (10, 11), # Left Forearm to Left Hand
            # Right arm  
            (4, 13),  # Upper Chest to Right Shoulder
            (13, 14), # Right Shoulder to Right Upper Arm
            (14, 15), # Right Upper Arm to Right Forearm
            (15, 16), # Right Forearm to Right Hand
            # Left leg
            (0, 22),  # Pelvis to Left Thigh
            (22, 23), # Left Thigh to Left Shin
            (23, 24), # Left Shin to Left Foot
            # Right leg
            (0, 25),  # Pelvis to Right Thigh
            (25, 26), # Right Thigh to Right Shin  
            (26, 27), # Right Shin to Right Foot
        ]
        
        try:
            for bone1, bone2 in bone_connections:
                bone1_pos = entity.bone_pos(bone1)
                bone2_pos = entity.bone_pos(bone2)
                
                bone1_2d = pm.world_to_screen(view_matrix, bone1_pos, 1)
                bone2_2d = pm.world_to_screen(view_matrix, bone2_pos, 1)
                
                if bone1_2d and bone2_2d:
                    if cfg.ESP.skeleton_shadow:
                        pm.draw_line(bone1_2d["x"] + 1, bone1_2d["y"] + 1, 
                                   bone2_2d["x"] + 1, bone2_2d["y"] + 1, 
                                   Colors.black, thickness + 0.5)
                    pm.draw_line(bone1_2d["x"], bone1_2d["y"], 
                               bone2_2d["x"], bone2_2d["y"], 
                               skeleton_color, thickness)
        except Exception as e:
            print(f"[Skeleton ESP] Error: {e}")

    @staticmethod
    def draw_head_circle(entity, view_matrix, local_pos):
        if not cfg.ESP.show_head_circle:
            return
            
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
        
        color_name = cfg.ESP.skeleton_color
        hex_color = color_map.get(color_name, "#FF00FF")  # Default to magenta if not found
        head_color = pm.get_color(hex_color)
        
        try:
            # Get head position
            head_pos = entity.bone_pos(6)  # Head bone
            head_2d = pm.world_to_screen(view_matrix, head_pos, 1)
            
            if head_2d:
                try:
                    distance = entity.get_distance(local_pos)
                except:
                    distance = 10  
                
                radius = max(4, min(8, 50 / distance)) 
                
                segments = 16  
                for i in range(segments):
                    angle1 = (i * 2 * math.pi) / segments
                    angle2 = ((i + 1) * 2 * math.pi) / segments
                    
                    x1 = head_2d["x"] + radius * math.cos(angle1)
                    y1 = head_2d["y"] + radius * math.sin(angle1)
                    x2 = head_2d["x"] + radius * math.cos(angle2)
                    y2 = head_2d["y"] + radius * math.sin(angle2)
                   
                    if cfg.ESP.skeleton_shadow:
                        pm.draw_line(x1 + 1, y1 + 1, x2 + 1, y2 + 1, Colors.black, cfg.ESP.skeleton_thickness + 0.5)
                   
                    pm.draw_line(x1, y1, x2, y2, head_color, cfg.ESP.skeleton_thickness)
        except:
            pass

class ProcessDetector:
    """Utility class for detecting CS2 process with multiple fallback methods"""
    
    @staticmethod
    def find_cs2_by_name():
        """Try to find CS2 by exact process name"""
        try:
            pm = Utils.get_pyMeow()
            # Try multiple possible names for CS2
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
                        
                        # Try to open by PID - check if method exists
                        if hasattr(pm, 'open_process_by_pid'):
                            proc = pm.open_process_by_pid(pid)
                        else:
                            # Fallback: try to open by exact name if PID method doesn't exist
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
                    # Try to open by PID - check if method exists
                    if hasattr(pm, 'open_process_by_pid'):
                        proc = pm.open_process_by_pid(pid)
                    else:
                        # Fallback: get process name and try to open by name
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
                                
                                # Try to open by PID - check if method exists
                                if hasattr(pm, 'open_process_by_pid'):
                                    proc = pm.open_process_by_pid(pid)
                                else:
                                    # Fallback: try to open by process name
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
            
            # Look for Steam processes first
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
                
                # Look for CS2 processes that might be children of Steam
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
        """Try multiple methods to find CS2 process with retries"""
        print("[ProcessDetector] Starting CS2 process detection...")
        
        methods = [
            ("exact name", ProcessDetector.find_cs2_by_name),
            ("PID scan", ProcessDetector.find_cs2_by_pid_scan),
            ("Steam detection", ProcessDetector.find_cs2_via_steam),
            ("window title", ProcessDetector.find_cs2_by_window_title),
            ("common paths", ProcessDetector.find_cs2_by_common_paths)
        ]
        
        for attempt in range(max_retries):
            print(f"[ProcessDetector] Attempt {attempt + 1}/{max_retries}")
            
            for method_name, method in methods:
                print(f"[ProcessDetector] Trying method: {method_name}")
                proc = method()
                if proc:
                    print(f"[ProcessDetector] Successfully found CS2 using {method_name}")
                    return proc
                    
            if attempt < max_retries - 1:
                print(f"[ProcessDetector] All methods failed, waiting {retry_delay}s before retry...")
                time.sleep(retry_delay)
        
        print("[ProcessDetector] Failed to find CS2 process after all attempts")
        return None


class Cheat:
    def __init__(self):
        # Try to find CS2 process using multiple methods
        self.proc = ProcessDetector.find_cs2_with_retry()
        if not self.proc:
            raise Exception("Could not find CS2 process. Make sure Counter-Strike 2 is running.")
            
        print("[Cheat] CS2 process found, attempting to get client.dll module...")
        
        try:
            pm = Utils.get_pyMeow()
            self.mod = pm.get_module(self.proc, "client.dll")["base"]
            print(f"[Cheat] client.dll module found at: 0x{self.mod:X}")
        except Exception as e:
            raise Exception(f"Could not find client.dll module in CS2 process: {e}")

        print("[Cheat] Downloading offsets...")
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
        
        # Store overlay instance for dynamic FPS updates
        self.overlay_initialized = False

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
                print(f"[Cheat] Dynamic FPS update not supported by pyMeow version")
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
                controller_ptr = pm.r_int64(self.proc, entry_ptr + 120 * (i & 0x1FF))
                if controller_ptr == local:
                    continue
                controller_pawn_ptr = pm.r_int64(self.proc, controller_ptr + Offsets.m_hPlayerPawn)
                list_entry_ptr = pm.r_int64(self.proc, ent_list + 0x8 * ((controller_pawn_ptr & 0x7FFF) >> 9) + 16)
                pawn_ptr = pm.r_int64(self.proc, list_entry_ptr + 120 * (controller_pawn_ptr & 0x1FF))
            except:
                continue

            yield Entity(controller_ptr, pawn_ptr, self.proc)

    def get_local_pawn(self):
        return pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerPawn)

    def get_local_player_pos(self):
        return pm.r_vec3(self.proc, self.get_local_pawn() + Offsets.m_vOldOrigin)
    
    def get_local_player_team(self):
        try:
            local_pawn = self.get_local_pawn()
            if local_pawn:
                return pm.r_int(self.proc, local_pawn + Offsets.m_iTeamNum)
        except:
            pass
        return 0

    def run(self):
        print("[Security] Applying security measures...")
        
        if SecurityUtils.enable_debug_privileges():
            print("[Security] Debug privileges enabled")
        else:
            print("[Security] Warning: Could not enable debug privileges")
        
        if SecurityUtils.hide_from_process_list():
            print("[Security] Process hidden from basic enumeration")
        else:
            print("[Security] Warning: Could not hide process")
        
        if SecurityUtils.rename_process():
            print("[Security] Process name obfuscated")
        else:
            print("[Security] Warning: Could not rename process")
        
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
        print(f"[Security] Overlay attached to: {game_window_title} with {cfg.MISC.overlay_fps} FPS")
        self.overlay_initialized = True
        
        
        random_title = SecurityUtils.generate_random_title()
        try:
            SecurityUtils.set_overlay_title(random_title)
            print(f"[Security] Overlay title obfuscated to: {random_title}")
        except Exception as e:
            print(f"[Security] Warning: Could not set overlay title: {e}")
        
        frame_counter = 0
        title_change_interval = 5000  
        
        while pm.overlay_loop():
            frame_counter += 1
            if frame_counter % title_change_interval == 0:
                new_title = SecurityUtils.generate_random_title()
                try:
                    SecurityUtils.set_overlay_title(new_title)
                    print(f"[Security] Overlay title changed to: {new_title}")
                except:
                    pass
            
            view_matrix = pm.r_floats(self.proc, self.mod + Offsets.dwViewMatrix, 16)

            pm.begin_drawing()
            pm.draw_fps(0, 0)
            local_pos = self.get_local_player_pos()
            local_team = self.get_local_player_team()
            
            for ent in self.it_entities():
                if ent.wts(view_matrix) and ent.health > 0 and not ent.dormant:
                    
                    distance = ent.get_distance(local_pos)
                    if distance > cfg.ESP.max_distance:
                        continue
                    
                    
                    if not cfg.ESP.show_teammates and ent.team == local_team:
                        continue
                    
                    color = Colors.cyan if ent.team != 2 else Colors.orange
                    head = ent.pos2d["y"] - ent.head_pos2d["y"]
                    width = head / 2
                    center = width / 2

                    # Draw line to player with configurable color and position
                    if cfg.ESP.show_line:
                        line_color = Render.get_color_from_config(cfg.ESP.line_color)
                        
                        # Determine line start position based on configuration
                        screen_width = pm.get_screen_width()
                        screen_height = pm.get_screen_height()
                        
                        if cfg.ESP.line_position == "Top":
                            start_x = screen_width / 2
                            start_y = 0
                        elif cfg.ESP.line_position == "Bottom":
                            start_x = screen_width / 2
                            start_y = screen_height
                        else:  # Center (default)
                            start_x = screen_width / 2
                            start_y = screen_height / 2
                        
                        # Draw line with shadow
                        pm.draw_line(start_x + 1, start_y + 1, ent.head_pos2d["x"] + 1, ent.head_pos2d["y"] - center / 2 + 1, Colors.black, 1.0)
                        pm.draw_line(start_x, start_y, ent.head_pos2d["x"], ent.head_pos2d["y"] - center / 2, line_color, 0.8)
                    
                    # Draw boxes
                    Render.draw_box(ent.head_pos2d["x"] - center, ent.head_pos2d["y"] - center / 2, width, head + center / 2, color)
                    
                    # Draw skeleton ESP
                    Render.draw_skeleton(ent, view_matrix)
                    
                    # Draw head circle ESP
                    Render.draw_head_circle(ent, view_matrix, local_pos)
                    
                    # Draw health bar and get its exact coordinates
                    health_bar_x = ent.head_pos2d["x"] + center + 2
                    health_bar_y = ent.head_pos2d["y"] - center / 2
                    health_bar_width = 4
                    health_bar_height = head + center / 2
                    
                    actual_hb_x, actual_hb_y, actual_hb_w, actual_hb_h = Render.draw_health(100, ent.health, 
                                        health_bar_x,
                                        health_bar_y, 
                                        health_bar_width, 
                                        health_bar_height)
                    
                    # Draw information using EXACT same coordinates as health text
                    info_texts = []
                    if cfg.ESP.show_name:
                        info_texts.append(ent.name)
                    if cfg.ESP.show_distance:
                        info_texts.append(f"{distance}m")
                    if cfg.ESP.show_weapon:
                        weapon_name = ent.get_weapon_name()
                        if weapon_name and weapon_name != "Unknown":
                            info_texts.append(weapon_name)
                    
                    font_size = 12
                    line_spacing = 16
                    total_height = len(info_texts) * line_spacing
                    box_center_x = ent.head_pos2d["x"]
                    box_top_y = ent.head_pos2d["y"] - center / 2
                    text_start_y = box_top_y - total_height - 4  # 4px gap above box
                    for idx, text in enumerate(info_texts):
                        # Estimate text width: font_size * 0.6 * len(text)
                        text_width = font_size * 0.6 * len(text)
                        text_x = box_center_x - text_width / 2
                        text_y = text_start_y + idx * line_spacing
                        pm.draw_text(text, text_x + 1, text_y + 1, font_size, Colors.black)
                        pm.draw_text(text, text_x, text_y, font_size, pm.get_color("#FF0000"))

            pm.end_drawing()

            # Periodically change the window title to a new random title
            frame_counter += 1
            if frame_counter >= title_change_interval:
                new_title = SecurityUtils.generate_random_title()
                pm.set_window_title(new_title)
                print(f"[Security] Window title changed to: {new_title}")
                frame_counter = 0  # Reset counter

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
        16: "m4a1", 
        61: "usp", 
        60: "m4a1_silencer", 
        63: "cz75a", 
        64: "revolver", 
        59: "t_knife"
    }
