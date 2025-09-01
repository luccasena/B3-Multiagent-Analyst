from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from langchain_openai import ChatOpenAI
from typing import List
from dotenv import load_dotenv, find_dotenv
from .tools.custom_tool import FAISSRAGTool 
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# === LLM Base ===

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=OPENAI_API_KEY, 
    temperature=0
)

# ======================

@CrewBase
class FinancialAgents():
    """FinancialAgents crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
# ------------------------------------------------------------------------------
   
    @agent
    def analista_financeiro(self) -> Agent:
        return Agent(
            config=self.agents_config['analista_financeiro'],
            verbose=True,
            llm=llm 
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
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )