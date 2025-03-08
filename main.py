from apps import *

class Main():
    def __init__(self):
        self.player_list_g = [[None,None,None] for i in range(15)]
        self.player_list_r = [[None,None,None] for i in range(15)]

        self.app = PlayerEntry(self)
        self.app.splash()
        self.app.after(3000, self.app.player_entry)
        self.app.mainloop()
    
    def switchEntry(self):
        self.app.destroy()
        self.app = PlayerEntry(self)
        self.app.mainloop()

    def switchPlayAction(self):
        self.app.destroy()
        self.app = PlayAction()
        self.app.mainloop()

Main()
