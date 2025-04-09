from apps import *

class Main():
    def __init__(self):
        self.player_list_g = [[None,None,None] for i in range(15)]
        self.player_list_r = [[None,None,None] for i in range(15)]

        self.app = PlayerEntry(self)
        self.app.splash()
        self.app.after(3000, self.app.show)
        self.app.mainloop()

    def switchPlayAction(self):
        self.app.withdraw()
        count = CountDown()
        data = self.createPlayerData()
        self.window = PlayAction(data)
        self.window.withdraw()
        self.window.wait_window(count)
        self.window.show()
        self.app.wait_window(self.window)
        self.app.show()

    def createPlayerData(self):
        playerData = {}
        redPlayerData = {}
        greenPlayerData = {}

        for i in range(len(self.player_list_g)):
            player = self.player_list_g[i]
            if(player[0]):
                greenPlayerData[player[2]] = player[1]

        playerData["Green"] = greenPlayerData

        for i in range(len(self.player_list_r)):
            player = self.player_list_r[i]
            if(player[0]):
                redPlayerData[player[2]] = player[1]
        
        playerData["Red"] = redPlayerData

        return playerData

        

Main()
