# === Bibliotecas Base ===

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# === LLM Base ===

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")  # Configure sua API key como variável de ambiente
)

# === AGENTES ===

gerente = Agent(
    role="Gerente de Projeto Financeiro",
    goal="Interpretar o pedido do usuário, identificar o tipo de análise desejada e organizar as etapas necessárias para resolvê-lo com clareza e eficiência.",
    backstory=(
        "Você é um gerente experiente no setor financeiro com profundo conhecimento em processos analíticos. "
        "Seu papel é entender solicitações de usuários relacionadas a análises de investimentos e estruturar a resolução do problema"
        "dividindo em etapas claras e atribuindo responsabilidades adequadas aos demais agentes. "
        "Você preza por clareza, organização e foco na entrega de valor. Responda sempre em português."
    ),
    verbose=False,
    llm=llm
)

analista = Agent(
    role="Analista Financeiro",
    goal="Desenvolver um relatório organizado sobre as ações exportadas",
    backstory=(
        "Você é um analista de dados altamente qualificado com experiência em finanças. "
        "Ao receber os ativos informados pelo gerente, você é especialista em gerar um relatório técnico inicial com os principais indicadores que serão usados na visualização."
        "Em seguida, você carrega os dados prontos para análise e gera uma base clara e confiável."
        "Você se comunica de forma técnica, precisa e voltada para a integridade dos dados. Responda sempre em português."
    ),
    verbose=False,
    llm=llm,
    
)

consultor = Agent(
    role="Consultor de Investimentos",
    goal="Interpretar relatório e dashboard gerado, auxiliando o usuário a tomar decisões de investimento embasadas nos dados apresentados.",
    backstory=(
        "Você é um consultor experiente do mercado financeiro com habilidade em interpretar dashboards e traduzir informações técnicas em orientações acessíveis para o usuário. "
        "Seu papel é receber os relatórios e visualizações criados pelo analista de dados e explicar de forma clara o que os dados significam, destacando oportunidades, riscos e pontos de atenção. "
        "Você responde às dúvidas do usuário sobre os ativos analisados e pode sugerir caminhos estratégicos com base nos dados. "
        "Seu foco está em tornar o conteúdo compreensível, promover educação financeira e orientar a análise de forma prática e informada. Responda sempre em português."
    ),
    verbose=False,
    llm=llm
)

# === Tasks ===

with open('dashboard_escrito.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.read()

def crew_ai_project(prompt):

    tarefa_gerente = Task(
        description="Entender o problema do usuário e extrair um relatório do que deve ser feito para resolve-lo. Prompt do Usuário: "+prompt,
        agent=gerente,
        expected_output="Relatório detalhado sobre as necessidades dp usuário e o que ele deseja saber."
    )

    tarefa_analista = Task(
        description = "Baseado no relatório fornecido, aplicar o processo de ETL (extração, transformação e carga)."
        "Aqui está o dashboard financeiro para análise:\n\n"+conteudo,
        agent=analista,
        expected_output="Arquivo CSV tratado com Python e salvo como 'data_cleaned.csv'.",
        context=[tarefa_gerente]

    )

    tarefa_consultor = Task(
        description="Analisar os dados presentes no dashboard e gerar um relatório, focando em gerar insights/soluções para o usuário",
        agent=consultor,
        expected_output=f"Relatório de análise com insights e recomendações baseadas nos dados. Utilize o seguinte caminho para acessar o resumo:",
        context=[tarefa_gerente, tarefa_analista],

    )
    
    # === Crew ===

    crew = Crew(
        input=prompt,
        agents=[gerente, analista, consultor],
        tasks=[tarefa_gerente, tarefa_analista, tarefa_consultor],
        verbose=True,
        process=Process.sequential
    )

    # === Execução ===

    resultado = crew.kickoff()

    return resultado

# Me forneça um feedback sobre sua rentabilidade nesse período de tempo
