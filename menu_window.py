""" Menu Window part """

import os
import shutil
import tkinter as tk
from tkinter import ttk
from group_window import GroupWindow


class MenuWindow:
    """ Menu Window """
    
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

        # Escape key bind
        self.master.bind('<Escape>', self.MASTER_quit_func)

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
        self.frame_master.place(relx=0.03, rely=0.03)

        # Create group part (CRTG)
        self.CRTG_main_button = tk.Button(self.frame_master, text="Créer un nouveau groupe", 
                                             font=("Helvetica", int(self.screen_height/70), "bold"), command=self.CRTG_main_button_func)
        self.CRTG_main_button.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        self.CRTG_label = tk.Label(self.frame_master, text="Nom du nouveau groupe :", bg=self.GREEN,
                                        font=("Helvetica", int(self.screen_height/95)))

        self.CRTG_reg_frame_master = self.frame_master.register(self.CRTG_callback_func)
        self.CRTG_entry = tk.Entry(self.frame_master, validate="key", validatecommand=(self.CRTG_reg_frame_master, '%P'))
        self.CRTG_entry.bind('<Return>', self.CRTG_secondary_button_func)

        self.CRTG_secondary_button = tk.Button(self.frame_master, text="CRÉER", command=self.CRTG_secondary_button_func)

        self.CRTG_already_exists_label = tk.Label(self.frame_master, text="Ce groupe existe déjà !",
                                                  font=("Helvetica", int(self.screen_height/100)), fg="red", bg=self.GREEN)
        
        self.CRTG_saved_label = tk.Label(self.frame_master, text="Groupe créé !", font=("Helvetica", int(self.screen_height/90)),
                                          fg="green", bg=self.GREEN)

        # Remove group part (RMG)
        self.RMG_main_button = tk.Button(self.frame_master, text="Supprimer un groupe", 
                                             font=("Helvetica", int(self.screen_height/70), "bold"), command=self.RMG_main_button_func)
        self.RMG_main_button.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

        self.RMG_label = tk.Label(self.frame_master, text="Liste des groupes :", bg=self.GREEN,
                                           font=("Helvetica", int(self.screen_height/95)))

        self.RMG_combobox = ttk.Combobox(self.frame_master)
        self.RMG_combobox.bind('<Return>', self.RMG_secondary_button_func)

        self.RMG_secondary_button = tk.Button(self.frame_master, text="SUPPRIMER", command=self.RMG_secondary_button_func)
        
        self.RMG_deteted_label = tk.Label(self.frame_master, text="Groupe supprimé !",
                                             font=("Helvetica", int(self.screen_height/100)), fg="red", bg=self.GREEN)

        # Group selection part (GS)
        self.GS_main_button = tk.Button(self.frame_master, text="Sélectionner un groupe", 
                                        font=("Helvetica", int(self.screen_height/70), "bold"), command=self.GS_main_button_func)
        self.GS_main_button.grid(row=6, column=0, columnspan=2, sticky="w", pady=5)

        self.GS_label = tk.Label(self.frame_master, text="Liste des groupes :", bg=self.GREEN,
                                           font=("Helvetica", int(self.screen_height/95)))

        self.GS_combobox = ttk.Combobox(self.frame_master)
        self.GS_combobox.bind('<Return>', self.GS_secondary_button_func)

        self.GS_secondary_button = tk.Button(self.frame_master, text="SELECTIONNER", command=self.GS_secondary_button_func)
        
        # Display
        self.master.mainloop()
    
    def MASTER_quit_func(self, event=None):
        """ Reset all widgets """
        
        # make clickable button
        self.CRTG_main_button.config(state="normal")
        self.RMG_main_button.config(state="normal")
        self.GS_main_button.config(state="normal")

        # make invisible widgets
        self.CRTG_label.grid_forget()
        self.CRTG_entry.grid_forget()
        self.CRTG_secondary_button.grid_forget()
        self.CRTG_already_exists_label.grid_forget()

        self.RMG_label.grid_forget()
        self.RMG_combobox.grid_forget()
        self.RMG_secondary_button.grid_forget()
        self.RMG_deteted_label.grid_forget()

        self.GS_label.grid_forget()
        self.GS_combobox.grid_forget()
        self.GS_secondary_button.grid_forget()

        # special actions
        self.CRTG_entry.delete(first=0, last="end")
        self.RMG_combobox.set("")
        self.GS_combobox.set("")

    def CRTG_main_button_func(self, event=None):
        """ Display label + entry for saving group """
        
        # Close group remove part
        self.MASTER_quit_func(event)

        # disable main creation button
        self.CRTG_main_button.config(state="disable")
        
        # make group saved label invisible
        self.CRTG_saved_label.grid_forget()

        # display label + entry button + secondary creation button
        self.CRTG_label.grid(row=1, column=0, sticky="w", padx=5)
        self.CRTG_entry.grid(row=1, column=1, sticky="w", padx=5)
        self.CRTG_secondary_button.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    
    def CRTG_callback_func(self, input):
        """ Callback function for CRTG_entry """
        
        if " " in input or "é" in input:
            return False
        
        if len(input) > 15:
            return False

        else:
            self.CRTG_already_exists_label.grid_forget()
            return True
    
    def CRTG_secondary_button_func(self, event=None):
        """ Save group """

        # Check if group already exist
        new_group = self.CRTG_entry.get()
        new_group_path = os.path.join(self.GROUPS_PATH, new_group)
        if os.path.exists(new_group_path):
            self.CRTG_already_exists_label.grid(row=2, column=1, sticky="w", padx=5)

        # Create new group
        else:
            os.mkdir(new_group_path)
            self.CRTG_saved_label.grid(row=1, column=0)
            self.RMG_main_button.config(state="normal")
            self.MASTER_quit_func(event)
    
    def RMG_main_button_func(self, event=None):
        """ Display label + combobox for removing group """
        
        # make group saved label invisible
        self.CRTG_saved_label.grid_forget()

        # Close group creation part + group selection part
        self.MASTER_quit_func(event)

        # disable main remove button
        self.RMG_main_button.config(state="disable")

        self.RMG_label.grid(row=4, column=0, sticky="w", padx=5)
        self.RMG_combobox.config(value=sorted(os.listdir(self.GROUPS_PATH)), state="readonly")
        self.RMG_combobox.grid(row=4, column=1, sticky="w", padx=5)
        self.RMG_secondary_button.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.RMG_secondary_button.config(state="normal")

    def RMG_secondary_button_func(self, event=None):
        """ Remove a group """
        
        # if combobox selected a group name
        if self.RMG_combobox.get():
            shutil.rmtree(os.path.join(self.GROUPS_PATH, self.RMG_combobox.get()))
            self.RMG_combobox.config(value=sorted(os.listdir(self.GROUPS_PATH)), state="readonly")
            self.RMG_combobox.set("")
            self.RMG_deteted_label.grid(row=5, column=1, sticky="w", padx=5)

        # If no group disable secondary remove button 
        if len(os.listdir(self.GROUPS_PATH)) == 0:
            self.RMG_secondary_button.config(state="disable")

    def GS_main_button_func(self, event=None):
        """ Display label + combobox to select group """
        
        # make group saved label invisible
        self.CRTG_saved_label.grid_forget()

        # Close group creation part + remove group part
        self.MASTER_quit_func(event)

        # disable main select button
        self.GS_main_button.config(state="disable")     

        self.GS_label.grid(row=7, column=0, sticky="w", padx=5)
        self.GS_combobox.config(value=sorted(os.listdir(self.GROUPS_PATH)), state="readonly")
        self.GS_combobox.grid(row=7, column=1, sticky="w", padx=5)
        self.GS_secondary_button.grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.GS_secondary_button.config(state="normal")

    def GS_secondary_button_func(self, event=None):
        """ Select a group and open the group window """

        group_selected = self.GS_combobox.get()

        # if combobox selected a group name
        if group_selected:
            
            # create a file with the group selected name
            with open(os.path.join(self.SAVED_FILES_PATH, "group_selected.txt"), "w") as f:
                f.write(group_selected)

            # destroy menu window
            self.master.destroy()

            # launch group window
            launch_group_window()

        if len(os.listdir(self.GROUPS_PATH)) == 0:
            self.GS_secondary_button.config(state="disable")


def launch_group_window():
    """ A function wich launch GroupWindow class """

    GroupWindow()
