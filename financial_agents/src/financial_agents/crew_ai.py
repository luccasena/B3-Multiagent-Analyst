from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from typing import List
from .tools.custom_tool import FAISSRAGTool 

# ======================

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
            tools=[FAISSRAGTool()]
        )
    
    @agent
    def consultor_investimentos(self) -> Agent:
        return Agent(
            config=self.agents_config['consultor_investimentos'],
            verbose=True,
            llm=self.llm
        )
    
# ------------------------------------------------------------------------------

    @task
    def tarefa_gerente(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_gerente']   
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
    