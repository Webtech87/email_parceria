# Mudanças feitas por Felipe

## Backend

### Em form/form.py
* Import de openpyxl
* Criação de função save_to_excel que cria um novo ficheiro excel, ou carrega se já existente, e armazena as informações obtidas no formulário
* Dentro de class PartnerShipForm(FlaskForm), houve mudança do nome da class dentro de render_kw: de input_class para form-control para melhor uso do Bootstrap no frontend

### Em app.py
* Import da função save_to_excel
* Criação da variável "data" com os dados a extrair do formulário
* Chamada da função save_to_excel tendo como parametro a variável "data"

### Em requirements.txt
* Correção nome do ficheiro de requirments.txt para requirements.txt
* Adição de versão de openpyxl

### .gitignore adicionado ao main

## Frontend

### Em styles.css e media_query.css
* Uso de framework Bootstrap 4 (Bootswatch Spacelab)
* Uso de fonte "Roboto" para visual mais profissional
* Retirada de margens de valores negativos para impedir que o formulário e seus elementos ultrapassassem limite do ecrã
* Mudança de align-items: center para align-items: flex-start no body
* Alinhamento do label com o input
* Uso de padding dentro do input para melhor visualização do placeholder
* Centralização e mudança no tamanho da fonte do texto "Eu concordo..."
* Mudanças necessárias em alguns elementos para responsividade para tablet e telemóvel