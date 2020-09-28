""" Bill-Splitting App """

import os
import json
import shutil
import tkinter as tk
from tkinter import ttk
from constants import *


# Folders and paths creation
MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
SAVED_FILES_PATH = os.path.join(MAIN_PATH, "saved_files")
if os.path.exists(SAVED_FILES_PATH) is False:
    os.mkdir(SAVED_FILES_PATH)

GROUPS_PATH = os.path.join(SAVED_FILES_PATH, "groups")
if os.path.exists(GROUPS_PATH) is False:
    os.mkdir(GROUPS_PATH)


class PopUpWindow:
    """ Pop Up window cuztomization """

    def __init__(self, window, title, width_master, height_master, x_master, y_master):
        """
        window : a tkinter.TopLevel(master) window
        title : pop up windwow title
        width_master : master width
        height_master : master height
        x_master : master x position
        y_master : master y_position
        """

        self.window = window

        # Espace bind key
        self.window.bind("<Escape>", lambda x: self.window.destroy())

        # Window customization 
        self.window.title(title)
        self.window.geometry("{}x{}+{}+{}".format(PUW_WIDTH, PUW_HEIGHT, 
                                                  int(x_master + (width_master - PUW_WIDTH)*0.5), 
                                                  int(y_master + (height_master - PUW_HEIGHT)*0.3)))
        self.window.minsize(PUW_WIDTH, PUW_HEIGHT)
        self.window.maxsize(PUW_WIDTH, PUW_HEIGHT)

        # grab_set : disable main window while new window open
        # attributes('-topmost', True) : new window always in front
        self.window.attributes('-topmost', True)
        self.window.grab_set() 


class MenuWindow:
    """ Menu Window """

    def __init__(self):

        self.master = tk.Tk()

        # Master window customization
        self.master.title("Partage des dépenses")
        self.master.geometry("{}x{}+{}+{}".format(MW_WIDTH, MW_HEIGHT, MW_POS_X, MW_POS_Y))
        self.master.minsize(MW_WIDTH, MW_HEIGHT)
        self.master.maxsize(MW_WIDTH, MW_HEIGHT)
        self.master.config(bg=GREEN)

        # Master frame
        self.frame_master = tk.Frame(self.master, width=MW_WIDTH*0.94, height=MW_HEIGHT*0.94, bg=GREEN)
        self.frame_master.place(relx=0.03, rely=0.03)

        # Master buttons
        self.CREATE_main_button = tk.Button(self.frame_master, text="Créer un nouveau groupe", font=("Helvetica", MW_BUTTON_FONT_SIZE, "bold"),
                                       command=self.CREATE_main_button_func)
        self.CREATE_main_button.grid(row=0, column=0, sticky="w", pady=5)

        self.REMOVE_main_button = tk.Button(self.frame_master, text="Supprimer un groupe", font=("Helvetica", MW_BUTTON_FONT_SIZE, "bold"),
                                            command=self.REMOVE_main_button_func)
        self.REMOVE_main_button.grid(row=1, column=0, sticky="w", pady=5)

        self.SELECT_main_button = tk.Button(self.frame_master, text="Sélectionner un groupe", font=("Helvetica", MW_BUTTON_FONT_SIZE, "bold"),
                                            command=self.SELECT_main_button_func)
        self.SELECT_main_button.grid(row=2, column=0, sticky="w", pady=5)
        
        # display
        self.master.mainloop()

