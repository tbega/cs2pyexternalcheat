import time
import random
import threading
from typing import Optional
from pynput.mouse import Controller, Button
import keyboard

from Cheat.config import cfg
import Cheat.utils as utils


class TriggerBot:
    def __init__(
        self,
        cheat_instance: Optional[object] = None,
        aimbot_instance: Optional[object] = None,
        offsets: Optional[object] = None
    ):
        self.cheat_instance = cheat_instance
        self.aimbot_instance = aimbot_instance
        self.last_shot_time: float = 0.0
        self.pm = utils.get_pyMeow()
        self.offsets = offsets
        self.is_shooting: bool = False
        self.mouse = Controller()
        self.lock = threading.Lock()

    def shoot_async(self, delay_min: float, delay_max: float) -> None:
        if self.is_shooting:
            return
        self.is_shooting = True

        def shoot_task():
            try:
                delay = random.uniform(delay_min / 1000.0, delay_max / 1000.0)
                time.sleep(delay)
                with self.lock:
                    self.mouse.press(Button.left)
                    time.sleep(random.uniform(0.01, 0.02))  # shorter click to minimize input blocking
                    self.mouse.release(Button.left)
                self.last_shot_time = time.time()
            except Exception as e:
                print(f"[TriggerBot] Shoot exception: {e}")
            finally:
                self.is_shooting = False

        thread = threading.Thread(target=shoot_task, daemon=True)
        thread.start()

    def shoot(self) -> None:
        try:
            delay_min = getattr(cfg.TRIGGERBOT, 'delay_min', 0)
            delay_max = getattr(cfg.TRIGGERBOT, 'delay_max', 0)
            self.shoot_async(delay_min, delay_max)
        except Exception as e:
            print(f"[TriggerBot] Shoot exception: {e}")

    def check_and_shoot(self, process, module) -> bool:
        if not getattr(cfg.TRIGGERBOT, 'enabled', False):
            return False

        if not self.offsets:
            print("[TriggerBot] Offsets not available")
            return False

        if self.is_shooting:
            return False

        trigger_key = getattr(cfg.TRIGGERBOT, 'trigger_key', None)
        shoot_teammates = getattr(cfg.TRIGGERBOT, 'shoot_teammates', False)
        delay_min = getattr(cfg.TRIGGERBOT, 'delay_min', 10)
        delay_max = getattr(cfg.TRIGGERBOT, 'delay_max', 30)

        # Add a small sleep to reduce CPU usage and input contention
        time.sleep(0.005)

        if not trigger_key or not keyboard.is_pressed(trigger_key):
            return False

        try:
            offsets = self.offsets
            pm = self.pm

            player = pm.r_int64(process, module + offsets.dwLocalPlayerPawn)
            if not player or player < 0x1000:
                return False

            entity_id = pm.r_int(process, player + offsets.m_iIDEntIndex)
            if entity_id is None or entity_id <= 0:
                return False

            ent_list = pm.r_int64(process, module + offsets.dwEntityList)
            if not ent_list or ent_list < 0x1000:
                return False

            ent_entry_addr = ent_list + 0x8 * (entity_id >> 9) + 0x10
            ent_entry = pm.r_int64(process, ent_entry_addr)
            if not ent_entry or ent_entry < 0x1000:
                return False

            entity_addr = ent_entry + 120 * (entity_id & 0x1FF)
            entity = pm.r_int64(process, entity_addr)
            if not entity or entity < 0x1000:
                return False

            entity_team = pm.r_int(process, entity + offsets.m_iTeamNum)
            player_team = pm.r_int(process, player + offsets.m_iTeamNum)
            if entity_team is None or player_team is None:
                return False

            if not shoot_teammates and entity_team == player_team:
                return False

            entity_hp = pm.r_int(process, entity + offsets.m_iHealth)
            if entity_hp is None or entity_hp <= 0:
                return False

            self.shoot_async(delay_min, delay_max)
            return True

        except Exception as e:
            print(f"[TriggerBot] check_and_shoot exception: {e}")

        return False