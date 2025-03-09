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
        self.window = PlayAction()
        self.window.withdraw()
        self.window.wait_window(count)
        self.window.show()
        self.app.wait_window(self.window)
        self.app.show()

Main()
