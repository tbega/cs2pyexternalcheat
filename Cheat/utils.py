import requests as rq
import pyMeow as pm
from Cheat.mouse_utils import move_mouse_relative_sendinput

def get_pyMeow() -> pm:
    return pm

def get_requests() -> rq:
    return rq

class Mem:
    @staticmethod
    def trace_address(proc, base_address: int, offsets: list[int]) -> int:

        if not offsets:
            return base_address
        address = pm.r_int(proc, base_address)
        if address == 0:
            return 0
        for i, offset in enumerate(offsets[:-1]):
            address = pm.r_int(proc, address + offset)
            if address == 0:
                return 0
        return address + offsets[-1] if address != 0 else 0