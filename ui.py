import customtkinter as ctk
from PIL import Image, ImageTk
from UDP.changeSettings import changeSettings
from database import Database

def query(id):
    if(id == 1):
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
        self.validating = None

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
            row[1] = ctk.CTkLabel(self, width = 200, height=30, fg_color="White", text_color="Black",text="")
            row[1].grid(row=i+1, column=2,padx=(0,10), pady=5, sticky="ne")
            self.widgets.append(row)

    def validate(self, event):
        box = event.widget
        id = box.get()
        if(not id.isnumeric()):
            row = self.findRow(id)
            self.widgets[row][1].configure(text="")
            self.master.clear(row,self.bg_color)
            box.delete(0,999)
            return
        
        response = self.master.store_query(id,self.bg_color)

        if(response == ""):
            return
        
        for i in range(len(self.widgets)):
            if(self.widgets[i][0].get() == id):
                self.widgets[i][1].configure(text=response)
        return "break"

    def lock(self):
        for i in range(len(self.widgets)):
            self.widgets[i][0].configure(state="disabled")
    
    def unlock(self):
        for i in range(len(self.widgets)):
            self.widgets[i][0].configure(state="normal")
    
    def findRow(self, id):
        for i in range(len(self.widgets)):
            if(self.widgets[i][0].get() == id):
                return i
        return -1
    
    def set(self, index, value):
        self.widgets[index][1].configure(text=value)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()
        self.player_list_g = [[None,None] for i in range(15)]
        self.player_list_r = [[None,None] for i in range(15)]
        self.popup = None
        
        self.curid = None

        # Initialize database connection
        self.db = Database()
        self.db.connect()

    def lock(self):
        self.button.configure(state="disabled")
        self.red.lock()
        self.green.lock()
    
    def unlock(self):
        self.button.configure(state="normal")
        self.red.unlock()
        self.green.unlock()
      
    def splash(self):
        self.splash = Splash(self)

    def player_entry(self):
        self.state("normal")
        self.splash.destroy()

        # setup UI structure
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.red = TeamFrame(self, "Red")
        self.green = TeamFrame(self, "Green")

        self.red.grid(row=0, column=0,sticky="e")
        self.green.grid(row=0, column=1,sticky="w")
        
        # Create and place the button
        self.button = ctk.CTkButton(self, text="Change UDP Port", command=self.on_button_click)
        self.button.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="sew")

    def on_button_click(self):
        changeSettings()
    


    def store_query(self,id,color):
        #TODO Joey this should be a query method called from self.db that returns the codename if there  is one or an empty string if there isnt
        response = query(id)
        if(len(response) > 0):
            player = (id, response)

            #TODO Joey I keep getting an error that the cursor is none for the add_player method fixed issue of being called twice
            #self.db.add_player(id, response)

            if color == "Red":
                self.player_list_r.append(player)
            else:
                self.player_list_g.append(player)
            return response
        else:
            self.curid = id
            self.askForCodename()
            return ""
        

    def clear(self, row, color):
        if(color == "Red"):
            self.player_list_r[row] = [None,None]
        else:
            self.player_list_g[row] = [None,None]

    def store_id(self,id):
        red_index = self.red.findRow(id)
        green_index = self.green.findRow(id)

        if(red_index > -1):
            self.player_list_r[red_index][0] = id
        if(green_index > -1):
            self.player_list_g[green_index][0] = id
    
    def store_codename(self,id, codename):
        red_index = self.red.findRow(id)
        green_index = self.green.findRow(id)

        if(red_index > -1):
            self.player_list_r[red_index][0] = id
            self.player_list_r[red_index][1] = codename
            self.red.set(red_index, codename)
        if(green_index > -1):
            self.player_list_g[green_index][0] = id
            self.player_list_g[green_index][1] = codename
            self.green.set(green_index, codename)

    def askForCodename(self):
        if(self.popup != None):
            return
        
        #Lock input for app
        self.lock()

        #Frame for popup
        self.popup = ctk.CTkFrame(self)
        self.popup.place(relx = .5, rely = .5, anchor = "center")
        
        #Instructions
        self.popup_instructions = ctk.CTkLabel(self.popup,width = 10, text="No codename was found for this id,\n please enter one")
        self.popup_instructions.grid(row = 0, column = 0, padx = 10, pady = 10)

        #Entrybox for codename
        self.popup_entry = ctk.CTkEntry(self.popup,width = 100, height=30,placeholder_text="",corner_radius=0, fg_color="White", text_color="Black")
        self.popup_entry.bind("<Return>", self.codenameRecieved)
        self.popup_entry.grid(row = 1, column = 0, pady=10)
        self.popup_entry.focus_force()
        
    def codenameRecieved(self, event):
        codename = event.widget.get()
        self.store_codename(self.curid,codename)
        print(self.player_list_g)
        print(self.player_list_r)
        #TODO Joey we need to store the self.curid and codename in the database
        self.unlock()
        self.popup.destroy()
        self.popup = None



app = App()
app.splash()
app.after(3000, app.player_entry)
app.mainloop()
