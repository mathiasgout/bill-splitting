""" Bill-Splitting App """

import os
import re
import json
import shutil
import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk
from pandastable import Table
from tkcalendar import DateEntry
from collections import Counter
from constants import *


# -------------------------------------------- Folders and paths -----------------------------------------------------

MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
SAVED_FILES_PATH = os.path.join(MAIN_PATH, "saved_files")
if os.path.exists(SAVED_FILES_PATH) is False:
    os.mkdir(SAVED_FILES_PATH)

GROUPS_PATH = os.path.join(SAVED_FILES_PATH, "groups")
if os.path.exists(GROUPS_PATH) is False:
    os.mkdir(GROUPS_PATH)


# -------------------------------------------- Transversal classes -----------------------------------------------------

class PopUpWindow(tk.Toplevel):
    """ Pop up window """

    def __init__(self, master, title, popup_width, popup_height):
        tk.Toplevel.__init__(self, master)

        # Espace bind key
        self.bind("<Escape>", lambda x: self.destroy())

        # Window customization 
        self.title(title)
        self.geometry("{}x{}+{}+{}".format(popup_width, popup_height, 
                                           int(master.winfo_x() + (master.winfo_width() - popup_width)*0.5), 
                                           int(master.winfo_y() + (master.winfo_height() - popup_height)*0.3)))
        self.minsize(popup_width, popup_height)
        self.maxsize(popup_width, popup_height)

        # grab_set : disable main window while new window open
        # attributes('-topmost', True) : new window always in front
        self.attributes('-topmost', True)
        self.grab_set() 


# -------------------------------------------- Menu Window classes -----------------------------------------------------

