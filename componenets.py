import customtkinter as ctk

class TeamFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.validating = None

        if title == "Red":
            self.color = "#591717"
        else:
            self.color = "#0e450e"
        
        self.configure(fg_color = self.color, corner_radius=0)
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

            entry = ctk.CTkEntry(self,width = 100, height=30,placeholder_text="",corner_radius=0, fg_color="White", text_color="Black")
            entry.grid(row=i+1, column=1,padx=(5,0), pady=5, sticky="nw")
            entry.bind("<Return>", self.validate)

            label = ctk.CTkLabel(self, width = 200, height=30, fg_color="White", text_color="Black",text="")
            label.grid(row=i+1, column=2,padx=(0,10), pady=5, sticky="ne")
            label.bind("<Button-1>", self.codename_label_clicked)
            row[0] = entry
            row[1] = label
            self.widgets.append(row)

    def validate(self, event):
        box = event.widget
        rowNumber = box.master.grid_info()["row"] - 1
        id = box.get()
        if(not id.isnumeric()):
            self.clearRow(rowNumber)
            self.master.clearRow(rowNumber,self.bg_color)
            return
        
        self.master.storeID(id, self.bg_color, rowNumber)
        response = self.master.queryID(id)

        if(not response):
            self.master.clearRow(rowNumber,self.bg_color)
            self.clearRow(rowNumber)
            return

        self.setCodename(rowNumber,response)
        self.master.storeCodename(response, self.bg_color, rowNumber)
    
    # Event handler updating a codename
    def codename_label_clicked(self, event):
        rowNumber = event.widget.master.grid_info()["row"] - 1
        playerId = self.widgets[rowNumber][0].get()
        if playerId:
            dialog = ctk.CTkInputDialog(text="New Codename:", title="Update Codename")
            newCodename = dialog.get_input()
            self.master.handleUpdateCodename(playerId, newCodename)
            self.setCodename(rowNumber, newCodename)
    
    def setCodename(self, row, codename):
        self.widgets[row][1].configure(text=codename)
    
    def setID(self, row, ID):
        print(ID)
        self.widgets[row][0].configure(textvariable=ID)

    def clearRow(self,row):
        self.widgets[row][1].configure(text="")
        self.widgets[row][0].delete(0,999)



class portPopup(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inputs = {
        "UDP IP": "127.0.0.1",
        "Broadcast Port": 7500,
        "Receive Port": 7501,
        }
        
        self.entries = {}

        for i, (key, label) in enumerate(self.inputs.items()):
            field = ctk.CTkLabel(self, text=key, corner_radius=6, font=("default",10))
            field.grid(row=i, column=0, padx=5, pady=(10, 0))

            entry = ctk.CTkEntry(self,width = 100, height=30,placeholder_text=label,corner_radius=0, fg_color="White", text_color="Black")
            entry.grid(row=i, column=1,padx=(5,0), pady=5)
            entry.bind("<Return>", self.update)

            self.entries[key] = entry

        okButton = ctk.CTkButton(self, text = "Ok", command=self.submit)
        okButton.grid(row=3, column=0, padx=(5,0), pady=5)

        cancelButton = ctk.CTkButton(self, text = "Cancel", command=self.submit)
        cancelButton.grid(row=3, column=1, padx=(5,0), pady=5)

    def submit(self):
        self.destroy()

    def update(self):
        for key in self.entries:
            self.inputs[key] = self.entries[key].get()

    def get_input(self):
        self.master.wait_window(self)
        return self.inputs

