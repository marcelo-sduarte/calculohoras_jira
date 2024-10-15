import pieces
from gvars import *

    
def start_process():
    try: 
        pieces.lib_logging.logger.info(f'[INICIO] ->start_process: {PROCESS_NAME} ----  {title} ----')          
        # ==================== CHAMA OS PROCESSOS PRINCIPAIS ==================== #
        #verifica strutura pastas
        pieces.lib_process.verify_structure()
        #recupera mes e ano anterior
        mes, ano = pieces.lib_calendar.get_mes_ano_anterior()
        # limpando dados temp
        pieces.lib_process.remove_files_in_folder(PATH_FILES)
        # Exclui todos files temporarios
        pieces.lib_process.remove_files_in_folder(PATH_OUTPUT)     
        # recupera os feriados
        continuar, string_return = pieces.lib_calendar.get_feriados_api(ano=ano, mes=mes)
        # chama funcao para recuperar dias uteis
        if continuar:         
            continuar, string_return = pieces.lib_calendar.get_dias_uteis(ano=ano, mes=mes, feriados=string_return)                    
        # chama funcao para recuperar jira
        if continuar:
            continuar, string_return = pieces.lib_jira.connect_api_jira()        
        #Se houver falhas sinaliza para o exception
        if continuar:
            # inicia criacao da planilha
            continuar, string_return = pieces.lib_spreadsheet.create_plan_modelo(dias_uteis=string_return,mes=mes,ano=ano) 
        # finaliza automacao
        if continuar:
            pieces.lib_logging.logger.info(f'Processo de calculo executou com sucesso!!!')    
        else:
            raise            
    except Exception as error:
        if string_return != None and continuar == False:
            error = string_return
        pieces.lib_logging.logger.error(f'>> start_process error message: {error}') 
        falha = True         
    finally:
        #envia email com planilha em anexo
        envio_report_email(falha,string_return)
        pieces.lib_logging.logger.info(f'[FIM] -> start_process : {PROCESS_NAME} ----  {title} ----')

def envio_report_email(falha, mensagem_execucao):
    if ENVIO_EMAIL:
        try:
            pieces.lib_logging.logger.info(f'[INICIO] -> envio_report_email')
            if PRD:
                if falha:    
                    pieces.lib_email.send_email(EmailTo = EMAIL_CLIENT,
                                                Co = EMAIL_INTERNO,
                                                Body= f" Falha ao processar, message: {mensagem_execucao}",
                                                Subject= "[Falha] Robo Calculo Jira - Envio relatorio Horas Squads Vortx")
                else:
                    pieces.lib_email.send_email(EmailTo = EMAIL_CLIENT,
                                                Co = EMAIL_INTERNO,
                                            Body= """Processo de calculos de horas, processou com sucesso, verificar file em anexo.   
                                            """,
                                            nameFile= FILE_OUTPUT_JIRA,
                                            output_path= PATH_REPORT,
                                        Subject= "[Sucesso] Robo Calculo Jira - Envio relatorio Horas Squads Vortx")
            else:
                if falha:    
                    pieces.lib_email.send_email(EmailTo = EMAIL_SUPPORT ,                                           
                                                Body= f" Falha ao processar, message: {mensagem_execucao}",
                                                Subject= "[Falha] Homologação - Teste envio relatorio Vortx")
                else:
                    pieces.lib_email.send_email(EmailTo = EMAIL_SUPPORT ,                                     
                                            Body= "Processo de calculos de horas, processou com sucesso, verificar file em anexo.",
                                            nameFile= FILE_OUTPUT_JIRA,
                                            output_path= PATH_REPORT,
                                        Subject= "[SUCESSO] Homologação - Teste envio relatorio Vortx")
            pieces.lib_logging.logger.info(f'-> envio_report_email, modo PRD: {PRD} com status falha: {falha}')
        except Exception as error:
            pieces.lib_logging.logger.error(f' -> envio_report_email, message: {error}')
        finally:
            pieces.lib_logging.logger.info(f'[FIM] -> envio_report_email')


if __name__ == '__main__':
    start_process()
            