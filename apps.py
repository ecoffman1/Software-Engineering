import customtkinter as ctk
from tkinter import messagebox
import os
import random
import pygame
from PIL import Image
from UDP.changeSettings import changeSettings
from UDP.UDP_Client import broadcastEquipmentId, broadcastEndGame,broadcastStartGame
from UDP.UDP_Server import server
from database import Database
from resource_loader import ResourceLoader
from components import *
import threading
from time import sleep

ctk.set_appearance_mode("dark")

image_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(image_path, "icon.xbm")

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{x}+{y}")

def isAllSpaces(string):
    result = True
    for char in string:
        if char != " ":
            result = False
    return result

class Splash(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        loader = ResourceLoader()
        image = loader.load_image("logo.jpg")
        scale = 5
        img_width = image.width//scale
        img_height = image.height//scale
        photo = ctk.CTkImage(image, size=(img_width,img_height))
        label = ctk.CTkLabel(self,text = "", image=photo)
        label.grid(row=0,column=0)
        center_window(self)

class CountDown(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        loader = ResourceLoader()
        self.countNum = 30
        background_image = loader.load_image("countdown_images/background.tif")
        background_photo = ctk.CTkImage(background_image, size=(background_image.width,background_image.height))
        self.background = ctk.CTkLabel(self,text = "", image=background_photo)
        self.background.grid(row=0, column=0)
        center_window(self)

        counter_image = loader.load_image("countdown_images/30.tif")
        counter_photo = ctk.CTkImage(counter_image, size=(counter_image.width,counter_image.height))
        self.counter = ctk.CTkLabel(self,text="",image=counter_photo)
        self.counter.place(x=171,y=204)
        self.after(1000,self.count)
        

    def count(self):
            if(self.countNum == 0):
                self.destroy()
                return
            self.countNum -= 1
            loader = ResourceLoader()
            counter_image = loader.load_image(f"countdown_images/{self.countNum}.tif")
            counter_photo = ctk.CTkImage(counter_image, size=(counter_image.width,counter_image.height))
            self.counter.configure(image=counter_photo)
            self.after(1000,self.count)

class music:
    def __init__ (self):
        self.folder_path = 'photon_tracks'
        pygame.mixer.init()

    def start_music(self):
        threading.Timer(15.0, self.random_music).start()
         
    def random_music(self):
        folder_path = 'photon_tracks'

        tracks = [f for f in os.listdir(folder_path) if f.startswith('Track') and f.endswith('.mp3')]
        selected_track = random.choice(tracks)
        track_path = os.path.join(self.folder_path, selected_track)

        #stop any music
        pygame.mixer.music.stop()

        #load and play
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
play = music()

class PlayerEntry(ctk.CTk):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.iconbitmap(f"@{icon_path}")
        self.title("Photon")

        self.main = master
        self.bind("<F5>",self.startGame)
        self.bind("<F12>",self.clear)

        self.player_list_g = master.player_list_g
        self.player_list_r = master.player_list_r

        # setup UI structure
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.red = TeamFrame(self, "Red")
        self.green = TeamFrame(self, "Green")

        self.red.grid(row=0, column=0,sticky="e")
        self.green.grid(row=0, column=1,sticky="w")
        
        self.buttonFrame = ctk.CTkFrame(self)
        self.buttonFrame.grid(row=1,column=0,columnspan=2,sticky="nsew")
        self.buttonFrame.grid_columnconfigure((0, 1, 2), weight=1)
        # Create and place the button
        self.button = ctk.CTkButton(
            self.buttonFrame, 
            text="Change UDP Port", 
            command=self.updatePort,
            fg_color = "gray",
            hover_color = "black",
            text_color = "white",
            corner_radius = 0
        )
        self.button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.start = ctk.CTkButton(
            self.buttonFrame, 
            text="F5 Start Game", 
            command=self.startGame,
            fg_color = "gray",
            hover_color = "black",
            text_color = "white",
            corner_radius = 0
        )
        self.start.grid(row=1, column=1, pady=10, padx=10,sticky="ew")

        self.clearButton = ctk.CTkButton(
            self.buttonFrame, 
            text="F12 Clear Players", 
            command=self.clear,
            fg_color = "gray",
            hover_color = "black",
            text_color = "white",
            corner_radius = 0
        )
        self.clearButton.grid(row=1, column=2, pady=10, padx=10, sticky="ew")

        # Initialize ResourceLoader and load the config file path
        loader = ResourceLoader()
        self.config_path = loader.load_json("UDP/config.json")

        # Initialize database connection
        self.db = Database(self.config_path)

        self.withdraw()

    def splash(self):
        self.splash = Splash(self)

    def show(self):
        self.splash.destroy()
        self.state("normal")
        center_window(self)

    def updatePort(self):
        port = PortPopup(self)
        values = port.get_input()
        if(not values):
            return
        changeSettings(values)

    def clearRow(self, row, color):
        if(color == "Red"):
            self.player_list_r[row] = [None,None,None]
            self.red.clearRow(row)
        else:
            self.player_list_g[row] = [None,None,None]
            self.green.clearRow(row)

    def storeID(self,playerID,color,row):
        if(color == "Red"):
            self.player_list_r[row][0] = playerID
        else:
            self.player_list_g[row][0] = playerID
    
    # Find codename from given playerID, if none prompts for new codename.
    def handleGetCodename(self,playerID):
        self.db.connect()
        codename = self.db.get_codename(playerID)
        self.db.close()

        return codename
    
    # Stores codename in player list
    def storeCodename(self,codename, color, row):
        if(color == "Red"):
            team = self.player_list_r
        else:
            team = self.player_list_g
            
        team[row][1] = codename

        if(not team[row][2]):
            self.askForEquipmentID(color, row)

    def storeEquipmentID(self, equipmentID, color, row):
        if(color == "Red"):
            self.player_list_r[row][2] = equipmentID
        else:
            self.player_list_g[row][2] = equipmentID

    # Handles updating codenames in the database
    def handleUpdateCodename(self, playerID, newCodename):
        self.db.connect()
        updateSucceeded = self.db.update_codename(playerID, newCodename)
        self.db.close()
        return updateSucceeded

    # handles adding a player to the database
    def handleAddPlayer(self, playerID, codename):
        self.db.connect()
        self.db.add_player(playerID, codename)
        self.db.close()

    def askForCodename(self):
        dialog = ctk.CTkInputDialog(text="Codename:", title="Could not Find Codename in Database\nPlease Enter One")
        codename = dialog.get_input()

        while(not codename or codename == "" or isAllSpaces(codename)):
            dialog = ctk.CTkInputDialog(text="Codename:", title="Codename Entered was not Valid\nPlease Enter a Valid One")
            codename = dialog.get_input()

        return codename

    def playerIDExists(self, playerID):
        for player in self.player_list_r + self.player_list_g:
            if playerID == player[0]:
                return True
        return False
    
    def askForEquipmentID(self, color, row):
        dialog = ctk.CTkInputDialog(text="Equipment ID:", title="Please Enter Your Equipment ID")
        equipmentID = dialog.get_input()

        while(not equipmentID or not equipmentID.isnumeric()):
            dialog = ctk.CTkInputDialog(text="Equipment ID:", title="The ID You Entered Was Not Valid")
            equipmentID = dialog.get_input()
        
        self.storeEquipmentID(equipmentID, color, row)

        # Broadcast the equipment id over UDP
        broadcastEquipmentId(equipmentID)

    def clear(self, *args):
        for i in range(len(self.player_list_g)):
            self.player_list_g[i] = [None,None,None]
            self.player_list_r[i] = [None,None,None]
        self.red.clear()
        self.green.clear()
    
    def startGame(self, *args):
        if not self.hasEnoughPlayers():
            messagebox.showinfo("", "Not enough players to start!")
            return
        play.start_music()
        self.main.switchPlayAction()

    def hasEnoughPlayers(self):
        redHasPlayer = any(player[0] for player in self.player_list_r)
        greenHasPlayer = any(player[0] for player in self.player_list_g)
        return redHasPlayer and greenHasPlayer
    
    def random_music():
     folder_path = 'photon_tracks'
     
     tracks = [f for f in os.listdir(folder_path) if f.startswith('Track') and f.endswith('.mp3')]
     selected_track = random.choice(tracks)

     #play music
     print(f'Selected track: {selected_track}')

class PlayAction(ctk.CTkToplevel):
    def __init__(self,data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.after(250, lambda :self.iconbitmap(f"@{icon_path}"))
        self.title("Game Window")
        center_window(self)
        self.columnconfigure(1,weight=1)

        self.redLeaderBoard = TeamLeaderBoard(self,"Red", data["Red"])
        self.redLeaderBoard.grid(row=0,column=0,rowspan=2)
        
        self.greenLeaderBoard = TeamLeaderBoard(self,"Green", data["Green"])
        self.greenLeaderBoard.grid(row=0,column=2,rowspan=2)

        self.actionLog = ActionLog(self)
        self.actionLog.grid(row=0,column=1,sticky="ns")

        self.timer = GameTimer(self)
        self.timer.grid(row=1,column=1,sticky="nsew")

    def show(self):
        self.state("normal")
        center_window(self)
        self.startGame()

    def startGame(self):
        threading.Thread(target=server, args=(self.updateScoreboard,), daemon=True).start()
        sleep(0.5)
        broadcastStartGame()
        self.timer.count()

    def endGame(self):
        broadcastEndGame()
                
    def updateScoreboard(self, shooter_id, hit_id):
        print(f"Score event: {shooter_id} hit {hit_id}")

        if hit_id == "53":
            slot = self.greenLeaderBoard.playerMapping.get(shooter_id)
            if slot:
                slot.updateScore(100)
                self.greenLeaderBoard.updateTeamScore()
                slot.addBaseHitMarker()
                self.actionLog.update(f"{slot.getCodename()} hit the RED BASE!")
                return

        if hit_id == "43":
            slot = self.redLeaderBoard.playerMapping.get(shooter_id)
            if slot:
                slot.updateScore(100)
                self.redLeaderBoard.updateTeamScore()
                slot.addBaseHitMarker()
                self.actionLog.update(f"{slot.getCodename()} hit the GREEN BASE!")
                return

        slot = self.redLeaderBoard.playerMapping.get(shooter_id)
        if not slot:
            slot = self.greenLeaderBoard.playerMapping.get(shooter_id)

        if slot:
                        # print(f"[DEBUG] Found shooter {shooter_id}")
            
            hitSlot = self.redLeaderBoard.playerMapping.get(hit_id) or self.greenLeaderBoard.playerMapping.get(hit_id)

            friendlyFire = hitSlot and (
                (slot in self.redLeaderBoard.playerMapping.values() and hitSlot in self.redLeaderBoard.playerMapping.values()) or
                (slot in self.greenLeaderBoard.playerMapping.values() and hitSlot in self.greenLeaderBoard.playerMapping.values())
            )

            if friendlyFire:
                slot.updateScore(-10)
                log_message = f"{slot.getCodename()} hit a teammate! -10 points"
            else:
                slot.updateScore(10)
                hitName = hitSlot.getCodename() if hitSlot else hit_id
                log_message = f"{slot.getCodename()} hit {hitName}"

            if slot in self.redLeaderBoard.playerMapping.values():
                self.redLeaderBoard.updateTeamScore()
                self.redLeaderBoard.sortSlots()
            elif slot in self.greenLeaderBoard.playerMapping.values():
                self.greenLeaderBoard.updateTeamScore()
                self.greenLeaderBoard.sortSlots()

            self.actionLog.update(log_message)
            
            return friendlyFire

        else:
            # print(f"[DEBUG] No slot found for shooter_id: {shooter_id}")
            return False

