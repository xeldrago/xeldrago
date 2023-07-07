import tkinter as tk
import random

# Possible responses
responses = ["Yes", "No", "Maybe", "Definitely not"]


def shake_ball():
    response = random.choice(responses)
    response_label.config(text=response)


# Create the main window
window = tk.Tk()
window.title("Magic 8 Ball")

# Create the response label
response_label = tk.Label(window, text="")
response_label.pack(pady=20)

# Create the shake button
shake_button = tk.Button(window, text="Shake the Ball", command=shake_ball)
shake_button.pack()

# Run the application
window.mainloop()
