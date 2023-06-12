import tkinter as tk
from tkinter import filedialog
import pyautogui
import cv2
import threading
import numpy as np
import screeninfo
from PIL import ImageTk, Image
from PIL import ImageOps
from tkinter import messagebox

def togglez_theme():
    current_theme = root["bg"]
    if current_theme == "white":
        root.config(bg="black")
    else:
        root.config(bg="white")   


class ScreenRecorder:
    def __init__(self):
        self.is_recording = False
        self.is_paused = False
        self.video_writer = None
        self.output_file = None
        
        

    def start_recording(self):
        self.is_recording = True
        self.is_paused = False

        # Get the screen dimensions for the mainwindow screen of app
        screen_info = screeninfo.get_monitors()[0]
        screen_width = screen_info.width
        screen_height = screen_info.height

        # Ask the user for the save location in their local storage 
        self.output_file = filedialog.asksaveasfilename(defaultextension=".avi")

        if self.output_file:
            # Create a video writer
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            self.video_writer = cv2.VideoWriter(self.output_file, fourcc, 20.0, (screen_width, screen_height))

            # Start recording in a separate thread
            recording_thread = threading.Thread(target=self._record_screen)
            recording_thread.start()
            status_label.config(text="Recording started...")
        else:
            status_label.config(text="Recording canceled")

    def _record_screen(self):
        while self.is_recording:
            if not self.is_paused:
                # Capture the screen shot of current window
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                # Write the frame to the video file
                self.video_writer.write(frame)

                # Delay to control the frame rate
                time.sleep(0.05)

    def pause_recording(self):
        if self.is_recording and not self.is_paused:
            self.is_paused = True
            status_label.config(text="Recording paused...")

    def resume_recording(self):
        if self.is_recording and self.is_paused:
            self.is_paused = False
            status_label.config(text="Recording resumed...")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.video_writer.release()
            status_label.config(text="Recording stopped...")

            if self.output_file:
                status_label.config(text="Video saved as '{}'".format(self.output_file))
            else:
                status_label.config(text="Video saving canceled")


def start_recording():
    screen_recorder.start_recording()


def pause_recording():
    screen_recorder.pause_recording()


def resume_recording():
    screen_recorder.resume_recording()


def stop_recording():
    screen_recorder.stop_recording()


def capture_screenshot():
    root.iconify()
    # Get the screen dimensions
    screen_info = screeninfo.get_monitors()[0]
    screen_width = screen_info.width
    screen_height = screen_info.height

    # Capture the screenshot
    screenshot = pyautogui.screenshot()

    # Ask the user for the save location
    save_path = filedialog.asksaveasfilename(defaultextension=".png")

    if save_path:
        # Save the screenshot in the desired path
        screenshot.save(save_path)

        # Load the captured screenshot in the mainwindow
        screenshot_image = ImageTk.PhotoImage(screenshot)

        # Update the screenshot label in the main window
        screenshot_label.configure(image=screenshot_image)
        screenshot_label.image = screenshot_image

        status_label.config(text="Screenshot saved as '{}'".format(save_path))
    else:
        status_label.config(text="Screenshot capture canceled")





            



root = tk.Tk()
root.title("Screen Recorder")
root.geometry("300x150")
root.config(bg="white")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a "Screen Video Record" menu
record_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Screen Video Record", menu=record_menu)

# Add the video recording commands to the "Screen Video Record" menu
record_menu.add_command(label="Start", command=start_recording)
record_menu.add_command(label="Pause", command=pause_recording)
record_menu.add_command(label="Resume", command=resume_recording)
record_menu.add_command(label="Stop", command=stop_recording)

# Create a "Capture Screenshot" menu
capture_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Capture Screenshot", menu=capture_menu)

# Add the screenshot capture command to the "Capture Screenshot" menu
capture_menu.add_command(label="Capture", command=capture_screenshot)

# Create a "Crop" menu
"""crop_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Crop", menu=crop_menu)

# Add the screenshot crop command to the "Crop" menu
crop_menu.add_command(label="Crop Screenshot", command=crop_screenshot)"""

# Create a "Save" menu
"""save_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Save", menu=save_menu) """

# Add the cropped screenshot save command to the "Save" menu
#save_menu.add_command(label="Save Cropped Screenshot", command=save_cropped_screenshot)

# Create a status label
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Create a screen recorder instance
screen_recorder = ScreenRecorder()

# Create a label to display the screenshot
screenshot_label = tk.Label(root)
screenshot_label.pack()

root.mainloop()