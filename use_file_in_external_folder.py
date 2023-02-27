# just a memo of how to make the paths

# this is only model of code we don't use it in the actual  software
# wher writing a script to windows
# any file that is frequently storing information as sqlite file must be outside
# main app file
# they stay in appdata folder
# then we must build code andduring instalation transfer then to app folder
# remember to script in a way they are transfered just 1 time (during instalation)
# if each time we start the program they are transfered again to app folder
# the options' ex: which language to use...neer change
#
# tranfering sqlite:

# create folder goes in EEG_weaver_Reporter_funcs_dez_22.py
def create_folder_in_appdata(self, subfolder_to_create):
    """
    This method creates a folder in ['APPDATA'] to insert files
    https://stackoverflow.com/questions/21761982/creating-a-folder-in-the-appdata
    files that update frequently during app use
     they can´t be in program folder, must be in appdata
    
    """
    
    dir_path = os.path.join(os.environ['APPDATA'], subfolder_to_create)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# ----------------------
def connect_db_fidbgen(self):
    # """ dbin --> database internal: sql that controls just name and path of
    # sql where reports are, to allow access to those databanks
    # it is just one sqlite file while report sqlite can be many
    #
    # code bellow create eeg_report_db diretory because db and other files that change can't be
    # in the same directory as the main program
    # C:\Users\PK\AppData\Roaming\eeg_report_files\kanda_multi_sql3.db """
    
    # create new directory in appdata, in program files whe can't change information saved
    Funcs.create_folder_in_appdata(self, 'eeg_report_files')
    
    dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
    # or
    # dir_path = os.path.join(os.environ['APPDATA'], file_to_insert)
    # if not os.path.exists(dir_path):
    #     os.makedirs(dir_path)
    
    appdata_db_file_path = "%skanda_multi_sql3.db" % dir_path
    
    try:
        self.conn_dbin = sqlite3.connect(appdata_db_file_path)
        # sqlite3.connect(internal_db_file_path)
    except (FileNotFoundError, IOError):
        # pass
        messagebox.showerror("DataBank Message",
                             "Databank 'kanda_multi_sql3.db' not found in C:/Users/<USER>/AppData/Local/<APPNAME>.")
    
    try:
        self.cursor_dbin = self.conn_dbin.cursor()
    except FileNotFoundError:
        pass
    
    # -------------------
    # -------------------transfering json files to new folder


# this func goes in  Application script EEG_weaver_Reporter_2.5.py
# and is the first called func:

def transfer_json_to_appdata(self):
    """
    this func is used just during instalation to create folder in appdata
    and transfer json to that folder. Json files change each time we modify
    config. So Json files must stay out of app folder (same for sqlite file)

    the problem is that all files that we must rewrite and resave
    during app use cannot stay in "program files/app_folder"
    then sqlite database and json files must be transfered to folder
    C:\\Users\\PK\\AppData\\Roaming\\eeg_report_files
    this function transfer json files from app_folder to
    C:\\Users\\PK\\AppData\\Roaming\\eeg_report_files
    sqlite internal is tranfered inside function def connect_db_fidbgen(self):

    """
    # create folder in APPDATA:
    Funcs.create_folder_in_appdata(self, 'eeg_report_files')
    
    # external pathfolder is eeg_report_files
    destiny_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
    
    # folder inside appdir and used just during instalation:
    base_folder = (resource_path('./json_objects/'))
    
    origin_files = os.listdir(base_folder)  # list of files in origin folder
    files_in_external_dir = os.listdir(destiny_path)  # list of files in end folder
    
    # sqlite data bank could be  here I just coded separated to learn
    for filename in origin_files:
        if filename not in files_in_external_dir:
            # copying from install folder to APPDATA folder:
            shutil.copy('currentFont_comBx_aba4_json.json', destiny_path)
            shutil.copy('current_db_used.json', destiny_path)
            shutil.copy('current_radiob_cbox_aba4_var_json.json', destiny_path)
            shutil.copy('letter_or_A4_json.json', destiny_path)
            shutil.copy('main_file_path_to_use.json', destiny_path)
            shutil.copy('pdf_Newtitle_from_entry_json.json', destiny_path)
            shutil.copy('pdf_title_1or2_radiob90_json.json', destiny_path)
            shutil.copy('pdf_title_name_radiob90_json.json', destiny_path)
            shutil.copy('portuguese_or_english_pdf.json', destiny_path)
            shutil.copy('radiob1_arrow_json.json', destiny_path)
            shutil.copy('show_or_not_pdf_after_creation.json', destiny_path)
            shutil.copy('Table_header_YorN_radiob78_json.json', destiny_path)
            shutil.copy('updated_list_db_created.json', destiny_path)
        
        else:
            pass


# this bellow have nothing to do with transfer, it opens file in external folder and write to it
# is:

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
    # print(appdata_file_path)
    # C: / Users / PK / AppData / Roaming / eeg_report_files / portuguese_or_english_pdf.json
    
    with open(appdata_file_path, 'w') as file_object:  # open the file in write mode
        json.dump(portuguese_or_english_get, file_object)
        # json.dump() function to store the set of numbers in numbers.json file
    # to see what is inside the json file
    # with open(appdata_db_file_path, 'r') as G:
    #     print(G.read())
    # result is 1 or 2


def retrieve_portg_or_eng_radiob34_aba4_json(self):
    """
    to change language of interface if 1 english if 2 português
    retrieve_lframe1_aba4_json
    get option from aba4 if page size chosen is  letter (1) or A4(2)
    """
    dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
    
    appdata_file_path = "%sportuguese_or_english_pdf.json" % dir_path
    appdata_file_path = appdata_file_path.replace('\\', '/')
    
    # with open(resource_path('portuguese_or_english_pdf.json')) as file_object_db:
    with open(appdata_file_path) as file_object_db:
        self.json_port_eng_radiob34_aba4_var = json.load(file_object_db)
    # this is page size chosen:
    print('self.json_port_eng_radiob34_aba4_var', self.json_port_eng_radiob34_aba4_var)
    return self.json_port_eng_radiob34_aba4_var


# -------------------

# generalizing functions:


def store_variable_to_json_in_external_path(self,
                                            variable_to_store,
                                            external_folder,
                                            file_to_write,
                                            ):
    """
    store json to build pdf portuguese or english not used yet , created just in case
    """
    
    # getting your variable to be stored:
    # portuguese_or_english_get = self.radiob34_aba4_var.get()
    # variable_to_store = self.radiob34_aba4_var.get()
    my_variable = variable_to_store
    
    # dir_path = '%s\\eeg_report_files\\' % os.environ['APPDATA']
    dir_path = '%s\\externalfolder\\' % os.environ['APPDATA']
    
    appdata_file_path = "%sfile_to_write" % dir_path
    # change back to forward slashes to work:
    appdata_file_path = appdata_file_path.replace('\\', '/')
    
    # write json file
    with open(appdata_file_path, 'w') as file_object:  # open the file in write mode
        json.dump(my_variable, file_object)
        # json.dump() function stores variable in json file
    
    # atention to see what is inside the json file
    # with open(appdata_file_path, 'r') as G:
    #     print(G.read())
    # example: result is 1 or 2
