# Changes Made by WEbTech87

## Geral email Data

  - MAIL_USERNAME = 'academiasaudesucesso@gmail.com'
  - MAIL_PASSWORD = 'xxxx xxxx xxxx' - confirm with WEbTech87(Roberto or Boris)
  - MAIL_SENDER = 'academiasaudesucesso@gmail.com'
  - TO_EMAIL_PARSERIA = 'parceria@santiclinic.eu'

The file with secret information is storage in drive boris.isac@webtech87.pt

## Backend

# Translation using flask-babel

### In form/form.py


Created Form with next fields:
  
    nome-First name(chardield)
    apelido-Last name(chardield)
    tel - Phone number(charfield)
    email - Emailfield
    partner_ship_list-SelectField
    procedure_list - SelectField
    checkbox -Bool
    submit - Button


### In app.py

**Function get_locale()** get from chockes a location and set it up by default

**Function set_language()** Change languages from list stored in variable(app.config['BABEL_SUPPORTED_LOCALES'])

**INDEX** load a main page with form. On clicking to submit if form is valif it will create **data** with form_data and it will send  
a email to  "**_parceria@santiclinic.eu_**" with all data and append to google sheet new rec 


### Em requirements.txt
* Fixed the file name from requirments.txt to requirements.txt
* Added versions of openpyxl and google libraries for authentication and API access

### .gitignore added to the main branch

## Frontend

### In styles.css and media_query.css
* Implemented Bootstrap 4 (Bootswatch Spacelab)
* Used the "Roboto" font for a more professional look
* Removed negative margin values to prevent the form and its elements from exceeding the screen limits
* Changed align-items: center to align-items: flex-start in body
* Aligned the label with the input field
* Added padding inside the input field for better placeholder visibility
* Centered and resized the font of the text "Eu concordo..."
* Made necessary adjustments for responsiveness on tablets and mobile devices