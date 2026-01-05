# Arcane Odyssey Fishing Macro

## Overview
An automated fishing macro for Arcane Odyssey that detects the fishing notifier and performs spam clicking.

## How to Build the Executable

### Method 1: Use the build script (Windows)
1. Double-click `build.bat`
2. Wait for the build to complete
3. Find the executable in the `dist` folder

### Method 2: Manual build
```bash
# Install dependencies
pip install -r requirements.txt

# Build the executable
python -m PyInstaller build_exe.spec --clean
```

The compiled executable will be located in: `dist\AO-Fishing-Macro.exe`

## Features
- **Image Template Matching**: Uses OpenCV to detect the fishing notifier with 80%+ confidence
- **Customizable Spam Duration**: Set how long to spam click (in seconds, whole numbers only)
- **Inventory Slot Management**: Configure rod and non-rod inventory slots
- **Persistent Settings**: All settings are automatically saved and loaded
- **No Flicker**: Uses MSS for ultra-fast, flicker-free screenshot capture
- **Single Executable**: The notifier image is bundled inside the .exe file

## How to Use

### Initial Setup
1. Run `AO-Fishing-Macro.exe`
2. Press **F2** to set the Notifier Area (adjust the red box to cover where the notifier appears)
3. Click **"Set Fish Point"** button and click where you want to cast your fishing rod
4. Configure your inventory slots:
   - **Rod Slot**: The slot where your fishing rod is located (1-9, 0)
   - **Not Rod Slot**: Any other slot (used to switch equipment)
5. Set the **Spam Click Duration** (how many seconds to spam click when notifier appears)

### Starting the Macro
1. Press **F1** to start fishing
2. The window will minimize
3. The macro will automatically:
   - Switch to not-rod slot
   - Switch to rod slot
   - Click the fish point to cast
   - Monitor for the notifier image
   - Spam click when detected with 80%+ confidence
   - Repeat the cycle

### Keyboard Shortcuts
- **F1**: Start/Stop Fishing
- **F2**: Toggle Notifier Area Selection
- **F3**: Close Application

## Template Image
The fishing notifier template (`image.png`) is bundled inside the executable. If you need to update it:
1. Replace `image.png` in the source folder
2. Rebuild the executable using `build.bat`

## Requirements (for building from source)
- Python 3.7+
- keyboard
- numpy
- pyautogui
- mss
- opencv-python
- pyinstaller

## File Structure
```
arcane-odyssey-fishing/
├── main.py                  # Main application code
├── image.png                # Notifier template image (bundled in exe)
├── build_exe.spec           # PyInstaller specification file
├── build.bat                # Build script for Windows
├── requirements.txt         # Python dependencies
├── AO-Settings.json         # Auto-generated settings file
└── dist/
    └── AO-Fishing-Macro.exe # Compiled executable
```

## Notes
- The executable is standalone and portable
- Settings are saved in `AO-Settings.json` in the same folder as the .exe
- The template image is embedded in the .exe during compilation
- Confidence threshold is set to 0.8 (80%) for reliable detection
- The macro uses MSS for fast, flicker-free screenshot capture

## Made by @aauto1