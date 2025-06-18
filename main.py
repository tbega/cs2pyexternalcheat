import sys
import os
cheat_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Cheat'))
if not os.path.isdir(cheat_dir):
    print(f"[Launcher] Cheat directory not found: {cheat_dir}")
    sys.exit(1)
if cheat_dir not in sys.path:
    sys.path.insert(0, cheat_dir)

try:
    import Main
    if hasattr(Main, 'main'):
        Main.main()
    elif hasattr(Main, '__main__'):
        Main.__main__()
    else:
        print("[Launcher] Could not find an entry point in Main module.")
except Exception as e:
    print(f"[Launcher] Failed to run Main module: {e}")
