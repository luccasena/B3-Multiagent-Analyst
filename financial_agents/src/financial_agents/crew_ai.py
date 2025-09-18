from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from langchain_groq import ChatGroq
from typing import List
from dotenv import load_dotenv, find_dotenv
from .tools.custom_tool import FAISSRAGTool 
import os

# === LLM Base ===

load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL")

llm = ChatGroq(model=MODEL, api_key=GROQ_API_KEY)

# ======================

@CrewBase
class FinancialAgents():
    """FinancialAgents crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
   
    @agent
    def analista_financeiro(self) -> Agent:
        return Agent(
            config=self.agents_config['analista_financeiro'],
            verbose=True,
            llm=llm,
        )

    @agent
    def gerente_financeiro(self) -> Agent:
        return Agent(
            config=self.agents_config['gerente_financeiro'],
            verbose=True,
            llm=llm,
            tools=[FAISSRAGTool()]
          
        )
    
    @agent
    def consultor_investimentos(self) -> Agent:
        return Agent(
            config=self.agents_config['consultor_investimentos'],
            verbose=True,
            llm=llm
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
            verbose = True,

        )
    