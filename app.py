from flask import Flask, render_template, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from form.secret_CSRF import MAIL_SENDER, MAIL_PASSWORD, TO_EMAIL_PARSERIA
from form.form import PartnerShipForm, save_to_excel, create_or_get_sheet, add_data_to_sheet # import functions from form.py
from form.secret_CSRF import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

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

@app.route('/test')
def test():
    return "This is a test!"

if __name__ == '__main__':
    app.run(debug=True)