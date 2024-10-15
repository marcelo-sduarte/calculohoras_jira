import pieces
from gvars import *
       
def coleta_indicadores(dataframe):
    try:
        
        pieces.lib_logging.logger.info("> INICIO coleta_indicadores()")            

        # pega todos coloboradores do dataframe
        lista_colaboradores = dataframe['Nome'].unique()

        for item in lista_colaboradores:
            dados_filtrados = dataframe.loc[dataframe['Nome'] == item]
            total_titulos = dados_filtrados['Título'].nunique()
            pieces.lib_logging.logger.info(f"total de itens do {item} foi: {total_titulos}")
                                
    except Exception as error:
        pieces.lib_logging.logger.error(f"ERRO no coleta_indicadores: message: {error}")

    finally:
        pieces.lib_logging.logger.info("> FIM coleta_indicadores()")
        
def export_to_excel(dataframes, filenames):
    try:
        pieces.lib_logging.logger.info(">[INICIO] export_to_excel()")
        for df, file_name in zip(dataframes, filenames):
            file_name = PATH_FILES + pieces.os.sep +f"{file_name}.xlsx"  # Adicionando a extensão .xlsx
            df.to_excel(file_name, index=False)
            print(f"DataFrame exportado para '{file_name}' com sucesso.")
    except Exception as error:
        pieces.lib_logging.logger.error(f"> ERRO create_base: message: {error}")
    finally:
        pieces.lib_logging.logger.info(">[FIM] export_to_excel()")

def mapear_qtd_funcionarios_projeto(file_path,sheet_name):
    try:
        pieces.lib_logging.logger.info(">[INICIO] mapear_qtd_funcionarios_projeto() ")
        df_funcionarios = pieces.pd.read_excel(file_path, sheet_name=sheet_name)

        contagens_por_projeto = {}
        # Agrupando as funcionario por projeto
        funcao_por_projeto = df_funcionarios.groupby(f'{COLUNA_PROJETO_FUNC}')[f'{COLUNA_FUNCAO}'].apply(list) 
        
        for projeto, funcoes in funcao_por_projeto.items():            
            # Filtrar funcionários por  projeto
            filter_projeto = df_funcionarios[(df_funcionarios[f'{COLUNA_PROJETO_FUNC}'] == projeto)]
            # Filtrando valores nulos na coluna 'Nome'
            filter_projeto_sem_nulos = filter_projeto[(filter_projeto[f'{COLUNA_NOME_FUNC}'].notna()) & (filter_projeto[f'{COLUNA_HORAS}'].notna())]            
            # Filtrar funcionários por projeto
            funcionarios_projeto = filter_projeto_sem_nulos[(filter_projeto_sem_nulos[f'{COLUNA_PROJETO_FUNC}'] == projeto)]  

            # Agrupar os dados pela coluna 'Funcao' e contar o número de ocorrências de cada função
            contagem_funcoes = funcionarios_projeto[f'{COLUNA_FUNCAO}'].value_counts()

            # Adicionar a contagem de funcionários por função ao dicionário
            contagens_por_projeto[projeto] = contagem_funcoes.to_dict()        

        pieces.lib_logging.logger.info(f"contagens_por_projeto: {contagens_por_projeto}")
        
        return contagens_por_projeto

    except Exception as error:
        pieces.lib_logging.logger.error(f">[ERRO] mapear_qtd_funcionarios_squad(): message: {error}")
    finally:
        pieces.lib_logging.logger.info(">[FIM] mapear_qtd_funcionarios_projeto() ")

def get_qtd_funcao(dictionary,projeto, funcao):
    try:
        total = dictionary[f'{projeto}'][f'{funcao}']
        pieces.lib_logging.logger.info(f"[INICIO]get_qtd_funcao")
        pieces.lib_logging.logger.info(f" > total: {total} na funcao: {funcao}")
        return total
    except Exception as error:
        pieces.lib_logging.logger.error(f"ERRO get_qtd_funcao, menssage: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM]get_qtd_funcao")

