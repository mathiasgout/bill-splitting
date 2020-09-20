""" Bill-Splitting App """

import os
import re
import shutil
import tkinter as tk
from tkinter import ttk


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
        self.screen_width = self.master.winfo_screenwidth()
        self.WIDTH, self.HEIGHT = int(self.screen_height * 0.4), int(self.screen_height * 0.4)
        
        # Main Window customization 
        self.master.title("Partage des dépenses")
        self.master.geometry("{}x{}+{}+{}".format(self.WIDTH, self.HEIGHT, int((self.screen_width-self.WIDTH)/2), int((self.screen_height-1.5*self.HEIGHT)/2)))
        self.master.minsize(self.WIDTH, self.HEIGHT)
        self.master.maxsize(self.WIDTH, self.HEIGHT)
        self.master.config(bg=self.GREEN) 

        # Create master frame
        self.frame_master = tk.Frame(self.master, width=(self.WIDTH*0.94), height=(self.HEIGHT*0.94), bg=self.GREEN)
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
        
        # Delete group selected
        with open(os.path.join(self.SAVED_FILES_PATH, "group_selected.txt"), "w") as f:
            pass       

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
        
        if any(i in input for i in ("\\", " ", "/", ">", "<", ":", "|", "?", "*", "[", "]", "@", "!", "#", "$", "%",
                                    "^", "&", "(", ")", '"', "'", "{", "}", "~", "°", "`", "ç", "à", "-", "=",
                                    "+", ".", ";", ",", "§", "£", "€")):
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


class GroupWindow:
    """ Group Window """
    
    # Colors
    GREEN = "#D8EEED"

    # path folders
    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
    SAVED_FILES_PATH = os.path.join(MAIN_PATH, "saved_files")
    GROUPS_PATH = os.path.join(SAVED_FILES_PATH, "groups")
    
    def __init__(self):
        
        self.master = tk.Tk()
        
        # Get group name and path
        with open(os.path.join(self.SAVED_FILES_PATH, "group_selected.txt"), "r") as f:
            self.GROUP_NAME = f.readline()
        
        self.GROUP_PATH = os.path.join(self.GROUPS_PATH, self.GROUP_NAME)

        # Height and width
        self.screen_height = self.master.winfo_screenheight()
        self.screen_width = self.master.winfo_screenwidth()
        self.WIDTH, self.HEIGHT = int(self.screen_height * 0.8), int(self.screen_height * 0.6)

        # Main window cuztomization
        self.master.title("Groupe : {}".format(self.GROUP_NAME))
        self.master.geometry("{}x{}+{}+{}".format(self.WIDTH, self.HEIGHT, int((self.screen_width-self.WIDTH)/2), int((self.screen_height-self.HEIGHT)/2)))
        self.master.minsize(self.WIDTH, self.HEIGHT)
        self.master.maxsize(self.WIDTH, self.HEIGHT)
        self.master.config(bg="white")

        # Menu bar
        self.menu_bar = tk.Menu(self.master, bg="white")
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg="white")
        self.file_menu.add_command(label="Ouvrir un nouveau groupe", command=self.MENU_file_open_new_group_func)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
        
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg="white")
        self.edit_menu.add_command(label="Ajouter un membre")
        self.edit_menu.add_command(label="Supprimer un membre")
        self.menu_bar.add_cascade(label="Éditer", menu=self.edit_menu)
        self.master.config(menu=self.menu_bar)

        # Left frame
        self.left_frame = tk.Frame(self.master, width=self.WIDTH/4, height=self.HEIGHT, highlightbackground="black",
                                   highlightthickness=1, bg=self.GREEN)
        self.left_frame.grid(row=0, column=0)

        # Right frame
        self.right_frame = tk.Frame(self.master, width=3*self.WIDTH/4, height=self.HEIGHT, highlightbackground="black",
                                    highlightthickness=1, bg="white")
        self.right_frame.grid(row=0, column=1)

        self.master.mainloop()

    def MENU_file_open_new_group_func(self):
        """ Close this window and open menu window """
        
        # Quit group window
        self.master.destroy()
        
        # Open menu window
        launch_menu_window()
        
def launch_menu_window():
    """ A function which launch MenuWindow class """

    MenuWindow()


if __name__ == "__main__":
    MenuWindow()