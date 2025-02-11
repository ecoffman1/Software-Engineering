import customtkinter as ctk
from PIL import Image, ImageTk
import time

class Splash(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        splash_width = 600
        splash_height = 400
        self.overrideredirect(True)
        self.geometry(f"{splash_width}x{splash_height}+" + str(self.winfo_screenwidth() // 2 - 200) + "+" + str(self.winfo_screenheight() // 2 - 200)) # Center the splash screen
        image = Image.open("logo.jpg")
        photo = ctk.CTkImage(image, size=(splash_width,splash_height))
        label = ctk.CTkLabel(self,text = "", image=photo,width=splash_width, height=splash_height)
        label.pack()

class TeamFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)

        self.title = title

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=2)

        self.widgets = []
        for i in range(15):
            row = [None, None]
            row[0] = ctk.CTkEntry(self,width = 20, placeholder_text="")
            row[0].grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            row[1] = ctk.CTkTextbox(self, height=10)
            row[1].grid(row=i+1, column=1, padx=10, pady=(10, 0), sticky="w")
            self.widgets.append(row)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()
      
    def splash(self):
        self.splash = Splash(self)

    def player_entry(self):
        self.state("zoomed")
        self.splash.destroy()

        # setup UI structure
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.red = TeamFrame(self, "Red")
        self.red.grid(row=0, column=0, padx=10, pady=(10, 0),sticky="e")

        self.green = TeamFrame(self, "Green")
        self.green.grid(row=0, column=1, padx=10, pady=(10, 0),sticky="w")

        
        


app = App()
app.splash()
app.after(3000, app.player_entry)
app.mainloop()