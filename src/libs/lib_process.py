import pieces

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
    texto_sem_acentos = ''.join(char for char in pieces.unicodedata.normalize('NFD', texto) if pieces.unicodedata.category(char) != 'Mn')
    return pieces.re.sub(r'[^\w\s]', '', texto_sem_acentos)
