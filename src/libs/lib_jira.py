import pieces
from gvars import JIRA_API_TOKEN, JIRA_SERVER, JIRA_USER, JIRA_QUERY

def connect_api_jira(ano, mes):
    try:
        pieces.lib_logging.logger.info(f"[INICIO] connect_api_jira()")
        # Conecta-se ao Jira
        jira = pieces.JIRA(JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

        # Define a data de início do mês anterior e o início deste mês
        primeiro_dia = pieces.datetime.datetime(ano, mes, 1).strftime("%Y-%m-%d")
        ultimo_dia = pieces.datetime.datetime(ano, mes, pieces.calendar.monthrange(ano, mes)[1]).strftime("%Y-%m-%d") 

        # Define a query JQL
        '''
        query = ('project in (BANK, COR, CS, FBACK, FIDC, FLIQ, INV, "Fundos Backoffice Cadmus", Escrituracao) '
                'and issuetype in ("Automação", "Debito Tecnico", Story) '
                'and resolutiondate >= "{}" '
                'and resolutiondate <= "{}" '
                'and status = Done').format(primeiro_dia, ultimo_dia)
        
        '''
        query = ('project in ("Fundos 175 - Cadmus" , "Fundos BackOffice - Cadmus" , Boletador , "Fundos Liquidos" , FID2, Tech-Descentralizada, Investor , "Corporate Back" , "Corporate Front" , Plataformas , BAAS ) '
                 'and issuetype in ( "Debito Tecnico", Story) '
                 'and resolutiondate >= startOfMonth(-1) and '
                 'resolutiondate < startOfMonth() and status = Done')
        
        # Faz a consulta ao Jira   
        issues = jira.search_issues(query)
        # Extrai os dados relevantes das issues
        data = []
        for issue in issues:
            data.append({
            'Key': issue.key,
            'Summary': issue.fields.summary,
            'Resolution Date': issue.fields.resolutiondate
            })
        # Cria um DataFrame a partir dos dados
        df = pieces.pd.DataFrame(data)
        return df
    except Exception as error:
        pieces.lib_logging.logger.error(f" > message error connect_api_jira: {error}")
    finally:
        pieces.lib_logging.logger.info(f"[FIM] connect_api_jira()")


