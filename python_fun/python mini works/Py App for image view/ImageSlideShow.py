import os
import time
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

# Global flag to stop the slideshow
stop_slideshow = False


def scroll_images(folder_path, interval):
    global stop_slideshow

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

    for image_file in image_files:
        if stop_slideshow:
            break

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

        image_window.update()  # Update the event loop
        time.sleep(interval)  # Wait for the interval before proceeding

    image_window.destroy()  # Close the window after the slideshow ends


def browse_folder():
    global stop_slideshow
    stop_slideshow = False  # Reset the stop flag
    folder_path = filedialog.askdirectory()
    if folder_path:
        interval = 4  # Time interval in seconds
        # Replace forward slashes with backslashes
        folder_path = folder_path.replace('/', '\\')
        scroll_images(folder_path, interval)


def stop_show():
    global stop_slideshow
    stop_slideshow = True  # Set the stop flag to True to stop the slideshow


# Create Tkinter application window
window = tk.Tk()

# Add a button to browse for the input folder
browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.pack()

# Add a button to close the slideshow
close_button = tk.Button(window, text="Close Slideshow", command=stop_show)
close_button.pack()

# Start the Tkinter event loop
window.mainloop()
