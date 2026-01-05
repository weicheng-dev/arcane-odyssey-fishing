import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import threading
import sys
import numpy as np
import pyautogui
import time
import json
import os
import mss

class FishingMacroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arcane Odyssey Fishing Macro")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Variables to store selected areas
        self.notifier_area = None
        self.fish_point = None
        self.is_selecting = False
        self.selection_type = None

        # Selection box windows
        self.notifier_box = None
        self.point_selector = None

        # Monitoring state
        self.monitoring = False
        self.monitor_thread = None

        # Rod slot variables
        self.rod_slot = tk.StringVar(value="1")
        self.not_rod_slot = tk.StringVar(value="2")

        # Settings file path
        self.settings_file = "AO-Settings.json"

        # Set up the UI
        self.setup_ui()

        # Center window on screen
        self.center_window()

        # Load saved settings
        self.load_settings()

        # Register hotkeys (after UI is set up)
        self.register_hotkeys()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        # Main title
        title_label = tk.Label(
            self.root,
            text="Arcane Odyssey Fishing Macro",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()

        # Instructions frame
        instructions_frame = tk.LabelFrame(
            self.root,
            text="Keyboard Shortcuts",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )
        instructions_frame.pack(padx=20, pady=10, fill="both")

        shortcuts = [
            ("F1", "Start/Stop Fishing"),
            ("F2", "Toggle Notifier Area Selection"),
            ("F3", "Close Application")
        ]

        for key, description in shortcuts:
            shortcut_frame = tk.Frame(instructions_frame)
            shortcut_frame.pack(fill="x", pady=2)

            key_label = tk.Label(
                shortcut_frame,
                text=key,
                font=("Arial", 10, "bold"),
                width=5,
                anchor="w"
            )
            key_label.pack(side="left", padx=5)

            desc_label = tk.Label(
                shortcut_frame,
                text=description,
                font=("Arial", 10),
                anchor="w"
            )
            desc_label.pack(side="left", padx=5)

        # Status frame
        status_frame = tk.LabelFrame(
            self.root,
            text="Status",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )
        status_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Notifier area status
        notifier_label = tk.Label(
            status_frame,
            text="Notifier Area:",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        notifier_label.grid(row=0, column=0, sticky="w", pady=5)

        self.notifier_status = tk.Label(
            status_frame,
            text="Not set",
            font=("Arial", 10),
            fg="red",
            anchor="w"
        )
        self.notifier_status.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Fish point status
        fish_label = tk.Label(
            status_frame,
            text="Fish Point:",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        fish_label.grid(row=1, column=0, sticky="w", pady=5)

        self.fish_status = tk.Label(
            status_frame,
            text="Not set",
            font=("Arial", 10),
            fg="red",
            anchor="w"
        )
        self.fish_status.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Button to set fish point
        set_fish_button = tk.Button(
            self.root,
            text="Set Fish Point",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=self.start_fish_point_selection,
            cursor="hand2"
        )
        set_fish_button.pack(pady=10)

        # Rod slot selection frame
        slot_frame = tk.LabelFrame(
            self.root,
            text="Inventory Slots (1-9, 0)",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )
        slot_frame.pack(padx=20, pady=10, fill="x")

        # Rod slot dropdown
        rod_frame = tk.Frame(slot_frame)
        rod_frame.pack(side="left", padx=20, expand=True)

        rod_label = tk.Label(
            rod_frame,
            text="Rod Slot:",
            font=("Arial", 10, "bold")
        )
        rod_label.pack(side="left", padx=5)

        rod_dropdown = ttk.Combobox(
            rod_frame,
            textvariable=self.rod_slot,
            values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            state="readonly",
            width=5,
            font=("Arial", 10)
        )
        rod_dropdown.pack(side="left", padx=5)

        # Not rod slot dropdown
        not_rod_frame = tk.Frame(slot_frame)
        not_rod_frame.pack(side="left", padx=20, expand=True)

        not_rod_label = tk.Label(
            not_rod_frame,
            text="Not Rod Slot:",
            font=("Arial", 10, "bold")
        )
        not_rod_label.pack(side="left", padx=5)

        not_rod_dropdown = ttk.Combobox(
            not_rod_frame,
            textvariable=self.not_rod_slot,
            values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            state="readonly",
            width=5,
            font=("Arial", 10)
        )
        not_rod_dropdown.pack(side="left", padx=5)

        # Message label for instructions
        self.message_label = tk.Label(
            self.root,
            text="Setup: F2 (Notifier Area), Set Fish Point\nPress F1 to start fishing!",
            font=("Arial", 9, "italic"),
            fg="gray"
        )
        self.message_label.pack(pady=10)

    def register_hotkeys(self):
        """Register global hotkeys"""
        keyboard.add_hotkey('f1', self.on_f1_start_fishing)
        keyboard.add_hotkey('f2', self.on_f2_set_notifier)
        keyboard.add_hotkey('f3', self.on_f3_exit)

    def on_f1_start_fishing(self):
        """F1: Start/Stop fishing process"""
        print("F1 pressed!")  # Debug message
        if not self.monitoring:
            # Check if all required settings are configured
            if self.notifier_area is None:
                self.update_message("ERROR: Please set the Notifier Area first (F2)")
                messagebox.showwarning("Setup Required", "Please set the Notifier Area first (F2)")
                return
            if self.fish_point is None:
                self.update_message("ERROR: Please set the Fish Point first")
                messagebox.showwarning("Setup Required", "Please set the Fish Point first using the button.")
                return

            # Start fishing
            self.monitoring = True
            self.update_message("Fishing started! Minimizing window...")

            # Minimize the window
            self.root.withdraw()

            # Start fishing thread
            self.monitor_thread = threading.Thread(target=self.fishing_process, daemon=True)
            self.monitor_thread.start()
        else:
            # Stop fishing
            self.monitoring = False
            self.root.deiconify()  # Restore window
            self.update_message("Fishing stopped.")

    def on_f2_set_notifier(self):
        """F2: Toggle notifier area selection box"""
        if self.notifier_box is None:
            # Create the selection box
            self.notifier_box = self.create_selection_box("Notifier Area")
            self.update_message("Adjust the Notifier box, then press F2 again to confirm.")
        else:
            # Save the area and close the box
            self.save_area("notifier")
            self.notifier_box.destroy()
            self.notifier_box = None

    def on_f3_exit(self):
        """F3: Exit application"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.save_settings()
            self.cleanup()
            self.root.quit()
            sys.exit(0)

    def create_selection_box(self, title):
        """Create a draggable and resizable selection box"""
        box = tk.Toplevel(self.root)
        box.overrideredirect(True)  # Remove title bar
        box.attributes('-topmost', True)
        box.attributes('-alpha', 0.5)

        # Default size and position
        screen_width = box.winfo_screenwidth()
        screen_height = box.winfo_screenheight()
        box_width = 300
        box_height = 200
        x = (screen_width - box_width) // 2
        y = (screen_height - box_height) // 2
        box.geometry(f"{box_width}x{box_height}+{x}+{y}")

        # Configure the box appearance
        box.configure(bg='red', highlightthickness=2, highlightbackground='white')

        # Create main content frame
        content = tk.Frame(box, bg='red')
        content.pack(fill='both', expand=True, padx=5, pady=5)

        # Label to show instructions
        label = tk.Label(
            content,
            text=f"{title}\nDrag center to move\nPress F2 to confirm",
            font=("Arial", 9, "bold"),
            bg='red',
            fg='white',
            justify='center'
        )
        label.pack(expand=True)

        # Create resize handles (visible squares in corners and edges)
        handle_size = 15
        handles = {}

        # Corner and edge positions
        positions = {
            'nw': (0, 0),
            'n': ('center', 0),
            'ne': ('right', 0),
            'w': (0, 'center'),
            'e': ('right', 'center'),
            'sw': (0, 'bottom'),
            's': ('center', 'bottom'),
            'se': ('right', 'bottom')
        }

        for pos_name, (x_pos, y_pos) in positions.items():
            handle = tk.Frame(box, bg='white', width=handle_size, height=handle_size, cursor='sizing')
            handle.place(
                x=x_pos if x_pos != 'center' and x_pos != 'right' else None,
                y=y_pos if y_pos != 'center' and y_pos != 'bottom' else None,
                relx=0.5 if x_pos == 'center' else (1.0 if x_pos == 'right' else 0),
                rely=0.5 if y_pos == 'center' else (1.0 if y_pos == 'bottom' else 0),
                anchor='center'
            )
            handles[pos_name] = handle

        # Variables for dragging and resizing
        box._drag_data = {"x": 0, "y": 0, "mode": None}

        def start_drag(event):
            box._drag_data["x"] = event.x_root
            box._drag_data["y"] = event.y_root
            box._drag_data["mode"] = "move"

        def on_drag(event):
            if box._drag_data["mode"] == "move":
                deltax = event.x_root - box._drag_data["x"]
                deltay = event.y_root - box._drag_data["y"]
                x = box.winfo_x() + deltax
                y = box.winfo_y() + deltay
                box.geometry(f"+{x}+{y}")
                box._drag_data["x"] = event.x_root
                box._drag_data["y"] = event.y_root

        def make_resize_handler(direction):
            def start_resize(event):
                box._drag_data["x"] = event.x_root
                box._drag_data["y"] = event.y_root
                box._drag_data["mode"] = f"resize_{direction}"

            def on_resize(event):
                if box._drag_data["mode"] == f"resize_{direction}":
                    deltax = event.x_root - box._drag_data["x"]
                    deltay = event.y_root - box._drag_data["y"]

                    x = box.winfo_x()
                    y = box.winfo_y()
                    width = box.winfo_width()
                    height = box.winfo_height()

                    # Handle each direction
                    if 'e' in direction:
                        width += deltax
                    if 'w' in direction:
                        width -= deltax
                        x += deltax
                    if 's' in direction:
                        height += deltay
                    if 'n' in direction:
                        height -= deltay
                        y += deltay

                    # Minimum size
                    if width < 100:
                        width = 100
                        if 'w' in direction:
                            x = box.winfo_x()
                    if height < 50:
                        height = 50
                        if 'n' in direction:
                            y = box.winfo_y()

                    box.geometry(f"{width}x{height}+{x}+{y}")
                    box._drag_data["x"] = event.x_root
                    box._drag_data["y"] = event.y_root

            return start_resize, on_resize

        # Bind dragging to label
        label.bind("<ButtonPress-1>", start_drag)
        label.bind("<B1-Motion>", on_drag)

        # Bind resize handlers to each handle
        for direction, handle in handles.items():
            start_resize, on_resize = make_resize_handler(direction)
            handle.bind("<ButtonPress-1>", start_resize)
            handle.bind("<B1-Motion>", on_resize)

        return box

    def start_fish_point_selection(self):
        """Start the fish point selection process"""
        if self.point_selector is not None:
            # Already selecting, ignore
            return

        self.update_message("Click anywhere on the screen to set the fish point...")

        # Minimize main window
        self.root.withdraw()

        # Create fullscreen transparent overlay
        self.point_selector = tk.Toplevel(self.root)
        self.point_selector.attributes('-fullscreen', True)
        self.point_selector.attributes('-topmost', True)
        self.point_selector.attributes('-alpha', 0.01)
        self.point_selector.configure(bg='black', cursor='crosshair')

        # Create a label to show instructions
        instruction = tk.Label(
            self.point_selector,
            text="Click anywhere to set Fish Point\nPress ESC to cancel",
            font=("Arial", 16, "bold"),
            bg='black',
            fg='white',
            padx=20,
            pady=20
        )
        instruction.place(relx=0.5, rely=0.05, anchor='n')

        def on_click(event):
            # Save the clicked point
            self.fish_point = (event.x, event.y)
            self.fish_status.config(
                text=f"Set: ({event.x}, {event.y})",
                fg="green"
            )
            self.update_message(f"Fish point set at ({event.x}, {event.y})")
            self.save_settings()  # Auto-save settings

            # Close selector and restore main window
            self.point_selector.destroy()
            self.point_selector = None
            self.root.deiconify()

        def on_escape(event):
            # Cancel selection
            self.update_message("Fish point selection cancelled.")
            self.point_selector.destroy()
            self.point_selector = None
            self.root.deiconify()

        self.point_selector.bind('<Button-1>', on_click)
        self.point_selector.bind('<Escape>', on_escape)

    def save_area(self, area_type):
        """Save the selected area from the box"""
        if area_type == "notifier" and self.notifier_box:
            x = self.notifier_box.winfo_x()
            y = self.notifier_box.winfo_y()
            width = self.notifier_box.winfo_width()
            height = self.notifier_box.winfo_height()

            self.notifier_area = (x, y, x + width, y + height)
            self.notifier_status.config(
                text=f"Set: ({x}, {y}, {x + width}, {y + height})",
                fg="green"
            )
            self.update_message("Notifier area set successfully!")
            self.save_settings()  # Auto-save settings

    def update_message(self, message):
        """Update the message label"""
        self.message_label.config(text=message)

    def save_settings(self):
        """Save current settings to JSON file"""
        settings = {
            "notifier_area": self.notifier_area,
            "fish_point": self.fish_point,
            "rod_slot": self.rod_slot.get(),
            "not_rod_slot": self.not_rod_slot.get()
        }

        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
            print(f"Settings saved to {self.settings_file}")
        except Exception as e:
            print(f"Error saving settings: {str(e)}")

    def load_settings(self):
        """Load settings from JSON file"""
        if not os.path.exists(self.settings_file):
            self.update_message("No saved settings found. Please configure setup.")
            return

        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)

            # Load notifier area
            if settings.get("notifier_area"):
                self.notifier_area = tuple(settings["notifier_area"])
                x1, y1, x2, y2 = self.notifier_area
                self.notifier_status.config(
                    text=f"Set: ({x1}, {y1}, {x2}, {y2})",
                    fg="green"
                )

            # Load fish point
            if settings.get("fish_point"):
                self.fish_point = tuple(settings["fish_point"])
                x, y = self.fish_point
                self.fish_status.config(
                    text=f"Set: ({x}, {y})",
                    fg="green"
                )

            # Load rod slots
            if settings.get("rod_slot"):
                self.rod_slot.set(settings["rod_slot"])
            if settings.get("not_rod_slot"):
                self.not_rod_slot.set(settings["not_rod_slot"])

            self.update_message("Settings loaded successfully!")
            print(f"Settings loaded from {self.settings_file}")
        except Exception as e:
            self.update_message(f"Error loading settings: {str(e)}")
            print(f"Error loading settings: {str(e)}")

    def fishing_process(self):
        """Main fishing process: switch slots, click fish point, wait for notifier, spam click"""
        while self.monitoring:
            try:
                # Step 1: Select not rod slot
                not_rod = self.not_rod_slot.get()
                print(f"Pressing not rod slot: {not_rod}")
                keyboard.press_and_release(not_rod)
                time.sleep(0.3)

                # Step 2: Select rod slot
                rod = self.rod_slot.get()
                print(f"Pressing rod slot: {rod}")
                keyboard.press_and_release(rod)
                time.sleep(0.3)

                # Step 3: Click the fish point to cast
                pyautogui.click(self.fish_point[0], self.fish_point[1])
                time.sleep(1)

                # Step 4: Wait for notifier to appear
                notifier_detected = False

                # Use MSS for faster, flicker-free screenshots
                with mss.mss() as sct:
                    while self.monitoring and not notifier_detected:
                        # Capture the notifier area (fast screenshot with mss)
                        x1, y1, x2, y2 = self.notifier_area
                        monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
                        screenshot = sct.grab(monitor)
                        screenshot_np = np.array(screenshot)

                        # Fast pixel-based detection (mss returns BGRA format)
                        # Looking for white box with red exclamation mark
                        red_mask = (
                            (screenshot_np[:, :, 2] > 150) &  # High red (BGR format)
                            (screenshot_np[:, :, 1] < 100) &  # Low green
                            (screenshot_np[:, :, 0] < 100)    # Low blue
                        )

                        white_mask = (
                            (screenshot_np[:, :, 2] > 200) &
                            (screenshot_np[:, :, 1] > 200) &
                            (screenshot_np[:, :, 0] > 200)
                        )

                        red_pixel_count = np.sum(red_mask)
                        white_pixel_count = np.sum(white_mask)

                        # If both red and white pixels detected (threshold: at least 50 red and 500 white)
                        if red_pixel_count > 50 and white_pixel_count > 500:
                            notifier_detected = True

                            # Step 5: Spam click for 7 seconds at 0.1 second intervals
                            start_time = time.time()
                            while self.monitoring and (time.time() - start_time) < 7:
                                pyautogui.click(self.fish_point[0], self.fish_point[1])
                                time.sleep(0.1)

                            # Step 6: Switch back to not rod slot
                            keyboard.press_and_release(self.not_rod_slot.get())
                            time.sleep(0.3)

                            # Wait before starting next fishing cycle
                            time.sleep(2)
                        else:
                            # Check every 0.1 seconds for faster detection
                            time.sleep(0.1)

            except Exception as e:
                print(f"Error in fishing process: {str(e)}")
                self.update_message(f"Error: {str(e)}")
                time.sleep(1)

    def cleanup(self):
        """Clean up resources before closing"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        keyboard.unhook_all()

def main():
    root = tk.Tk()
    app = FishingMacroGUI(root)

    # Handle window close button
    root.protocol("WM_DELETE_WINDOW", app.on_f3_exit)

    root.mainloop()

if __name__ == "__main__":
    main()
