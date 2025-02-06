import tkinter as tk
import random
from PIL import Image, ImageTk

# Create Splash Screen
splash_root = tk.Tk()

# Adjust size
splash_root.attributes('-fullscreen',True)

# Load and display image
image = Image.open("logo.jpg")
image = image.resize((splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()))
photo = ImageTk.PhotoImage(image)
label = tk.Label(splash_root, image=photo)
label.pack()


def main():
    splash_root.destroy()
    # Create the main window
    root = tk.Tk()
    
    root.state("zoomed")
    
        

    

if __name__ == "__main__":
    # splash screen
    splash_root.after(3000, main)
    # Start the GUI event loop
    tk.mainloop()