import sys
import os

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from Cheat import Main
    if hasattr(Main, 'main'):
        Main.main()
    elif hasattr(Main, '__main__'):
        Main.__main__()
    else:
        print("[Launcher] Could not find an entry point in Main module.")
except Exception as e:
    print(f"[Launcher] Failed to run Main module: {e}")
