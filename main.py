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
        screen_height = self.master.winfo_screenheight()
        self.WIDTH_MASTER, self.HEIGHT_MASTER = int(screen_height * 0.4), int(screen_height * 0.4)
        
        # Main Window customization 
        self.master.title("Partage des dépenses")
        self.master.geometry("{}x{}".format(self.WIDTH_MASTER, self.HEIGHT_MASTER))
        self.master.minsize(self.WIDTH_MASTER, self.HEIGHT_MASTER)
        self.master.maxsize(self.WIDTH_MASTER, self.HEIGHT_MASTER)
        self.master.config(bg=self.GREEN) 

        # Create group button
        self.create_group_button = tk.Button(self.master, text="Créer un nouveau groupe", 
                                             font=("Helvetica", int(screen_height/80), "bold"), command=self.create_new_group)
        self.create_group_button.place(relx=0.02, rely=0.02, relheight=0.08)

        self.master.mainloop()

    def create_new_group(self):
        """ New group creation"""
        
        self.new_group_label = tk.Label(self.master, text="Nom du nouveau groupe :", bg=self.GREEN)
        self.new_group_label.place(relx=0.02, rely=0.11, relheight=0.05, relwidth=0.48)
        
        self.new_group_entry = tk.Entry(self.master)
        self.new_group_entry.place(relx=0.55, rely=0.11)


if __name__ == "__main__":
    BillSplitting()