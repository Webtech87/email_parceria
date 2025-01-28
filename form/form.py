from flask import session
from random import choices
from select import select
from wtforms import BooleanField
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.simple import SubmitField, TextAreaField, EmailField
from wtforms import Form, StringField, validators
from wtforms.validators import DataRequired, Email, Regexp

# imports for working with excel
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font

# import necessary to implement Google Sheets
from .secret_CSRF import CLIENT_SECRET_FILE
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials


partners_list = [
    'Márcia Monteiro Micropigmentação','Claudia Vieira'
]

procedure_list = [
    'Microcirurgia cosmética Consulta',
    'Micro lifting de sobrancelha',
    'Micro blefaroplastia superior',
    'Micro blefaroplastia inferior',
    'Lifting do terço médio e inferior',
    'Micro cervicoplastia (papada e pescoço)'
]

class PartnerShipForm(FlaskForm):
    nome = StringField(
        'Nome',
        [
            DataRequired(message="Este campo é obrigatório."),
            validators.Length(min=4, max=25),
            Regexp(r'^[A-Za-zÀ-ÿ\s]+$', message="O nome pode conter apenas letras e espaços.")
        ],
        render_kw={"class": "form-control", "placeholder": "Introduza o seu Nome"}
    )
    apelido = StringField(
        'Apelido',
        [
            DataRequired(message="Este campo é obrigatório."),
            validators.Length(min=3, max=25),
            Regexp(r'^[A-Za-zÀ-ÿ\s]+$', message="O nome pode conter apenas letras e espaços.")
        ],
        render_kw={"class": "form-control", "placeholder": "Introduza o seu Apelido"}
    )
    tel = StringField(
    'Telefone',
    [
        DataRequired(message="Este campo é obrigatório."),
        validators.Length(min=9, max=14),
        Regexp(r'^\d+$', message="Apenas números são permitidos.")
    ],
    render_kw={
        "class": "form-control",
        "placeholder": "Introduza o seu contacto telefónico",
        "inputmode": "tel",  # Isso ajuda a exibir o teclado numérico no mobile
        "pattern": "\\d*"  # Garante que apenas números sejam aceitos
    }
)
    email = EmailField(
        'Email',
        [
            DataRequired(message="Este campo é obrigatório."),
            validators.Email(), validators.Length(min=6, max=35)
        ],
        render_kw={"class": "form-control", "placeholder": "Introduza o seu Email", "type": "email"}
    )
    partner_ship_list = SelectField(
    'Parceiro(a)',
    choices=[("", "Selecione um parceiro(a)")] + [(partner, partner) for partner in partners_list],
    validators=[DataRequired(message="Por favor, selecione um parceiro(a).")],
    render_kw={
        "class": "input_class_selection form-control",
        "placeholder": "Selecione um parceiro(a)"
    }
)
    procedure_list = SelectField(
        'Procedimento',
        choices= [("", "Selecione uma procedimento")] +[(procedure, procedure) for procedure in procedure_list],
        validators=[DataRequired(message="Por favor, selecione um procedimento).")],
        render_kw={"class": "input_class_selection form-control"}
    )
    checkbox = BooleanField(
        'Eu concordo em partilhar minhas informações de contato com o propósito de ser contactado pela Santiclinic',
        default=False,
        validators=[DataRequired(message="Por favor, aceite os termos de responsabilidade.).")],
        render_kw={"class": "custom_checkbox form-check-input"}
    )
    submit = SubmitField(
        "Enviar",
        render_kw={"class": "input_class_submit btn-success"}
    )

# Create or load Excel file and save information from the form
def save_to_excel(data):
    file_name = 'client_info.xlsx'

    if not os.path.exists(file_name):
        wb = Workbook()
        sheet = wb.active

        headers = ["Nome", "Apelido", "Telefone", "Email", "Parceiro(a)", "Procedimento"]
        bold_font = Font(bold=True)

        for col, header in enumerate(headers, start=1):
            cell = sheet.cell(row=1, column=col, value=header)
            cell.font = bold_font
    
    else:
        wb = load_workbook(file_name)
    
    sheet = wb.active
    sheet.append(data)
    wb.save(file_name)

# Google Sheets logic
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Get credentials (you should have your OAuth setup already)
def get_credentials():
    credentials = None
    credentials = None
    if 'credentials' in session:
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)

    # If no valid credentials, initiate the OAuth flow
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=5000)

        # Save credentials to session for future use
        session['credentials'] = credentials.to_json()

    return credentials

def search_sheet_by_name(service, sheet_name="clients_info"):
    # Search for a sheet by name in Google Drive.
    query = f"name = '{sheet_name}' and mimeType = 'application/vnd.google-apps.spreadsheet'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    sheets = results.get('files', [])
    
    if sheets:
        return sheets[0]['id']  # Return the first sheet's ID found
    else:
        return None  # No sheet found

# Create a new sheet if it doesn't exist, or return the existing sheet's ID.
def create_or_get_sheet(sheet_name='clients_info'):
    credentials = get_credentials()

    # First, use the Drive API to check for an existing sheet
    drive_service = build('drive', 'v3', credentials=credentials)
    sheet_id = search_sheet_by_name(drive_service, sheet_name)
    
    if not sheet_id:
        # If no sheet exists, create a new one using the Sheets API
        sheets_service = build('sheets', 'v4', credentials=credentials)
        spreadsheet = {
            'properties': {'title': sheet_name}
        }
        sheet = sheets_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        sheet_id = sheet['spreadsheetId']

        # Define the headers to insert into the first row
        headers = ["Nome", "Apelido", "Telefone", "Email", "Parceiro(a)", "Procedimento"]

        # Prepare the request body to update the first row with headers
        body = {'values': [headers]}

        # Update the first row with headers
        range_ = f'{sheet_name}!A1:F1'  # Adjust this range to your needs 
        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=range_,
            valueInputOption='RAW',  # Use 'RAW' if you just want the raw data inserted, 'USER_ENTERED' for Google Sheets functions
            body=body
        ).execute()

    return sheet_id

def add_data_to_sheet(sheet_id, data):
    # Append data to the given Google Sheet.
    credentials = get_credentials()
    service = build('sheets', 'v4', credentials=credentials)
    
    # Prepare data to be added
    body = {'values': [data]}
    
    # Append data to the first sheet in the document
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='clients_info',  # Adjust this range if needed
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',  # Ensure rows are added, not overwritten
        body=body
    ).execute()