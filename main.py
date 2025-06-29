from crews.content_crew.content_crew import FinancialCrew

def crew_ai_project(prompt):

    crew_instance = FinancialCrew()

    result = crew_instance.crew().kickoff(inputs={"prompt": prompt})

    return result