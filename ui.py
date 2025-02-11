import customtkinter as ctk
from PIL import Image, ImageTk
import time

def query(id):
    if(id.isnumeric()):
        return "Player1"
    return ""


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

        if title == "Red":
            self.color = "#591717"
        else:
            self.color = "#0e450e"
        
        self.configure(fg_color = self.color)

        self.title = title
        self.bg_color = title
        self.master = master

        self.title = ctk.CTkLabel(self, text=self.title, corner_radius=6, font=("default",40))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=3)

        self.widgets = []
        for i in range(15):
            row = [None, None]
            num = ctk.CTkLabel(self, width = 20, height=30,text=str(i+1).zfill(2))
            num.grid(row=i+1, column=0,padx=(5,0), pady=5, sticky="ne")
            row[0] = ctk.CTkEntry(self,width = 100, height=30,placeholder_text="",corner_radius=0, fg_color="White", text_color="Black")
            row[0].grid(row=i+1, column=1,padx=(5,0), pady=5, sticky="nw")
            row[0].bind("<FocusOut>", self.validate)
            row[0].bind("<Return>", self.validate)
            row[1] = ctk.CTkLabel(self, width = 200, height=30, fg_color="White", text_color="Black",text="")
            row[1].grid(row=i+1, column=2,padx=(0,10), pady=5, sticky="ne")
            self.widgets.append(row)


    def validate(self, event):
        box = event.widget
        response = self.master.store_query(box.get(),self.bg_color)
        if(len(response) > 0):
            for i in range(len(self.widgets)):
                if(self.widgets[i][0].get() == box.get()):
                    self.widgets[i][1].configure(text=response)
        else:
            box.delete(0, 999)
        





class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()
        self.player_list_g = []
        self.player_list_r = []
      
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
        self.green = TeamFrame(self, "Green")

        self.red.grid(row=0, column=0,sticky="e")
        self.green.grid(row=0, column=1,sticky="w")

    def store_query(self,id,color):
        response = query(id)
        if(len(response) > 0):
            player = (id, response)
            if color == "Red":
                self.player_list_r.append(player)
            else:
                self.player_list_g.append(player)
            return response
        else:
            self.askForCodename()
            return ""

    
    def askForCodename(self):
        pass


        
        


app = App()
app.splash()
app.after(3000, app.player_entry)
app.mainloop()