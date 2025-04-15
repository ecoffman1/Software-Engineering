import customtkinter as ctk
import re
import os
from UDP.getSettings import getSettings

ctk.set_appearance_mode("dark")

image_path = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(image_path, "settings.xbm")

class TeamFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.validating = None

        if title == "Red":
            self.color = "#591717"
            self.text_color = "White"
            self.font_style = ("Arial", 20, "bold")
        else:
            self.color = "#0e450e"
            self.text_color = "White"
            self.font_style = ("Arial", 20, "bold")
        
        self.configure(fg_color = self.color, corner_radius=0)
        self.title = title
        self.bg_color = title
        self.master = master

        self.title_label = ctk.CTkLabel(
            self, 
            text=self.title.upper(),  
            font=self.font_style,
            text_color = self.text_color,
            anchor="center",  
            padx=20,  
            pady=10
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=3)

        self.currentPlayers = []
        self.widgets = []
        for i in range(15):
            row = [None, None]
            num = ctk.CTkLabel(self, width = 20, height=30,text=str(i+1).zfill(2))
            num.grid(row=i+1, column=0,padx=(5,0), pady=5, sticky="ne")

            entry = ctk.CTkEntry(self,width = 100, height=30,placeholder_text="",corner_radius=0, fg_color="White", text_color="Black")
            entry.grid(row=i+1, column=1,padx=(5,0), pady=5, sticky="nw")
            entry.bind("<Return>", self.validate)
            entry.bind("<BackSpace>", self.removePlayer)

            label = ctk.CTkLabel(self, width = 200, height=30, fg_color="White", text_color="Black",text="")
            label.grid(row=i+1, column=2,padx=(0,10), pady=5, sticky="ne")
            label.bind("<Button-1>", self.codename_label_clicked)
            row[0] = entry
            row[1] = label
            self.widgets.append(row)

    def validate(self, event):
        box = event.widget
        rowNumber = box.master.grid_info()["row"] - 1
        playerID = box.get()

        if(not playerID.isnumeric() or self.playerExists(playerID)):
            self.clearRow(rowNumber)
            self.master.clearRow(rowNumber,self.bg_color)
            return
        
        self.master.storeID(playerID, self.bg_color, rowNumber)
        # Check db to see if a codename exists for this playerID
        codename = self.master.handleGetCodename(playerID)

        if codename is None:
            # ask for codename and add player to db
            codename = self.master.askForCodename()
            self.master.handleAddPlayer(playerID, codename)

        self.currentPlayers.append(playerID)
        self.setCodename(rowNumber, codename)
        self.master.storeCodename(codename, self.bg_color, rowNumber)

    def removePlayer(self, event):
        rowNumber = event.widget.master.grid_info()["row"] - 1
        playerID = self.widgets[rowNumber][0].get()
        if playerID.isnumeric():
            if playerID in self.currentPlayers:
                self.currentPlayers.remove(playerID)
            self.clearRow(rowNumber)
            self.master.clearRow(rowNumber, self.bg_color)

    def playerExists(self, playerID):
        for id in self.currentPlayers:
            if playerID == id:
                return True
        return False

    # Event handler updating a codename
    def codename_label_clicked(self, event):
        rowNumber = event.widget.master.grid_info()["row"] - 1
        playerID = self.widgets[rowNumber][0].get()
        if playerID:
            dialog = ctk.CTkInputDialog(text="New Codename:", title="Update Codename")
            newCodename = dialog.get_input()
            self.master.handleUpdateCodename(playerID, newCodename)
            self.setCodename(rowNumber, newCodename)
    
    def setCodename(self, row, codename):
        self.widgets[row][1].configure(text=codename)
    
    def setID(self, row, ID):
        print(ID)
        self.widgets[row][0].configure(textvariable=ID)

    def clearRow(self,row):
        self.widgets[row][1].configure(text="")
        self.widgets[row][0].delete(0,999)
    
    def clear(self):
        for i in range(len(self.widgets)):
            self.clearRow(i)
        
        self.currentPlayers.clear()
