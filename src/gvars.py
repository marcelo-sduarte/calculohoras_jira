import pieces
# environment
PRD = True
ENVIO_EMAIL = False

# PROCESS
PROCESS_NAME = "CALCULOSHORAS_JIRA"

if PRD:
    title = 'Executando em modo Produção'
else:
    title = 'Executando em modo Homologação'



# TODAY
today = pieces.date.today().strftime('%d-%m-%y') 

# paths
PATH_PROCESS_FOLDER = r"C:\Users\YOUR_USER\Documents\Python\Automation"+ pieces.os.sep + PROCESS_NAME
PATH_OUTPUT = PATH_PROCESS_FOLDER + pieces.os.sep + "output"
PATH_INPUT = PATH_PROCESS_FOLDER + pieces.os.sep + "input"
PATH_LOGS = PATH_OUTPUT + pieces.os.sep +"logs"
PATH_FILES = PATH_OUTPUT + pieces.os.sep +"files"

# Nome do File de exportacao
FILE_OUTPUT_JIRA = "export.xlsx"
# Path file  saida
PATH_REPORT = pieces.os.path.join(PATH_FILES, FILE_OUTPUT_JIRA)

#filename logs
FILENAME = PATH_LOGS + pieces.os.sep + f"output-{today}.log"

# CONFIG FILE JIRA 
#PATH_EXCEL_2 = PATH_INPUT + pieces.os.sep + "jira_api_fabio.xlsx"
PATH_EXCEL_2 = PATH_INPUT + pieces.os.sep + "jira_api.xlsx"
#SHEET_2 = "Your Jira Issues"
SHEET_2 = "Sheet1"
COLUNA_PROJETO = 'Project'
COLUNA_WORK_ITEM = 'Summary'
COLUNA_KEY = 'Key'

# CONFI FILE BASE DE FUNCIONARIOS
PATH_EXCEL_3 = PATH_INPUT + pieces.os.sep + "BookSet.xlsx"
COLUNA_SQUAD = 'Squad'
COLUNA_PROJETO_FUNC = 'Projeto'
COLUNA_NOME_FUNC = 'Nome'
COLUNA_FUNCAO = 'Funcao'
COLUNA_HORAS = 'Horas'
COLUNA_INICIO = 'Inicio ferias'
COLUNA_FIM = 'Fim ferias'
SHEET_3 = "Colaboradores"

JSON_FILE = PATH_FILES+ pieces.os.sep +"output_jira.json"

# ====== time ======
SATURDAY = 5
SUNDAY = 6
DAYS_WEEK = [SATURDAY, SUNDAY]


# URLS
# Endpoint Homologacao ANBIMA
HMG_ANBIMA = "https://privateservices-stg.vortx.com.br/vxferiados/api/Holiday/GetInRange?"
PRD_ANBIMA = ""

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
]

COLUMNS_BASE =[
    "Squad","Projeto","Horizonte","ID","Tipo Demanda","Título","Team Leader","Início","Fim","Qtde Horas",
    "Tech Leader","Início","Fim","Qtde Horas","Analista PM","Início","Fim","Qtde Horas",
    "Analista Desenvolvimento","Início","Fim","Qtde Horas","Analista Testes","Início","Fim","Qtde Horas",
    "Analista UX",	"Início","Fim","Qtde Horas"
]

COLUMNS_PLAN_MODELO = ["Squad","Projeto","Título","Função","Nome","Inicio","Fim","Qtd Horas"]

COL_JIRA_API = ["TDES","PLAT","INVT","FULQ","FID2","FBCK","F175","CORB","BAAS"]



# Hoje string formato dd/mm/yyyy
HOJE_DATA = pieces.date.today().strftime('%d-%m-%y') 

# Obtendo a data e hora atuais
data_atual = pieces.datetime.datetime.now()

# Subtrair um mês
mes = data_atual.month
if mes == 1:  # Se estivermos em janeiro, voltamos para dezembro do ano anterior
    ano = data_atual.year
    ano -= 1
    mes = 12
else:
    ano = data_atual.year
    mes -= 1

ANO_ATUAL = ano

# HOJE int formato dd
HOJE = int(pieces.date.today().strftime('%d') )

# CREDENTIAL TARGET
EMAIL_TARGET = "email_cadmus"

# CONF EMAIL
EMAIL_SMTP = "email-ssl.com.br"
EMAIL_PORT = 587
EMAIL_CLIENT = ""
EMAIL_SUPPORT = ""
EMAIL_INTERNO = ""

#JIRA
JIRA_ENDPOINT = 'https://vortxtech.atlassian.net'
PROJECTS = ["Tech-Descentralizada","Plataformas","Investor","Fundos Liquidos","FIDC","Fundos Estruturados","Fundos 175 - Cadmus","Corporate Back","Banking FrontOffice"]
TARGET_TOKEN_JIRA = "token_jira"




