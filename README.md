# Changes Made by WEbTech87

## General email Data

  - MAIL_USERNAME = 'request.sender@webtech87.pt'
  - MAIL_PASSWORD = 'xxxx xxxx xxxx' - confirm with WEbTech87(Roberto or Boris)
  - MAIL_SENDER = 'request.sender@webtech87.pt'
  - TO_EMAIL_PARSERIA = 'parceria@santiclinic.eu'

## Backend

### In form/form.py
* Imported openpyxl
* Created the save_to_excel function, which creates a new Excel file or loads an existing one and stores the form data
* In the PartnerShipForm(FlaskForm) class, changed the class name inside render_kw from input_class to form-control for better Bootstrap integration in the frontend
* Implemented Google Sheets integration using the **Google Sheets API** and **Google Drive API**.
* Added authentication with a **service account** to securely access and modify Google Sheets.
* Developed functions to:
  * **Search for an existing spreadsheet** by name in Google Drive.
  * **Create a new spreadsheet** if it doesn’t exist and insert predefined headers.
  * **Share the spreadsheet** with a specified email address with edit permissions.
  * **Append form data** to the sheet dynamically.
* Ensured proper access control and streamlined data entry for storing client information efficiently.


### In app.py
* Imported functions from form.py
* Created the "data" variable to extract form data
* Saves form data to an Excel file using save_to_excel(data).  
* Sends form data to Google Sheets for cloud storage and accessibility.  
* Utilizes create_or_get_sheet() to create or retrieve the Google Sheet.  
* Appends new data to the sheet using add_data_to_sheet(sheet_id, data).  
* Implements error handling to catch and display any Google Sheets-related issues.

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