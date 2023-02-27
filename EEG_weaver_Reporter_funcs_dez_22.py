# ----------------------------------------------------------------
# Paulo Afonso Medeiros Kanda
# Taubate São Paulo Brazil
# 2023-04-20
# EEG Reporter is part of EEGWeaver project
# to improve clinical use of post-processing EEG
# Yes! If you are here You will see the code is messy, with lots of comments and  debugs
# part of my learning process, indulge me.
# ----------------------------------------------------------------

import tkinter as tk
# from tkinter import PhotoImage
from tkinter import ttk, END, Toplevel
from tkinter import messagebox
# from tkinter import filedialog
from tkinter import Label
from tkinter import LEFT, CENTER, SOLID
# from tkinter import font
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename

import PIL
from PIL import Image, ImageTk
import PIL.Image
import sqlite3

import datetime
from datetime import datetime

from pages_to_connect_pages import Pages
import json
from reportlab.lib.pagesizes import letter, A4
from reporter_filepath import resource_path

# to create csv backups of each report
import csv
import pyperclip  # to copy to clipboard
import os
import sys
import shutil


class Funcs:
    """
    functions related to sql3
    """
    
    def __init__(self):
        self.font_size_selected = None
        self.now = None
        self.report_date = None
        self.reportlab_fonts_to_use = None
        self.my_specific_font = None
        self.retrieved_radiob1_cbox_aba4_json = None
        self.json_show_or_not_PDFradiob56_aba4_var = None
        self.retrieved_currentFont_comBx_aba4_json = None
        self.retrieved_radiob_arrow_aba4_json = None
        self.retrieved_Pdf_NewTitle_typedin_entry_json = None
        self.retrieved_Pdf_Title_1or2_aba4_var_json = None
        self.json_letter_or_A4_radiob1_aba4_var = None
        self.json_show_or_not_Table_radiob78_aba4_var = None
        self.json_port_eng_radiob34_aba4_var = None
        self.updated_list_with_newdb = None
        self.current_db = None
        self.signature_image = None
        self.tkimage2 = None
        self.tkimage1 = None
        # self.tkimage_font_normal = None
        # self.tkimage_font_bold = None
        self.advise_label = None
        self.listaCli_Dic = None
        self.listaCli_imagePath = None
        self.listaCli_imagePath_logo = None
        self.history_ref = None
        self.history1_ref = None
        self.signature_image_ref = None
        self.signature_image_ref_logo = None
        self.footer_ref = None
        self.body_ref = None
        self.header_ref = None
        self.report_Date_ref = None
        self.srate_ref = None
        self.hff_ref = None
        self.lff_ref = None
        self.diag_ref = None
        self.age_ref = None
        self.comboGender_ref = None
        self.patient_ref = None
        self.id_ref = None
        self.Id_entry = None
        self.cursor = None
        self.conn = None
        self.radiob_cbox_aba4_var = None
        self.font_chosen_cbox = None
        self.radiob_arrow_aba4_var = None
        # self.pdf_titlename_var = None
        self.radiob90_1or2_aba4_var = None
        self.radiob78_aba4_var = None
        self.radiob1_aba4_var = None
        self.radiob56_aba4_var = None
        self.radiob34_aba4_var = None
        self.db_path_aba3_cbox = None
        self.collected_image = None
        self.frame_header = None
        self.search_patient_entry3 = None
        self.listaCli = None
        self.gender_chosen = None
        self.txt_history = None
        self.txt_history1 = None
        self.signature_img_entry = None
        self.signature_img_entry_logo = None
        self.txt_footer = None
        self.txt_body = None
        self.txt_header = None
        self.report_Date_entry = None
        self.srate_entry = None
        self.HFF_entry = None
        self.LFF_entry = None
        self.diag_entry = None
        self.age_entry = None
        self.comboGender = None
        self.patient_entry = None
    
    
    # # -------------------------get gender chosen
    #
    # def check_comboGender(self, event):
    #     """
    #     binding to sex chosen
    #     """
    #
    #     self.this_is_gender_chosen = self.comboGender.get()
    #
    #     print('self.this_is_gender_chosen', self.this_is_gender_chosen)
    #
    #
    #
    # # -------------------------get gender chosen end
    
    # --------------get date for today
    def get_today_date(self):
        
        self.now = datetime.now()
        
        self.json_port_eng_radiob34_aba4_var = self.retrieve_portg_or_eng_radiob34_aba4_json()
        
        if self.json_port_eng_radiob34_aba4_var == 1:
            self.report_date = (self.now.strftime("%m-%d-%Y"))
        elif self.json_port_eng_radiob34_aba4_var == 2:
            self.report_date = (self.now.strftime("%d-%m-%Y"))  # report_date(now.strftime("%d-%m-%y %H:%M:%S"))    #
        self.report_Date_entry.delete(0, END)
        self.report_Date_entry.insert(END, self.report_date)  #
    
    def clear_screen_funcs(self):
        """
        clean gui fields
        """
        self.Id_entry.config(state="normal")
        self.Id_entry.delete(0, END)
        self.Id_entry.config(state="disable")
        
        self.patient_entry.delete(0, END)
        self.comboGender.set('')
        self.age_entry.delete(0, END)
        self.diag_entry.delete(0, END)
        self.LFF_entry.delete(0, END)
        self.HFF_entry.delete(0, END)
        self.srate_entry.delete(0, END)
        self.report_Date_entry.delete(0, END)
        self.txt_header.delete('1.0', END)  # this is a text widget not entry
        self.txt_body.delete('1.0', END)
        self.txt_footer.delete('1.0', END)
        self.signature_img_entry_logo.delete(0, END)
        self.signature_img_entry.delete(0, END)
        self.txt_history1.delete('1.0', END)
        self.txt_history.delete('1.0', END)
        
        # delete:  self.report_Date_entry.delete(0, END) and insert it again to avoid
        # a bug that keeps repeting date in pdf generation
        self.get_today_date()
    
    def delete_history(self):
        self.txt_history.delete('1.0', END)  # this is a text widget not entry
        self.update_report()
    
    def clear_screen_but_history(self):
        """
        clean gui fields, it does not clear treeview fields at bottom of first
        notebook ear
        """
        #  self.Id_entry.config allow and deny using entry to avoid user imput value but allow app insert value in entry
        self.Id_entry.config(state="normal")
        self.Id_entry.delete(0, END)
        self.Id_entry.config(state="disable")
        self.patient_entry.delete(0, END)
        self.comboGender.set('')
        self.age_entry.delete(0, END)
        self.diag_entry.delete(0, END)
        self.LFF_entry.delete(0, END)
        self.HFF_entry.delete(0, END)
        self.srate_entry.delete(0, END)
        self.report_Date_entry.delete(0, END)
        self.txt_header.delete('1.0', END)
        self.txt_body.delete('1.0', END)
        self.txt_footer.delete('1.0', END)
        self.signature_img_entry_logo.delete(0, END)
        self.signature_img_entry.delete(0, END)
        self.txt_history1.delete('1.0', END)
        
        # delete:  self.report_Date_entry.delete(0, END) and insert it again to avoid
        # a bug that keeps repeting date in pdf generation
        self.get_today_date()
    
    def delete_logo(self):
        self.signature_img_entry_logo.delete(0, END)
        self.update_report()
    
    def delete_signature(self):
        """
        self.signature is an image file use to show your signature
        """
        self.signature_img_entry.delete(0, END)
        self.update_report()
    
    def connect_db(self):
        
        #  to allow relative path
        # appdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        #
        # try:
        #     self.conn = sqlite3.connect(os.path.join(appdir, Pages.current_main_db_in_use))
        # except (FileNotFoundError, IOError):
        #     pass
        
        try:
            self.conn = sqlite3.connect(Pages.current_main_db_in_use)  # databank name
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError:
            pass
            # tk.messagebox.showwarning('warning', 'Cannot find that databank')
    
    def disconnect_db(self):
        self.conn.close()
    
    def create_Table(self):
        db_new_name = Pages.current_main_db_in_use
        self.connect_db()
        # criar tabela  cliente é tabela dentro do banco clientes.db
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY,
                    patient_name CHAR NOT NULL,
                    gender CHAR,
                    age CHAR,
                    diagnosis CHAR,
                    lff FLOAT,
                    hff FLOAT,
                    sampling_rate INTEGER,
                    recdate DATE,
                    header  CHAR,
                    body  CHAR,
                    footer  CHAR,
                    signature_image_db_logo CHAR,
                    signature_image_db CHAR,
                    patient_history1 CHAR,
                    patient_history CHAR)
            """)
        except AttributeError:
            return
        self.conn.commit()
        self.disconnect_db()
    
    def report_variables(self):
        
        self.id_ref = self.Id_entry.get()
        # print("self.id_ref", self.id_ref)
        
        self.patient_ref = self.patient_entry.get()
        # print('self.patient_ref ', self.patient_ref)
        # ___________________
        self.combobox_chosen()
        # self.gender_chosen = self.comboGender.get()
        # return self.gender_chosen
        
        self.comboGender_ref = self.gender_chosen
        # print('self.comboGender_ref', self.comboGender_ref)
        # ___________________
        
        self.age_ref = self.age_entry.get()
        # print('self.age_ref', self.age_ref)
        
        self.diag_ref = self.diag_entry.get()
        # print('self.diag_ref', self.diag_ref)
        
        self.lff_ref = self.LFF_entry.get()
        # print('self.lff_ref', self.lff_ref)
        
        self.hff_ref = self.HFF_entry.get()
        # print('self.hff_ref', self.hff_ref)
        
        self.srate_ref = self.srate_entry.get()
        # print('self.srate_ref', self.srate_ref)
        # ___________________

        self.report_Date_entry.delete(0, END)
        self.report_Date_entry.insert(END, self.report_date)
        self.report_Date_ref = self.report_Date_entry.get()
        # print('self.report_Date_ref', self.report_Date_ref)
        
        # ___________________
        self.header_ref = self.txt_header.get('1.0', 'end-1c')
        Pages.header_object = self.header_ref
        
        self.body_ref = self.txt_body.get('1.0', 'end-1c')
        self.footer_ref = self.txt_footer.get('1.0', 'end-1c')
        
        # we create a "self.signature_img_entry_logo = ttk.Entry" 'fake'
        # just to insert the image to direct it to treeview
        self.signature_image_ref_logo = self.signature_img_entry_logo.get()
        self.signature_image_ref = self.signature_img_entry.get()
        
        self.history1_ref = self.txt_history1.get('1.0', 'end-1c')
        self.history_ref = self.txt_history.get('1.0', 'end-1c')
    
    def duplicate_report(self):
        """
        what is inserted in data bank is   self.patient_ref, self.comboGender_ref, etc
        """
        self.report_variables()
        self.connect_db()
        # id don't go bellow because it is a prymary key
        self.cursor.execute(""" INSERT INTO clientes(
                                patient_name,
                                gender,
                                age,
                                diagnosis,
                                lff,
                                hff,
                                sampling_rate,
                                recdate,
                                header,
                                body,
                                footer,
                                signature_image_db_logo,
                                signature_image_db,
                                patient_history1,
                                patient_history)
                             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """,
                            (
                                self.patient_ref,
                                self.comboGender_ref,
                                self.age_ref,
                                self.diag_ref,
                                self.lff_ref,
                                self.hff_ref,
                                self.srate_ref,
                                self.report_Date_ref,
                                self.header_ref,
                                self.body_ref,
                                self.footer_ref,
                                self.signature_image_ref_logo,
                                self.signature_image_ref,
                                self.history1_ref,
                                self.history_ref)
                            )
        
        self.conn.commit()
        self.disconnect_db()
        self.select_lista()
        # self.clear_screen_funcs()
        
        # message pops up and desapear after seconds:
        advise_label_variable = 'Report\nDuplicated'  # , tk.font=("Arial", 25)
        self.I_did_it(advise_label_variable)
    
    def save_report(self):
        
        self.report_Date_entry.delete(0, END)
        self.report_Date_entry.insert(END, self.report_date)
        
        self.report_variables()
        self.connect_db()
        
        # date_today = self.report_Date_entry.get()
        # if date_today != ''
        #     self.report_Date_ref = self.report_Date_entry.get()
        # else:
        #
        
        # id don't go bellow because it is a prymary key
        self.cursor.execute(""" INSERT INTO clientes(patient_name, gender, age, diagnosis,
                                lff, hff, sampling_rate, recdate, header, body, footer,
                                signature_image_db_logo, signature_image_db, patient_history1,
                                patient_history) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """,
                            (
                                self.patient_ref,
                                self.comboGender_ref,
                                self.age_ref,
                                self.diag_ref,
                                self.lff_ref,
                                self.hff_ref,
                                self.srate_ref,
                                self.report_Date_ref,
                                self.header_ref,
                                self.body_ref,
                                self.footer_ref,
                                self.signature_image_ref_logo,
                                self.signature_image_ref,
                                self.history1_ref,
                                self.history_ref
                            ))
        self.conn.commit()
        self.disconnect_db()
        # updatetreeview:
        self.select_lista()
        
        advise_label_variable = 'Report Saved'
        self.I_did_it(advise_label_variable)

        self.report_Date_entry.delete(0, END)
        self.report_Date_entry.insert(END, self.report_date)

    # ---- import from csv start
    
    def import_one_report(self):
        """
        get csv values from func read_csv_to_import
        
        """
        f1 = askopenfilename()
        
        self.read_csv_to_import(f1)
    
    def read_csv_to_import(self, filename_csv):
        
        # self.report_variables()
        
        self.connect_db()
        
        with open(filename_csv) as f:
            reader = csv.reader(f)
            for field in reader:
                # id don't go bellow because it is a prymary key
                self.cursor.execute(""" INSERT INTO clientes(patient_name, gender, age, diagnosis,
                                            lff, hff, sampling_rate, recdate, header, body, footer,
                                            signature_image_db_logo, signature_image_db, patient_history1,
                                            patient_history) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """, field)
        
        self.conn.commit()
        self.disconnect_db()
        
        # updatetreeview:
        self.select_lista()
        
        advise_label_variable = 'Report Imported'
        self.I_did_it(advise_label_variable)
    
    # ---- import from csv end
    
    def select_lista(self):
        """
        to data appear in listacli(update)
        """
        self.listaCli.delete(*self.listaCli.get_children())
        self.connect_db()
        try:
            lista = self.cursor.execute(""" SELECT id,
                                        patient_name,
                                        gender,
                                        age,
                                        diagnosis,
                                        lff,
                                        hff,
                                        sampling_rate,
                                        recdate,
                                        header,
                                        body,
                                        footer,
                                        signature_image_db_logo,
                                        signature_image_db,
                                        patient_history1,
                                        patient_history
                                        FROM clientes ORDER BY patient_name ASC; """)
        except AttributeError:
            return
        # ASC  calls client in ascendent order    DESC is the contrary
        
        self.listaCli.tag_configure('oddrow', background='#ebf5fb')
        self.listaCli.tag_configure('evenrow', background="#d4e6f1")
        
        for i in lista:
            # self.listaCli.insert("", END, values=i)
            if i[0] % 2 == 0:
                self.listaCli.insert("", END, values=i, tags=('evenrow',))
            if i[0] % 2 != 0:
                self.listaCli.insert("", END, values=i, tags=('oddrow',))
        
        self.disconnect_db()
    
    # __________________
    # @property
    def get_header_image_logo(self) -> str:
        """
        self.select_listaCli_Item() returns:
        self.listaCli_Dic['values'][12] --> that is the position of image [12]
        in a dictionary from values found in treeview table,
        this func returns imagepath found in treeview. Image goes in header of pdf
        """
        
        self.listaCli_imagePath_logo = ''
        self.select_listaCli_Item()
        
        try:
            
            if self.listaCli_Dic['values'][12] == '':
                self.listaCli_imagePath_logo = ''
            elif self.listaCli_Dic['values'][12] != '':
                # self.select_listaCli_Item()
                self.listaCli_imagePath_logo = self.listaCli_Dic['values'][12]
            Pages.listaCli_imagePath_logo = self.listaCli_imagePath_logo
        
        except IndexError:
            pass
        
        return self.listaCli_imagePath_logo
    
    # __________________
    
    def get_footer_image(self):
        """
        self.select_listaCli_Item() returns:
        self.listaCli_Dic['values'][12] --> that is the position of image [12]
        in a dictionary from values found in treeview table,
        this func returns imagepath found in treeview. Image goes in footer of pdf
        """
        
        self.listaCli_imagePath = ''
        self.select_listaCli_Item()
        
        # if self.listaCli_Dic['values'][12] == '':
        #     self.listaCli_imagePath = ''
        try:
            if self.listaCli_Dic['values'][13] == '':
                self.listaCli_imagePath = ''
            elif self.listaCli_Dic['values'][13] != '':
                # self.select_listaCli_Item()
                self.listaCli_imagePath = self.listaCli_Dic['values'][13]
            Pages.listaCli_imagePath = self.listaCli_imagePath
        except IndexError:
            pass
        
        return self.listaCli_imagePath
        
        # except:
        #     pass
    
    def LeftButtonClick(self, event):
        
        col3 = ''
        self.clear_screen_funcs()
        self.listaCli.selection()
        # self. signature_image_to_list()
        # test =self.signature_image_ref.list()
        self.get_header_image_logo()
        self.get_footer_image()
        
        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, \
                col10, col11, col12, col13, col14, col15, col16 = self.listaCli.item(n, 'values')
            
            self.Id_entry.config(state="normal")
            self.Id_entry.insert(END, col1)
            self.Id_entry.config(state="disable")
            
            self.patient_entry.insert(END, col2)
            self.comboGender.insert(END, col3)
            self.age_entry.insert(END, col4)
            self.diag_entry.insert(END, col5)
            self.LFF_entry.insert(END, col6)
            self.HFF_entry.insert(END, col7)
            self.srate_entry.insert(END, col8)
            self.report_Date_entry.insert(END, col9)
            self.txt_header.insert(END, col10)
            self.txt_body.insert(END, col11)
            self.txt_footer.insert(END, col12)
            self.signature_img_entry_logo.insert(END, col13)
            self.signature_img_entry.insert(END, col14)
            self.txt_history1.insert(END, col15)
            self.txt_history.insert(END, col16)
        
        self.select_listaCli_Item()
        # print(self.listaCli.item(listaCli_Item))
        # self.get_header_image_logo
        self.get_footer_image()
        Pages.listaCli_imagePath_logo = self.listaCli_imagePath_logo
        Pages.listaCli_imagePath = self.listaCli_imagePath
        
        #get listaCli treeview item sex (col3) and set as comboGender option chosen
        self.comboGender.set(col3)
        # get sex to put in pdf
        
        self.gender_chosen = self.comboGender.get()

        
    def select_listaCli_Item(self) -> dict:
        """
        https://stackoverflow.com/questions/30614279/tkinter-treeview-get-selected-item-values
        This will output a dictionary, from which you can then retrieve individual values
        we return all values in listaCli as dictionary
        """
        listaCli_Item = self.listaCli.focus()
        self.listaCli_Dic = self.listaCli.item(listaCli_Item)
        
        # DEBUG:
        # print('self.listaCli.item(listaCli_Item)',self.listaCli.item(listaCli_Item))
        # print('self.listaCli_Dic', self.listaCli_Dic)
        # {'text': '', 'image': '',
        #  'values': [8, 'dfsa', 'Male', 'w', 'dfgfsd', '1.0', '1.0', 11111, '25-03-2022', 'fasdfsa', 'fsdfsad',
        #             'fdsafsad', 'C:/000_tmp/rafael_kanda_2022.png', ''], 'open': 0, 'tags': ''}
        
        # if self.listaCli_Dic['values'][12] == '':
        #     self.listaCli_Dic['values'][12] = 0
        # print('self.listaCli_Dic', self.listaCli_Dic['values'][12])
        
        return self.listaCli_Dic  # a dictionary with values of treeview.
    
    def delete_report(self):
        result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.report_variables()
            self.connect_db()
            self.cursor.execute("""DELETE FROM clientes WHERE id = ?""", (self.id_ref,))
            # self.cursor.execute("""DELETE FROM clientes WHERE patient_name = ?""", (self.patient_ref,))
            self.conn.commit()
            self.disconnect_db()
            self.select_lista()
            self.clear_screen_funcs()
            # atualiza treeview
            
            advise_label_variable = 'Report Deleted'
            self.I_did_it(advise_label_variable)
            self.report_Date_entry.delete(0, END)
            self.report_Date_entry.insert(END, self.report_date)
            # restore entry date after del
        else:
            pass
    
    def delete_many(self):
        response = messagebox.askyesnocancel("Delete Selected????",
                                             "This will DELETE ITEMS SELECTED FROM the Table\nAre you sure? ")
        
        if response == 1:  # yes
            # designate selections
            x = self.listaCli.selection()  # --> it is the lines selected
            
            # create list  of ids for delete
            ids_to_delete = []
            
            # this loop gives us a sequence of ids to  be deleted,
            # but  we must create a list as reference for delect
            # add selections to ids_to_delete list
            for record in x:
                ids_to_delete.append(self.listaCli.item(record, 'values')[0])  # -->index of id
            
            # debug
            # print(ids_to_delete)
            # ['4', '5', '7']
            # we must say delete all records with those ids
            
            # delete from treeview
            for record in x:
                self.listaCli.delete(record)
            
            self.connect_db()
            
            self.cursor.executemany("DELETE FROM clientes WHERE id = ?", [(a,) for a in ids_to_delete])
            
            self.conn.commit()
            self.cursor.close()
            self.disconnect_db()
            self.clear_screen_funcs()
            self.report_Date_entry.delete(0, END)
            self.report_Date_entry.insert(END, self.report_date)
            # restore entry date after del
    
    def drop_table_all(self):
        """
        Delete all
        """
        response = messagebox.askyesnocancel("Delete All????",
                                             "This will DELETE EVERYTHING FROM the Table\nAre you sure? ")
        
        if response == 1:  # yes
            
            for record in self.listaCli.get_children():
                # clear treeview
                self.listaCli.delete(record)
                
                self.connect_db()
                
                # delete everything from table   (dropp a table= delete)
                self.cursor.execute("DROP TABLE clientes")
                
                # self.cursor.execute
                self.conn.commit()
                self.cursor.close()
                self.disconnect_db()
                
                # clear entry boxes if filled:
                self.clear_screen_funcs()
                
                # recretate new table
                self.create_Table()
        
        advise_label_variable = 'Table Destroyed'
        self.I_did_it(advise_label_variable)
        self.report_Date_entry.delete(0, END)
        self.report_Date_entry.insert(END, self.report_date)  # restore entry date after del
    
    def update_report(self):  # button save update
        
        self.report_Date_entry.delete(0, END)
        self.report_Date_entry.insert(END, self.report_date)
        self.report_variables()
        self.connect_db()
        # self.clear_screen_funcs()
        # self.listaCli.selection()
        
        self.cursor.execute(""" UPDATE clientes SET
                                patient_name = ?,
                                gender = ?,
                                age = ?,
                                diagnosis = ?,
                                lff = ?,
                                hff = ?,
                                sampling_rate = ?,
                                recdate = ?,
                                header = ?,
                                body= ?,
                                footer = ?,
                                signature_image_db_logo = ?,
                                signature_image_db = ?,
                                patient_history1 = ?,
                                patient_history = ?
                                WHERE id = ? """, (
            self.patient_ref,
            self.comboGender_ref,
            self.age_ref,
            self.diag_ref,
            self.lff_ref,
            self.hff_ref,
            self.srate_ref,
            self.report_Date_ref,
            self.header_ref,
            self.body_ref,
            self.footer_ref,
            self.signature_image_ref_logo,
            self.signature_image_ref,
            self.history1_ref,
            self.history_ref,
            self.id_ref))
        
        self.conn.commit()
        self.disconnect_db()
        # self.clear_screen_funcs()
        
        self.select_lista()  # populate list from databank
        
        self.select_listaCli_Item()  # gives us a dictionary with all values of listaCli by index
        
        # ----------------------------create Pages.listaClin_imagePath_logo
        try:  # [12] is image path from listaClin
            self.listaCli_imagePath_logo = self.listaCli_Dic['values'][12]
        except IndexError:
            self.listaCli_imagePath_logo = self.signature_img_entry_logo.get()
        
        # except Exception as e:
        #     print('type is:', e.__class__.__name__)
        #     # print_exc()
        
        Pages.listaCli_imagePath_logo = self.listaCli_imagePath_logo
        
        # ----------------------------create Pages.listaClin_imagePath
        try:  # [12] is image path from listaClin
            self.listaCli_imagePath = self.listaCli_Dic['values'][13]
            # except :
            self.listaCli_imagePath = self.signature_img_entry.get()
            
            Pages.listaCli_imagePath = self.listaCli_imagePath
        except IndexError:
            pass
        # --------------------------------------
        
        advise_label_variable = 'Report Modified'
        self.I_did_it(advise_label_variable)
    
    # ---------
    def export_one_report(self):
        """
        get info from sqlite:
        https://sqlite.org/forum/info/114a1772a20ea870
        """
        # result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
        # if result == 'yes':
        self.report_variables()
        self.connect_db()
        
        # debug:
        # select all where id is:
        # self.cursor.execute("""SELECT * FROM clientes WHERE id = ?""", (self.id_ref,))
        # delete where id is:
        # self.cursor.execute("""DELETE FROM clientes WHERE id = ?""", (self.id_ref,))
        # select all where patient_name is:
        # self.cursor.execute("""SELECT * FROM clientes WHERE patient_name = ?""", (self.patient_ref,))
        
        self.cursor.execute("""SELECT * FROM clientes WHERE patient_name = ?""", (self.patient_ref,))
        # gets one row:
        row = self.cursor.fetchone()
        
        # debug:
        # print(row) has the index 2
        # (2, 'test2', 'Sex', '', '', '', '', '', '01-08-2023', '', '', '', '', '', '', '')
        
        # when creating csv, sqlit_items remove the index id which is not used in csv, ex: number 2 above:
        sqlit_items = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                       row[9], row[10], row[11], row[12], row[14], row[14], row[15])
        # print(sqlit_items)
        # ('test2', 'Sex', '', '', '', '', '', '01-08-2023', '', '', '', '', '', '', '')
        
        inicial_name = row[1]
        # file_csv = ''
        self.save_file_csv(sqlit_items, inicial_name)
        
        self.conn.commit()
        self.disconnect_db()

    
    # ---------
    
    @staticmethod
    def save_file_csv(one_row, inicial_name):
        """
        this makes backup of individual report to allow share with other users or backup of
        report, it goes inside "export_one_report"
        """
        # data = [('All tyes(*.*)', '*.*'), ("csv file(*.csv)", "*.csv")]
        data = [("csv file(*.csv)", "*.csv")]
        file_csv = asksaveasfilename(filetypes=data, defaultextension=data, initialfile=inicial_name)
        # asksaveasfile return a file object,
        # while asksaveasfilename only return the selected filename.
        # file will have file name provided by user.
        
        # Now we can use this file name to save file.
        # user selected file:
        if file_csv:
            try:
                # with open(file_csv, 'w') as f:
                with open(file_csv, mode = "w", encoding = "utf-8",  newline='') as csv_file:
                    
                    # create the csv writer
                    writer = csv.writer(csv_file)
                    
                    # writer.writerow([i[0] for i in self.cursor.description])
                    
                    # write a row to the csv file
                    writer.writerow(one_row)
                    
                    # message pops up and desapear after seconds:
            
            # user don't selected file:
            except csv.Error as error:
                message_csv = 'Your file is empty! \nFirst choose \n(click) on a report \nto export it.'
                tk.messagebox.showerror(title="Attention:", message=message_csv)
        else:
            # if user cancel copy
            return
    
    # ---- import from csv start
    
    def import_one_report(self):
        """
        get csv values from func read_csv_to_import
        """
        data = [("csv file(*.csv)", "*.csv")]
        f1 = askopenfilename(filetypes=data, defaultextension=data)
        self.read_csv_to_import(f1)
    
    def read_csv_to_import(self, filename_csv):
        # self.report_variables()
        self.connect_db()
        
        try:
            with open(filename_csv,'r', encoding='utf-8', errors='ignore') as file_csv:   # , mode = "r"
                reader = csv.reader(file_csv)

                for field in reader:
                    print('field', field)
                    self.field_csv = field
                    patient_input = self.field_csv[0]
                    print('patient_input',patient_input)
                    gender_input = self.field_csv[1]
                    age_input = self.field_csv[2]
                    diag_input = self.field_csv[3]
                    lff_input = self.field_csv[4]
                    hff_input = self.field_csv[5]
                    sample_input = self.field_csv[6]
                    recdate_input = self.field_csv[7]
                    header_input = self.field_csv[8]
                    body_input = self.field_csv[9]
                    footer_input = self.field_csv[10]
                    logo_input = self.field_csv[11]
                    sig_input = self.field_csv[12]
                    history1_input = self.field_csv[13]
                    history_input = self.field_csv[14]
                    
                    
                    # id don't go bellow because it is a prymary key
                    # You need to use a list as the second argument to conn.execute(...)! in our case field
                    self.cursor.execute(""" INSERT INTO clientes(patient_name, gender, age, diagnosis,
                                                lff, hff, sampling_rate, recdate, header, body, footer,
                                                signature_image_db_logo, signature_image_db, patient_history1,
                                                patient_history) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", (
                                                patient_input,
                                                gender_input,
                                                age_input,
                                                diag_input,
                                                lff_input,
                                                hff_input,
                                                sample_input,
                                                recdate_input,
                                                header_input,
                                                body_input,
                                                footer_input,
                                                logo_input,
                                                sig_input,
                                                history1_input,
                                                history_input
                                                # self.field_csv,
                                                ))  #(field,))
                   
                   
                   
                   
                   
                    # # [field]) # (field,))
                    # self.cursor.executemany('INSERT INTO clientes VALUES(?)', zip(field))
            
            self.conn.commit()
            self.disconnect_db()
            
            # updatetreeview:
            self.select_lista()
            
            advise_label_variable = 'Report Imported'
            self.I_did_it(advise_label_variable)
        
        except FileNotFoundError:
            tk.messagebox.showwarning('Warning:', 'Cannot find that File.')
    
    # ---- import from csv end
    
    def search_report(self, name):
        
        self.connect_db()
        self.listaCli.delete(*self.listaCli.get_children())
        
        self.search_patient_entry3.insert(END, '%')  # % search for everything plus  typed charaacters
        name = self.search_patient_entry3.get()
        
        # use   names of columns from sqlite3 table,don't use names of our variables
        # LIKE searches for where is patient_name full column search
        self.cursor.execute(
            """ SELECT
            id,
            patient_name,
            gender,
            age,
            diagnosis,
            lff,
            hff,
            sampling_rate,
            recdate,
            header,
            body,
            footer,
            signature_image_db_logo,
            signature_image_db,
            patient_history1,
            patient_history
            FROM clientes WHERE patient_name LIKE ? """, ('%' + name + '%',))
        # fantastic: https://stackoverflow.com/questions/48928370/how-to-query-from-sqlite3-database-if-content-in-
        # the-entry-match-small-requireme
        # ('%' + name + '%',) --> allows to find any word in string value
        # (name+'%',) --> just first word in string.
        
        # FROM clientes WHERE patient_name LIKE '%s' ORDER BY patient_name ASC""" % name)  --> first word in string
        
        search_name_Cli = self.cursor.fetchall()
        for i in search_name_Cli:
            self.listaCli.insert('', END, values=i)
        
        self.clear_screen_funcs()
        
        self.disconnect_db()
        self.search_patient_entry3.delete(0, 'end')
        
        advise_label_variable = 'Searching'
        self.I_did_it(advise_label_variable)
    
    def record_up(self):
        rows = self.listaCli.selection()
        for row in rows:
            self.listaCli.move(row, self.listaCli.parent(row), self.listaCli.index(row) - 1)
    
    def ascending(self):
        self.connect_db()
        
        self.listaCli.delete(*self.listaCli.get_children())
        
        try:
            # self.cursor.execute("SELECT * FROM clientes ORDER BY 'id' ASC")
            self.cursor.execute("SELECT * FROM clientes ORDER BY PATIENT_NAME ASC")
        except AttributeError:
            return
        
        fetch = self.cursor.fetchall()
        # print(fetch)
        
        # for data in fetch:
        #     self.listaCli.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5],
        #                                             data[6], data[7], data[8], data[9], data[10], data[11],
        #                                             data[12], data[13], data[14], data[15]))
        
        self.listaCli.tag_configure('oddrow', background='#ebf5fb')
        self.listaCli.tag_configure('evenrow', background="#d4e6f1")
        
        for data in fetch:
            # self.listaCli.insert("", END, values=i)
            
            if data[0] % 2 == 0:
                self.listaCli.insert("", END, values=(data[0], data[1], data[2], data[3], data[4], data[5],
                                                      data[6], data[7], data[8], data[9], data[10], data[11],
                                                      data[12], data[13], data[14], data[15]),
                                     tags=('evenrow',))
            if data[0] % 2 != 0:
                self.listaCli.insert("", END, values=(data[0], data[1], data[2], data[3], data[4], data[5],
                                                      data[6], data[7], data[8], data[9], data[10], data[11],
                                                      data[12], data[13], data[14], data[15]),
                                     tags=('oddrow',))
        
        self.cursor.close()
        self.conn.close()
    
    def record_down(self):
        rows = self.listaCli.selection()
        for row in reversed(rows):
            self.listaCli.move(row, self.listaCli.parent(row), self.listaCli.index(row) + 1)
    
    def descending(self):
        self.connect_db()
        
        self.listaCli.delete(*self.listaCli.get_children())
        
        self.cursor.execute("SELECT * FROM clientes ORDER BY PATIENT_NAME DESC")
        
        fetch = self.cursor.fetchall()
        # print(fetch)
        
        self.listaCli.tag_configure('oddrow', background='#ebf5fb')
        self.listaCli.tag_configure('evenrow', background="#d4e6f1")
        
        for data in fetch:
            # self.listaCli.insert("", END, values=i)
            if data[0] % 2 == 0:
                self.listaCli.insert("", END, values=(data[0], data[1], data[2], data[3], data[4], data[5],
                                                      data[6], data[7], data[8], data[9], data[10], data[11],
                                                      data[12], data[13], data[14], data[15]),
                                     tags=('evenrow',))
            if data[0] % 2 != 0:
                self.listaCli.insert("", END, values=(data[0], data[1], data[2], data[3], data[4], data[5],
                                                      data[6], data[7], data[8], data[9], data[10], data[11],
                                                      data[12], data[13], data[14], data[15]),
                                     tags=('oddrow',))
        self.cursor.close()
        self.conn.close()
    
    def I_did_it(self, advise_label_variable):
        """
        label that appears and disappears to say that something was done
        """
        adviseStyle = ttk.Style()
        # style.configure("Red.TLabel", foreground="red")
        
        adviseStyle.theme_use('clam')
        # boldStyle.configure("Bold.TButton", font=('Sans', '10', 'bold'))
        adviseStyle.configure('TLabel', foreground="black", background='#FFC300')
        
        self.advise_label = ttk.Label(self.frame_header, text=advise_label_variable, style='TLabel',
                                      anchor=CENTER, borderwidth=6, relief="solid", font='Helvetica 10 bold')
        self.advise_label.place(relx=0.8, rely=0.3, relwidth=0.1, relheight=0.4)
        self.frame_header.after(3000, self.advise_label.destroy)
        
        # self.advise_label.configure("Red.TLabel")
    
    def icon_images(self):
        """
        these images are used no make icons
        """
        # image_bold = r"G:\PycharmProjects\EEG_WEAVER\images\font_bold.png"
        # image_bold = resource_path("font_bold.png")
        #
        # image_font_bold = PIL.Image.open(image_bold)
        # image_font_bold = image_font_bold.resize((30, 30), PIL.Image.ANTIALIAS)
        # self.tkimage_font_bold = PIL.ImageTk.PhotoImage(image_font_bold)
        #
        # image_normal = r"G:\PycharmProjects\EEG_WEAVER\images\font_normal.png"
        # image_normal = resource_path("font_normal.png")
        # image_font_normal = PIL.Image.open(image_normal)
        # image_font_normal = image_font_normal.resize((30, 30), PIL.Image.ANTIALIAS)
        # self.tkimage_font_normal = PIL.ImageTk.PhotoImage(image_font_normal)
        
        # Create a photoimage object of the image in the path
        image_up = resource_path("./images/up_arrow.png")
        image1 = PIL.Image.open(image_up)
        # image1 = image1.resize((15, 15), PIL.Image.ANTIALIAS)
        self.tkimage1 = PIL.ImageTk.PhotoImage(image1)
        # zoom also works but I prefer resize
        # https://stackoverflow.com/questions/28786147/limit-the-size-of-a-button-with-an-image
        
        image_down = resource_path("./images/down_arrow.png")
        image2 = PIL.Image.open(image_down)
        # image2 = image2.resize((15, 15), PIL.Image.ANTIALIAS)
        self.tkimage2 = PIL.ImageTk.PhotoImage(image2)
    
    # -----
    
    def collect_image_footer(self):
        """
        That was  tough because treeview doesnot accept strings just tuples and lists
        get image to use as signature in right part of footer
        this function generates a path a file
        example: self.signature_image  C:/000_tmp/Paulo.png
        https://stackoverflow.com/questions/54358461/how-to-correctly-save-a-absolute-path-as-the-values-of-a-treeview
        """
        self.collect_image()
        
        self.signature_image = self.collected_image
        
        self.signature_img_entry.delete(0, END)  # Remove any previous content
        self.signature_img_entry.insert(0, self.signature_image)  # Insert new content
        
        #
        # # debug
        # # self.signature_image  C:/000_tmp/Paulo.png
        # # ("'" + '"' + self.signature_image + '"'+ "'") The outer set of '
        # # means "send this string (including the double quotes ") to the shell –
        # # SiHa May 13, 2015 at 11:52
        # # https://stackoverflow.com/questions/30212375/python-error-for-space-in-path
        # Pages.signature_image = self.signature_image
        # print("Pages.signature_image in  self.collect_image_footer", Pages.signature_image)
        # # raw name of file G:/FOTOS PARA REVELAÇÃO/16997548134_4f805a60a4_o.jpg
        #
        # self.signature_image_pluscotes = ("'" + '"' + self.signature_image + '"'+ "'")
        # print('self.signature_image in  collect_image_footer', self.signature_image)
        # # self.signature_image in collect_image_footer '"G:/FOTOS PARA REVELAÇÃO/16997548134_4f805a60a4_o.jpg"'
        # #name with two cotes to avoid bug of spaces inter istrings in path
        # Pages.signature_image_pluscotes = self.signature_image_pluscotes
        # print('Pages.signature_image_pluscotes', Pages.signature_image_pluscotes)
        #
        # # Pages.signature_image make local variable self.signature_image to global.
        #
        # # self.signature_image_to_list()
        # self.signature_image_list = (self.signature_image)
        # # self.signature_image_list.append(self.signature_image)
        # print('self.signature_image_list in  collect_image_footer', self.signature_image_list)
        #
        # #bellow   self.signature_image_list['"C:/000_tmp/2021-12-13_gui.jpg"']
        # # this format is used to insert path in treeview and double cotation to accept spaces in path
        # # return self.signature_image_list
        
        self.get_footer_image()
        Pages.listaCli_imagePath = self.listaCli_imagePath
    
    # ------------------------functions to work with json
    # -------------------------get gender chosen
    #
    # def check_comboGender(self, event):
    #     """
    #     binding to sex chosen
    #     """
    #     # self.this_is_gender_chosen=''
    #     self.this_is_gender_chosen = self.comboGender.get()
    #
    #     # print('self.this_is_gender_chosen', self.this_is_gender_chosen)
    #     self.store_comboGender()
    # # -------------------------get gender chosen end
    #
    #
    # # -----------------store comboGender
    # def store_comboGender(self):
    #     """
    #     method used in  check_comboGender to store last combo option selected
    #     and use it as combo defaut next time app opens
    #     """
    #
    #     current_sex = self.this_is_gender_chosen # get combo option
    #
    #     # dir path for external folder eeg_report_files
    #     dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
    #
    #     # filepath for file curreent_db_used.json
    #     appdata_db_file_path = "%scurrent_sex_used.json" % dir_path
    #     appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
    #
    #     # absolute path don't work in instalations because it is different for each computer:
    #     # current_db = r"G:\PycharmProjects\EEG_WEAVER\json_objects\current_db_used.json"  # use the file extension
    #
    #     # if files inside app folder use:
    #     # current_db = (resource_path("current_db_used.json"))  # use the file extension .json
    #
    #     # for files outside app folder:
    #     filepath_current_sex = appdata_db_file_path  # file extension .json
    #
    #     with open(filepath_current_sex, 'w') as file_object:  # open the file in write mode
    #         # json.dump() function to store the value in current_sex_used.json file:
    #         json.dump(current_sex, file_object)
    #
    # def retrieve_comboGender(self):
    #
    #     # if file in subfolder of app folder:
    #     # with open(r'/json_objects/updated_list_db_created.json') as file_object_db:
    #
    #     # if file in app folder
    #     # with open('updated_list_db_created.json') as file_object_db:
    #     # with open(resource_path('updated_list_db_created.json')) as file_object_db:
    #
    #     # if file in external folder:
    #     dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
    #
    #     appdata_db_file_path = "%scurrent_sex_used.json" % dir_path
    #     appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
    #
    #     with open(appdata_db_file_path) as file_object_db:
    #         self.updated_sex_used = json.load(file_object_db)
    #         Pages.updated_sex_used = self.updated_sex_used
    #         print('Pages.updated_sex_used in func', Pages.updated_sex_used)
    #         print('self.updated_sex_used in funcs', self.updated_sex_used)
    #
    #     return self.updated_sex_used
        
        #     self.comboGender.set(self.updated_sex_used)
    # -----------------store comboGender end
    
    
    def store_db_to_json(self):
        """
        method used in  self.db_path_aba3_cbox to store last combo option selected
        and use it as combo defaut next time app opens
        """
        # print('self.db_path_aba3_cbox.get() in def store_db_to_json(self, event)' ,self.db_path_aba3_cbox.get())
        # https: // www.section.io / engineering - education / storing - data - in -python - using - json - module /
        
        # self.get_databk_values_to_cbox()
        current_db_in_use = self.db_path_aba3_cbox.get()  # get combo option
        
        # dir path for external folder eeg_report_files
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        # filepath for file curreent_db_used.json
        appdata_db_file_path = "%scurrent_db_used.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        # absolute path don't work in instalations because it is different for each computer:
        # current_db = r"G:\PycharmProjects\EEG_WEAVER\json_objects\current_db_used.json"  # use the file extension
        
        # if files inside app folder use:
        # current_db = (resource_path("current_db_used.json"))  # use the file extension .json
        
        # for files outside app folder:
        current_db = appdata_db_file_path  # file extension .json
        
        with open(current_db, 'w') as file_object:  # open the file in write mode
            # json.dump() function to store the set of numbers in numbers.json file:
            json.dump(current_db_in_use, file_object)
        # src_path = current_db
        # dst_path = os.path.join(os.environ['APPDATA'], "current_db_used.json")
        # shutil.copy(src_path, dst_path)
    
    def retrieve_db_cbox(self):
        # to always start app with combobox showing the cbox value chosen in last session
        # this gets the value of combobox chosen in previous session
        # and stored in current_db_used.json.old
        # populate combobox, it means, the databank of reports (laudos) in use
        
        # get variable:
        self.get_databk_values_to_cbox()
        # with open(r"/json_objects/current_db_used.json") as file_object_db:
        # with open("current_db_used.json") as file_object_db:
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        appdata_db_file_path = "%scurrent_db_used.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        # with open(resource_path("current_db_used.json")) as file_object_db:
        with open(appdata_db_file_path) as file_object_db:
            self.current_db = json.load(file_object_db)
            Pages.current_main_db_in_use = self.current_db
        return self.current_db
    
    def retrieve_updated_list_db_cbox(self):
        
        # if file in subfolder of app folder:
        # with open(r'/json_objects/updated_list_db_created.json') as file_object_db:
        
        # if file in app folder
        # with open('updated_list_db_created.json') as file_object_db:
        # with open(resource_path('updated_list_db_created.json')) as file_object_db:
        
        # if file in external folder:
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_db_file_path = "%supdated_list_db_created.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        with open(appdata_db_file_path) as file_object_db:
            self.updated_list_with_newdb = json.load(file_object_db)
            Pages.updated_list_with_newdb = self.updated_list_with_newdb
        return self.updated_list_with_newdb
    
    def on_select_db_path_aba3_cbox(self):
        """
        this method and 'def store_db_to_json' are used together in bind_db_path_aba3_cbox
        in combobox
        """
        
        Pages.current_main_db_in_use = self.db_path_aba3_cbox.get()
    
    def bind_db_path_aba3_cbox(self, event):
        """
        when changing option in db_path_aba3_cbox combobox this method:
        stores last databank selected in json
        and
        updates treeview
        """
        self.store_db_to_json()
        
        # cleans all fields when new databank is called:
        self.clear_screen_funcs()
        
        # select new databank in aba3:
        self.on_select_db_path_aba3_cbox()
        self.select_lista()
    
    def store_port_or_engl_json(self):
        """
        store json to build pdf portuguese or english not used yet , created just in case
        """
        portuguese_or_english_get = self.radiob34_aba4_var.get()
        # print('portuguese_or_english_get', portuguese_or_english_get)
        # current_portuguese_or_english = r'G:\PycharmProjects\EEG_WEAVER\json_objects\portuguese_or_english_pdf.json'
        # use the file extension .json
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%sportuguese_or_english_pdf.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        # debug:
        # to allow reading:
        # print(appdata_db_file_path)
        # C: / Users / PK / AppData / Roaming / eeg_report_files / portuguese_or_english_pdf.json
        Pages.portuguese_or_english = portuguese_or_english_get
        with open(appdata_file_path, 'w') as file_object:  # open the file in write mode
            json.dump(portuguese_or_english_get, file_object)
            # json.dump() function to stores variable in json file
        # to see what is inside the json file
        # with open(appdata_db_file_path, 'r') as G:
        #     print(G.read())
        # result is 1 or 2
        # return self.json_port_eng_radiob34_aba4_var
    
    def retrieve_portg_or_eng_radiob34_aba4_json(self):
        """
        to change language of interface if 1 english is 2 português
        retrieve_lframe1_aba4_json

        """
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_db_file_path = "%sportuguese_or_english_pdf.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        # with open(resource_path('portuguese_or_english_pdf.json')) as file_object_db:
        with open(appdata_db_file_path) as file_object_db:
            self.json_port_eng_radiob34_aba4_var = json.load(file_object_db)
        # this is page size chosen:
        # print('self.json_port_eng_radiob34_aba4_var', self.json_port_eng_radiob34_aba4_var)
        return self.json_port_eng_radiob34_aba4_var
    
    def store_show_or_not_pdf_json(self):
        """
        store json to build pdf portuguese or english not used yet , created just in case
        """
        show_or_not_pdf_get = self.radiob56_aba4_var.get()
        # Pages.portuguese_or_english = portuguese_or_english_get
        
        # full path
        # current_show_or_not_pdf_get = r'G:\PycharmProjects\EEG_WEAVER\json_objects
        # \show_or_not_pdf_after_creation.json'
        # file in app folder:
        # current_show_or_not_pdf_get = (resource_path('show_or_not_pdf_after_creation.json'))
        
        # dir outside app main folder:
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        appdata_file_path = "%sshow_or_not_pdf_after_creation.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        
        # use the file extension .json
        with open(appdata_file_path, 'w') as file_object:  # open the file in write mode
            json.dump(show_or_not_pdf_get, file_object)
            # json.dump() function to store the set of numbers in numbers.json file
    
    def store_letter_or_A4_json(self):
        """
        store json  just to open app with self.radiobutton1 previously selected in def root_widgets
        """
        # get variable:
        letter_or_A4_json = self.radiob1_aba4_var.get()
        # current_letter_or_A4 = 'G:\PycharmProjects\EEG_WEAVER\json_objects\letter_or_A4_json.json'
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        # explanation:
        # name of file letter_or_A4_json.json
        # % os.environ['APPDATA'] = folder C:\Users\PK\AppData\Roaming
        # '%s\\eeg_report_files\\' = folder .\Roaming\eeg_report_files\
        # dir_path = folder C:\Users\PK\AppData\Roaming\eeg_report_files\
        # appdata_db_file_path = C:\Users\PK\AppData\Roaming\eeg_report_files\letter_or_A4_json.json
       
        appdata_db_file_path = "%sletter_or_A4_json.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        # resource_path is used when the path is main app path:
        # current_letter_or_A4 = (resource_path('letter_or_A4_json.json'))  # use the file extension .json
        current_letter_or_A4 = appdata_db_file_path  # use the file extension .json
        
        with open(current_letter_or_A4, 'w') as file_object:  # open the file in write mode
            json.dump(letter_or_A4_json, file_object)
            # json.dump() function stores variable in json file
    
    def store_Table_header_YorN_radiob78_json(self):
        """
        store json  just to open app with self.radiobutton78
        previously selected in def root_widgets
        """
        table_YorN_json = self.radiob78_aba4_var.get()
        
        # current_yorn_table = r'G:\PycharmProjects\EEG_WEAVER\json_objects\Table_header_YorN_radiob78_json.json'
        # current_yorn_table = (resource_path('Table_header_YorN_radiob78_json.json'))
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%sTable_header_YorN_radiob78_json.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        # use the file extension .json
        
        with open(appdata_file_path, 'w') as file_object:  # open the file in write mode
            json.dump(table_YorN_json, file_object)
            # json.dump() function to store the set of numbers in numbers.json file
    
    def store_radiob1_arrow_aba4_var(self):
        """
        store json to select option '1' or two = to use title= Electroencephalogram
        or '2' create new name in  self.pdf_titlename_entry selected in def root_widgets
        """
        
        radiob1_arrow_json = self.radiob_arrow_aba4_var.get()
        
        # current_radiob1_arrow = r'G:\PycharmProjects\EEG_WEAVER\json_objects
        # \radiob1_arrow_json.json'  # use the file extension .json
        # current_radiob1_arrow = (resource_path('radiob1_arrow_json.json'))  # use the file extension .json
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%sradiob1_arrow_json.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        
        with open(appdata_file_path, 'w') as file_object:  # open the file in write mode
            json.dump(radiob1_arrow_json, file_object)
            # json.dump() function to store in json file
    
    def retrieve_Table_header_YorN_radiob78_json(self):
        """
        retrieve_lframe1_aba4_json
        get option from aba4 if page size chosen is  letter (1) or A4(2)
        """
        
        # try:
        # with open(r'G:\PycharmProjects\EEG_WEAVER\json_objects
        # \Table_header_YorN_radiob78_json.json') as file_object_db:
        # with open(resource_path('Table_header_YorN_radiob78_json.json')) as file_object_db:
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_db_file_path = "%sTable_header_YorN_radiob78_json.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        with open(appdata_db_file_path) as file_object_db:
            self.json_show_or_not_Table_radiob78_aba4_var = json.load(file_object_db)
        # this is page size chosen:
        return self.json_show_or_not_Table_radiob78_aba4_var
        
        # except:
        #     return
    
    def retrieve_letter_or_A4_radiob1_aba4_json(self):
        """
        retrieve_lframe1_aba4_json
        get option from aba4 if page size chosen is  letter (1) or A4(2)
        """
        
        # try:
        # with open(r'G:\PycharmProjects\EEG_WEAVER\json_objects\letter_or_A4_json.json') as file_object_db:
        # with open(resource_path('letter_or_A4_json.json')) as file_object_db:
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%sletter_or_A4_json.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        
        with open(appdata_file_path) as file_object_db:
            self.json_letter_or_A4_radiob1_aba4_var = json.load(file_object_db)
        # this is page size chosen:
        return self.json_letter_or_A4_radiob1_aba4_var
    
    def retrieve_show_or_not_pdf_radiob56_aba4_json(self):
        """
        retrieve_lframe2_aba4_json
        restore option if portuguese or english   from aba4 second combobox
        just a number reference --> 1 is english 2 is portuguese  /

        """
        # try:
        #     # with open(r'G:\PycharmProjects\EEG_WEAVER\json_objects
        #     # \show_or_not_pdf_after_creation.json') as file_object_db:
        # with open(resource_path('show_or_not_pdf_after_creation.json')) as file_object_db:
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%sshow_or_not_pdf_after_creation.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        
        with open(appdata_file_path) as file_object_db:
            self.json_show_or_not_PDFradiob56_aba4_var = json.load(file_object_db)
            # this is language chosen
        return self.json_show_or_not_PDFradiob56_aba4_var
        # except:
        # return
    
    def retrieve_Pdf_Title_1or2_radiob90_aba4_var_json(self):
        """
        retrieve if title electroencefalogram should be changed or not
        this gets button options 1 = keep name electroencephalogram
        option 2 change to variable from
        aba4def retrieve_Pdf_newTitle_typed_radiob90_aba4_var_json(self):
        """
        
        # with open(r'G:\PycharmProjects\EEG_WEAVER\json_objects\pdf_title_1or2_radiob90_json.json') as file_object_db:
        
        # with open(resource_path('pdf_title_1or2_radiob90_json.json')) as file_object_db:
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%spdf_title_1or2_radiob90_json.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        
        with open(appdata_file_path) as file_object_db:
            self.retrieved_Pdf_Title_1or2_aba4_var_json = json.load(file_object_db)
            # this is language chosen
        return self.retrieved_Pdf_Title_1or2_aba4_var_json
    
    def retrieve_Pdf_newTitle_typedin_entry_json(self):
        """
        new name typed in entrybox to substitute 'Electroencephalogram'
        retrieve if title electroencefalogram should be changed or not
        from     def store_newPdf_Title_from_entry(self):
        
        we get here what is typed in  entry --> self.pdf_titlename_entry
        """
        
        # this is fullpath = not usefull when creating install folder (path changes in new computer):
        # with open(r'G:\PycharmProjects\EEG_WEAVER\json_objects\pdf_Newtitle_from_entry_json.json') as file_object_db:
        
        # if file is inside app folder, example, image inside app folder
        # with open(resource_path('pdf_Newtitle_from_entry_json.json')) as file_object_db:
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_db_file_path = "%spdf_Newtitle_from_entry_json.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        with open(appdata_db_file_path) as file_object_db:
            self.retrieved_Pdf_NewTitle_typedin_entry_json = json.load(file_object_db)
            # this is language chosen
        return self.retrieved_Pdf_NewTitle_typedin_entry_json
    
    def retrieve_radiob_arrow_aba4_json(self):
        """
        retrieve if arrow is up or down
        """
        # try:
        # with open(r'G:\PycharmProjects\EEG_WEAVE\json_objects\radiob1_arrow_json.json') as file_object_db:
        # with open(resource_path('radiob1_arrow_json.json')) as file_object_db:
        
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%sradiob1_arrow_json.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        
        with open(appdata_file_path) as file_object_db:
            self.retrieved_radiob_arrow_aba4_json = json.load(file_object_db)
            # this is language chosen
        return self.retrieved_radiob_arrow_aba4_json
        # except:
        #     return
    
    def organize_list_arrow(self):
        """
        set if list is ascending or descending
        """
        self.retrieve_radiob_arrow_aba4_json()  # returns self.retrieved_radiob_arrow_aba4_json
        
        # try:
        if self.retrieved_radiob_arrow_aba4_json == 1:
            self.ascending()
        elif self.retrieved_radiob_arrow_aba4_json == 2:
            self.descending()
        # except:
        #     self.ascending()
        #
    
    def pageSize_letter_or_A4(self):
        """
        def retrieve_letter_or_A4_radiob1_aba4_json(self):
        come here to give the options of page size
        """
        # try:
        if self.json_letter_or_A4_radiob1_aba4_var == 1:
            width, height = letter
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:
            width, height = A4
        else:
            width, height = letter
        return width, height
        # except:
        #     width, height = letter
        # return width, height
        #
    
    def store_font_cbox_aba4_json(self, event):
        
        """
         just get font chosen from combobox and save
        to: currentFont_comBx_aba4_json.json
        Attention nothing to do direct with radiobuttons
        it stores the name of the font chosen
        """
        # get font from combobox:
        new_Font_to_use_json = self.font_chosen_cbox.get()
        # discriminate folder where file is:
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        # put file in path:
        appdata_db_file_path = "%scurrentFont_comBx_aba4_json.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        # current_font_to_use = r'G:\PycharmProjects\EEG_WEAVER
        # \json_objects\currentFont_comBx_aba4_json.json'  # use the file extension .json
        # current_font_to_use = (resource_path('currentFont_comBx_aba4_json.json'))  # use the file extension .json
        current_font_to_use = appdata_db_file_path  # use the file extension .json
        
        # open the file in write mode:
        with open(current_font_to_use, 'w') as file_object:
            json.dump(new_Font_to_use_json, file_object)
            # json.dump() function stores the set of numbers in numbers.json file
    
    def retrieve_font_cbox_aba4_json(self):
        """
        retrieve just the name of the font chosen in
        combobox in self.lframe6_aba4 -->third column from left in aba4
        """
        # discriminate folder where file is:
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        # put file in path:
        appdata_db_file_path = "%scurrentFont_comBx_aba4_json.json" % dir_path
        appdata_db_file_path = appdata_db_file_path.replace('\\', '/')
        
        try:
            # with open(r'G:\PycharmProjects\EEG_WEAVER\json_objects
            # \currentFont_comBx_aba4_json.json') as file_object_db:
            # with open(resource_path('currentFont_comBx_aba4_json.json')) as file_object_db:
            with open(appdata_db_file_path) as file_object_db:
                
                self.retrieved_currentFont_comBx_aba4_json = json.load(file_object_db)
                # this is language chosen
            return self.retrieved_currentFont_comBx_aba4_json
        # except:
        #     return 'Helvetica'
        
        except Exception as e:
            print('type is:', e.__class__.__name__)
            # print_exc()
    
    def store_radiob1_cbox_aba4_var(self):
        """
        self.lframe6_aba4 -->third column from left in aba4
        store json to select option '1' or two =
        radiobuttons to use default font or another(2)
        """
        
        radiob1_cbox_aba4_var = self.radiob_cbox_aba4_var.get()
        
        # current_radiob_cbox_aba4_var = r'G:\PycharmProjects\EEG_WEAVER
        # json_objects\current_radiob_cbox_aba4_var_json.json'  # use the file extension .json
        
        # resource_path func gives us the relative app path, to work after instalation in any system.
        # current_radiob_cbox_aba4_var = (resource_path('current_radiob_cbox_aba4_var_json.json'))
        
        # external folder where files are:
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%scurrent_radiob_cbox_aba4_var_json.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        
        with open(appdata_file_path, 'w') as file_object:  # open the file in write mode
            json.dump(radiob1_cbox_aba4_var, file_object)
            # json.dump() function to store the set of numbers in numbers.json file
    
    def retrieve_radiob1_cbox_aba4_json(self):
        """
        self.lframe6_aba4 -->third column from left in aba4
        retrieve just the name of the font chosen in combobox
        """
        dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
        
        appdata_file_path = "%scurrent_radiob_cbox_aba4_var_json.json" % dir_path
        appdata_file_path = appdata_file_path.replace('\\', '/')
        try:
            # with open(r'G:\PycharmProjects\EEG_WEAVE\json_objects
            # current_radiob_cbox_aba4_var_json.json') as file_object_db:
            # with open(resource_path('current_radiob_cbox_aba4_var_json.json')) as file_object_db:
            
            with open(appdata_file_path) as file_object_db:
                self.retrieved_radiob1_cbox_aba4_json = json.load(file_object_db)
                # this is language chosen
            return self.retrieved_radiob1_cbox_aba4_json
        except Exception as e:
            print('type is:', e.__class__.__name__)
            return
        
        # ---------------func to change fonts based in
    
    def choose_font_to_use(self):
        """
        fonts we get in: self.lframe6_aba4 -->third column from left in aba4
        """
        self.my_specific_font = 'Helvetica'
        # method retrieve just the name of the font
        # chosen in combobox in self.lframe6_aba4 --> 'currentFont_comBx_aba4_json.json'
        # in variable  self.retrieved_currentFont_comBx_aba4_json
        self.retrieve_font_cbox_aba4_json()
        
        # here we  get 'current_radiob_cbox_aba4_var_json.json' - the variable
        # we create when click in radiob1 aba4 in variable
        # 'self.retrieved_radiob1_cbox_aba4_json'
        self.retrieve_radiob1_cbox_aba4_json()
        
        try:
            if self.retrieved_radiob1_cbox_aba4_json == 1:
                self.my_specific_font = 'Helvetica'
            elif self.retrieved_radiob1_cbox_aba4_json == 2:
                self.my_specific_font = self.retrieved_currentFont_comBx_aba4_json
        except Exception as e:
            print('type is:', e.__class__.__name__)
            self.my_specific_font = 'Helvetica'
        
        return self.my_specific_font
    
    def list_font_available_reportLab(self):  # , canvas):
        """
        this method is used to show all fonts available to reportlab
        witch aren't many
        then we make then append to a list to appear in combobox aba4
        to be used in pdf creation
        """
        
        # __________this code print availables fonts to pdf
        from reportlab.pdfgen import canvas
        cc = canvas.Canvas('../FontChoices.pdf')  # this is created just to get fonts
        # from reportlab.lib.units import inch
        # text = "The quick brown fox jumped over the lazy dog."
        # x = 1.8 * inch
        # y = 2.7 * inch
        # for font in cc.getAvailableFonts():
        #     cc.setFont(font, 10)
        #     cc.drawString(x, y, text)
        #     cc.setFont("Helvetica", 10)
        #     cc.drawRightString(x - 10, y, font + ":")
        #     y = y - 13
        # cc.showPage()
        # cc.save()
        
        # strictly gravy.
        # import os
        # os.system('start FontChoices.pdf')
        # _______________this code print availables fonts to pdf
        # _______________this code print availables fonts to sistem
        self.reportlab_fonts_to_use = []
        
        for font in cc.getAvailableFonts():
            self.reportlab_fonts_to_use.append(font)
        
        return self.reportlab_fonts_to_use
        # print(reportlab_fonts_to_use)
    
    @staticmethod
    def insert_in_Textwidget(event, my_textwidget):
        
        # when click ENTER inserts <b/> in text
        textinsert = '<br/>'
        # my_textwidget.insert('end', textinsert)
        my_textwidget.insert(tk.INSERT, textinsert)
    
    @staticmethod
    def insert_Tab_in_Textwidget(event, my_textwidget):
        
        # when click ENTER inserts <b/> in text
        # textinsert = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' \
        #              '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        textinsert = '<Tab>'
        # my_textwidget.insert('end', textinsert)
        my_textwidget.insert(tk.INSERT, textinsert)
    
    # def focus_next_window(self, event):
    #     event.widget.tk_focusNext().focus()
    #     return ("break")
    #
    #     # when click ENTER inserts <b/> in text
    #     # textinsert = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' \
    #     #              '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    #     textinsert = '<Tab>'
    #     # my_textwidget.insert('end', textinsert)
    #     my_textwidget.insert(tk.INSERT, textinsert)
    #
    @staticmethod
    def determine_date():
        
        now = datetime.now()
    
    # def combobox_chosen(self):
    #     pass
    #
    # def collect_image(self):
    #     pass
    
    # def get_databk_values_to_cbox(self):
    #     pass
    #
    @staticmethod
    def center(win):
        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
    
    @staticmethod
    def copy_from_treeview(tree, event):
        """
        Click with left button to copy treeview cell to clipboard
        """
        selection = tree.selection()
        column = tree.identify_column(event.x)
        column_no = int(column.replace("#", "")) - 1
        
        copy_values = []
        for each in selection:
            try:
                value = tree.item(each)["values"][column_no]
                copy_values.append(str(value))
            except ValueError:
                pass
        
        copy_string = "\n".join(copy_values)
        pyperclip.copy(copy_string)
        print(copy_string)
    
    @staticmethod
    def create_folder_in_appdata(subfolder_to_create):
        """
        This method creates a folder in ['APPDATA']
        https://stackoverflow.com/questions/21761982/creating-a-folder-in-the-appdata
        files that update frequently during app use
        they can´t be in program folder, must be in appdata
        
        """
        
        dir_path = os.path.join(os.environ['APPDATA'], subfolder_to_create)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def combo_fontsize_selected(self, event):
        self.font_size_selected = self.current_font.get()
        Pages.new_font_size = self.font_size_selected
        return self.font_size_selected


