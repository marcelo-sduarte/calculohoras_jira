from gvars import HMG_ANBIMA
import pieces

def get_calendario_anbima_api():
    try:
        pieces.lib_logging.logger.info(f"[INICIO] get_feriados")
        url = HMG_ANBIMA
    
        #response = pieces.requests.get(url, headers=headers)
        response = pieces.requests.get(url)

        if response.status_code in (200,201,202,204):
            pieces.lib_logging.logger.info(f" > Conectado com sucesso na api, response: {response.status_code}")
            feriados = response.json()
            return feriados
        else:
            pieces.lib_logging.logger.error(f" > Falha ao obter os feriados. response: {response.status_code}")
            return None
    except Exception as error:
        pieces.lib_logging.logger.error(f"mensagem: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM] get_feriados")

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