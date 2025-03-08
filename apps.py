import customtkinter as ctk
from PIL import Image
from UDP.changeSettings import changeSettings
from UDP.UDP_Client import broadcastEquipmentId
from database import Database
from resource_loader import ResourceLoader
from components import *

class Splash(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        splash_width = 600
        splash_height = 400
        self.overrideredirect(True)
        self.geometry(f"{splash_width}x{splash_height}+" + str(self.winfo_screenwidth() // 2 - 200) + "+" + str(self.winfo_screenheight() // 2 - 200)) # Center the splash screen
        loader = ResourceLoader()
        image = loader.load_image("logo.jpg")
        photo = ctk.CTkImage(image, size=(splash_width,splash_height))
        label = ctk.CTkLabel(self,text = "", image=photo,width=splash_width, height=splash_height)
        label.pack()

class PlayerEntry(ctk.CTk):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = master
        self.withdraw()
        self.player_list_g = master.player_list_g
        self.player_list_r = master.player_list_r

        # Initialize ResourceLoader and load the config file path
        loader = ResourceLoader()
        self.config_path = loader.load_json("UDP/config.json")

        # Initialize database connection
        self.db = Database(self.config_path)
      
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
        self.button = ctk.CTkButton(self, text="Change UDP Port", command=self.updatePort)
        self.button.grid(row=1, column=0, pady=10, padx=10, sticky="s")

        self.start = ctk.CTkButton(self, text="F5 Start Game", command=self.startGame)
        self.start.grid(row=1, column=1, pady=10, padx=10, sticky="s")
    
    def updatePort(self):
        port = portPopup(self)
        values = port.get_input()

    def settingsReceived(self, event):
        #get values
        setting = self.setting.get()
        value = self.value.get()

        changeSettings(setting, value)

        self.unlock()
        self.popup.destroy()

    def queryID(self,playerId):
        self.db.connect()
        codename = self.db.get_codename(playerId)
        self.db.close()

        if codename is None:
            codename = self.askForCodename()

        return codename
        
    def clearRow(self, row, color):
        if(color == "Red"):
            self.player_list_r[row] = [None,None,None]
        else:
            self.player_list_g[row] = [None,None,None]

    def storeID(self,playerID,color,row):
        if(color == "Red"):
            self.player_list_r[row][0] = playerID
        else:
            self.player_list_g[row][0] = playerID
    
    def storeCodename(self,codename, color, row):
        if(color == "Red"):
            team = self.player_list_r
        else:
            team = self.player_list_g
            
        team[row][1] = codename

        self.db.connect()
        self.db.add_player(team[row][0], codename)
        self.db.close()

        if(not team[row][2]):
            self.askForEquipmentID(color, row)

    def storeEquipmentID(self, equipmentID, color, row):
        if(color == "Red"):
            self.player_list_r[row][2] = equipmentID
        else:
            self.player_list_g[row][2] = equipmentID

    # Handles updating codenames in the database
    def handleUpdateCodename(self, playerId, newCodename):
        self.db.connect()
        self.db.update_codename(playerId, newCodename)
        self.db.close()

    def askForCodename(self):
        dialog = ctk.CTkInputDialog(text="Codename:", title="Could not Find Codename in Database\nPlease Enter One")
        codename = dialog.get_input()

        while(codename and codename == ""):
            dialog = ctk.CTkInputDialog(text="Codename:", title="Codename Entered was not Valid\nPlease Enter a Valid One")
            codename = dialog.get_input()

        if(not codename):
            return None

        return codename

    def askForEquipmentID(self, color, row):
        dialog = ctk.CTkInputDialog(text="Equipment ID:", title="Please Enter Your Equipment ID")
        equipmentID = dialog.get_input()

        while(equipmentID and (equipmentID == "" or not equipmentID.isnumeric())):
            dialog = ctk.CTkInputDialog(text="Equipment ID:", title="The ID You Entered Was Not Valid")
            equipmentID = dialog.get_input()
        
        if(not equipmentID):
            self.clearRow(row, color)
            return

        self.storeEquipmentID(equipmentID, color, row)

        # Broadcast the equipment id over UDP
        broadcastEquipmentId(equipmentID)

    def startGame(self):
        self.main.switchPlayAction()

class PlayAction(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = ctk.CTkLabel(self, text="New Menu")
        self.placeholder.grid(row=0,column=0,padx=30,pady=30)
        