class ToolTip(object):
    """
    https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
    Display message when hovering over something with mouse cursor in Python
    """
    
    def __init__(self, widget):
        self.text = None
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
    
    def showtip(self, text):
        """Display text in tooltip window"""
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#36454F", relief=SOLID, borderwidth=1,
                      # fg='#36454F', #color of text
                      fg='white',  # color of text
                      font=("arial", "12", "normal"))
        label.pack(ipadx=1)
    
    #
    
    # --------------------
    def hidetip(self):
        """
        
        remove tip when left the widget
        """
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
    
    def quit_weaver_reporter(self):
        self.root.destroy()
        # this is the use of function above:
        
        # def CreateToolTip(widget, text):
        #     toolTip = ToolTip(widget)
        #     def enter(event):
        #         toolTip.showtip(text)
        #     def leave(event):
        #         toolTip.hidetip()
        #     widget.bind('<Enter>', enter)
        #     widget.bind('<Leave>', leave)
    
    @staticmethod
    def config_label_style():
        style = ttk.Style()
        style.configure("Custom.TLabel", foreground="#DCDCDC",
                        # style.configure("Custom.TLabel",foreground="#708090",
                        background='#36454F',
                        # background='#000000',
                        padding=[10, 10, 10, 10],
                        relief="groove",
                        # relief = "solid",
                        # font="Times 30 bold italic",
                        # font="Arial 30 Black",
                        # width=18,
                        anchor=tk.CENTER,
                        highlightbackground="black",
                        bordercolor='#36454F',
                        borderwidth='1')
    
    # --------------------
