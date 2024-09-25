import pieces
from gvars import *

def verify_structure():
    try:
        if not pieces.os.path.exists(PATH_INPUT):
            pieces.os.mkdir(PATH_INPUT)
        if not pieces.os.path.exists(PATH_OUTPUT):
            pieces.os.mkdir(PATH_OUTPUT)
        if not pieces.os.path.exists(PATH_LOGS):
            pieces.os.mkdir(PATH_LOGS)
        if not pieces.os.path.exists(PATH_FILES):
            pieces.os.mkdir(PATH_FILES)    
    except Exception as error:
        print(error)
        
def remove_files_in_folder(folder_path):
    # Verifica se o caminho fornecido é um diretório
    if not pieces.os.path.isdir(folder_path):
        pieces.lib_logging.logger.info(f"{folder_path} não é um diretório válido.")
        return
    # Itera sobre todos os arquivos no diretório
    for filename in pieces.os.listdir(folder_path):
        file_path = pieces.os.path.join(folder_path, filename)
        # Verifica se o caminho é um arquivo
        if pieces.os.path.isfile(file_path):
            try:
                # Remove o arquivo
                pieces.os.remove(file_path)
                pieces.lib_logging.logger.info(f"Arquivo {filename} removido com sucesso.")
            except Exception as e:
                pieces.lib_logging.logger.info(f"Erro ao remover o arquivo {filename}: {e}")

def normalizar_texto(texto):
    if isinstance(texto, str):  
        return pieces.unidecode(texto).upper()
    else:
        return texto
    
def remover_acentos(texto):
    try:
        texto_sem_acentos = ''.join(char for char in pieces.unicodedata.normalize('NFD', texto) if pieces.unicodedata.category(char) != 'Mn')
        return pieces.re.sub(r'[^\w\s]', '', texto_sem_acentos)
    except Exception as error:
        pieces.lib_logging.logger.error(f"> error message: ",error)
        
def save_credential(target_name, username, password):
    try: 
        pieces.lib_logging.logger.info(f"[INICIO] save_credential()")
        # Converte a senha para uma string
        password_str = str(password)
        # Define a estrutura da credencial como um dicionário
        cred = {
            'TargetName': target_name,
            'Type': pieces.win32cred.CRED_TYPE_GENERIC,
            'UserName': username,
            'CredentialBlob': password_str,
            'Persist': pieces.win32cred.CRED_PERSIST_LOCAL_MACHINE
        } 
        # Salva a credencial no cofre de senhas do Windows   
        pieces.win32cred.CredWrite(cred)
        pieces.lib_logging.logger.info(f"> user e senha salvos com sucesso!")
    except Exception as error:
        pieces.lib_logging.logger.error(f"> error message:", error)
    finally:
        pieces.lib_logging.logger.info(f"[FIM] save_credential()")

def get_credential(target_name):        
    try:
        pieces.lib_logging.logger.info(f"[INICIO] get_credential()")
        # Tenta obter a credencial do cofre de senhas do Windows
        cred = pieces.win32cred.CredRead(target_name, pieces.win32cred.CRED_TYPE_GENERIC)

        # Decodifica a senha de bytes para uma string UTF-16
        password_decoded = cred['CredentialBlob'].decode('utf-16')

        # Retorna o nome de usuário e a senha
        return cred['UserName'], password_decoded
    except Exception as error:
        if error.winerror == 1168:  # ERROR_NOT_FOUND
            return None, None
        else:
            pieces.lib_logging.logger.error(f"> error message: ", error)
    finally:
        pieces.lib_logging.logger.info(f"[FIM] get_credential()")