class CreateGroup(tk.Button):
    """ Create group part """
    
    def __init__(self, master):
        tk.Button.__init__(self, master)
        self.master = master
        self.config(text="Créer un nouveau groupe")
        self.config(font=("Helvetica", MW_BUTTON_FONT_SIZE, "bold"))
        self.config(command=self.main_button_func)

    def main_button_func(self):
        
        self.window = PopUpWindow(self.master.master, "Créer un nouveau groupe", PUW_WIDTH, PUW_HEIGHT)
        
        # window widgets 
        self.window.register = self.window.register(self.callback_func)
        self.window.entry = tk.Entry(self.window, font=("Helvetica", PUW_ENTRY_FONT_SIZE), justify="center", validate="key", 
                              validatecommand=(self.window.register, '%P'))
        self.window.entry.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.window.entry.bind("<Return>", self.window_button_func)

        self.window.button = tk.Button(self.window, text="AJOUTER", command=self.window_button_func)
        self.window.button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

        self.window.already_exist_label = tk.Label(self.window, text="Ce groupe existe déjà !", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")
        
        self.window.member_created_label = tk.Label(self.window, text="Nouveau groupe créé !", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")

        self.window.invalid_name_label = tk.Label(self.window, text="Nom invalide", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")

    def window_button_func(self, event=None):
        """ Add new group """ 

        # Check if group already exist
        new_group = self.window.entry.get()
        new_group_path = os.path.join(GROUPS_PATH, new_group)

        # clear entry
        self.window.entry.delete(0, "end")

        # Check if it is a valid name
        if not new_group:
            self.window.invalid_name_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

        # Check if member already exist
        if os.path.exists(new_group_path):
            self.window.button.place_forget()
            self.window.already_exist_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

        # Create new group
        else:
            os.mkdir(new_group_path)
            self.window.button.place_forget()
            self.window.member_created_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

            # create members.txt file
            with open(os.path.join(new_group_path, "members.txt"), "w") as f:
                pass

    def callback_func(self, input):
        """ Callback function for entry """
        
        if any(i in input for i in INVALID_CHAR):
            return False

        if len(input) > 15:
            return False

        else:
            self.window.invalid_name_label.place_forget()
            self.window.already_exist_label.place_forget()
            self.window.member_created_label.place_forget()
            self.window.button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)
            return True


class RemoveGroup(tk.Button):
    """ Remove group part """

    def __init__(self, master):
        tk.Button.__init__(self, master)
        self.master = master
        self.config(text="Supprimer un groupe")
        self.config(font=("Helvetica", MW_BUTTON_FONT_SIZE, "bold"))
        self.config(command=self.main_button_func)       

    def main_button_func(self):
        """ Remvove a group """

        self.window = PopUpWindow(self.master.master, "Supprimer un groupe", PUW_WIDTH, PUW_HEIGHT)

        # window widgets
        self.combobox = ttk.Combobox(self.window, value=sorted(os.listdir(GROUPS_PATH)), state="readonly", font=("Helvetica", PUW_ENTRY_FONT_SIZE))
        self.combobox.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.combobox.bind("<Button-1>", self.bind_func)
        self.combobox.bind("<Return>", self.secondary_button_func)

        self.secondary_button = tk.Button(self.window, text="SUPPRIMER", command=self.secondary_button_func)
        self.secondary_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

        self.member_deleted_label = tk.Label(self.window, text="Groupe supprimé !", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")

    def secondary_button_func(self, event=None):
        """ Remove a group """

        # if combobox selected a group name
        if self.combobox.get():
            shutil.rmtree(os.path.join(GROUPS_PATH, self.combobox.get()))
            self.member_deleted_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)
            self.combobox.set("")
            self.combobox.config(value=sorted(os.listdir(GROUPS_PATH)), state="readonly")

        # If no group, disable remove button 
        if len(os.listdir(GROUPS_PATH)) == 0:
            self.secondary_button.config(state="disable")

    def bind_func(self, event=None):
        """ button 1 bind on 'remove window' """

        self.member_deleted_label.place_forget()
        self.secondary_button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)


class SelectGroup(tk.Button):
    """ Select group part """

    def __init__(self, master):
        tk.Button.__init__(self, master)
        self.master = master
        self.config(text="Sélectionner un groupe")
        self.config(font=("Helvetica", MW_BUTTON_FONT_SIZE, "bold"))
        self.config(command=self.main_button_func) 

    def main_button_func(self):
        """ Select a group """

        self.window = PopUpWindow(self.master.master, "Selectionner un groupe", PUW_WIDTH, PUW_HEIGHT)

        # window widgets
        self.combobox = ttk.Combobox(self.window, value=sorted(os.listdir(GROUPS_PATH)), 
                                            state="readonly", font=("Helvetica", PUW_ENTRY_FONT_SIZE))
        self.combobox.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.combobox.bind("<Return>", self.secondary_button_func)

        self.secondary_button = tk.Button(self.window, text="SELECTIONNER", command=self.secondary_button_func)
        self.secondary_button.place(relx=0.35, rely=0.55, relwidth=0.30, relheight=0.40)

    def secondary_button_func(self, event=None):
        """ Open the group window """

        group_selected = self.combobox.get()

        # if combobox selected a group name
        if group_selected:
            
            # create a global variable for selected group and selected group path
            global GROUP_NAME
            global GROUP_PATH
            GROUP_NAME = group_selected
            GROUP_PATH = os.path.join(GROUPS_PATH, GROUP_NAME)

            # make invisible menu window and destroy toplevelwindow
            self.master.master.withdraw()
            self.window.destroy()

            # launch group window
            GroupWindow(self.master)

        if len(os.listdir(GROUPS_PATH)) == 0:
            self.secondary_button.config(state="disable")


class MenuWindow(tk.Frame):
    """ Menu Window """

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.config(bg=GREEN)

        # Classes
        self.create_group = CreateGroup(self)
        self.remove_group = RemoveGroup(self)
        self.select_group = SelectGroup(self)

        # Classes position
        self.create_group.grid(row=0, column=0, sticky="w", padx=15, pady=(20, 5))
        self.remove_group.grid(row=1, column=0, sticky="w", padx=15, pady=(5,5))
        self.select_group.grid(row=2, column=0, sticky="w", padx=15, pady=(5,5))


# ------------------------------------------- Group Window classes ----------------------------------------------------

class OpenNewGroup(tk.Menu):
    """ Open new group in the file menu """

    def __init__(self, menu, master):
        tk.Menu.__init__(self, menu)
        self.master = master
        self.menu = menu

        self.menu.add_command(label="Ouvrir un nouveau groupe", command=self.main_func)

    def main_func(self):
        """ Close this window and make visible the menu window """
        
        # Make visible menu window 
        self.master.master.master.deiconify()

        # Quit group window
        self.master.destroy()


class AddNewMember(tk.Menu):
    """ Add a new member """

    def __init__(self, menu, master):
        tk.Menu.__init__(self, menu)
        self.master = master
        self.menu = menu

        self.menu.add_command(label="Ajouter un membre", command=self.main_func)

    def main_func(self):
        """ Add a new member in the group """

        self.window = PopUpWindow(self.master, "Créer un nouveau membre", PUW_WIDTH, PUW_HEIGHT)
        
        # Widget in window
        self.register = self.window.register(self.callback_func)
        self.entry = tk.Entry(self.window, font=("Helvetica", PUW_ENTRY_FONT_SIZE), justify="center", validate="key", 
                              validatecommand=(self.register, '%P'))
        self.entry.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.entry.bind("<Return>", self.button_func)

        self.button = tk.Button(self.window, text="AJOUTER", command=self.button_func)
        self.button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

        self.already_exist_label = tk.Label(self.window, text="Ce membre existe déjà !", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")
        
        self.member_created_label = tk.Label(self.window, text="Nouveau membre créé !", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")

        self.invalid_name_label = tk.Label(self.window, text="Nom invalide", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")

        self.too_many_members_label = tk.Label(self.window, text="Trop de membres (max. 12)", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")

    def button_func(self, event=None):
        """ Add new member """ 

        new_member = self.entry.get()
        new_member_path = os.path.join(GROUP_PATH, "{}.csv".format(new_member))

        # clear entry and make button invisible
        self.entry.delete(0, "end")
        self.button.place_forget()
        
        # Check if there is more than 12 members
        if len(self.master.members_list) > 12:
            self.too_many_members_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

        # Check if it is a valid name
        elif not new_member:
            self.invalid_name_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)

        # Check if member already exist
        elif new_member in self.master.members_list:
            self.already_exist_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)
    
        # Create new member
        else:
            self.master.members_list.append(new_member)
            self.member_created_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)
            
            # Update member left frame widgets
            self.master.left_frame.create_member_rows()

            # hide widgets on right frame
            self.master.right_frame.hide_widget()

    def callback_func(self, input):
        """ Callback function """
        
        if any(i in input for i in INVALID_CHAR):
            return False

        if len(input) > 12:
            return False

        else:
            self.invalid_name_label.place_forget()
            self.already_exist_label.place_forget()
            self.member_created_label.place_forget()
            self.too_many_members_label.place_forget()
            self.button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)
            return True


class RemoveMember(tk.Menu):
    """ Remove a member """

    def __init__(self, menu, master):
        tk.Menu.__init__(self, menu)
        self.master = master
        self.menu = menu

        self.menu.add_command(label="Supprimer un membre", command=self.main_func)

    def main_func(self):
        """ Remove a group member """

        self.window = PopUpWindow(self.master, "Supprimer un membre", PUW_WIDTH, PUW_HEIGHT)
 
        # Widget in window
        self.combobox = ttk.Combobox(self.window, value=self.master.members_list, state="readonly", font=("Helvetica", PUW_ENTRY_FONT_SIZE))
        self.combobox.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.45)
        self.combobox.bind("<Button-1>", self.bind_func)
        self.combobox.bind("<Return>", self.button_func)

        self.button = tk.Button(self.window, text="SUPPRIMER", command=self.button_func)
        self.button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)

        self.member_deleted_label = tk.Label(self.window, text="Membre supprimé !", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")  

    def button_func(self, event=None):
        """ Remove a member """

        removed_member = self.combobox.get()

        # if combobox selected a group name
        if removed_member:
            
            # remove member row
            self.master.data = self.master.data.loc[self.master.data.member != removed_member, :]
        
            # remove member from members_list
            self.master.members_list.remove(removed_member)
            
            # display changes on top level window
            self.member_deleted_label.place(relx=0.10, rely=0.55, relwidth=0.80, relheight=0.40)
            self.combobox.set("")
            self.combobox.config(value=self.master.members_list)
            
            # remove member from left frame widgets
            self.master.left_frame.create_member_rows()
            
            # hide widgets on right frame
            self.master.right_frame.hide_widget()

        # If no group, disable remove button 
        if len(self.master.members_list) == 0:
            self.button.config(state="disable")

    def bind_func(self, event=None):
        """ button 1 bind on 'remove window' """

        self.member_deleted_label.place_forget()
        self.button.place(relx=0.40, rely=0.55, relwidth=0.20, relheight=0.40)


class EditMenu(tk.Menu):
    """ File Menu in the menu bar"""

    def __init__(self, menu, master):
        tk.Menu.__init__(self, menu)
        self.master = master
        self.menu = menu
        self.config(tearoff=0)
        self.config(bg="white")

        # Commands in edit menu
        AddNewMember(self, self.master)
        RemoveMember(self, self.master)


class FileMenu(tk.Menu):
    """ File Menu in the menu bar"""

    def __init__(self, menu, master):
        tk.Menu.__init__(self, menu)
        self.master = master
        self.menu = menu
        self.config(tearoff=0)
        self.config(bg="white")

        # Commands in file menu
        OpenNewGroup(self, self.master)


class MenuBar(tk.Menu):
    """ Menu Bar part """

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.master = master
        self.config(bg="white")
        self.config(relief="flat")

        # Cascade
        self.add_cascade(label="Ficher", menu=FileMenu(self, self.master))
        self.add_cascade(label="Édition", menu=EditMenu(self, self.master))


class LeftFrame(tk.Frame):
    """ Left Frame Container """
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.config(width=GW_LEFT_FRAME_SIZE)
        self.config(highlightbackground="black", highlightthickness=1)
        self.config(bg=GREEN)
        self.config(padx=10, pady=10)

        self.create_member_rows()

        self.calculate_part = CalculatePart(self)
        self.calculate_part.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)

    def create_member_rows(self):
        """ A function to create members widget """
        
        # Clean members_widget_list
        for widget in self.master.members_widget_list:
            widget.destroy()

        # Fill members_widget_list
        self.master.members_widget_list = []
        for member in self.master.members_list:
            self.master.members_widget_list.append(MemberRow(self, member))
        
        self._display_member_rows()

    def _display_member_rows(self):
        """ A function to display members widget """

        for i, member in enumerate(self.master.members_list):
            self.master.members_widget_list[i].entry.delete(0, "end")
            self.master.members_widget_list[i].entry.insert(0, int(100/len(self.master.members_list)))

            self.master.members_widget_list[i].pack()