# ------------------------------------- Create Group part --------------------------------------------

    def CREATE_main_button_func(self):
        """ Create a new group """

        self.CREATE_window = tk.Toplevel(self.frame_master)
        
        # Pop Up window cuztomization
        PopUpWindow(self.CREATE_window, "Créer un nouveau groupe", MW_WIDTH, MW_HEIGHT, self.master.winfo_x(), self.master.winfo_y())

        # Pop Up window widgets 
        self.CREATE_register = self.CREATE_window.register(self.CREATE_callback_func)
        self.CREATE_entry = tk.Entry(self.CREATE_window, font=("Helvetica", PUW_ENTRY_FONT_SIZE), justify="center",
                                     validate="key", validatecommand=(self.CREATE_register, '%P'))
        self.CREATE_entry.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.CREATE_entry.bind("<Return>", self.CREATE_secondary_button_func)

        self.CREATE_secondary_button = tk.Button(self.CREATE_window, text="AJOUTER", command=self.CREATE_secondary_button_func)
        self.CREATE_secondary_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

        self.CREATE_already_exist_label = tk.Label(self.CREATE_window, text="Ce groupe existe déjà !",
                                               font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")
        
        self.CREATE_member_created_label = tk.Label(self.CREATE_window, text="Nouveau groupe créé !",
                                                font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")

        self.CREATE_invalid_name_label = tk.Label(self.CREATE_window, text="Nom invalide",
                                               font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")

    def CREATE_secondary_button_func(self, event=None):
        """ Add new group """ 

        # Check if group already exist
        new_group = self.CREATE_entry.get()
        new_group_path = os.path.join(GROUPS_PATH, new_group)

        # clear entry
        self.CREATE_entry.delete(0, "end")

        # Check if it is a valid name
        if not new_group:
            self.CREATE_invalid_name_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

        # Check if member already exist
        if os.path.exists(new_group_path):
            self.CREATE_secondary_button.place_forget()
            self.CREATE_already_exist_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

        # Create new group
        else:
            os.mkdir(new_group_path)
            self.CREATE_secondary_button.place_forget()
            self.CREATE_member_created_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

            # create members.txt file
            with open(os.path.join(new_group_path, "members.txt"), "w") as f:
                pass

    def CREATE_callback_func(self, input):
        """ Callback function for CREATE_entry """
        
        if any(i in input for i in INVALID_CHAR):
            return False

        if len(input) > 15:
            return False

        else:
            self.CREATE_invalid_name_label.place_forget()
            self.CREATE_already_exist_label.place_forget()
            self.CREATE_member_created_label.place_forget()
            self.CREATE_secondary_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)
            return True
    
# ------------------------------------- Remove Group part --------------------------------------------

    def REMOVE_main_button_func(self):
        """ Remvove a group """

        self.REMOVE_window = tk.Toplevel(self.master)

        # Pop Up window cuztomization
        PopUpWindow(self.REMOVE_window, "Supprimer un groupe", MW_WIDTH, MW_HEIGHT, self.master.winfo_x(), self.master.winfo_y())

        # Pop Up window widgets
        self.REMOVE_combobox = ttk.Combobox(self.REMOVE_window, value=sorted(os.listdir(GROUPS_PATH)), 
                                            state="readonly", font=("Helvetica", PUW_ENTRY_FONT_SIZE))
        self.REMOVE_combobox.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.REMOVE_combobox.bind("<Button-1>", self.REMOVE_bind_func)
        self.REMOVE_combobox.bind("<Return>", self.REMOVE_secondary_button_func)

        self.REMOVE_secondary_button = tk.Button(self.REMOVE_window, text="SUPPRIMER", command=self.REMOVE_secondary_button_func)
        self.REMOVE_secondary_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

        self.REMOVE_member_deleted_label = tk.Label(self.REMOVE_window, text="Groupe supprimé !",
                                                    font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")

    def REMOVE_secondary_button_func(self, event=None):
        """ Remove a group """

        # if combobox selected a group name
        if self.REMOVE_combobox.get():
            shutil.rmtree(os.path.join(GROUPS_PATH, self.REMOVE_combobox.get()))
            self.REMOVE_member_deleted_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)
            self.REMOVE_combobox.set("")
            self.REMOVE_combobox.config(value=sorted(os.listdir(GROUPS_PATH)), state="readonly")

        # If no group, disable remove button 
        if len(os.listdir(GROUPS_PATH)) == 0:
            self.REMOVE_secondary_button.config(state="disable")

    def REMOVE_bind_func(self, event=None):
        """ button 1 bind on 'remove window' """

        self.REMOVE_member_deleted_label.place_forget()
        self.REMOVE_secondary_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

# ------------------------------------- Select Group part --------------------------------------------

    def SELECT_main_button_func(self):
        """ Select a group """

        self.SELECT_window = tk.Toplevel(self.master)

        # Pop Up window cuztomization
        PopUpWindow(self.SELECT_window, "Selectionner un groupe", MW_WIDTH, MW_HEIGHT, self.master.winfo_x(), self.master.winfo_y())

        # Pop Up window widgets
        self.SELECT_combobox = ttk.Combobox(self.SELECT_window, value=sorted(os.listdir(GROUPS_PATH)), 
                                            state="readonly", font=("Helvetica", PUW_ENTRY_FONT_SIZE))
        self.SELECT_combobox.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.SELECT_combobox.bind("<Return>", self.SELECT_secondary_button_func)

        self.SELECT_secondary_button = tk.Button(self.SELECT_window, text="SELECTIONNER", command=self.SELECT_secondary_button_func)
        self.SELECT_secondary_button.place(relx=0.35, rely=0.55, relwidth=0.30, relheight=0.40)

    def SELECT_secondary_button_func(self, event=None):
        """ Open the group window """

        group_selected = self.SELECT_combobox.get()

        # if combobox selected a group name
        if group_selected:
            
            # create a file with the group selected name
            with open(os.path.join(SAVED_FILES_PATH, "group_selected.txt"), "w") as f:
                f.write(group_selected)

            # destroy menu window
            self.master.destroy()

            # launch group window
            GroupWindow()

        if len(os.listdir(GROUPS_PATH)) == 0:
            self.SELECT_secondary_button.config(state="disable")


class GroupWindow:
    """ Group Window """

    def __init__(self):
        
        self.master = tk.Tk()
        
        # Get group name and path
        with open(os.path.join(SAVED_FILES_PATH, "group_selected.txt"), "r") as f:
            self.GROUP_NAME = f.readline()
        self.GROUP_PATH = os.path.join(GROUPS_PATH, self.GROUP_NAME)

        # Create members list and members button
        try :
            with open(os.path.join(self.GROUP_PATH, "members.txt"), "r") as f:
                self.members_list = json.loads(f.read())
        except:
            self.members_list = []
        
        self.members_button = []

        # Save member list while master window is closed
        self.master.protocol("WM_DELETE_WINDOW", self.save_member_list_func)

        # Master window customization
        self.master.title("Partage des dépenses")
        self.master.geometry("{}x{}+{}+{}".format(GW_WIDTH, GW_HEIGHT, GW_POS_X, GW_POS_Y))
        self.master.minsize(GW_WIDTH, GW_HEIGHT)
        self.master.maxsize(GW_WIDTH, GW_HEIGHT)
        self.master.config(bg="white")

        # Menu bar
        self.menu_bar = tk.Menu(self.master, bg="white", relief="flat")
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg="white")
        self.file_menu.add_command(label="Ouvrir un nouveau groupe", command=self.MENU_FILE_ONG_main_func)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
        
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg="white")
        self.edit_menu.add_command(label="Ajouter un membre", command=self.MENU_EDIT_ANM_main_func)
        self.edit_menu.add_command(label="Supprimer un membre", command=self.MENU_EDIT_RMM_main_func)
        self.menu_bar.add_cascade(label="Édition", menu=self.edit_menu)
        self.master.config(menu=self.menu_bar)

        # Left frame
        self.left_frame = tk.Frame(self.master, width=GW_LEFT_FRAME_SIZE, height=GW_HEIGHT, highlightbackground="black",
                                   highlightthickness=1, bg=GREEN, padx=10)
        self.left_frame.grid(row=0, column=0)
        self.display_members()

        # Right frame
        self.right_frame = tk.Frame(self.master, width=GW_RIGHT_FRAME_SIZE, height=GW_HEIGHT, highlightbackground="black",
                                    highlightthickness=1, bg="white")
        self.right_frame.grid(row=0, column=1)
        
        # display
        self.master.mainloop()