def insert_rows_dataframe(dataframe,row_df_modelo,add_total_item,work_itens,total_work_item,squad,funcao,nome,horas_por_work_itens,random_itens, row_horas, dias_uteis,mes,ano,inicio_ferias,fim_ferias,ferias, projeto):
    # filtrar somente work iten do squad em loop                                 
    try:
        pieces.lib_logging.logger.info(f"[INICIO]insert_rows_dataframe()")
        linha_add = 0
        row_data = 0 
        saldo = 0 

        for i in range(int(add_total_item)):   
            # Associa horas
            horas = horas_por_work_itens[row_horas]
            lista_horas = horas_por_work_itens
            #verificar data ferias
            if ferias:
                dias_uteis_mes = pieces.lib_calendar.dias_fora_do_intervalo_ferias(dia_inicial= int(inicio_ferias.day), dia_final= int(fim_ferias.day),lista_dias_uteis= dias_uteis) 
            else:
                dias_uteis_mes = dias_uteis
            # pegar data inicio e fim
            dt_inicio, dt_fim, row_data,saldo_horas, add_horas, saldo = pieces.lib_calendar.get_data_inicio_fim(list_horas = horas_por_work_itens,dias_uteis=dias_uteis_mes, row=row_data, horas=horas, mes=mes, ano=ano, saldo=saldo)          
            # guarda saldo se houver
            saldo = saldo + saldo_horas
            # ajuste horas 
            if add_horas:
                horas = horas + saldo_horas
            elif saldo > 0 and saldo < horas:
                horas = horas - saldo_horas
            elif saldo > 0 and saldo <= horas:
                horas = saldo
            # incremento de linhas
            row_data += 1
            #  sorteia um work item para inserir na row datagrame modelo
            tentativa = 0 
            while True: 
                tentativa += 1               
                work_item = work_itens.sample(n=1).values[0]
                #remover acentos
                #work_sem_acento = pieces.lib_process.remover_acentos(work_item)
                if str(work_item[0]) not in random_itens:
                    random_itens.append(work_item[0])                            
                    break 
                if total_work_item == tentativa:
                        random_itens = []       
            #insere row no dataframe             
            dataframe.loc[row_df_modelo] = {
                'Squad': squad, 
                'Projeto': projeto, 
                'Título': work_item[1], 
                'Função': funcao, 
                'Nome': nome,
                'Inicio': dt_inicio ,
                'Fim': dt_fim,
                'Qtd Horas': horas}
            pieces.lib_logging.logger.info(f"> Adicionando: {nome} item: {work_item}  horas:{horas}")                               
            row_df_modelo += 1
            linha_add += 1            
            row_horas +=1                    
        return row_df_modelo
    except Exception as error:
        pieces.lib_logging.logger.error(f" > message error ao insert_rows_dataframe(): {error}")
        pieces.traceback.print_exc()
    finally:
        pieces.lib_logging.logger.info(f"[FIM] insert_rows_dataframe()")                

def distribuir_numero(numero, partes):
    quociente, resto = divmod(numero, partes)
    partes_distribuidas = [quociente] * partes
    # Adiciona o resto à primeira parte
    partes_distribuidas[0] += resto
     # se o numero for que a parte retorna sempre o indice 0
    if numero < partes:
        return partes_distribuidas
    # Encontra o valor majoritário e o valor das partes restantes
    #valor_majoritario = quociente
    #valor_restante = quociente
    #for valor in partes_distribuidas:
    #    if valor != quociente:
    #        valor_restante = valor
     #       break
    return partes_distribuidas

