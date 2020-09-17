import os
import tkinter as tk


class BillSplitting:
    """ Bill-splitting """
    
    # Colors
    GREEN = "#D8EEED"

    # Check if folders exists
    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
    SAVED_FILES_PATH = os.path.join(MAIN_PATH, "saved_files")
    if os.path.exists(SAVED_FILES_PATH) is False:
        os.mkdir(SAVED_FILES_PATH)
    
    GROUPS_PATH = os.path.join(SAVED_FILES_PATH, "groups")
    if os.path.exists(GROUPS_PATH) is False:
        os.mkdir(GROUPS_PATH)

    def __init__(self):

        self.master = tk.Tk()

        # Height and width
        self.screen_height = self.master.winfo_screenheight()
        self.WIDTH_MASTER, self.HEIGHT_MASTER = int(self.screen_height * 0.4), int(self.screen_height * 0.4)
        
        # Main Window customization 
        self.master.title("Partage des dépenses")
        self.master.geometry("{}x{}".format(self.WIDTH_MASTER, self.HEIGHT_MASTER))
        self.master.minsize(self.WIDTH_MASTER, self.HEIGHT_MASTER)
        self.master.maxsize(self.WIDTH_MASTER, self.HEIGHT_MASTER)
        self.master.config(bg=self.GREEN) 

        # Create master frame
        self.frame_master = tk.Frame(self.master, width=(self.WIDTH_MASTER*0.94), height=(self.HEIGHT_MASTER*0.94),
                                     bg=self.GREEN)
        self.frame_master.place(relx=0.03, rely=0.03)

        # Create group button
        self.create_group_button = tk.Button(self.frame_master, text="Créer un nouveau groupe", 
                                             font=("Helvetica", int(self.screen_height/70), "bold"), command=self.create_new_group)
        #self.create_group_button.place(relx=0, rely=0, relheight=0.08)
        self.create_group_button.grid(row=0, column=0, columnspan=2, sticky="w")

        self.master.mainloop()

    def create_new_group(self):
        """ New group creation"""
        
        self.new_group_label = tk.Label(self.frame_master, text="Nom du nouveau groupe :", bg=self.GREEN,
                                        font=("Helvetica", int(self.screen_height/95)))
        self.new_group_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.new_group_entry = tk.Entry(self.frame_master)
        self.new_group_entry.grid(row=1, column=1, padx=5, sticky="e")


if __name__ == "__main__":
    BillSplitting()