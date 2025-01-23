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