def distribuir_horas(horas, partes):
    try:
        pieces.lib_logging.logger.info("[INICIO] distribuir_horas()") 
        if partes < 1:
            raise Exception(f"Numero negativo em partes: {partes}")
      
        # Inicializa a lista com partes iguais a 8
        distribuicao = [8] * partes

        # Verifica se há somente uma parte
        if partes == 1 or horas <= 8 :
            distribuicao = []
            distribuicao.append(horas)
            return distribuicao
        elif partes == 2:
            distribuicao = []
            horas_distribuidas = horas / partes
            for i in range(partes):
                distribuicao.append(horas_distribuidas)
        
        # Calcula a soma inicial das partes
        soma_total = sum(distribuicao)

        # Define os múltiplos de 8 a serem adicionados em ordem crescente
        multiplos_de_8 = [8 * i for i in range(1, 26)]

        # Verifica se a soma total é menor que o número de horas desejado
        if soma_total < horas:
            # Adiciona partes extras, respeitando o total de partes e o número de horas desejado
            for multiplo in multiplos_de_8:
                if soma_total == horas:
                        break
                for index,num in enumerate(distribuicao):
                    if soma_total == horas:
                        break
                    if soma_total < horas:
                        distribuicao.pop(index)
                        distribuicao.append(multiplo)
                        soma_total = sum(distribuicao)
                    else:
                        distribuicao.pop()
                        distribuicao.append(8)
                        soma_total = sum(distribuicao)
        elif soma_total > horas:
            diferenca_horas = soma_total - horas
            dif_qtd = (diferenca_horas /8)+1
            for i in range(int(dif_qtd)):
                if soma_total == horas:
                    break
                distribuicao.pop(i)
                soma_total = sum(distribuicao)
                partes_total = len(distribuicao)
            if soma_total < horas:
                diferenca_horas = horas - soma_total
                distribuicao.append(diferenca_horas)
                soma_total = sum(distribuicao)

        # ajuste tamanho se necessário
        if len(distribuicao) != partes:
            saldo_partes = partes - partes_total
            for saldo in range(saldo_partes):
                distribuicao.append(1)
                soma_total = sum(distribuicao)
        # Ajusta hora se necessário
        if soma_total != horas:
            diferenca_horas = horas  - soma_total
            if diferenca_horas < 0 :
                for index, numero in enumerate(distribuicao):
                    diferenca_horas = horas  - soma_total
                    if soma_total == horas:
                        break
                    value = distribuicao[index]
                    if value > abs(diferenca_horas):
                        saldo_horas = value - abs(diferenca_horas)
                        distribuicao[index] = saldo_horas
                        soma_total = sum(distribuicao)
        return distribuicao
    except Exception as error:
         pieces.lib_logging.logger.error(f"> error message: {error}")  
    finally:
        pieces.lib_logging.logger.info("[FIM] distribuir_horas()") 

