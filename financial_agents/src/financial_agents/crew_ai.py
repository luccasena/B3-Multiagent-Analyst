from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, task, crew
from crewai import Agent, Crew, Process, Task
from typing import Tuple, Any
from crewai import TaskOutput
from .tools.custom_tool import FAISSRAGTool 
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from typing import List
import re

# ------------------------------------------------------------------------------

def validar_resposta_conceitual(result: TaskOutput) -> Tuple[bool, Any]:

    try:
        texto = result.raw.strip()
        tamanho = len(texto)

        print(f"Comprimento da resposta: {tamanho} caracteres")

        if tamanho < 500:
            return (False, f"A resposta é muito curta ({tamanho} caracteres). Deve ter pelo menos 500 caracteres.")
        
        return (True, texto)
    except Exception as e:
        return (False, f"Erro ao validar resposta: {e}")


def limitar_resposta(output) -> Tuple[bool, str]:

    try:
        if hasattr(output, "output"):  
            resposta = str(output.output)
        else:
            resposta = str(output)

        if len(resposta) > 1500:
            return (False, "A resposta ultrapassa o limite de 1500 caracteres. Reformule de forma mais direta e objetiva.")
        
        return (True, resposta)
    
    except Exception as e:
        return (False, f"Erro ao validar resposta: {e}")


def usar_rag_tool(prompt: str) -> str:
    """
    Decide se deve acionar o RAG antes da execução da task.
    Retorna o conteúdo da busca RAG ou o prompt original.
    """
    try:
        if validar_resposta_conceitual(prompt):
            print("Pergunta conceitual detectada. Usando RAG...")
            return FAISSRAGTool()._run(prompt)
        
        print("Pergunta não conceitual. RAG não acionado.")
        return prompt
    
    except Exception as e:
        print(f"Erro ao verificar pergunta conceitual: {e}")
        return prompt

# ------------------------------------------------------------------------------

@CrewBase
class FinancialAgents():
    """FinancialAgents crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self, PROVIDER, API_KEY):
        self.API_KEY = API_KEY

        if PROVIDER == "OpenAI":
            self.llm = ChatOpenAI(model="gpt-4.1-mini", api_key=self.API_KEY)

        if PROVIDER == "Groq":
            self.llm = ChatGroq(model="groq/llama-3.3-70b-versatile", api_key=self.API_KEY)
            
   
    @agent
    def analista_financeiro(self) -> Agent:
        return Agent(
            config=self.agents_config['analista_financeiro'],
            verbose=True,
            llm=self.llm
        )

    @agent
    def gerente_financeiro(self) -> Agent:
        return Agent(
            config=self.agents_config['gerente_financeiro'],
            verbose=True,
            llm=self.llm,
        )
    
    @agent
    def consultor_investimentos(self) -> Agent:
        return Agent(
            config=self.agents_config['consultor_investimentos'],
            verbose=True,
            llm=self.llm,
        )
# ------------------------------------------------------------------------------

    @task
    def tarefa_gerente(self) -> Task:
        def pre_run_fn(inputs):
            inputs["prompt"] = usar_rag_tool(inputs.get("prompt", ""))
            return inputs

        return Task(
            config=self.tasks_config['tarefa_gerente'], 
            tools=[FAISSRAGTool()],
            pre_run=pre_run_fn,
            guardrail=validar_resposta_conceitual,
            max_iterations=3
        )

    @task
    def tarefa_analista(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_analista'], 
        )
    
    @task
    def tarefa_consultor(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_consultor'],
            max_output_tokens=1500,
            guardrail=limitar_resposta,
            max_iterations=3
        )

# ------------------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True
        )
    