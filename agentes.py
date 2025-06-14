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
    role="Gerente de Projeto Financeiro: Leonardo",
    goal="Interpretar o pedido do usuário, identificar o tipo de análise solicitada e estruturar um plano de ação claro e eficiente.",
    backstory=(
        "Você é um gerente experiente no setor financeiro, especializado em coordenar projetos de análise de dados. "
        "Seu papel é compreender a necessidade do usuário com precisão, definir os objetivos da análise e organizar as etapas necessárias para solucioná-la. "
        "Você documenta o problema, identifica os dados e define um plano para que os demais agentes possam trabalhar de forma eficiente. "
        "É detalhista, organizado e orientado à entrega de valor. Responda sempre em português."
    ),
    verbose=False,
    llm=llm
)

analista = Agent(
    role="Analista de Dados Financeiros: Lucca",
    goal="Realizar análise técnica dos dados fornecidos, destacando padrões, métricas relevantes e possíveis insights.",
    backstory=(
        "Você é um analista de dados com ampla experiência no mercado financeiro. "
        "Recebe o direcionamento do gerente e os dados fornecidos, aplicando técnicas de análise estatística e financeira para identificar tendências, anomalias e informações relevantes. "
        "Sua entrega consiste em um relatório técnico que servirá de base para recomendações consultivas. "
        "Você prioriza precisão, integridade dos dados e clareza na apresentação dos resultados. Responda sempre em português."
    ),
    verbose=False,
    llm=llm
)

consultor = Agent(
    role="Consultor de Investimentos: ",
    goal="Interpretar os relatórios e transformar os dados analisados em recomendações práticas e estratégicas para o usuário.",
    backstory=(
        "Você é um consultor de investimentos com sólida experiência em traduzir dados financeiros em decisões estratégicas. "
        "Recebe os relatórios do gerente e do analista, e transforma as informações técnicas em recomendações compreensíveis para o usuário. "
        "Seu foco é apontar oportunidades, alertar sobre riscos e oferecer caminhos de ação com base em dados. "
        "Você valoriza clareza, orientação ao usuário e educação financeira. Responda sempre em português."
    ),
    verbose=False,
    llm=llm
)

# === Tasks ===

with open('dashboard_escrito.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.read()

def crew_ai_project(prompt):

    tarefa_gerente = Task(
    description=(
        "Você é o Gerente de Projeto responsável por interpretar a solicitação inicial do usuário.\n"
        "Analise o seguinte prompt enviado pelo usuário:\n\n"
        f"{prompt}\n\n"
        "Com base nesse texto, gere um **relatório técnico detalhado** que identifique:\n"
        "- O problema principal apresentado pelo usuário\n"
        "- Os objetivos que o usuário deseja alcançar\n"
        "- As informações ou dados necessários para análise\n"
        "- Possíveis abordagens de solução que envolvam análise de dados\n\n"
        "O objetivo é fornecer um briefing claro para que os demais agentes consigam atuar com precisão."
    ),
    agent=gerente,
    expected_output="Relatório técnico com diagnóstico do problema, objetivos do usuário e proposta de solução com base em análise de dados."
)

    tarefa_analista = Task(
    description=(
        "Você é o Analista de Dados.\n"
        "Com base no relatório produzido pelo Gerente, realize uma análise exploratória detalhada dos dados contidos no dashboard financeiro fornecido.\n\n"
        "Aqui está o conteúdo do dashboard (texto estruturado):\n\n"
        f"{conteudo}\n\n"
        "Realize as seguintes análises:\n"
        "- Identifique padrões de variação nos preços das ações\n"
        "- Verifique indicadores como média móvel, variação percentual e volume\n"
        "- Aponte possíveis anomalias ou comportamentos fora do padrão\n"
        "- Gere visualizações (se possível)\n\n"
        "Seu objetivo é transformar os dados em um relatório técnico com interpretações claras."
    ),
    agent=analista,
    expected_output="Relatório técnico com análise dos dados do dashboard, incluindo estatísticas relevantes, padrões e observações.",
    context=[tarefa_gerente]
)

    tarefa_consultor = Task(
    description=(
        "Você é o Consultor de Negócios.\n"
        "Com base no relatório do Gerente (entendimento do problema) e no relatório do Analista (análise dos dados), produza um documento consultivo que forneça **insights estratégicos e recomendações práticas** para o usuário.\n\n"
        "Sua análise deve incluir:\n"
        "- Principais oportunidades identificadas nos dados\n"
        "- Riscos ou alertas relevantes\n"
        "- Sugestões de ações ou investimentos com base nas tendências observadas\n"
        "- Qualquer recomendação para novos dados a serem analisados ou acompanhados\n\n"
        "Use linguagem consultiva, clara e orientada a valor para o usuário final."
    ),
    agent=consultor,
    expected_output="Relatório consultivo com insights estratégicos e recomendações com base nos dados analisados e necessidades do usuário.",
    context=[tarefa_gerente, tarefa_analista]
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