# --------------------------------------------- Other functions -------------------------------------------------------

    def save_member_list_func(self):
        """ Save member list as members.txt """
        
        with open(os.path.join(self.GROUP_PATH, "members.txt"), "w") as f:
            f.write(json.dumps(self.members_list))
        
        self.master.destroy()

# --------------------------------------------- Menu part -------------------------------------------------------

# ------------------------------------- Menu : File -> Open New Group --------------------------------------------

    def MENU_FILE_ONG_main_func(self):
        """ Close this window and open menu window  (ONG : Open New Group) """
        
        # Quit group window
        self.master.destroy()
        
        # Open menu window
        MenuWindow()

# ------------------------------------- Menu : Edit -> Add New Member ---------------------------------------------

    def MENU_EDIT_ANM_main_func(self):
        """ Add a new member in the group (ANM : Add New Member) """

        self.ANM_window = tk.Toplevel(self.master)
        
        # Pop Up window cuztomization
        PopUpWindow(self.ANM_window, "Créer un nouveau membre", GW_WIDTH, GW_HEIGHT, self.master.winfo_x(), self.master.winfo_y())

        # Widget in "add member" window
        self.ANM_register = self.ANM_window.register(self.MENU_EDIT_ANM_callback_func)
        self.ANM_entry = tk.Entry(self.ANM_window, font=("Helvetica", PUW_ENTRY_FONT_SIZE), justify="center",
                                  validate="key", validatecommand=(self.ANM_register, '%P'))
        self.ANM_entry.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.ANM_entry.bind("<Return>", self.MENU_EDIT_ANM_button_func)

        self.ANM_button = tk.Button(self.ANM_window, text="AJOUTER", command=self.MENU_EDIT_ANM_button_func)
        self.ANM_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

        self.ANM_already_exist_label = tk.Label(self.ANM_window, text="Ce membre existe déjà !",
                                               font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")
        
        self.ANM_member_created_label = tk.Label(self.ANM_window, text="Nouveau membre créé !",
                                                font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")

        self.ANM_invalid_name_label = tk.Label(self.ANM_window, text="Nom invalide",
                                               font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")

        self.ANM_too_many_members_label = tk.Label(self.ANM_window, text="Trop de membres (max. 15)",
                                                  font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")

    def MENU_EDIT_ANM_button_func(self, event=None):
        """ Add new member """ 

        new_member = self.ANM_entry.get()
        new_member_path = os.path.join(self.GROUP_PATH, "{}.csv".format(new_member))

        # clear entry and make button invisible
        self.ANM_entry.delete(0, "end")
        self.ANM_button.place_forget()

        # Check if there is more than 15 members
        if len(self.members_list) > 15:
            self.ANM_too_many_members_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

        # Check if it is a valid name
        elif not new_member:
            self.ANM_invalid_name_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

        # Check if member already exist
        elif os.path.exists(new_member_path):
            self.ANM_already_exist_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)
    
        # Create new member
        else:
            with open(new_member_path, 'w') as f:
                pass
            self.members_list.append(new_member)
            self.ANM_member_created_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)
            self.display_members()
        
    def MENU_EDIT_ANM_callback_func(self, input):
        """ Callback function for ANM_entry """
        
        if any(i in input for i in INVALID_CHAR):
            return False

        if len(input) > 15:
            return False

        else:
            self.ANM_invalid_name_label.place_forget()
            self.ANM_already_exist_label.place_forget()
            self.ANM_member_created_label.place_forget()
            self.ANM_too_many_members_label.place_forget()
            self.ANM_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)
            return True
    
# ------------------------------------- Menu : Edit -> Remove Member ---------------------------------------------

    def MENU_EDIT_RMM_main_func(self):
        """ Remove a member (RMM : ReMove Member) """

        self.RMM_window = tk.Toplevel(self.master)
 
        # Pop Up window cuztomization
        PopUpWindow(self.RMM_window, "Supprimer un membre", GW_WIDTH, GW_HEIGHT, self.master.winfo_x(), self.master.winfo_y())

        # Widget in "Remove member" window
        self.RMM_combobox = ttk.Combobox(self.RMM_window, value=self.members_list, 
                                         state="readonly", font=("Helvetica", PUW_ENTRY_FONT_SIZE))
        self.RMM_combobox.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.RMM_combobox.bind("<Button-1>", self.MENU_EDIT_RMM_bind_func)
        self.RMM_combobox.bind("<Return>", self.MENU_EDIT_RMM_button_func)

        self.RMM_button = tk.Button(self.RMM_window, text="SUPPRIMER", command=self.MENU_EDIT_RMM_button_func)
        self.RMM_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

        self.RMM_member_deleted_label = tk.Label(self.RMM_window, text="Membre supprimé !",
                                                 font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")

    def MENU_EDIT_RMM_button_func(self, event=None):
        """ Remove a member """

        # if combobox selected a group name
        if self.RMM_combobox.get():
            os.remove(os.path.join(self.GROUP_PATH, "{}.csv".format(self.RMM_combobox.get())))
            self.members_list.remove(self.RMM_combobox.get())
            self.RMM_member_deleted_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)
            self.RMM_combobox.set("")
            self.RMM_combobox.config(value=self.members_list)
            self.display_members()

        # If no group, disable remove button 
        if len(os.listdir(self.GROUP_PATH)) == 1:
            self.RMM_button.config(state="disable")

    def MENU_EDIT_RMM_bind_func(self, event=None):
        """ button 1 bind on 'remove window' """

        self.RMM_member_deleted_label.place_forget()
        self.RMM_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

# ---------------------------------------- Left Frame -----------------------------------------------------

    def display_members(self):
        """ A function to display the members """

        for widget in self.members_button:
            widget.destroy()

        self.members_button = []
        for i, mb in enumerate(self.members_list):
            self.members_button.append(tk.Button(self.left_frame, text="{}".format(mb), command=lambda mb=mb: self.open_this(mb)))
            self.members_button[i].place(relx=0.02, rely=0.02 + i/20, relwidth=0.96, relheight=0.05)
    
    @staticmethod
    def open_this(member):
        print(member)


if __name__ == "__main__":
    MenuWindow()
