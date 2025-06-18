# CS2 External Cheat

an external cheat for cs2, it has esp and a menu

## features

### esp
- **Player Boxes**: Outline players with customizable colored boxes
- **Skeleton ESP**: Display player bone structure with customizable colors and thickness
- **Head Circle ESP**: Draw circles around player heads
- **Health Bars**: Visual health indicators with numerical values
- **Player Information**: Display names, distances, and weapon information
- **Line ESP**: Draw lines from screen center/top/bottom to players
- **Teammate Toggle**: Option to show/hide ESP for teammates
- **Distance Filtering**: Configurable maximum ESP distance

### gui
- **Real-time Configuration**: Adjust all settings while the cheat is running
- **Color Customization**: Choose from multiple color options for all ESP elements
- **Intuitive Controls**: Easy-to-use checkboxes, sliders, and dropdowns

## Installation & Setup

### Prerequisites
- Windows 10/11
- Python 3.11 or newer
- Counter-Strike 2 installed

### Quick Setup (Recommended)

1. **Download the cheat files** to a folder on your computer
2. **Run the installer** by double-clicking `install.bat`
   - This will automatically install all required dependencies
3. **Launch the cheat** by running `python main.py` in the folder

### Manual Setup

If the automatic installer doesn't work:

1. **Install Python dependencies manually**:
   ```
   pip install -r requirements.txt
   ```

2. **Install build tools** (if you want to compile from source):
   ```
   pip install cython setuptools wheel
   ```

## Usage

### Starting the Cheat

1. **Launch Counter-Strike 2** first
2. **Run the cheat** by executing `python main.py` in the cheat folder \ or by double click main.py
3. The cheat will automatically:
   - Find and attach to the CS2 game window
   - Open the configuration GUI

### Using the GUI

The GUI is divided into several sections:

#### Main ESP Settings
- **Show Box**: Toggle player outline boxes
- **Show Line**: Toggle lines pointing to players
- **Show Health**: Toggle health bars
- **Show Distance**: Display distance to players
- **Show Weapon**: Display player weapon names
- **Show Name**: Display player names
- **Show Teammates**: Toggle ESP for your teammates

#### Skeleton Settings
- **Show Skeleton**: Enable/disable skeleton ESP
- **Skeleton Shadow**: Add shadow effects to skeleton lines
- **Skeleton Color**: Choose skeleton color (Red, Green, Blue, etc.)
- **Skeleton Thickness**: Adjust line thickness (0.5 - 5.0)

#### Head Circle Settings
- **Show Head Circle**: Enable/disable head circle ESP
- Head circles automatically match your skeleton color and thickness

#### Other Settings
- **Box Color**: Choose color for player boxes
- **Line Color**: Choose color for ESP lines
- **Line Position**: Set where lines start (Top, Center, Bottom of screen)
- **Max Distance**: Set maximum ESP range (1-100 meters)

### Security Warnings

When you start the cheat, you may see these warnings:
- `[Security] Warning: Could not enable debug privileges`
- `[Security] Warning: Could not hide process`

**These are normal** and occur because:
- Debug privileges require administrator rights
- Process hiding is not possible from user-mode Python without a kernel driver

To minimize these warnings:
- Run the cheat as Administrator (right-click → "Run as administrator")
- Even as admin, some warnings may still appear due to Windows security restrictions

## Troubleshooting

### Common Issues

**"No module named 'Main'" Error**:
- Ensure you're running `python main.py` from the correct folder

**Cheat doesn't detect CS2**:
- Make sure CS2 is running before starting the cheat
- Try running both CS2 and the cheat as Administrator
- Verify CS2 window title matches what the cheat expects

**ESP not showing**:
- Check that ESP features are enabled in the GUI
- Ensure you're in a game with other players
- Verify the max distance setting isn't too low
- Make sure the game window is active and not minimized

**Performance issues**:
- Lower the ESP distance limit
- Disable unnecessary ESP features
- Close other resource-intensive programs

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Try running both the game and cheat as Administrator
4. Make sure your Python version is compatible (3.11+)

## Legal Disclaimer

This software is for educational purposes only. Using cheats in online games may violate the game's terms of service and could result in account bans. Use at your own risk. I take no responsiblity for any consequences resulting from the use of this software. You choose to cheat.

## Features Overview

- ✅ Player ESP boxes with multiple colors
- ✅ Skeleton ESP with customizable appearance
- ✅ Head circle ESP
- ✅ Health bars with numerical values
- ✅ Player information display (names, distances, weapons)
- ✅ Teammate filtering
- ✅ Line ESP with multiple positions
- ✅ Security features and obfuscation
- ✅ Real-time GUI configuration
- ✅ Distance-based filtering

Enjoy responsibly!
