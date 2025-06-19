import subprocess
import sys
def install_pyqt6():
    """Install PyQt6 and dependencies"""
    print("Installing PyQt6 for Launcher.")
    print("=" * 50)
    try:
        print("Installing PyQt6.")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"], check=True)
        print("Installing other dependencies.")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("\nInstallation completed successfully!")
        print("You can now run the launcher.") 
    except subprocess.CalledProcessError as e:
        print(f"\nInstallation failed: {e}")
        print("Try running this script as Administrator.")
        return False
    return True
if __name__ == "__main__":
    install_pyqt6()
    input("\nPress Enter to exit...")
