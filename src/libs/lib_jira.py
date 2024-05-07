import pieces
from gvars import JIRA_API_TOKEN, JIRA_SERVER, JIRA_USER

def connect_api_jira():
    try:
        pieces.lib_logging.logger.info(f"[INICIO] connect_api_jira()")
        
        # Conectando ao Jira
        jira = pieces.JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))
        # Exemplo: obtendo informações de um issue
        issue_key = 'PROJ-123'  # Substitua 'PROJ-123' pelo código do seu issue
        issue = jira.issue(issue_key)
        pieces.lib_logging.logger.info("Detalhes do issue:")
        pieces.lib_logging.logger.info("Título:", issue.fields.summary)
        pieces.lib_logging.logger.info("Descrição:", issue.fields.description)
    except Exception as error:
        pieces.lib_logging.logger.error(f" > message error connect_api_jira: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM] connect_api_jira()")


