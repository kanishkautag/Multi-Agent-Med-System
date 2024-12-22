from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

my_llm = LLM(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini/gemini-pro",
)

symptom_analyst = Agent(
    role='Symptom Analyst',
    goal='Analyze patient symptoms and suggest possible conditions.',
    backstory="Expert in analyzing symptoms and identifying potential conditions.",
    verbose=True,
    allow_delegation=False,
    llm=my_llm
)

test_interpreter = Agent(
    role='Test Interpreter',
    goal='Interpret lab results and imaging studies.',
    backstory="Specialist in interpreting medical tests and lab results.",
    verbose=True,
    allow_delegation=False,
    llm=my_llm
)

diagnosis_specialist = Agent(
    role='Diagnosis Specialist',
    goal='Suggest the most likely diagnosis based on all available information.',
    backstory="Experienced diagnostician who determines likely conditions.",
    verbose=True,
    allow_delegation=False,
    llm=my_llm
)

treatment_planner = Agent(
    role='Treatment Planner',
    goal='Recommend a treatment plan based on the diagnosis.',
    backstory="Expert in developing patient-specific treatment plans.",
    verbose=True,
    allow_delegation=False,
    llm=my_llm
)