from pathlib import Path
from docxtpl import DocxTemplate
from pages_to_connect_pages import Pages
import re


class ToWordDoc:
    
    #
    def __init__(self):
        self.docx_history_report_object = None
        self.docx_footer_object = None
        self.docx_listaCli_imagePath_sign = None
        self.docx_listaCli_imagePath_logo = None
        self.docx_doctor_name = None
        self.docx_body_Report_object = None
        self.docx_high_f_f_objectt = None
        self.docx_high_f_f_object = None
        self.docx_low_f_f_object = None
        self.docx_sample_rate_object = None
        self.docx_diagnosis_object = None
        self.docx_age_object = None
        self.docx_gender_object = None
        self.docx_date_object = None
        self.docx_patient_object = None
        self.docx_id_object = None
        self.docx_header = None
        self.word_template_path = None
        self.header = None
        
        #
    
    def create_word(self, main_module):
        """
        When  we edit text in Text widget, we use <> markup language,
        it doesnot export to docx (word), so, we get the string text and remove <>
        and all betwen <> with
        text_variable = re.sub(r'<.*?> *', '', text_variable)
        """
        
        self.list_report_variables(main_module)
        # print('Pages.id_object', Pages.id_object)
        # Pages.header_object = self.txt_header.get('1.0', 'end-1c')
        
        self.docx_header = Pages.header_object
        # remove markup language <> and everything between brackets
        self.docx_header = re.sub(r'<.*?> *', '', docx_header)
        
        self.docx_id_object = Pages.id_object
        self.docx_id_object = re.sub(r'<.*?> *', '', docx_id_object)
        
        self.docx_patient_object = Pages.patient_object
        self.docx_patient_object = re.sub(r'<.*?> *', '', docx_patient_object)
        
        self.docx_date_object = Pages.date_object
        self.docx_date_object = re.sub(r'<.*?> *', '', docx_date_object)
        
        self.docx_gender_object = Pages.gender_object
        self.docx_gender_object = re.sub(r'<.*?> *', '', docx_gender_object)
        
        self.docx_age_object = Pages.age_object
        self.docx_age_object = re.sub(r'<.*?> *', '', docx_age_object)
        
        self.docx_diagnosis_object = Pages.diagnosis_object
        self.docx_diagnosis_object = re.sub(r'<.*?> *', '', docx_diagnosis_object)
        
        self.docx_sample_rate_object = Pages.sample_rate_object
        self.docx_sample_rate_object = re.sub(r'<.*?> *', '', docx_sample_rate_object)
        
        self.docx_low_f_f_object = Pages.low_f_f_object
        self.docx_low_f_f_object = re.sub(r'<.*?> *', '', docx_low_f_f_object)
        
        self.docx_high_f_f_object = Pages.high_f_f_object
        self.docx_high_f_f_objectt = re.sub(r'<.*?> *', '', docx_high_f_f_object)
        
        self.docx_body_Report_object = Pages.body_Report_object
        self.docx_body_Report_object = re.sub(r'<.*?> *', '', docx_body_Report_object)
        
        self.docx_doctor_name = Pages.doctor_name
        self.docx_doctor_name = re.sub(r'<.*?> *', '', docx_doctor_name)
        
        self.docx_listaCli_imagePath_logo = Pages.listaCli_imagePath_logo
        
        self.docx_listaCli_imagePath_sign = Pages.listaCli_imagePath
        
        self.docx_footer_object = Pages.history1_object
        self.docx_footer_object = re.sub(r'<.*?> *', '', docx_doctor_name)
        
        self.docx_history_report_object = Pages.history_report_object
        self.docx_history_report_object = re.sub(r'<.*?> *', '', docx_history_report_object)
        
        # print('docx_body_Report_object:', docx_body_Report_object)
        # print('Pages.patient_object:', Pages.patient_object)
        # --------
        
        # self.word_template_path = Path(__file__).parent / 'docs' / "weaver_docx_template.docx"
        # doc = DocxTemplate(self.word_template_path)
        #
        # context = {"HEADER": docx_header,
        #            "Patient_ID": docx_id_object,
        #            "Name": docx_patient_object,
        #            "Date": docx_date_object,
        #            "Gender": docx_gender_object,
        #            "Age": docx_age_object,
        #            "Diagnosis": docx_diagnosis_object,
        #            "Sample_Rate": docx_sample_rate_object,
        #            "Low_Freq_Filter": docx_low_f_f_object,
        #            "High_Freq_Filter": docx_high_f_f_object,
        #            "Doc_Name": docx_doctor_name,
        #            "Body_of_Report": docx_body_Report_object,
        #            "Logo_docx": docx_listaCli_imagePath_logo,
        #            "Signature": docx_listaCli_imagePath_sign,
        #            "Footer": docx_footer_object,
        #            "History": docx_history_report_object,
        #            }
        #
        # doc.render(context)
        #
        #
        # doc.save(r'c:/000_tmp/aaaaaa.docx')
    
    def list_report_variables(self, main_module):
        Pages.header_object = main_module.txt_header.get('1.0', 'end-1c')
        Pages.id_object = main_module.Id_entry.get()
        Pages.date_object = main_module.report_Date_entry.get()
        Pages.patient_object = main_module.patient_entry.get()
        Pages.gender_object = main_module.gender_chosen
        Pages.age_object = main_module.age_entry.get()
        Pages.diagnosis_object = main_module.diag_entry.get()
        Pages.low_f_f_object = main_module.LFF_entry.get()
        Pages.high_f_f_object = main_module.HFF_entry.get()
        Pages.sample_rate_object = main_module.srate_entry.get()
        Pages.body_Report_object = main_module.txt_body.get('1.0', 'end-1c')
        Pages.doctor_name = main_module.txt_footer.get('1.0', 'end-1c')
        Pages.listaCli_imagePath_logo = main_module.signature_img_entry_logo.get()
        Pages.listaCli_imagePath = main_module.signature_img_entry.get()
        Pages.history1_object = main_module.txt_history1.get('1.0', 'end-1c')
        Pages.history_report_object = main_module.txt_history.get('1.0', 'end-1c')
