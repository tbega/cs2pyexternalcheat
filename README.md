# CS2 External Cheat

[![Python 3.11.9](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## Why This Exists

Counter-Strike 2 dropped with updated anti-cheat systems, but the community needed a solution that actually works. This external cheat bypasses VAC detection through overlay rendering instead of memory injection - a approach that's proven effective for over two years without a single ban report.

Built from scratch using modern Python architecture, this isn't another paste job. Every component was designed for reliability, performance, and most importantly - staying undetected.

## What You Get

**Aimbot**
- Configurable FOV and smoothness settings
- Multiple targeting modes (closest, crosshair, health-based)
- Natural movement patterns to avoid obvious bot behavior

**ESP Wallhack** 
- Player boxes with health and armor indicators
- Distance calculations and weapon displays
- Fully customizable colors and visibility options
- Bone ESP for precise target identification

**Triggerbot**
- Configurable reaction time ranges
- Smart enemy detection algorithms

**Additional Tools**
- Stream-safe overlay (invisible on recordings)
- Performance optimization controls
- Real-time bomb timer 

## How It Works

This cheat operates as an external overlay, never touching CS2's memory directly. Instead of injecting code (which triggers VAC), it reads game state externally and renders information on top of your screen.

**Technical Details:**
- External memory reading through PyMeow
- PyMeow overlay + DearPy Gui
- Zero code injection into CS2 process
- Modular Python codebase for easy modification

**Why External Matters:**
Internal cheats inject DLLs into the game process - an immediate red flag for anti-cheat systems. External cheats like this one operate outside the game entirely, making detection nearly impossible through traditional methods.

## Getting Started

**Requirements:**
- Windows 10/11 
- Python 3.11.9+
- CS2 running in Windowed or Fullscreen Windowed mode

**Installation:**
1. Download and extract the files
2. Run `setup_premium.py` (installs dependencies automatically)
3. Start CS2
4. Launch `launcher_premium.py`

**Manual Setup:**
```bash
pip install -r requirements.txt
```

The GUI opens with your cheat ready to configure. All features can be toggled and customized in real-time without restarting.

## Common Problems

**"PyMeow not found"**
Download from https://github.com/qb-0/PyMeow and install with `pip install pymeow.zip`

**Black screen on AMD GPUs**
AMD has overlay compatibility issues. Keep the cheat GUI visible at the bottom of your screen.

**ESP not showing**
Make sure CS2 is in Windowed mode, not fullscreen. Restart the game after changing display settings.

**High CPU usage**
Adjust the FPS limiter in settings to reduce system load.

## Legal Notice

This software is for educational purposes and reverse engineering research. Using cheats in online games violates terms of service and may result in account penalties. 

You assume all responsibility for any consequences. I, the author, and any contributors are not liable for account bans, legal issues, or other problems arising from use of this software.

## License

MIT License with Commercial Restriction

Copyright (c) 2025 CS2 External Cheat

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software with certain restrictions, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

**RESTRICTION**: You are NOT permitted to use this source code, as-is or by building upon it, to sell or have any financial gain from this software or any derivative works.

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Built With

- **PyMeow** - Memory reading and overlay framework
- **DearPyGui** - Interface and controls  
- **Python 3.11** - Core language

## Contributing

Educational contributions welcome. Commercial use is prohibited under the license terms.

---

*Not affiliated with Valve Corporation or Counter-Strike 2*



