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
- **Color-Based Detection**: Detects red and white/transparent colors for reliable notifier detection
- **Adjustable Confidence Threshold**: Fine-tune detection sensitivity (0.0-1.0)
- **Customizable Spam Duration**: Set how long to spam click (in seconds, whole numbers only)
- **Inventory Slot Management**: Configure rod and non-rod inventory slots
- **Persistent Settings**: All settings are automatically saved and loaded
- **No Flicker**: Uses MSS for ultra-fast, flicker-free screenshot capture

## How to Use

### Initial Setup
1. Run `AO-Fishing-Macro.exe`
2. Press **F2** to set the Notifier Area (adjust the red box to cover where the notifier appears)
3. Click **"Set Fish Point"** button and click where you want to cast your fishing rod
4. Configure your inventory slots:
   - **Rod Slot**: The slot where your fishing rod is located (1-9, 0)
   - **Not Rod Slot**: Any other slot (used to switch equipment)
5. Set the **Spam Click Duration** (how many seconds to spam click when notifier appears)
6. Set the **Detection Confidence** threshold (0.8 recommended, lower if notifier not detected)

### Starting the Macro
1. Press **F1** to start fishing
2. The window will minimize
3. The macro will automatically:
   - Switch to not-rod slot
   - Switch to rod slot
   - Click the fish point to cast
   - Monitor for red and white colors in the notifier area
   - Spam click when detected above confidence threshold
   - Repeat the cycle

### Keyboard Shortcuts
- **F1**: Start/Stop Fishing
- **F2**: Toggle Notifier Area Selection
- **F3**: Close Application

## Detection Method
The macro uses **color-based detection** to find the fishing notifier:
- **Red Detection**: Looks for red pixels (the exclamation mark)
- **White Detection**: Looks for white/light gray pixels with a range to handle transparency
- **Combined Confidence**: Both colors must be present for detection

This is more reliable than template matching because it handles:
- Semi-transparent notifier backgrounds
- Slight color variations
- Different screen brightness levels

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
├── build_exe.spec           # PyInstaller specification file
├── build.bat                # Build script for Windows
├── requirements.txt         # Python dependencies
├── AO-Settings.json         # Auto-generated settings file
└── dist/
    └── AO-Fishing-Macro.exe # Compiled executable
```

**Note**: `image.png` is no longer required - the macro uses color-based detection instead of template matching.

## Notes
- The executable is standalone and portable
- Settings are saved in `AO-Settings.json` in the same folder as the .exe
- Uses color-based detection (red + white) instead of template matching
- Default confidence threshold is 0.8 (adjust lower if detection is too strict)
- The macro uses MSS for fast, flicker-free screenshot capture

## Troubleshooting
**Notifier not being detected:**
1. Make sure the notifier area (F2) fully contains the notifier when it appears
2. Lower the confidence threshold to 0.5 or 0.6 for more lenient detection
3. Adjust game brightness/contrast settings if needed
4. Check the console output for detection confidence values

**False detections:**
- Increase the confidence threshold to 0.9
- Make the notifier area smaller to exclude other UI elements with red/white colors

## Made by @aauto1