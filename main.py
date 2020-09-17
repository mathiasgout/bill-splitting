import os
import tkinter as tk
from tkinter import ttk


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
        self.frame_master = tk.Frame(self.master, width=(self.WIDTH_MASTER*0.94), height=(self.HEIGHT_MASTER*0.94), bg=self.GREEN)
        self.reg_frame_master = self.frame_master.register(self._callback_create_group)
        self.frame_master.place(relx=0.03, rely=0.03)

        # Create group part
        self.create_group_button = tk.Button(self.frame_master, text="Créer un nouveau groupe", 
                                             font=("Helvetica", int(self.screen_height/70), "bold"), command=self.group_creation)
        self.create_group_button.grid(row=0, column=0, columnspan=2, sticky="w")

        self.create_group_label = tk.Label(self.frame_master, text="Nom du nouveau groupe :", bg=self.GREEN,
                                        font=("Helvetica", int(self.screen_height/95)))

        self.create_group_entry = tk.Entry(self.frame_master, validate="key", validatecommand=(self.reg_frame_master, '%P'))
        self.create_group_entry.bind('<Return>', self._save_create_group)
        self.create_group_entry.bind('<Escape>', self._quit_create_group)

        self.create_group_already_exists_label = tk.Label(self.frame_master, text="Ce nom de groupe existe déjà",
                                                  font=("Helvetica", int(self.screen_height/100)), fg="red", bg=self.GREEN)
        
        self.create_group_saved_label = tk.Label(self.frame_master, text="Groupe créé !", font=("Helvetica", int(self.screen_height/90)),
                                          fg="green", bg=self.GREEN)

        # Remove group part
        self.remove_group_button = tk.Button(self.frame_master, text="Supprimer un groupe", 
                                             font=("Helvetica", int(self.screen_height/70), "bold"), command=self.group_remove)
        self.remove_group_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

        self.remove_group_label = tk.Label(self.frame_master, text="Liste des groupes :", bg=self.GREEN,
                                           font=("Helvetica", int(self.screen_height/95)))

        self.remove_group_combobox = ttk.Combobox(self.frame_master)

        self.remove_group_combobox_button = tk.Button(self.frame_master, text="SUPPRIMER")

        # Display
        self.master.mainloop()

    def group_creation(self, event=None):
        """ (Display create_group_label + create_group_entry) or save group """
        
        # Close group deletion part
        self._quit_remove_group(event)

        # make group_saved_label invisible
        self.create_group_saved_label.grid_forget()

        # if create_group_entry is displayed
        if self.create_group_entry.winfo_ismapped():
            self._save_create_group(event)

        else:
            self.create_group_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.create_group_entry.grid(row=1, column=1, padx=5, sticky="w")

    def _callback_create_group(self, input):
        """ Callback function for create_group_entry """
        
        if " " in input or "é" in input:
            return False
        else:
            self.create_group_already_exists_label.grid_forget()
            return True
    
    def _save_create_group(self, event):
        """ Save group """

        # Check if group already exist
        new_group = self.create_group_entry.get()
        new_group_path = os.path.join(self.GROUPS_PATH, new_group)
        if os.path.exists(new_group_path):
            self.create_group_already_exists_label.grid(row=2, column=1, sticky="w")

        # Create new group
        else:
            os.mkdir(new_group_path)
            self.create_group_saved_label.grid(row=1, column=0, pady=5)
            self._quit_create_group(event)

    def _quit_create_group(self, event):
        """ Quit group creation part """
        
        # Make create_group_already_exists_label, create_group_saved_label and create_group_entry invisible + forget create_group_entry text
        self.create_group_entry.delete(first=0, last="end")
        self.create_group_already_exists_label.grid_forget()
        self.create_group_label.grid_forget()
        self.create_group_entry.grid_forget()
    
    def group_remove(self, event=None):
        """ Display remove_group_label + """

        # Close group creation part
        self._quit_create_group(event)

        self.remove_group_label.grid(row=4, column=0, sticky="w", padx=5)
        self.remove_group_combobox.config(value=[1,2,3])
        self.remove_group_combobox.grid(row=4, column=1, sticky="w", padx=5)
        self.remove_group_combobox_button.grid(row=5, column=0)


    def _quit_remove_group(self, event):
        """ Quit group deletion """

        self.remove_group_label.grid_forget()
        self.remove_group_combobox.grid_forget()
        self.remove_group_combobox_button.grid_forget()


if __name__ == "__main__":
    BillSplitting()