class MemberRow(tk.Frame):
    """ Member name + member entry + pourcent label """

    def __init__(self, master, member):
        tk.Frame.__init__(self, master)
        self.master = master
        self.config(width=GW_LEFT_FRAME_SIZE, height=GW_MEMBER_ROW_HEIGHT)
        self.config(bg=GREEN)
        
        self.button = tk.Button(self, font=("Helvetica", GW_MEMBER_LABEL_FONT_SIZE, "bold"), relief="flat", 
                                anchor="w", bg=GREEN, highlightthickness=0, text=member, command=lambda m=member: self.main_func(m))
        self.entry = tk.Entry(self)
        self.pourcent_label = tk.Label(self, text="%", bg=GREEN, font=("Helvetica", GW_POURCENT_LABEL_FONT_SIZE))

        self.button.place(relx=0, rely=0, relwidth=0.75, relheight=1)
        self.entry.place(relx=0.75, rely=0.1, relwidth=0.15, relheight=0.8)
        self.pourcent_label.place(relx=0.9, rely=0.2, relwidth=0.1, relheight=0.8)

    def main_func(self, member):
        """ Display right frame widgets """

        # Background button while it is selected
        for widget in self.master.master.members_widget_list:
            widget.button.config(bg=GREEN)
        self.button.config(bg="white")

        # Display new expense button + edit expenses on the right frame
        if member[0].lower() in ["a", "e", "i", "o", "u", "y"]:
            self.master.master.right_frame.new_expense_button.config(text="Nouvelle dépense d'{}".format(member))
            self.master.master.right_frame.edit_expenses_button.config(text="Modifier les dépenses d'{}".format(member))
        else:
            self.master.master.right_frame.new_expense_button.config(text="Nouvelle dépense de {}".format(member))
            self.master.master.right_frame.edit_expenses_button.config(text="Modifier les dépenses de {}".format(member))

        self.master.master.right_frame.new_expense_button.pack(fill="x")
        self.master.master.right_frame.edit_expenses_button.pack(fill="x")


