from flask import Flask, render_template, redirect, url_for, flash
import smtplib
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from google.oauth2 import service_account
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from form.form import PartnerShipForm
from form.secret_CSRF import MAIL_SENDER, MAIL_PASSWORD, TO_EMAIL_PARSERIA, SECRET_KEY, GOOGLE_SHEET_ID
from flask_babel import Babel
from flask import request
from flask_babel import gettext as _
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_file = os.path.join(BASE_DIR , 'credentials','client_secret.json')
print('****',os.path.exists(cred_file))

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'pt']

URL = "https://docs.google.com/spreadsheets/d/1Jr1gHIpyliXhP-2fE99hWEzoBUxZUUZAWVwMjI1X_4M/edit?usp=sharing"

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

SAMPLE_SPREADSHEET_ID = "1Jr1gHIpyliXhP-2fE99hWEzoBUxZUUZAWVwMjI1X_4M"

credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, SCOPES)

client = gspread.authorize(credentials)

google_sheet = client.open(
    title="Parceria",
    folder_id="1aHtbVM1_ZexrYtMy0TbxVdtCl8TdK_fo"
)

sheet = google_sheet.get_worksheet(0)

babel = Babel(app)

def get_locale():
    return request.cookies.get('lang') or request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

babel.init_app(app, locale_selector=get_locale)


@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    if lang_code in app.config['BABEL_SUPPORTED_LOCALES']:
        resp = redirect(url_for('index'))
        resp.set_cookie('lang', lang_code)
        return resp
    return 'Language does not suported!!', 400


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PartnerShipForm()

    if form.validate_on_submit():
        nome = form.nome.data
        apelido = form.apelido.data
        tel = form.tel.data
        email = form.email.data
        partner = form.partner_ship_list.data
        procedure = form.procedure_list.data
        acept = True
        dt_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        data = [nome, apelido, tel, email, partner, procedure, acept, dt_now]

        try:
            print("connect to google sheet, and add new data")
            sheet.append_row(data)
        except Exception as e:
            print(f"Error Google Sheets: {e}")

        # Создание HTML-письма
        msg = MIMEMultipart()
        msg['From'] = MAIL_SENDER
        msg['To'] = TO_EMAIL_PARSERIA
        msg['Subject'] = "Parceria SantiClinic"

        msg_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f9f9f9;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: auto;
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h2 {{ color: #333333; text-align: center; }}
                p {{ line-height: 1.5; color: #555555; }}
                .footer {{ text-align: center; font-size: 12px; color: #888; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <h2>{_('Parceria SantiClinic')}</h2>
                <p><strong>{_('Dados do Cliente')}:</strong></p>
                <p>{_('Nome')}: {nome}<br>{_('Apelido')}: {apelido}</p>
                <p><strong>{_('Contactos')}:</strong></p>
                <p>{_('Telefone')}: {tel}<br>Email: {email}</p>
                <p><strong>{_('Detalhes')}:</strong></p>
                <p>{_('Parceiro(a)')}: {partner}<br>{_('Procedimento')}: {procedure}</p>
                <p class="footer">{_('Dados preenchidos no formulario SantiClinic.')}</p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(msg_html, 'html'))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(MAIL_SENDER, MAIL_PASSWORD)
            server.sendmail(MAIL_SENDER, TO_EMAIL_PARSERIA, msg.as_string())
            server.quit()

            flash(_("Obrigado por enviar os seus dados"), "success")

            return redirect(url_for('index'))

        except Exception as e:
            print(f"EMail sender error: {e}")
            flash(_("Houve um erro ao enviar os dados. Tente novamente."), "error")

    return render_template('index.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)