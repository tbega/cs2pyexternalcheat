import time
import random
import threading
from random import uniform
from pynput.mouse import Controller, Button
import Cheat.utils as utils

class TriggerBot:
    def __init__(self, cheat_instance=None, aimbot_instance=None, offsets=None):
        self.cheat_instance = cheat_instance
        self.aimbot_instance = aimbot_instance
        self.last_shot_time = 0
        self.pm = utils.get_pyMeow()
        self.offsets = offsets
        self.shooting_thread = None
        self.is_shooting = False

    def shoot_async(self, delay_min, delay_max):
        """Execute the shooting action in a separate thread"""
        if self.is_shooting:
            return
            
        self.is_shooting = True
        
        def shoot_task():
            try:
                delay = random.uniform(delay_min / 1000.0, delay_max / 1000.0)
                time.sleep(delay)
                
                mouse = Controller()
                mouse.press(Button.left)
                time.sleep(uniform(0.01, 0.05))
                mouse.release(Button.left)
                
                self.last_shot_time = time.time()
            except Exception as e:
                print(f"[TriggerBot] Shoot exception: {e}")
            finally:
                self.is_shooting = False
        
        self.shooting_thread = threading.Thread(target=shoot_task)
        self.shooting_thread.daemon = True
        self.shooting_thread.start()

    def shoot(self):
        try:
            from Cheat.config import cfg
            delay_min = getattr(cfg.TRIGGERBOT, 'delay_min', 0)
            delay_max = getattr(cfg.TRIGGERBOT, 'delay_max', 0)
            self.shoot_async(delay_min, delay_max)
        except Exception as e:
            print(f"[TriggerBot] Shoot exception: {e}")

    def check_and_shoot(self, process, module):
        from Cheat.config import cfg
        
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
        
        try:
            import keyboard
        except ImportError:
            print("[TriggerBot] 'keyboard' module not found, key check will be disabled.")
            return False
            
        if not trigger_key or not keyboard.is_pressed(trigger_key):
            return False
            
        try:
            try:
                import win32api
                if win32api.GetAsyncKeyState(0x01) < 0:
                    return False
            except Exception:
                pass
                
            pm = utils.get_pyMeow()
            
            offsets = self.offsets
            
            player = pm.r_int64(process, module + offsets.dwLocalPlayerPawn)
            if not player or player < 0x1000:
                return False
                
            entityId = pm.r_int(process, player + offsets.m_iIDEntIndex)
            if entityId is None or entityId <= 0:
                return False
                
            entList = pm.r_int64(process, module + offsets.dwEntityList)
            if not entList or entList < 0x1000:
                return False
                
            entEntry_addr = entList + 0x8 * (entityId >> 9) + 0x10
            entEntry = pm.r_int64(process, entEntry_addr)
            if not entEntry or entEntry < 0x1000:
                return False
                
            entity_addr = entEntry + 120 * (entityId & 0x1FF)
            entity = pm.r_int64(process, entity_addr)
            if not entity or entity < 0x1000:
                return False
                
            entityTeam = pm.r_int(process, entity + offsets.m_iTeamNum)
            playerTeam = pm.r_int(process, player + offsets.m_iTeamNum)
            if entityTeam is None or playerTeam is None:
                return False
                
            if not shoot_teammates and entityTeam == playerTeam:
                return False
                
            entityHp = pm.r_int(process, entity + offsets.m_iHealth)
            if entityHp is None or entityHp <= 0:
                return False
                
            self.shoot_async(delay_min, delay_max)
            return True
            
        except Exception as e:
            print(f"[TriggerBot] check_and_shoot exception: {e}")
            
        return False