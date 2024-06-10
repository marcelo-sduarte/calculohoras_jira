import pieces
# environment
PRD = False

# PROCESS
PROCESS_NAME = "CALCULOSHORAS_JIRA"

if PRD:
    title = 'Executando em modo Produção'
else:
    title = 'Executando em modo Homologação'


# TODAY
today = pieces.date.today().strftime('%d-%m-%y') 

# paths
PATH_PROCESS_FOLDER = r"C:\Users\marce\Documents\Python\Automation"+ pieces.os.sep + PROCESS_NAME
PATH_OUTPUT = PATH_PROCESS_FOLDER + pieces.os.sep + "output"
PATH_INPUT = PATH_PROCESS_FOLDER + pieces.os.sep + "input"
PATH_LOGS = PATH_OUTPUT + pieces.os.sep +"logs"
PATH_FILES = PATH_OUTPUT + pieces.os.sep +"files"

# Nome do File
FILE_OUTPUT_JIRA = "export_jira.xlsx"
# Path file  saida
PATH_REPORT = pieces.os.path.join(PATH_FILES, FILE_OUTPUT_JIRA)

#filename logs
FILENAME = PATH_LOGS + pieces.os.sep + f"output-{today}.log"

# PATH E COLUNAS INPUT FILE XLSX JIRA
PATH_EXCEL_2 = PATH_INPUT + pieces.os.sep + "jira-2024-05.xlsx"

SHEET_2 = "Sheet1"
COLUNA_PROJETO = 'Project'
COLUNA_WORK_ITEM = 'Summary'
COLUNA_KEY = 'Key'

# COLUNAS INPUT FILE XLSX FUNCIONARIOS
PATH_EXCEL_3 = PATH_INPUT + pieces.os.sep + "BookMai.xlsx"
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
# endpoint homologacao ANBIMA
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
#EMAIL_INTERNO = "marcelo.duarte@cadmus.com.br,vinicius.cortez@cadmus.com.br"
#EMAIL_CLIENT = "fsh@vortx.com.br"
EMAIL_CLIENT = "marcelo.duarte@cadmus.com.br"
EMAIL_SUPPORT = "marcelo.duarte@cadmus.com.br"
EMAIL_INTERNO = "marcelo.duarte@cadmus.com.br"

#JIRA
JIRA_SERVER = 'https://vortxtech.atlassian.net'
JIRA_USER = 'seu_usuario'
JIRA_API_TOKEN = 'seu_token_de_api'
JIRA_QUERY = 'project in (BANK, COR, CS, FBACK, FIDC, FLIQ, INV, "Fundos Backoffice Cadmus", Escrituracao) and issuetype in ("Automação", "Debito Tecnico", Story) and resolutiondate >= startOfMonth(-1)  and resolutiondate < startOfMonth() and status = Done'