class NewExpense(tk.Button):
    """ New expense button on right frame """

    def __init__(self, master):
        tk.Button.__init__(self, master)
        self.master = master
        self.config(font=("Helvetica", GW_RIGHT_FRAME_BUTTON_FONT_SIZE, "bold"))
        self.config(command=self.main_func)
    
    def main_func(self):
        """ Create a pop up window to add an expense """

        self.member = re.split(r"\'|\s", self.cget("text"))[-1]

        # Create pop up window
        self.window = PopUpWindow(self.master.master, "Nouvelle dépense : {}".format(self.member), PUW_WIDTH_BIG, PUW_HEIGHT_BIG)

        # Bind
        self.window.bind("<Return>", self.button_func)
        self.window.bind("<Button-1>", self.bind_func)

        # Create widgets
        self.window.description_label = tk.Label(self.window, text="Description :", anchor="w", font=("Helvetica", PUW_LABEL_FONT_SIZE, "bold"))
        self.window.description_entry = tk.Entry(self.window, font=("Helvetica", PUW_BIG_ENTRY_FONT_SIZE))
        self.window.amount_label = tk.Label(self.window, text="Montant (€) :", anchor="w", font=("Helvetica", PUW_LABEL_FONT_SIZE, "bold"))
        self.window.amount_register = self.window.register(self.callback_amount_func)
        self.window.amount_entry = tk.Entry(self.window, font=("Helvetica", PUW_BIG_ENTRY_FONT_SIZE), validatecommand=(self.window.amount_register, '%P'), validate="key")
        self.window.date_label = tk.Label(self.window, text="Date :", anchor="w", font=("Helvetica", PUW_LABEL_FONT_SIZE, "bold"))
        self.window.date_entry = DateEntry(self.window, date_pattern="dd/mm/y", locale="fr", font=("Helvetica", PUW_BIG_ENTRY_FONT_SIZE), state="readonly")
        self.window.type_label = tk.Label(self.window, text="Type :", anchor="w", font=("Helvetica", PUW_LABEL_FONT_SIZE, "bold"))
        self.window.combobox = ttk.Combobox(self.window, value=TYPE_LIST, state="readonly", font=("Helvetica", PUW_BIG_ENTRY_FONT_SIZE))
        self.window.ticketrestau_value = tk.BooleanVar()
        self.window.ticketrestau_checkbutton = tk.Checkbutton(self.window, text="Payé en ticket restaurant", anchor="w", var=self.window.ticketrestau_value)
        self.window.nottakeintoaccount_value = tk.BooleanVar()
        self.window.nottakeintoaccount_checkbutton = tk.Checkbutton(self.window, text="Ne pas prendre en compte lors des calculs", var=self.window.nottakeintoaccount_value)
        self.window.button = tk.Button(self.window, text="AJOUTER", command=self.button_func)
        self.window.unvalid_label = tk.Label(self.window, text="Erreur de saisi !", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="red")
        self.window.expense_added_label = tk.Label(self.window, text="Nouvelle dépense ajouté !", font=("Helvetica", PUW_LABEL_FONT_SIZE), fg="green")

        # Config widgets
        self.nb_expenses = self.master.master.data.loc[self.master.master.data.member == self.member].shape[0] + 1
        self.window.description_entry.insert(0, "Dépense {}".format(self.nb_expenses))
        self.window.combobox.set("<AUTRE>")

        # Place widgets
        self.relx_left = 0.02
        self.relx_right = 0.5
        self.rely_bonus = 0.03
        self.relwidth=0.48
        self.relheight = 0.1
        self.window.description_label.place(relx=self.relx_left, rely=self.rely_bonus, relwidth=self.relwidth, relheight=self.relheight)
        self.window.description_entry.place(relx=self.relx_right, rely=self.rely_bonus, relwidth=self.relwidth, relheight=self.relheight)
        self.window.amount_label.place(relx=self.relx_left, rely=self.rely_bonus*2+self.relheight, relwidth=self.relwidth, relheight=self.relheight)
        self.window.amount_entry.place(relx=self.relx_right, rely=self.rely_bonus*2+self.relheight, relwidth=self.relwidth, relheight=self.relheight)
        self.window.date_label.place(relx=self.relx_left, rely=self.rely_bonus*3+self.relheight*2, relwidth=self.relwidth, relheight=self.relheight)
        self.window.date_entry.place(relx=self.relx_right, rely=self.rely_bonus*3+self.relheight*2, relwidth=self.relwidth, relheight=self.relheight)
        self.window.type_label.place(relx=self.relx_left, rely=self.rely_bonus*4+self.relheight*3, relwidth=self.relwidth, relheight=self.relheight)
        self.window.combobox.place(relx=self.relx_right, rely=self.rely_bonus*4+self.relheight*3, relwidth=self.relwidth, relheight=self.relheight)
        self.window.ticketrestau_checkbutton.place(relx=self.relx_left, rely=self.rely_bonus*7+self.relheight*4, relheight=self.relheight)
        self.window.nottakeintoaccount_checkbutton.place(relx=self.relx_left, rely=self.rely_bonus*7+self.relheight*5, relheight=self.relheight)
        self.window.button.place(relx=0.3, rely=self.rely_bonus*8+self.relheight*6, relwidth=0.4, relheight=self.relheight*1.2)

    def button_func(self, event=None):
        """ Command while pressing top level button """

        self.window.button.place_forget()

        # If no amount or date
        if not self.window.amount_entry.get() or not self.window.date_entry.get():
            self.window.unvalid_label.place(relx=0.1, rely=self.rely_bonus*8+self.relheight*6, relwidth=0.8, relheight=self.relheight*1.2)
        else:            
            # fill data.csv with this new expense
            new_expense = dict()
            new_expense["member"] = self.member
            new_expense["description"] = self.window.description_entry.get()
            new_expense["amount"] = float(self.window.amount_entry.get())
            new_expense["date"] = self.window.date_entry.get()
            new_expense["type"] = self.window.combobox.get()
            new_expense["ticket_restau"] = self.window.ticketrestau_value.get()
            new_expense["not_take_into_account"] = self.window.nottakeintoaccount_value.get()
            self.master.master.data = self.master.master.data.append(new_expense, ignore_index=True)

            # update widgets
            self.nb_expenses = self.nb_expenses + 1
            self.window.description_entry.delete(0, "end")
            self.window.description_entry.insert(0, "Dépense {}".format(self.nb_expenses))
            self.window.amount_entry.delete(0, "end")

            # place "new expense added" label
            self.window.expense_added_label.place(relx=0.1, rely=self.rely_bonus*8+self.relheight*6, relwidth=0.8, relheight=self.relheight*1.2)

    def bind_func(self, event=None):
        """ A function to make invisible "unvalid" label and make visible the button"""

        self.window.unvalid_label.place_forget()
        self.window.expense_added_label.place_forget()
        self.window.button.place(relx=0.3, rely=self.rely_bonus*8+self.relheight*6, relwidth=0.4, relheight=self.relheight*1.2)
    
    def callback_amount_func(self, input):
        """ Callback function """

        c = Counter(input)

        if c["."] > 1:
            return False

        if not all(i in ["0","1","2","3","4","5","6","7","8","9","."] for i in input):
            return False

        if len(input) > 6:
            return False

        else:
            self.window.unvalid_label.place_forget()
            self.window.expense_added_label.place_forget()
            self.window.button.place(relx=0.3, rely=self.rely_bonus*8+self.relheight*6, relwidth=0.4, relheight=self.relheight*1.2)
            return True  


