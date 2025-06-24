import time
import math
import threading
import random
from random import uniform
import keyboard
import Cheat.utils as utils
from Cheat.config import cfg
from .mouse_utils import move_mouse_relative_sendinput

class Aimbot:
    def __init__(self, offsets=None):
        self.pm = utils.get_pyMeow()
        self.offsets = offsets
        self.target_lock = None
        self.last_target_time = 0
        self.aimbot_thread = None
        self.running = False
        self.lock = threading.Lock()
        self.target_entity = None
        self.view_matrix = None
        self.local_pawn = None
        self.local_pos = None
        self.local_team = None
        self.proc = None
        self.mod = None
        self.bone_cycle_target_id = None
        self.entities = []
        
    def start_thread(self, proc, mod):
        """Start the aimbot in a separate thread"""
        if self.running:
            return
            
        self.proc = proc
        self.mod = mod
        self.running = True
        
        self.aimbot_thread = threading.Thread(target=self._aimbot_loop)
        self.aimbot_thread.daemon = True
        self.aimbot_thread.start()
        print("[Aimbot] Thread started")
        
    def stop_thread(self):
        """Stop the aimbot thread"""
        self.running = False
        if self.aimbot_thread and self.aimbot_thread.is_alive():
            self.aimbot_thread.join(timeout=1.0)
            print("[Aimbot] Thread stopped")
    
    def update_data(self, view_matrix, local_pawn, local_pos, local_team, entities):
        """Update the aimbot with current game data"""
        with self.lock:
            self.view_matrix = view_matrix
            self.local_pawn = local_pawn
            self.local_pos = local_pos
            self.local_team = local_team
            self.entities = entities
    
    def _get_scaled_smoothness(self, smoothness_percent):
        """Convert smoothness percentage to a usable value (lower = snappier, higher = smoother)"""
        if smoothness_percent is None:
            smoothness_percent = getattr(cfg.AIMBOT, 'smoothness', 50)
        
        smoothness_percent = max(1, min(100, smoothness_percent))

        min_scale = 0.5
        max_scale = 30.0
        scaled = min_scale * ((max_scale / min_scale) ** (smoothness_percent / 100.0))
        scaled += random.uniform(-0.5, 0.5)
        return scaled

    def draw_fov_circle(self):
        """Draw the FOV circle as an outlined ring (no fill) using lines"""
        if not getattr(cfg.AIMBOT, 'show_fov_circle', True):
            return
            
        try:
            screen_width = self.pm.get_screen_width()
            screen_height = self.pm.get_screen_height()
            center_x, center_y = screen_width // 2, screen_height // 2
            
            fov_value = getattr(cfg.AIMBOT, 'aim_fov', 30)
            radius = fov_value * (screen_height / 100.0)
            
            color = self.pm.get_color("#FFFFFF")
            segments = 64
            points = []
            for i in range(segments):
                angle = (i * 2 * math.pi) / segments
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            for i in range(segments):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % segments]
                self.pm.draw_line(x1, y1, x2, y2, color, 1.5)
        except Exception as e:
            print(f"[Aimbot] Error drawing FOV circle: {e}")

    def aim_at_target(self, target_tuple, process, local_pawn, smoothness_percent=None):
        """Aim at the specified target"""
        if not target_tuple:
            return False
        
        target_entity, bone_2d, bone_id = target_tuple
        
        if not bone_2d or not all(isinstance(bone_2d.get(k), (int, float)) for k in ['x', 'y']):
            return False
        
        try:
            screen_width = self.pm.get_screen_width()
            screen_height = self.pm.get_screen_height()
            center_x, center_y = screen_width // 2, screen_height // 2
            dx = bone_2d["x"] - center_x
            dy = bone_2d["y"] - center_y
            smoothness = self._get_scaled_smoothness(smoothness_percent)
            curve = getattr(cfg.AIMBOT, 'curve', 'Linear').lower()
            if curve == 'linear':
                move_x = dx / smoothness
                move_y = dy / smoothness
            elif curve == 'slinear':
                move_x = (dx / smoothness) * 0.7 + (dx / (smoothness * 2)) * 0.3
                move_y = (dy / smoothness) * 0.7 + (dy / (smoothness * 2)) * 0.3
            elif curve == 'rlinear':
                move_x = (dx / smoothness) * 0.3 + (dx / (smoothness * 2)) * 0.7
                move_y = (dy / smoothness) * 0.3 + (dy / (smoothness * 2)) * 0.7
            elif curve == 'beziercurve':
                t = 0.5
                ctrl_x = center_x + dx * 0.5
                ctrl_y = center_y
                bx = (1-t)**2 * center_x + 2*(1-t)*t*ctrl_x + t**2 * bone_2d['x']
                by = (1-t)**2 * center_y + 2*(1-t)*t*ctrl_y + t**2 * bone_2d['y']
                move_x = (bx - center_x) / smoothness
                move_y = (by - center_y) / smoothness
            else:
                move_x = dx / smoothness
                move_y = dy / smoothness
            move_mouse_relative_sendinput(int(move_x), int(move_y))
            return True
        except Exception as e:
            print(f"[Aimbot] Error in aim_at_target: {e}")
            return False

    def check_and_aim(self, entities, local_pos, local_team, process, local_pawn, view_matrix):
        """Check if we should aim and perform aiming if needed"""
        if not getattr(cfg.AIMBOT, 'enabled', False):
            return False
            
        aim_key = getattr(cfg.AIMBOT, 'aim_key', None)
        if not aim_key or not keyboard.is_pressed(aim_key):
            self.target_lock = None
            return False
            
        try:
            if self.target_lock:
                entity_id, bone_id = self.target_lock
                
                target_entity = None
                for entity in entities:
                    if id(entity) == entity_id:
                        target_entity = entity
                        break
                        
                if target_entity and target_entity.health > 0 and not target_entity.dormant:
                    visible_check = getattr(cfg.AIMBOT, 'visible_check', True)
                    if visible_check and not target_entity.spotted:
                        self.target_lock = None
                        return False
                        
                    bone_pos = target_entity.bone_pos(bone_id)
                    if not bone_pos:
                        self.target_lock = None
                        return False
                        
                    bone_2d = self.pm.world_to_screen(view_matrix, bone_pos, 1)
                    if not bone_2d:
                        self.target_lock = None
                        return False
                        
                    return self.aim_at_target((target_entity, bone_2d, bone_id), process, local_pawn)
                else:
                    self.target_lock = None
            
            target_tuple = self.find_best_target_cycle(entities, local_pos, local_team, view_matrix)
            if target_tuple:
                target_entity, bone_2d, bone_id = target_tuple
                self.target_lock = (id(target_entity), bone_id)
                return self.aim_at_target(target_tuple, process, local_pawn)
                
            return False
            
        except Exception as e:
            print(f"[Aimbot] Error in check_and_aim: {e}")
            return False

    def find_best_target_cycle(self, entities, local_pos, local_team, view_matrix):
        """Find the best target using bone cycling"""
        if not entities:
            return None
            
        try:
            target_bones = getattr(cfg.AIMBOT, 'target_bones', ["head"])
            max_distance = getattr(cfg.AIMBOT, 'max_distance', 50)
            visible_check = getattr(cfg.AIMBOT, 'visible_check', True)
            
            bone_map = {"head": 6, "neck": 5, "chest": 4, "stomach": 2}
            bone_ids = [bone_map.get(bone.lower(), 6) for bone in target_bones]
            if not bone_ids:
                bone_ids = [6]
                
            valid_targets = []
            for item in entities:
                if isinstance(item, tuple) and len(item) == 2:
                    entity, distance = item
                else:
                    entity = item
                    distance = entity.get_distance(local_pos) if hasattr(entity, 'get_distance') else float('inf')
                if not entity or not hasattr(entity, 'health') or entity.health <= 0 or getattr(entity, 'dormant', True):
                    continue
                    
                if getattr(entity, 'team', None) == local_team:
                    continue
                    
                if distance > max_distance:
                    continue
                    
                if visible_check and not getattr(entity, 'spotted', False):
                    continue
                    
                valid_targets.append((entity, distance))
                
            if not valid_targets:
                return None
                
            valid_targets.sort(key=lambda x: x[1])
            
            screen_width = self.pm.get_screen_width()
            screen_height = self.pm.get_screen_height()
            center_x, center_y = screen_width // 2, screen_height // 2
            
            fov_value = getattr(cfg.AIMBOT, 'aim_fov', 30)
            radius = fov_value * (screen_height / 100.0)
            
            best_ent = None
            best_bone_2d = None
            best_bone_id = None
            best_distance = float('inf')
            
            for entity, distance in valid_targets:
                for bone_id in bone_ids:
                    bone_pos = entity.bone_pos(bone_id)
                    if not bone_pos:
                        continue
                        
                    bone_2d = self.pm.world_to_screen(view_matrix, bone_pos, 1)
                    if not bone_2d:
                        continue
                        
                    delta_x = bone_2d["x"] - center_x
                    delta_y = bone_2d["y"] - center_y
                    distance_to_crosshair = math.sqrt(delta_x**2 + delta_y**2)
                    
                    if distance_to_crosshair <= radius:
                        if distance_to_crosshair < best_distance:
                            best_ent = entity
                            best_bone_2d = bone_2d
                            best_bone_id = bone_id
                            best_distance = distance_to_crosshair
            
            if best_ent:
                return (best_ent, best_bone_2d, best_bone_id)
            else:
                return None
            
        except Exception as e:
            print(f"[Aimbot] Error in find_best_target_cycle: {e}")
            return None

    def _aimbot_loop(self):
        """Main loop for the aimbot thread"""
        while self.running:
            try:
                with self.lock:
                    entities = self.entities.copy()
                    local_pos = self.local_pos
                    local_team = self.local_team
                    process = self.proc
                    local_pawn = self.local_pawn
                    view_matrix = self.view_matrix
                    
                if entities and local_pos and local_team and process and local_pawn and view_matrix:
                    self.check_and_aim(entities, local_pos, local_team, process, local_pawn, view_matrix)
                    
                time.sleep(0.01)
                
            except Exception as e:
                print(f"[Aimbot] Error in aimbot loop: {e}")
                time.sleep(1.0)