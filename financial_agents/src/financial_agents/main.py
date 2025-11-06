import warnings
from litellm.exceptions import RateLimitError, Timeout, APIError, BadRequestError
from financial_agents.src.financial_agents.crew_ai import FinancialAgents

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def crew_ai_project(prompt, conteudo, provider, api_key):
    try: 
        crew_instance = FinancialAgents(provider, api_key)
        
        result = crew_instance.crew().kickoff(inputs={
                                                        "prompt": prompt,
                                                        "conteudo": conteudo,
                                                    })
        return result
    
    except RateLimitError as rle:
        return f"""Limite de requisições atingido! 
            Tente novamente em alguns instantes. 
            (Modelo: {rle.model}) (Mensagem: {rle.message})"""
        

    except Timeout as to:
        return f"""A requisição demorou mais do que o esperado e foi cancelada. 
            Verifique sua conexão ou tente novamente.
            \nDetalhes técnicos: {to}"""
        

    except APIError as apierror:
        return f"""Ocorreu um erro ao se comunicar com a API do modelo. 
            Isso pode ser temporário. Tente novamente mais tarde.
            \nDetalhes técnicos: {apierror}"""
        

    except BadRequestError as bre:
        return f"""A solicitação enviada ao modelo não foi aceita (Bad Request). 
            Isso geralmente acontece por parâmetros incorretos ou incompatibilidade com o modelo escolhido.
            \nDetalhes técnicos: {bre}"""
        
