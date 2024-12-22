# tasks.py
from crewai import Task
from agents import (
    symptom_analyst, test_interpreter, diagnosis_specialist,
    treatment_planner
)

symptom_analysis_task = Task(
    description="Analyze reported symptoms and identify potential conditions.",
    expected_output='Symptom analysis report',
    agent=symptom_analyst
)

test_interpretation_task = Task(
    description="Interpret provided test results and imaging studies.",
    expected_output='Test results interpretation',
    agent=test_interpreter
)

diagnosis_suggestion_task = Task(
    description="Suggest most likely diagnosis based on all information.",
    expected_output='Diagnosis report',
    agent=diagnosis_specialist
)

treatment_planning_task = Task(
    description="Recommend treatment plan based on diagnosis.",
    expected_output='Treatment plan',
    agent=treatment_planner,
    async_execution=False
)