class EditExpenses(tk.Button):
    """ Edit expenses button on right frame """

    def __init__(self, master):
        tk.Button.__init__(self, master)
        self.master = master
        self.config(font=("Helvetica", GW_RIGHT_FRAME_BUTTON_FONT_SIZE, "bold"))
        self.config(command=self.main_func)
    
    def main_func(self):
        """ Create a pop up window to edit expense """

        self.member = re.split(r"\'|\s", self.cget("text"))[-1]

        # Create pop up window
        self.window = PopUpWindow(self.master.master, "Dépenses : {}".format(self.member), PUW_WIDTH_EDIT_EXPENSES, PUW_HEIGHT_EDIT_EXPENSES)


        self.window.table = Table(self.window, dataframe=self.master.master.data.loc[self.master.master.data.member==self.member,:].copy())
        self.window.table.show()


class CalculatePart(tk.Frame):
    """ Calculate Part at the bottom of the left frame """

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.config(width=GW_LEFT_FRAME_SIZE, height=GW_CALCULATE_PART_HEIGHT)
        self.config(bg=GREEN)

        self.start_label = tk.Label(self, text='Début :', anchor="sw", bg=GREEN, font=("Helvetica", GW_END_START_LABEL_FONT_SIZE))
        self.calendar_start_entry = DateEntry(self, date_pattern="dd/mm/y", locale="fr", state="readonly")
        self.end_label = tk.Label(self, text='Fin :', anchor="sw", bg=GREEN, font=("Helvetica", GW_END_START_LABEL_FONT_SIZE))
        self.calendar_end_entry = DateEntry(self, date_pattern="dd/mm/y", locale="fr", state="readonly")
        self.calculate_button = tk.Button(self, text="CALCULER", font=("Helvetica", GW_CALCULATE_BUTTON_FONT_SIZE, "bold"))

        self.start_label.place(relx=0, rely=0, relwidth=0.5, relheight=0.25)
        self.calendar_start_entry.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.25)
        self.end_label.place(relx=0, rely=0.30, relwidth=0.5, relheight=0.25)
        self.calendar_end_entry.place(relx=0.5, rely=0.30, relwidth=0.5, relheight=0.25)
        self.calculate_button.place(relx=0, rely=0.65, relwidth=1, relheight=0.35)      
        

class RightFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.config(width=GW_RIGHT_FRAME_SIZE)
        self.config(highlightbackground="black", highlightthickness=1)
        self.config(bg="white")

        # Widgets
        self.new_expense_button = NewExpense(self)
        self.edit_expenses_button = EditExpenses(self)

    def hide_widget(self):
        """ Hide right frame widgets """

        for widget in self.winfo_children():
            widget.pack_forget()


class GroupWindow(tk.Toplevel):
    """ Group Window """

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master

        # Close app if group window is close
        self.protocol("WM_DELETE_WINDOW", self.close_window_func)

        # Create members list
        try :
            with open(os.path.join(GROUP_PATH, "members.txt"), "r") as f:
                self.members_list = json.loads(f.read())
            
        except:
            self.members_list = []
        
        # Load data
        try:
            self.data = pd.read_csv(os.path.join(GROUP_PATH, "data.csv"))
        except:
            try:
                self.data = pd.DataFrame(columns=["member","description", "amount", "date", "type", "ticket_restau", "not_take_into_account"])
            except:
                self.data = pd.DataFrame(columns=["member","description", "amount", "date", "type", "ticket_restau", "not_take_into_account"],
                                         parse_dates=["date"])

        # Create members widget list
        self.members_widget_list = []
    
        # Window customization 
        self.title("Groupe {}".format(GROUP_NAME))
        self.geometry("{}x{}+{}+{}".format(GW_WIDTH, GW_HEIGHT, GW_POS_X, GW_POS_Y))
        self.minsize(GW_WIDTH, GW_HEIGHT)
        self.maxsize(GW_WIDTH, GW_HEIGHT)
        self.config(bg="white")

        # Classes
        self.left_frame = LeftFrame(self)
        self.right_frame = RightFrame(self)
        self.menu_bar = MenuBar(self)

        # Classes position
        self.config(menu=self.menu_bar)
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(0)
        self.right_frame.pack(side="right", fill="y")
        self.right_frame.pack_propagate(0)


    def close_window_func(self):
        """ Actions while group window is closed """

        # save members list as members.txt
        with open(os.path.join(GROUP_PATH, "members.txt"), "w") as f:
            f.write(json.dumps(self.members_list))

        # save data as data.csv
        self.data.to_csv(os.path.join(GROUP_PATH, "data.csv"), index=False)
        
        # close app
        self.master.master.destroy()


# ------------------------------------------------ Launcher ---------------------------------------------------------

def main():
    master = tk.Tk()

    # Master Menu Window Customization
    master.title("Partage des dépenses")
    master.geometry("{}x{}+{}+{}".format(MW_WIDTH, MW_HEIGHT, MW_POS_X, MW_POS_Y))
    master.minsize(MW_WIDTH, MW_HEIGHT)
    master.maxsize(MW_WIDTH, MW_HEIGHT)

    MenuWindow(master).pack(expand=True, fill="both")
    master.mainloop()


if __name__ == "__main__":
    main()



