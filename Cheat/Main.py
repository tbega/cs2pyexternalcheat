import threading
import time
import psutil

from Cheat import Cheat
import gui


cheat_instance = None

def check_cs2_running():
    """Check if CS2 is running and provide helpful information"""
    cs2_processes = []
    
    for process in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            proc_name = process.info['name']
            if proc_name and 'cs2' in proc_name.lower():
                cs2_processes.append((process.info['pid'], proc_name, process.info.get('exe', 'N/A')))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    

def get_cheat_instance():
    """Get the global cheat instance"""
    return cheat_instance

def main():
    """Main entry point for the cheat"""
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

    gui_thread = threading.Thread(target=gui.render, daemon=True)
    cheat_thread = threading.Thread(target=cheat_instance.run, daemon=True)

    gui_thread.start()
    cheat_thread.start()

    try:
        gui_thread.join()
        cheat_thread.join()
    except KeyboardInterrupt:
        print("[Main] Shutting down...")

if __name__ == "__main__":
    main()