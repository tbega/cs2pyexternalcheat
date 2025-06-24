# CS2 External Cheat

[![Python 3.11.9](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## Preview

| ESP In-Game | Menu  |
|:----------:|:-----------:|
| ![image](https://github.com/user-attachments/assets/53121c61-97f0-4a6e-9618-f458e5d8ef09) | ![image](https://github.com/user-attachments/assets/0c70db5b-d357-49f1-83eb-fc355799fe23) |


---

## What is this?

This is a free external cheat for CS2. It runs as a separate window (not injected), so it's way safer than most stuff out there. I made it for fun and to help my friend, and it actually works really well.

---

## Features

### Aimbot
- Change FOV and smoothness
- Pick what bones to aim at (head, chest, etc)

### ESP 
- Shows boxes and health on players
- Skeleton esp
- You can set different colors for enemies 
- Visble colors don't work, I will fix it soon

### Triggerbot
- Shoots for you when your crosshair is on someone
- You can set how fast it reacts

### Other Stuff
- You can change FPS and other settings
- Bomb timer (not currently working)

---

## How does it work?

It just reads memory from CS2 and draws an overlay on your screen. No DLLs or injection. You just run it, start CS2, and you're good. As long as you keep the menu open, ESP and everything works.
Also open source and made in python so you can check the code yourself :D

---

## Setup

### You need:
- Windows 10 or 11
- Python 3.11.9 or newer
- CS2 in Windowed or Borderless mode

### How to install
1. Download and unzip everything
2. Run `setup.py` (it installs all the stuff you need)
3. Start CS2
4. Run `launcher.py`

Or just do:
```bash
pip install -r requirements.txt
```

The menu pops up and you can turn stuff on/off or change colors without restarting. 

---

## Problems?

- **"PyMeow not found"**
  - Download it from [here](https://github.com/qb-0/PyMeow) and do `pip install pymeow.zip`

- **Black screen on AMD**
  - AMD is weird with overlays. Try keeping the menu at the bottom of your screen.

- **ESP not working**
  - Make sure CS2 is in Windowed/Borderless. Restart the game if you change display settings. Menu has to be open and on top.

- **High CPU**
  - Lower the FPS in settings.

---

## Legal stuff

This is for learning and messing around. If you use cheats online, you might get banned. That's on you, not me.

---

## License

MIT License, but you can't sell this or use it to make money. That's it.

---

## Built With

- **PyMeow** – for reading memory and overlay
- **PySide6 (Qt)** – for the menu
- **Python 3.11** – the language

## Contributing

If you want to help or add something, go for it. Just don't try to sell it.

---

*Not affiliated with Valve or CS2. This is just for fun.*



