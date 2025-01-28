from flask import Flask, render_template, request, redirect, url_for, flash, session
from wtforms import BooleanField
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from form.secret_CSRF import MAIL_SENDER, MAIL_PASSWORD, TO_EMAIL_PARSERIA
from form.form import PartnerShipForm, save_to_excel, get_credentials, create_or_get_sheet, add_data_to_sheet, SCOPES # import functions from form.py
from form.secret_CSRF import SECRET_KEY, CLIENT_SECRET_FILE
import threading
import multiprocessing

#imports to authenticate Google credentials
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)
oauth_app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
oauth_app.config['SECRET_KEY'] = SECRET_KEY

REDIRECT_URI = 'http://localhost:5000/oauth2callback'

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

        # Send to excel and to Google Sheets
        data = [nome, apelido, tel, email, partner, procedure]
        save_to_excel(data)
        try:
            # Create or retrieve the sheet and append data
            sheet_id = create_or_get_sheet()
            add_data_to_sheet(sheet_id, data)
        except Exception as e:
            print(f"An error occurred with Google Sheets: {e}")

        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = MAIL_SENDER
        msg['To'] = TO_EMAIL_PARSERIA
        msg['Subject'] = "Parceria SantiClinic"
        
        # HTML-styled email
        msg_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    padding: 0;
                    background-color: #f9f9f9;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h2 {{
                    color: #333333;
                    text-align: center;
                }}
                p {{
                    line-height: 1.5;
                    color: #555555;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #888888;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <h2>Parceria SantiClinic</h2>
                <p><strong>Dados do Cliente:</strong></p>
                <p>Nome: {nome}<br>
                   Apelido: {apelido}</p>
                <p><strong>Contactos:</strong></p>
                <p>Telefone: {tel}<br>
                   Email: {email}</p>
                <p><strong>Detalhes:</strong></p>
                <p>Parceiro(a): {partner}<br>
                   Procedimento: {procedure}</p>
                <p class="footer">Dados preenchidos no formulario SantiClinic.</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(msg_html, 'html'))

        # SMTP server configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(MAIL_SENDER, MAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(MAIL_SENDER, TO_EMAIL_PARSERIA, text)
            server.quit()

            print("Email has been sent!")
            flash("Obrigado por enviar os seus dados", "success")  # Flash success message
            return redirect(url_for('index'))

        except Exception as e:
            print(f"Email could not be sent due to error: {e}")
            flash("Houve um erro ao enviar os dados. Tente novamente.", "error")  # Flash error message

    return render_template('index.html', form=form)

@oauth_app.route('/oauth2callback')
def oauth2callback():
    # The flow is already initialized with the redirect URI
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES, redirect_uri=REDIRECT_URI)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    if not flow.credentials:
        flash("Failed to fetch the credentials!", "error")
        return redirect(url_for('index'))

    credentials = flow.credentials
    # Save credentials to session for future use
    session['credentials'] = credentials.to_json()

    flash("Autenticação bem-sucedida!", "success")
    return redirect(url_for('index'))
    
'''if __name__ == '__main__':
    import threading

    # Function to run the OAuth app on port 5000
    def run_oauth_app():
        print("Starting OAuth app on port 5000")
        oauth_app.run(port=5000, use_reloader=False)

    # Start the OAuth app in a separate thread
    oauth_thread = threading.Thread(target=run_oauth_app)
    oauth_thread.daemon = True  # Ensures it exits when the main program exits
    oauth_thread.start()

    # Run the main Flask app on port 5001
    print("Starting main app on port 5001")
    app.run(port=5001, use_reloader=False)'''

# Running in different processes for testing
def run_oauth_app():
    print("Starting OAuth app on port 5000")
    oauth_app.run(debug=True, port=5000, use_reloader=False)

def run_main_app():
    print("Starting Main app on port 5001")
    app.run(debug=True, port=5001, use_reloader=False)

if __name__ == '__main__':
    # Start both Flask apps in separate processes
    oauth_process = multiprocessing.Process(target=run_oauth_app)
    main_process = multiprocessing.Process(target=run_main_app)

    oauth_process.start()
    main_process.start()

    # Wait for both processes to finish (this will allow them to run independently)
    oauth_process.join()
    main_process.join()
