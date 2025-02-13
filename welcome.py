import tkinter as tk
from tkinter import*

t = tk.Tk()

#set window size
t.geometry('1400x1080')

# Add title to screen
t.title("WELCOME SCREEN")


#set background to grey
canvas = tk.Canvas(t, bg='gray17')
canvas.pack(fill=tk.BOTH, expand=True)

#set background to picture
#bg = PhotoImage(file = "initial_bg.png")
#canvas = tk.Canvas(t, width = 1400, height = 1080)
#canvas.pack(fill="both", expand = True)
#Create the canvas
#canvas.create_image(0,0, image=bg, anchor = "nw")

#box height and width
box_width = 1000
box_height = 800

def edit_game_fn():
    #write code to edit the game
    print("Edit game called")

def game_parameters():
    #Code for game parameters
    print("Game parameters called")

def start_game_fn():
    #Code to start the game
    print("Start fn called")

def pre_entered_fn():
    #Code for preEntered game
    print("PreEntered fn called")

def f7_fn():
    #code for F7
    print("F7 called")

def view_game_fn():
    #Code for view game
    print("View game called")

def flick_sync_fn():
    #Code for flick sync
    print("Flick Sync Fn called")

def clear_game_fn():
    #code for clear game
    print("Clear game fn")

def create_buttons():
    #instert buttons on bottom of the screen
    edit_game = tk.Button(t, text = "F1\nEdit Button", font = ("Arial", 8), bg = 'black', fg = 'grey', command = edit_game_fn)
    edit_game.place(relx = 0.05, rely = .95, anchor = 'sw', width = 80, height = 80)

    game_param = tk.Button(t, text = "F2\nGame\nParameters\n", font = ("Arial", 8), bg = 'black', fg = 'grey', command = game_parameters)
    game_param.place(relx = 0.13, rely = .95, anchor = 'sw', width = 80, height = 80)

    start_game = tk.Button(t, text = "\nF3\nStart Game\n", font = ("Arial", 8), bg = 'black', fg = 'grey', command = start_game_fn)
    start_game.place(relx = 0.21, rely = .95, anchor = 'sw', width = 80, height = 80)

    pre_entered = tk.Button(t, text = "\nF5\nPreEntered\nGames", font = ("Arial", 8), bg = 'black', fg = 'grey', command = pre_entered_fn)
    pre_entered.place(relx = 0.36, rely = .95, anchor = 'sw', width = 80, height = 80)

    f7 = tk.Button(t, text = "\nF7\n", font = ("Arial", 8), bg = 'black', fg = 'grey', command = f7_fn)
    f7.place(relx = 0.51, rely = .95, anchor = 'sw', width = 80, height = 80)

    view_game = tk.Button(t, text = "\nF8\nView\nGame", font = ("Arial", 8), bg = 'black', fg = 'grey', command = view_game_fn)
    view_game.place(relx = 0.60, rely = .95, anchor = 'sw', width = 80, height = 80)

    flick_sync = tk.Button(t, text = "\nF10\nFlick\nSync", font = ("Arial", 8), bg = 'black', fg = 'grey', command = flick_sync_fn)
    flick_sync.place(relx = 0.75, rely = .95, anchor = 'sw', width = 80, height = 80)

    clear_game = tk.Button(t, text = "\nF12\nClear\nGmae", font = ("Arial", 8), bg = 'black', fg = 'grey', command = clear_game_fn)
    clear_game.place(relx = 0.90, rely = .95, anchor = 'sw', width = 80, height = 80)


    


#Create red side
red = tk.Frame(t, bg='red', width = box_width, height = box_height, padx = 20, pady = 20)
red.place(relx = 0.3, rely = 0.5, anchor = "center") #sets at center left 

#Add red label
red_team = tk.Label(red, text = "RED TEAM", font=("Arial", 20, "bold"), bg= 'red', fg = 'white')
red_team.pack(side = "top", pady = 10)

#Room for red table
red_team_table = tk.Frame(red, bg='black')
red_team_table.pack(fill = "both", expand = True, pady = 10)




#Create Green Side
green = tk.Frame(t, bg='green',width = box_width, height = box_height, padx = 20, pady = 20)
green.place(relx = 0.7, rely = 0.5, anchor = "center") #center right

#Add green label
green_team = tk.Label(green, text = "GREEN TEAM", font=("Arial", 20, "bold"), bg= "green", fg = "white")
green_team.pack(side = "top", pady = 10)

#Room for green table
green_team_table = tk.Frame(green, bg = 'black') 
green_team_table.pack(fill = "both", expand = True, pady = 10)




#create 12x3 table
def create_table(frame):
    for row in range(13):
        for col in range(3):
            if col == 0:
                cell = tk.Label(frame, text=row, font=("Arial", 12), bg='black', fg='white',
                               borderwidth=2, relief="solid", highlightthickness=1, highlightbackground="grey70")
            elif col == 1:
                cell = tk.Label(frame, text="name", font=("Arial", 12), bg='black', fg='white',
                                 borderwidth=2, relief="solid", highlightthickness=1, highlightbackground="grey70")
            elif col == 2:
                cell = tk.Label(frame, text="Number", font=("Arial", 12), bg='black', fg='white',
                                borderwidth=2, relief="solid", highlightthickness=1, highlightbackground="grey70")
            cell.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        frame.grid_columnconfigure(col, weight=1)

#create
create_table(red_team_table)
create_table(green_team_table)
create_buttons()

t.mainloop()
