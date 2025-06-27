import time
import math
import threading
import random
import keyboard
import traceback
from typing import Optional
import Cheat.utils as utils
from Cheat.config import cfg
from .mouse_utils import move_mouse_relative_sendinput

class Aimbot:
    def __init__(self, offsets: Optional[object] = None):
        self.pm = utils.get_pyMeow()
        self.offsets = offsets
        self.target_lock = None
        self.aimbot_thread = None
        self.running = False
        self.lock = threading.Lock()
        self.view_matrix = None
        self.local_pawn = None
        self.local_pos = None
        self.local_team = None
        self.proc = None
        self.mod = None
        self.entities = []

    def start_thread(self, proc, mod) -> None:
        if self.running:
            return
        self.proc = proc
        self.mod = mod
        self.running = True
        self.aimbot_thread = threading.Thread(target=self._aimbot_loop, daemon=True)
        self.aimbot_thread.start()
        print("[Aimbot] Thread started")

    def stop_thread(self) -> None:
        self.running = False
        if self.aimbot_thread and self.aimbot_thread.is_alive():
            self.aimbot_thread.join(timeout=1.0)
            print("[Aimbot] Thread stopped")

    def update_data(
        self,
        view_matrix: object,
        local_pawn: object,
        local_pos: object,
        local_team: object,
        entities: list
    ) -> None:
        with self.lock:
            self.view_matrix = view_matrix
            self.local_pawn = local_pawn
            self.local_pos = local_pos
            self.local_team = local_team
            self.entities = list(entities) if entities else []

    def _get_scaled_smoothness(self, smoothness_percent: Optional[float]) -> float:
        if smoothness_percent is None:
            smoothness_percent = getattr(cfg.AIMBOT, 'smoothness', 50)
        smoothness_percent = max(1, min(100, smoothness_percent))
        min_scale = 0.5
        max_scale = 30.0
        scaled = min_scale * ((max_scale / min_scale) ** (smoothness_percent / 100.0))
        scaled += random.uniform(-0.5, 0.5)
        return scaled

    def draw_fov_circle(self) -> None:
        if not getattr(cfg.AIMBOT, 'show_fov_circle', True):
            return
        try:
            screen_width = self.pm.get_screen_width()
            screen_height = self.pm.get_screen_height()
            center_x = screen_width // 2
            center_y = screen_height // 2
            fov_value = getattr(cfg.AIMBOT, 'aim_fov', 30)
            radius = fov_value * (screen_height / 100.0)
            color = self.pm.get_color("#FFFFFF")
            segments = 64
            points = [
                (
                    center_x + radius * math.cos((i * 2 * math.pi) / segments),
                    center_y + radius * math.sin((i * 2 * math.pi) / segments)
                )
                for i in range(segments)
            ]
            for i in range(segments):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % segments]
                self.pm.draw_line(x1, y1, x2, y2, color, 1.5)
        except Exception as e:
            print(f"[Aimbot] Error drawing FOV circle: {e}")

    def aim_at_target(
        self,
        target_tuple: Optional[tuple],
        process: object,
        local_pawn: object,
        smoothness_percent: Optional[float] = None
    ) -> bool:
        if not target_tuple:
            return False
        target_entity, bone_2d, bone_id = target_tuple
        if not bone_2d or not all(isinstance(bone_2d.get(k), (int, float)) for k in ['x', 'y']):
            return False
        try:
            screen_width = self.pm.get_screen_width()
            screen_height = self.pm.get_screen_height()
            center_x = screen_width // 2
            center_y = screen_height // 2
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

    def check_and_aim(
        self,
        entities: list,
        local_pos: object,
        local_team: object,
        process: object,
        local_pawn: object,
        view_matrix: object
    ) -> bool:
        if not getattr(cfg.AIMBOT, 'enabled', False):
            return False
        aim_key = getattr(cfg.AIMBOT, 'aim_key', None)
        if not aim_key or not keyboard.is_pressed(aim_key):
            self.target_lock = None
            return False
        try:
            if self.target_lock is not None:
                entity_id, bone_id = self.target_lock
                target_entity = next((entity for entity in entities if id(entity) == entity_id), None)
                if (
                    target_entity is not None
                    and getattr(target_entity, 'health', 0) > 0
                    and not getattr(target_entity, 'dormant', True)
                ):
                    visible_check = getattr(cfg.AIMBOT, 'visible_check', True)
                    if visible_check and not getattr(target_entity, 'spotted', False):
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

    def find_best_target_cycle(
        self,
        entities: list,
        local_pos: object,
        local_team: object,
        view_matrix: object
    ):
        if not entities:
            return None
        try:
            # Move config lookups outside the loop for efficiency
            target_bones = getattr(cfg.AIMBOT, 'target_bones', ["head"])
            max_distance = getattr(cfg.AIMBOT, 'max_distance', 50)
            visible_check = getattr(cfg.AIMBOT, 'visible_check', True)
            bone_map = {"head": 6, "neck": 5, "chest": 4, "stomach": 2}
            bone_ids = [bone_map.get(bone.lower(), 6) for bone in target_bones] or [6]
            valid_targets = []
            for item in entities:
                if isinstance(item, tuple) and len(item) == 2:
                    entity, distance = item
                else:
                    entity = item
                    distance = entity.get_distance(local_pos) if hasattr(entity, 'get_distance') else float('inf')
                if (
                    not entity
                    or not hasattr(entity, 'health')
                    or entity.health <= 0
                    or getattr(entity, 'dormant', True)
                    or getattr(entity, 'team', None) == local_team
                    or distance > max_distance
                    or (visible_check and not getattr(entity, 'spotted', False))
                ):
                    continue
                valid_targets.append((entity, distance))
            if not valid_targets:
                return None
            valid_targets.sort(key=lambda x: x[1])
            screen_width = self.pm.get_screen_width()
            screen_height = self.pm.get_screen_height()
            center_x = screen_width // 2
            center_y = screen_height // 2
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
                    distance_to_crosshair = math.hypot(delta_x, delta_y)
                    if distance_to_crosshair <= radius and distance_to_crosshair < best_distance:
                        best_ent = entity
                        best_bone_2d = bone_2d
                        best_bone_id = bone_id
                        best_distance = distance_to_crosshair
            if best_ent:
                return (best_ent, best_bone_2d, best_bone_id)
            return None
        except Exception as e:
            print(f"[Aimbot] Error in find_best_target_cycle: {e}")
            return None

    def _aimbot_loop(self) -> None:
        while self.running:
            try:
                with self.lock:
                    entities = self.entities.copy()
                    local_pos = self.local_pos
                    local_team = self.local_team
                    process = self.proc
                    local_pawn = self.local_pawn
                    view_matrix = self.view_matrix
                if all([entities, local_pos, local_team, process, local_pawn, view_matrix]):
                    self.check_and_aim(
                        entities, local_pos, local_team, process, local_pawn, view_matrix
                    )
                sleep_interval = getattr(cfg.AIMBOT, 'loop_sleep', 0.01)
                time.sleep(sleep_interval)
            except Exception as e:
                print(f"[Aimbot] Error in aimbot loop: {e}")
                traceback.print_exc()
                time.sleep(1.0)