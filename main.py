from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from crew import medical_crew

app = FastAPI()

# Serve static files (e.g., for your CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Middleware for handling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for patient data
class PatientData(BaseModel):
    symptoms: str
    test_results: str

# Main route rendering the HTML page
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint for analyzing patient data
@app.post("/api/analyze")
async def analyze_patient(patient_data: PatientData):
    try:
        result = medical_crew.kickoff(
            inputs={
                'symptoms': patient_data.symptoms,
                'test_results': patient_data.test_results,
            }
        )
        
        treatment_summary = result
        if isinstance(result, dict):
            treatment_summary = result.get('task_output', '')
            if not treatment_summary:
                treatment_summary = result.get('treatment_plan', '')
                if not treatment_summary:
                    treatment_summary = str(result)
                    
        treatment_summary = str(treatment_summary).strip()
        
        return {"result": treatment_summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Entry point for Vercel, no need for uvicorn.run here
