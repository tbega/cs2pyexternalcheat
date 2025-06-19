# What is this?

A external cheat for CS2, made using python, pymeow, and dearpygui.

# ESP.
- Box ESP.
- Skeleton ESP.
- Line ESP.
- Name ESP.
- Weapon ESP.
- Health ESP.

# Triggerbot.
- Minimum/Maximum delay.
- Visible only.
- Triggerbot key.
- Deathmatch mode.

# Settings.
- Always on top.
- Overlay FPS slider.

# Menu Preview.

![image](https://github.com/user-attachments/assets/b5f2f467-4a16-45a8-ae6f-bf0339bb4aab)   
                                                                                                                       
# Cheat Preview.

![image](https://github.com/user-attachments/assets/88f15664-e4c9-4adf-83e8-69b7b199229b)


# Setup.
- Python installed --- https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe (Direct download link) \ https://www.python.org/downloads/ (Download page)
- Counter-Strike 2 installed

# Installation.

1. Download the zip folder to your computer, then extract it.

2. Run `install.bat`
   - This will automatically install all required dependencies

If the automatic installer doesn't work:
- In the folder containing requirments.txt, open a command prompt.

   `pip install -r requirements.txt` \ pip install psutil pywin32 requests pyMeow dearpygui keyboard pynput

# How to use this?

1. Launch Counter-Strike 2

2. Run the cheat by clicking on main.py, if this does not work, open a command prompt in admin, and navigate to the folder you have main.py in.

If you do not know how to use command prompt to navigate go here:

 **https://www.howtogeek.com/659411/how-to-change-directories-in-command-prompt-on-windows-10/**

3. Type `py main.py`

# Troubleshooting!

>[!IMPORTANT]
If it says pyMeow can't be found, here's what you need to do:

Go to https://github.com/qb-0/PyMeow

Download the latest release. Rename the pyMeow folder to exactly *pymeow*

Right click in the folder, click **"Open In Terminal"** \ For Windows 10 - Open powershell, and cd to the place you have the pymeow folder.

`pip install pymeow*.zip` 

If you get an error

Try:

 `pip install pymeow.zip` 

This should fix the pyMeow error.


# Black screen OR AMD GPU?

From testing, AMD GPU's seem to have a black screen issue when using most overlays (pyMeow included), to fix this I have added a some what compromise. When launching the cheat, click onto the GUI menu, and then click onto CS2. You will have to configure the settings and then drag the menu to the bottom of the screen. I do not know of a way to completely hide the menu while fixing the overlay.

# What if I have a NVIDIA GPU?

For NVIDIA GPU's you should not have this black screen problem, simply uncheck Always On Top in the settings and click the minimize button to completely hide the menu until you need it.


If you encounter the error "Cannot find Main.py module error" make sure you're running the launcher script `main.py` in the same folder where the sub-folder `\cheat` is contained.

--- 
# Other errors.
If you encounter the error "[Launcher] Failed to run Main module: Unexpected error encountered: Process 'cs2.exe' not found" or a command prompt simply flashes for a second not giving you enough time to read:
- Run the main.py script as admin.

---

If you encounter the error "[Skeleton ESP] Error: Unexpected error encountered: 2D Position out of bounds" 
- Make sure your game is Fullscreen Windowed \ Windowed.
- An easy way to make sure your game stays in FS windowed and doesn't switch to windowed, is to launch the game, set it to fullscreen windowed, then close it and relaunch it and not mess with any settings.


# Image Guide

![image](https://github.com/user-attachments/assets/a9a47de5-7496-4887-ad68-2bd16d679c32)

![image](https://github.com/user-attachments/assets/b698b4eb-4da6-41d1-8843-c297169cdebf)

![image](https://github.com/user-attachments/assets/02851483-89fc-4370-8890-de87f3797ca8)

![image](https://github.com/user-attachments/assets/40af647f-d351-4c4f-8f83-2c87ed2d523a)


![image](https://github.com/user-attachments/assets/ac80fd07-0e59-4f7b-a3a7-1e073176d47e)



# Legal Disclaimer.
This software is for educational purposes only. Using cheats in online games violate the game's terms of service and could result in account bans. Use at your own risk. I take no responsiblity for any consequences resulting from the use of this software.


# Credits.
https://github.com/qb-0/PyMeow
https://www.python.org/downloads/
https://github.com/hoffstadt/DearPyGui
https://github.com/gabsroot/Fury [Inspiration]

