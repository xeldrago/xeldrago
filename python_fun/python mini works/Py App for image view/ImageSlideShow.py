import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables
stop_slideshow = False
paused = False
current_index = 0
image_files = []
interval = 4  # Time interval in seconds


def show_controls():
    """Display the controls information."""
    control_window = tk.Toplevel(window)
    control_window.title("Controls")
    control_label = tk.Label(control_window, text="""
Controls:
- Right Arrow / Up Arrow: Move forward to the next image
- Left Arrow / Down Arrow: Move backward to the previous image
- Spacebar: Pause/Unpause the slideshow
""", justify="left")
    control_label.pack(padx=10, pady=10)


def display_image(label):
    """Function to display the current image."""
    global current_index, image_files

    image_file = image_files[current_index]
    image_path = os.path.join(folder_path, image_file)
    image = Image.open(image_path)

    # Resize the image while preserving the aspect ratio
    width, height = image.size
    new_width = 1000
    new_height = 1000
    image = image.resize((new_width, new_height), Image.LANCZOS)

    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo


def next_image(label):
    """Move to the next image and update display."""
    global current_index, image_files, interval, paused

    if not paused:
        current_index = (current_index + 1) % len(image_files)
        display_image(label)
        label.after(interval * 1000, lambda: next_image(label))


def previous_image(label):
    """Move to the previous image and update display."""
    global current_index, image_files, paused

    if not paused:
        current_index = (current_index - 1) % len(image_files)
        display_image(label)


def scroll_images(folder_path, interval):
    global stop_slideshow, paused, current_index, image_files

    image_files = [
        f
        for f in os.listdir(folder_path)
        if any(
            f.lower().endswith(ext)
            for ext in ['.jpg', '.png', '.gif', '.jpeg', '.jiff']
        )
    ]

    if not image_files:
        print("No image files found in the folder.")
        return

    # Create a window to display the images
    image_window = tk.Toplevel()
    label = tk.Label(image_window)
    label.pack()

    def key_pressed(event):
        global paused

        if event.keysym in ['Right', 'Up']:
            paused = True
            next_image(label)
            paused = False  # Resume slideshow after manual navigation
        elif event.keysym in ['Left', 'Down']:
            paused = True
            previous_image(label)
            paused = False  # Resume slideshow after manual navigation
        elif event.keysym == 'space':
            paused = not paused
            if not paused:  # Resume slideshow when unpaused
                next_image(label)

    image_window.bind("<Key>", key_pressed)
    image_window.focus_set()

    display_image(label)  # Display the first image
    label.after(interval * 1000, lambda: next_image(label))


def browse_folder():
    global stop_slideshow, paused, current_index, folder_path
    stop_slideshow = False  # Reset the stop flag
    paused = False  # Reset the paused flag
    current_index = 0  # Reset the current index
    folder_path = filedialog.askdirectory()
    if folder_path:
        scroll_images(folder_path, interval)


def stop_show():
    global stop_slideshow
    stop_slideshow = True  # Set the stop flag to True to stop the slideshow


# Create Tkinter application window
window = tk.Tk()

# Add a button to browse for the input folder
browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.pack()

# Add a button to show controls
controls_button = tk.Button(
    window, text="Show Controls", command=show_controls)
controls_button.pack()

# Add a button to close the slideshow
close_button = tk.Button(window, text="Close Slideshow", command=stop_show)
close_button.pack()

# Start the Tkinter event loop
window.mainloop()
