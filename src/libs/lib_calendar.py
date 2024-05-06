from gvars import HMG_ANBIMA
import pieces

def get_feriados_api(ano, mes):
    try:
        pieces.lib_logging.logger.info(f"[INICIO] get_feriados()")
        url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
       
        response = pieces.requests.get(url)

        if response.status_code in (200,201,202,204):
            pieces.lib_logging.logger.info(f" > Conectado com sucesso na api, response: {response.status_code}")
            feriados = response.json()
            #pieces.lib_logging.logger.info(f" > Retornou os feriados do ano: {feriados}")
            return get_feriado_mes(feriados=feriados, ano=ano, mes=mes)
        else:
            pieces.lib_logging.logger.error(f" > Falha ao obter os feriados. response: {response.status_code}")
            return None
    except Exception as error:
        pieces.lib_logging.logger.error(f"mensagem: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM] get_feriados()")

def get_feriado_mes(feriados, ano, mes):
   try:
    pieces.lib_logging.logger.info(f"[INICIO] get_feriado_mes()")
    list_feriado_mes = []
    for feriado in feriados:
        data = feriado['date']
        feriado_ano, feriado_mes, _ = map(int, data.split('-'))
        if feriado_ano == ano and feriado_mes == mes:
            list_feriado_mes.append(data)
            pieces.lib_logging.logger.info(f"> Neste mes tem os seguintes feriados: {list_feriado_mes}")
            return list_feriado_mes
        
   except Exception as error:
    pieces.lib_logging.logger.info(f" > message error: {error}")
   finally:
       pieces.lib_logging.logger.info(f"[FIM] get_feriado_mes()")

def get_dias_uteis(mes, ano, feriados=[]):
    try:
        pieces.lib_logging.logger.info(f"[INICIO] get_dias_uteis()")
        # Obtém o último dia do mês
        ultimo_dia_mes = pieces.calendar.monthrange(ano, mes)[1]
        # Lista para armazenar os dias úteis excluindo os feriados
        dias_uteis_sem_feriados = []
        # Itera por todos os dias do mês
        for i in range(1, ultimo_dia_mes + 1):
            dia = pieces.datetime.date(ano, mes, i)
            # Verifica se o dia não é um feriado, é um dia útil (não é sábado ou domingo) e não é feriado
            if dia.weekday() < 5 and dia.strftime('%Y-%m-%d') not in feriados:
                dias_uteis_sem_feriados.append(dia.day)
        pieces.lib_logging.logger.error(f" > Total Dias Uteis: {len(dias_uteis_sem_feriados)}, dias_uteis: {dias_uteis_sem_feriados}")
    
        return dias_uteis_sem_feriados
    except Exception as error:
        pieces.lib_logging.logger.error(f" > get_dias_uteis, message: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM] get_dias_uteis()")
    
def get_data_inicio_fim(dias_uteis,horas,row,saldo,mes,ano):
    pieces.lib_logging.logger.info(f"[INICIO] get_data_inicio_fim()")
    index = 0
    dif_horas = 0
    adicionado_horas = False
    try:                  
        dias = int(horas / 8)
        if (dias * 8) != horas:
            dif_horas = horas - (dias * 8) 
            saldo = int(saldo) + dif_horas
            if saldo == 8:
                #adiciona um dia a a mais para data fim
                dias = dias +1
                adicionado_horas = True
            else:
                # sinaliza saldo
                adicionado_horas = False
        data_inicio = dias_uteis[int(row)]
        index = int(row+(dias-1))
        data_fim = dias_uteis[index]
        dt_inicio = f"{data_inicio}/{mes}/{ano}"
        dt_fim = f"{data_fim}/{mes}/{ano}"
        pieces.lib_logging.logger.info(f"data_inicio:{dt_inicio} data_fim:{dt_fim}")
        # Converter a string em um objeto datetime
        dia_inicio = pieces.datetime.datetime.strptime(dt_inicio, '%d/%m/%Y')
        dia_fim = pieces.datetime.datetime.strptime(dt_fim, '%d/%m/%Y')
        return dia_inicio, dia_fim, index, dif_horas, adicionado_horas
    except Exception as error:
        pieces.lib_logging.logger.info(f" > error message: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM] get_data_inicio_fim()")

def dias_fora_do_intervalo_ferias(lista_dias_uteis, dia_inicial, dia_final):
    try:
        pieces.lib_logging.logger.info(f"[INICIO] dias_fora_do_intervalo_ferias()")
        # Criando um conjunto com os dias úteis no intervalo
        dias_uteis_no_intervalo = set(lista_dias_uteis) & set(range(dia_inicial, dia_final + 1))    
        # Retornando os dias úteis que não estão no intervalo

        return sorted(list(set(lista_dias_uteis) - dias_uteis_no_intervalo))
    except Exception as error:
        pieces.lib_logging.logger.error(f" > error message: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM] dias_fora_do_intervalo_ferias( :{sorted(list(set(lista_dias_uteis) - dias_uteis_no_intervalo))}")
        
def get_mes_ano_anterior():
    try:
        pieces.lib_logging.logger.info(f"[INICIO] get_mes_ano_anterior()")
        # Obtendo a data e hora atuais
        data_atual = pieces.datetime.datetime.now()
        ano = data_atual.year
        # Subtrair um mês
        mes = data_atual.month
        if mes == 1:  # 1 janeiro, se for janeiro volta ano anterior 
            ano -= 1
            mes = 12
        else:
            ano = data_atual.year
            mes -= 1
        pieces.lib_logging.logger.info(f" » Trabalhando com ano: {ano} mes: {mes}")
        return mes, ano
    except Exception as error:
        pieces.lib_logging.logger.error(f" > error message: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM] get_mes_ano_anterior()")