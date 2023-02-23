import tkinter as tk

# Create the main window
root = tk.Tk()
root.geometry("200x200")

# Create a label with text to display
label = tk.Label(root, text="FLASH", font=("Arial Bold", 50), bg="black", fg="white")

# Define the flashing function
def flash_label():
    if label['bg'] == 'black':
        label.config(bg='white')
    else:
        label.config(bg='black')
    root.after(1000, flash_label)  # repeat after 1000ms (1 second)

# Start the flashing function
flash_label()

# Pack the label in the window
label.pack(expand=True, fill='both')

# Start the GUI main loop
root.mainloop()