def create_plan_modelo(dias_uteis,mes,ano):
    try:  
        lista_erros = []
        total_anterior = 0
        falha = False
        pieces.lib_logging.logger.info("> INICIO create_plan_modelo()")    
        #recupera dados do excel JIRA
        df_jira_geral = pieces.pd.read_excel(PATH_EXCEL_2, sheet_name=SHEET_2)
        #selecionando somente duas colunas do Jira
        colunas_selecionadas = [f'{COLUNA_KEY}',f'{COLUNA_WORK_ITEM}', f'{COLUNA_PROJETO}']
        df_jira_selecao = df_jira_geral[colunas_selecionadas]
        #formata campo projeto para trocar de sigla para campo texto inteiro
        df_jira = formata_df(df=df_jira_selecao)
        #recupera dados do excel com horas, projeto e funcionarios
        df_funcionarios = pieces.pd.read_excel(PATH_EXCEL_3, sheet_name=SHEET_3)
        # Chama funcao para calcular total funcionario em todas do projeto
        dic_funcionarios = pieces.lib_spreadsheet.mapear_qtd_funcionarios_projeto(file_path=PATH_EXCEL_3, sheet_name=SHEET_3)
        # Cria o modelo dataframe que sera entregue        
        df_modelo = pieces.pd.DataFrame(columns=COLUMNS_PLAN_MODELO)
        #Agrupando projeto e Nome dos funcionarios planilha variavel
        funcionario_por_projeto = df_funcionarios.groupby(f'{COLUNA_PROJETO_FUNC}')[f'{COLUNA_NOME_FUNC}'].apply(list)
        row_df_modelo = 0
        # Iterar sobre cada projeto e suas work item
        for projeto, nome in funcionario_por_projeto.items():
            # Filtrar funcionários por projeto
            funcionarios_projeto = df_funcionarios[(df_funcionarios[f'{COLUNA_PROJETO_FUNC}'] == projeto)]
            # Filtrando valores nulos na coluna 'Nome'            
            filter_projeto_sem_nulos = funcionarios_projeto[(funcionarios_projeto[f'{COLUNA_NOME_FUNC}'].notna()) & (funcionarios_projeto[f'{COLUNA_HORAS}'].notna())]
            #filtrar projeto de acordo com resumo jira
            work_filter = df_jira[(df_jira[f'{COLUNA_PROJETO}'] == projeto)]
            #totalizar itens
            total_work_item = work_filter[f'{COLUNA_WORK_ITEM}'].count()
            try:                                                
                #work_itens = work_filter[f'{COLUNA_WORK_ITEM}']
                #work_itens = work_filter[f'{COLUNA_KEY}']                                                
                #work_filter[f'{COLUNA_KEY}']  
                if work_filter.empty:
                    pieces.lib_logging.logger.error(f"> Ver projeto: {projeto} esta divergente entre Jira e Base de Funcionários")
                    continue
            except Exception as error:
                pieces.lib_logging.logger.error(f"> ERRO new_create_plan_modelo: message: {error}")
            # Se tiver vazio significa que nao tem funcionario para este projeto pula para prox
            if filter_projeto_sem_nulos.empty:
                continue
            #localizar hora do funcionario pra dividir pelo total work itens 
            nome_anterior = "" 
            projeto_anterior = "" 
            indice = 0            
            for func, row in filter_projeto_sem_nulos.iterrows():                
                horas = row[f'{COLUNA_HORAS}']
                nome = row[f'{COLUNA_NOME_FUNC}']
                funcao = row[f'{COLUNA_FUNCAO}']
                squad = row[f'{COLUNA_SQUAD}']
                dt_inicio_ferias = row[f'{COLUNA_INICIO}']
                dt_fim_ferias = row[f'{COLUNA_FIM}']  
                

                # valida ferias
                if not pieces.pd.isnull(dt_inicio_ferias) and not pieces.pd.isnull(horas):
                    ferias = True
                else:
                    ferias = False
                # Valida Horas file funcionarios
                result_validation = pieces.lib_spreadsheet.valida_dias_uteis_file_func(dias_uteis=dias_uteis, horas=horas, ferias=ferias, nome= nome)
                if len(result_validation) > 0:
                    lista_erros += result_validation
                    falha = True
                    continue
                if nome != nome_anterior:
                    row_horas_funcionario = 0
                    #indice = 0
                nome_anterior = nome
                # zera indice se mudar de projeto ( esse indice controla a divisao de work item se for float)
                if nome != nome_anterior and projeto != projeto_anterior:
                    indice = 0
                #pega to total de funcionarios naquela funcao do projeto especifico
                total_funcionario_funcao = pieces.lib_spreadsheet.get_qtd_funcao(dic_funcionarios,projeto,funcao) 
                ''' Normalmente funcionarios que tem somente 1 na funcao como Team Leader e Teach Lead 
                    deve sempre limpar a lista para pegar todos itens por projeto 
                '''
                if total_funcionario_funcao == 1:
                    random_itens = []
                elif total_anterior == 1:
                    ''' Quando a linha anterior for igual 1 e nova for != entao pode ser funcao de desenvolvedor
                        que tem mais de um por projeto, no primeiro loop zeramos lista e nos proximos loops 
                        usa a mesma lista de itens para distribuir entre os dev da mesma projeto.
                    '''
                    random_itens = []
                # guarda numero anterior antes de prosseguir    
                total_anterior =  total_funcionario_funcao
                # Se tiver mais itens do que funcinario faz divisao por funcionario
                if total_work_item >= total_funcionario_funcao:
                    # divide o total de itens pelo total de funcionarios de uma funcao especifica
                    work_item_funcao = int(total_work_item) / int(total_funcionario_funcao)          
                else:
                # Se tiver mais funcinario faz divisao por work itens
                    work_item_funcao =  int(total_funcionario_funcao) / int(total_work_item)                                                                   
                # Trata diferente se o resultado der um numero inteiro
                if isinstance(work_item_funcao,int):
                    # divide horas por work itens
                    horas_por_work_itens  = distribuir_horas(horas=int(horas), partes=int(work_item_funcao))

                    add_total_item = work_item_funcao                                                                                
                    pieces.lib_logging.logger.info("""
                                                    Time: {} 
                                                    Nome: {}
                                                    Funcao {} 
                                                    Horas Linha: {}
                                                    Total horas:{}
                                                    Linhas Add:{}""".format(projeto,nome,funcao,work_item_funcao,horas_por_work_itens,add_total_item))                                    
                # se o resultado for float faz outro calculo
                
                else:
                    work_por_funcao = distribuir_numero(numero=total_work_item,partes=total_funcionario_funcao)                                                      
                    if len(work_por_funcao) > 1 and sum(work_por_funcao) > total_funcionario_funcao:                        
                        add_total_item = work_por_funcao[indice] 
                        indice += 1            
                    else:
                        add_total_item = work_por_funcao[0]                                             
                    # Inserir horas no dataframe
                    horas_por_work_itens  = distribuir_horas(horas=int(horas), partes=int(add_total_item))            
                    pieces.lib_logging.logger.info("""
                                                    Time: {} 
                                                    Nome: {}
                                                    Funcao {}                                                                                           
                                                    Linhas com int: {}                         
                                                    Total horas:{} 
                                                    Linhas add:{}""".format(projeto,nome,funcao,horas_por_work_itens,horas,add_total_item))                                                                                                   
                # funcao para adicionar as linhas no dataframe modelo
                
                row_df_modelo = insert_rows_dataframe(dataframe=df_modelo,
                                    row_df_modelo=row_df_modelo,
                                    add_total_item=add_total_item,
                                    work_itens=work_filter,
                                    total_work_item=total_work_item,
                                    squad=squad,
                                    funcao=funcao,
                                    nome=nome,
                                    horas_por_work_itens=horas_por_work_itens,
                                    random_itens = random_itens,
                                    row_horas = row_horas_funcionario,
                                    dias_uteis = dias_uteis,
                                    mes = mes,
                                    ano = ano,
                                    inicio_ferias = dt_inicio_ferias,
                                    fim_ferias = dt_fim_ferias,
                                    ferias = ferias,
                                    projeto = projeto
                                    )                                                                                     
       
        # Salva o Excel com resultado
        if not falha:
            pieces.lib_logging.logger.info(f"df modelo: {df_modelo.head()}")
            pieces.lib_logging.logger.info(f">create_plan_modelo: no path: {PATH_REPORT}")
            df_modelo.to_excel(PATH_REPORT, index=False) 
            continuar = True 
            msg = "Sucesso"
    except Exception as error:
        pieces.lib_logging.logger.error(f"> ERRO create_plan_modelo: message: {error}")
        pieces.traceback.print_exc()
        continuar = False
        msg = error
    finally:
        pieces.lib_logging.logger.info("> FIM create_plan_modelo()")
        return continuar, msg 
    
