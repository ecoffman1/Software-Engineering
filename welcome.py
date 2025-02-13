import tkinter as tk
from tkinter import*
import random
t = tk.Tk()

#Set window size
t.geometry('1400x1080')

# Add title to screen
t.title("WELCOME SCREEN")

#Set background
bg = PhotoImage(file = "background.png")
canvas = tk.Canvas(t, width = 1400, height = 1080)
canvas.pack(fill="both", expand = True)

#Create the canvas
canvas.create_image(0,0, image=bg, anchor = "nw")

#match color with background
#bg_color = "#f0f0f0"

def information(event = None):
    enterned_name = enter_name.get()
    entered_number = enter_number.get()

    if enter_number:
        print(f"Name: {enterned_name}\nNumber: {entered_number}")
    else:
        #make a random number for the person
        random_num = random.randint(1, 1000000)
        print(f"Name: {enterned_name}\nNumber: {random_num}")
        

    # delete the responses
    enter_name.delete(0, END)
    enter_number.delete(0, END)



# Make entry for name and badge number
name = tk.Label(t, text = 'Enter Name:', font=("Arial", 18))
number = tk.Label(t, text = 'Enter Number:', font=("Arial", 18))

# Keep track of the entrys
enter_name = tk.Entry(t, font=("Arial", 12))
enter_number = tk.Entry(t, font=("Arial", 12))

#when they hit the button, call the information function
enter = tk.Button(t, text = 'Enter', command = information, font=("Arial", 18))
t.bind('<Return>', information)

#Exit button for easy exit
exit = tk.Button(t, text = 'Exit' , command = t.destroy, font=("Arial", 18))


# Add to canvas
canvas.create_window(700, 300, window = name)
canvas.create_window(700, 350, window = enter_name)
canvas.create_window(700, 400, window = number)
canvas.create_window(700, 450, window = enter_number)
canvas.create_window(700, 500, window = enter)
canvas.create_window(700, 560, window = exit)

t.mainloop()

