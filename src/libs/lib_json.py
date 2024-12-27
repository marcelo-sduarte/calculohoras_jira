import pieces
from gvars import COLUMNS_PLAN_MODELO

def salvar_json(resultado_json, nome_arquivo):
    try:
        with open(nome_arquivo, 'w',encoding='utf-8') as file:
            pieces.json.dump(resultado_json, file, indent=4, ensure_ascii=False)
        pieces.lib_logging.logger.info(f'Arquivo JSON "{nome_arquivo}" salvo com sucesso!')
    except Exception as error:
        pieces.lib_logging.logger.error(f'Erro ao salvar o arquivo JSON: {error}')

def adicionar_dados_json(arquivo_json, novos_dados):
    try:
        # Abrir o arquivo JSON existente e carregar os dados
        with open(arquivo_json, 'r') as file:
            dados_existente = pieces.json.load(file)
        
        # Adicionar novos dados ao JSON existente
        dados_existente["vortex_team"].extend(novos_dados)
        
        # Salvar os dados atualizados de volta ao arquivo JSON
        with open(arquivo_json, 'w') as file:
            pieces.json.dump(dados_existente, file, indent=4)
        
        pieces.lib_logging.logger.info("Novos dados adicionados com sucesso ao arquivo JSON.")
    except Exception as error:
        pieces.lib_logging.logger.error(f"Erro ao adicionar dados ao arquivo JSON: {error}")

def localizar_dados_json(arquivo_json, key, json_name):
    try:
        pieces.lib_logging.logger.info(f"[Inicio] -> localizar_dados_json()")
        valores_encontrados = set()
        # Abrir o arquivo JSON existente e carregar os dados
        with open(arquivo_json, 'r', encoding='utf-8') as file:
            dados_existente = pieces.json.load(file)
            
            # Localiza pela Key no JSON existente
            for item in dados_existente.get(json_name, []):
                if key in item:
                    value = item[key]
                    #não trata projetos Banking
                    if "Banking" in value:
                        continue
                    value_sem_espaco = str.replace(value," ","_")
                    valores_encontrados.add(value_sem_espaco)  
            if valores_encontrados: 
                 # Convertendo o conjunto para uma lista antes de retornar
                valores_encontrados = list(valores_encontrados)             
                #pieces.lib_logging.logger.info(f"Na busca da {key}, encontrou o value: {valores_encontrados} ")                 
                return valores_encontrados
            else:
                pieces.lib_logging.logger.error(f"Nao foi localizada [{key}]no JSON {arquivo_json} ") 
        return True
    except Exception as error:
        pieces.lib_logging.logger.error(f"Erro ao localizar_dados_json() message: {error}")
        return False
    finally:
        pieces.lib_logging.logger.info(f"[Fim] -> localizar_dados_json()")

def get_json_keys(arquivo_json):
    try:
        pieces.lib_logging.logger.info(f"[Inicio] -> get_json_keys()")

        with open(arquivo_json, 'r') as json_file:
            data = pieces.json.load(json_file)
            keys = list(data.keys())  # Obtém todas as chaves do dicionário JSON
            return keys
        
    except Exception as error:
        pieces.lib_logging.logger.error(f"[ERRO] -> get_json_keys message: {error}")
        return None
    finally:
        pieces.lib_logging.logger.error(f"[FIM] -> get_json_keys()")