class PortPopup(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # have to delay the icon change due to CTk Top Level bug
        self.after(250, lambda :self.iconbitmap(f"@{settings_path}"))
        self.title("Settings")

        settings = getSettings()
        self.inputs = settings if settings else {
        "udp_ip": "127.0.0.1",
        "broadcastPort": 7500,
        "receivePort": 7501,
        }
        
        self.entries = {}

        for i, (key, label) in enumerate(self.inputs.items()):
            field = ctk.CTkLabel(self, text=key, corner_radius=6, font=("default",10))
            field.grid(row=i, column=0, padx=5, pady=(10, 0))

            entry = ctk.CTkEntry(self,width = 100, height=30,placeholder_text=label,corner_radius=0, fg_color="White", text_color="Black")
            entry.grid(row=i, column=1,padx=(5,0), pady=5)
            
            if isinstance(label, int):
                entry.insert(0, label)
            else:
                entry.insert(0, str(label))

            self.entries[key] = entry

        okButton = ctk.CTkButton(
            self, 
            text = "Ok", 
            command=self.submit,
            fg_color = "gray",
            hover_color = "black",
            text_color = "white",
            corner_radius = 0
        )
        okButton.grid(row=3, column=0, padx=(5,0), pady=5)

        cancelButton = ctk.CTkButton(
            self, 
            text = "Cancel", 
            command=self.cancel,
            fg_color = "gray",
            hover_color = "black",
            text_color = "white",
            corner_radius = 0
        )
        cancelButton.grid(row=3, column=1, padx=(5,0), pady=5)

    def submit(self):
        self.update()
        self.destroy()

    def cancel(self):
        self.inputs = None
        self.destroy()

    def keyNeedInt(key):
        print(key)
        if(key == "broadcastPort" or key == "receivePort"):
            return True
        return False
    
    def validate_ip(ip):
        pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
        if not re.match(pattern, ip):
            return False
        return all(0 <= int(octet) <= 255 for octet in ip.split("."))

    def update(self):
        for key in self.entries:
            value = self.entries[key].get()
            if(value == ""):
                continue
            needInt = PortPopup.keyNeedInt(key)

            if(needInt and not value.isnumeric()):
                #maybe replace later with popup
                print("port numbers must be numbers!")
                self.cancel()
                return

            if(needInt):
                value = int(value)

            if key == "udp_ip":
                if not PortPopup.validate_ip(value):
                    print("Invalid IP address format")
                    self.cancel()
                    return

            self.inputs[key] = value

        return False
    def get_input(self):
        self.master.wait_window(self)
        return self.inputs
    
class TeamLeaderBoard(ctk.CTkFrame):
    def __init__(self, master, color, codeNames):
        super().__init__(master)
        
        self.team = color
        self.players = {}
        self.playerMapping = {}
        self.slots = []
        numPlayerSlots = 16

        for id in codeNames:
            self.players[codeNames[id]] = 0

        if color == "Red":
            displayColor = "#591717"
        else:
            displayColor  = "#0e450e"

        self.configure(fg_color = displayColor)

        title = ctk.CTkLabel(self, text=color,font=("Normal",40))
        title.grid(row=0,column=0)

        self.teamScore = LeaderBoardSlot(self)
        self.teamScore.enterPlayer(f"{color} Team Score")
        self.teamScore.grid(row=1,column=0)

        for i in range(numPlayerSlots):
            slot = LeaderBoardSlot(self)
            slot.grid(row=i+2,column=0)
            self.slots.append(slot)
        
        for i, (equipment_id, codename) in enumerate(codeNames.items()):
            self.players[codename] = 0
            self.slots[i].enterPlayer(codename)
            self.playerMapping[equipment_id] = self.slots[i]
        
    def updateTeamScore(self):
        total = 0
        for slot in self.slots:
            total += slot.score
        self.teamScore.score = total
        self.teamScore.scoreLabel.configure(text=str(total))

    def sortSlots(self):
        self.slots.sort(key=lambda slot: slot.score, reverse=True)

        for i, slot in enumerate(self.slots):
            # remove old layout
            slot.grid_forget()
            # redraw
            slot.grid(row=i+2, column=0)

        self.update_idletasks()

class LeaderBoardSlot(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.score = 0

        if self.master.team == "Red":
            self.color = "#591717"
        else:
            self.color  = "#0e450e"

        self.player = ctk.CTkLabel(self,text = "",width=200,fg_color=self.color)
        self.player.grid(row=0,column=0)

        self.scoreLabel = ctk.CTkLabel(self,text="",width=100,fg_color=self.color)
        self.scoreLabel.grid(row=0,column=1)

    def enterPlayer(self, codename):
        self.score = 0
        self.player.configure(text=codename)
        self.scoreLabel.configure(text=str(self.score))

    def updateScore(self, points):

        self.score += points
        print(f"Updating Score to {self.score}")
        self.scoreLabel.configure(text = str(self.score))
        self.scoreLabel.update_idletasks()

    def getCodename(self):
        name = self.player.cget("text")
        return name[2:] if name.startswith("🅱 ") else name
    
    def addBaseHitMarker(self):
        name = self.player.cget("text")
        if not name.startswith("🅱"):
            self.player.configure(text="🅱 " + name)


class ActionLog(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        eventLimit = 10
        self.events = ["" for i in range(eventLimit)]
        self.lines = []

        self.configure(fg_color="Black")

        for i in range (eventLimit):
            line = ctk.CTkLabel(self,text="",width = 300, fg_color="Black")
            line.grid(row=i, column=0, sticky="w", padx=10, pady=1)
            self.lines.append(line)

    def update(self, message):
        self.events.pop()
        self.events.insert(0,message)

        for i in range(len(self.lines)):
            self.lines[i].configure(text=self.events[i])
        
        self.update_idletasks()

class GameTimer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.flash = True
        self.seconds = 6*60
        self.configure(fg_color="Black")

        self.counter = ctk.CTkLabel(self,text="",font=("Normal",60),fg_color="Black",justify=ctk.CENTER)
        self.counter.place(relx=.5,rely=.5,anchor=ctk.CENTER)

    def count(self):
        if self.seconds < 0:
            self.convertTimer()
            self.master.endGame()
            return

        mins, secs = divmod(self.seconds, 60)
        self.seconds -= 1
        self.counter.configure(text='{:01d}:{:02d}'.format(mins, secs))

        self.flashLeadingTeam()

        self.after(1000, self.count)

    def flashLeadingTeam(self):
        red = self.master.redLeaderBoard.teamScore.score
        green = self.master.greenLeaderBoard.teamScore.score

        self.flash = not self.flash
        flashColor = "yellow" if self.flash else "white"

        if red > green:
            self.master.redLeaderBoard.teamScore.scoreLabel.configure(text_color=flashColor)
            self.master.redLeaderBoard.teamScore.player.configure(text_color=flashColor)

            self.master.greenLeaderBoard.teamScore.scoreLabel.configure(text_color="white")
            self.master.greenLeaderBoard.teamScore.player.configure(text_color="white")

        elif green > red:
            self.master.greenLeaderBoard.teamScore.scoreLabel.configure(text_color=flashColor)
            self.master.greenLeaderBoard.teamScore.player.configure(text_color=flashColor)

            self.master.redLeaderBoard.teamScore.scoreLabel.configure(text_color="white")
            self.master.redLeaderBoard.teamScore.player.configure(text_color="white")

        else:
            self.master.redLeaderBoard.teamScore.scoreLabel.configure(text_color="white")
            self.master.redLeaderBoard.teamScore.player.configure(text_color="white")
            self.master.greenLeaderBoard.teamScore.scoreLabel.configure(text_color="white")
            self.master.greenLeaderBoard.teamScore.player.configure(text_color="white")


    def convertTimer(self):
        self.counter.destroy()
        button = ctk.CTkButton(
            self,
            text="Return to Player Entry",
            command=self.clicked,
            fg_color="gray",
            hover_color="black",
            text_color="white",
            corner_radius=0
        )

        button.place(relx=.5,rely=.5,anchor=ctk.CENTER)

    def clicked(self):
        self.master.destroy()