def valida_dias_uteis_file_func(dias_uteis, horas, ferias,nome):
    try:
        pieces.lib_logging.logger.info("> INICIO valida_dias_uteis_file_func()")
        erros = []
        total_dias_uteis = len(dias_uteis)
        total_horas_possiveis = total_dias_uteis * 8
        if ferias:
            if horas == total_horas_possiveis:
                msg = f"» Funcionario: {nome} - Não foi descontado horas de ferias na tab funcionarios: {horas}"
                pieces.lib_logging.logger.error(msg) 
                erros.append(msg)                       
        if horas >  total_horas_possiveis:
            msg = f"» Funcionario: {nome} - Divergencia entre horas possiveis: {total_horas_possiveis} e horas na tabela funcionario: {horas} em dias uteis: {total_dias_uteis}"
            pieces.lib_logging.logger.error(msg)
            erros.append(msg)  
        return erros 
        
    except Exception as error:
        pieces.lib_logging.logger.error(f"> ERRO valida_dias_uteis_file_func: message: {error}")
        pieces.traceback.print_exc()
    finally:
        pieces.lib_logging.logger.info("> FIM valida_dias_uteis_file_func()")
    
            
def formata_df(df):
    try:
       for palavra, substituicao in zip(COL_JIRA_API, PROJECTS):
            df['Project'] = df['Project'].str.replace(palavra, substituicao)
    except Exception as error:
       pieces.lib_logging.logger.error({error}) 
    finally:
        #df.to_excel(PATH_REPORT, index=False) 
        return df


    
    
