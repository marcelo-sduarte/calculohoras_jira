import pieces
from gvars import *

    
def start_process():
    try: 
        pieces.lib_logging.logger.info(f'[INICIO] ->start_process: {PROCESS_NAME} ----  {title} ----')          
        # ==================== CHAMA OS PROCESSOS PRINCIPAIS ==================== #
        #recupera mes e ano anterior
        mes, ano = pieces.lib_calendar.get_mes_ano_anterior()
        # limpando dados temp
        pieces.lib_process.remove_files_in_folder(PATH_FILES)
        # Exclui todos files temporarios
        pieces.lib_process.remove_files_in_folder(PATH_OUTPUT)     
        # recupera os feriados
        result = pieces.lib_calendar.get_feriados_api(ano=ano, mes=mes)

        if not result[0]:
            dias_uteis = pieces.lib_calendar.get_dias_uteis(ano=ano, mes=mes, feriados=result[1])
            #funcao para tabela modelo
            result = pieces.lib_spreadsheet.create_plan_modelo(dias_uteis=dias_uteis,mes=mes,ano=ano)          
    except Exception as error:
        pieces.lib_logging.logger.error(f'>> start_process error message: ',error)  
        result[0] = True
        result[1] = error
    finally:
        #envia email com planilha em anexo
        envio_report_email(result[0],result[1])
        pieces.lib_logging.logger.info(f'[FIM] -> start_process : {PROCESS_NAME} ----  {title} ----')

def envio_report_email(status, mensagem_execucao):
    try:
        pieces.lib_logging.logger.info(f'[INICIO] -> envio_report_email')
        if PRD:
            if status:    
                pieces.lib_email.send_email(EmailTo = EMAIL_CLIENT,
                                            Co = EMAIL_INTERNO,
                                            Body= f" Falha ao processar, message: {mensagem_execucao}",
                                            Subject= "[Falha] Robo Calculo Jira - Envio relatorio Horas Squads Vortx")
            else:
                pieces.lib_email.send_email(EmailTo = EMAIL_CLIENT,
                                            Co = EMAIL_INTERNO,
                                        Body= """Processo de calculos de horas, processou com sucesso, verificar file em anexo.
                                          Verificar a colaboradora THAIANA DA SILVA LOPES estava com ferias do dia 23 a 30 mais saldo permaneceu 176 ao inves 128
                                        """,
                                        nameFile= FILE_OUTPUT_JIRA,
                                        output_path= PATH_REPORT,
                                    Subject= "[Sucesso] Robo Calculo Jira - Envio relatorio Horas Squads Vortx")
        else:
            if status:    
                pieces.lib_email.send_email(EmailTo = EMAIL_SUPPORT ,                                           
                                            Body= f" Falha ao processar, message: {mensagem_execucao}",
                                            Subject= "[Falha] Homologação - Teste envio relatorio Vortx")
            else:
                pieces.lib_email.send_email(EmailTo = EMAIL_SUPPORT ,                                     
                                        Body= "Processo de calculos de horas, processou com sucesso, verificar file em anexo.",
                                        nameFile= FILE_OUTPUT_JIRA,
                                        output_path= PATH_REPORT,
                                    Subject= "[SUCESSO] Homologação - Teste envio relatorio Vortx")
        pieces.lib_logging.logger.info(f'-> envio_report_email, modo PRD: {PRD} com status falha: {status}')
    except Exception as error:
        pieces.lib_logging.logger.error(f' -> envio_report_email, message: {error}')
    finally:
        pieces.lib_logging.logger.info(f'[FIM] -> envio_report_email')


if __name__ == '__main__':
    start_process()
            