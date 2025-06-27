import threading
import time
import psutil

from Cheat.Cheat import Cheat
import Cheat.gui as gui


cheat_instance = None

def get_cheat_instance():
    return cheat_instance

def main():
    global cheat_instance

    print("[Main] Starting CS2 External Cheat...")

    try:
        cheat_instance = Cheat()
        print("[Main] Cheat initialized successfully")
    except Exception as e:
        print(f"[Main] Failed to initialize cheat: {e}")
        print("[Main] Troubleshooting tips:")
        print("  1. Make sure Counter-Strike 2 is running")
        print("  2. Try running as Administrator")
        print("  3. Check if antivirus is blocking the application")
        print("  4. Ensure CS2 is not running with higher privileges")
        input("[Main] Press Enter to exit...")
        return

    gui_thread = threading.Thread(target=gui.main, daemon=True)
    cheat_thread = threading.Thread(target=cheat_instance.run, daemon=True)

    gui_thread.start()
    cheat_thread.start()

    try:
        while gui_thread.is_alive() and cheat_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("[Main] Shutting down...")

if __name__ == "__main__":
    main()