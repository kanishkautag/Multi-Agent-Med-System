from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from crew import medical_crew

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    symptoms: str
    test_results: str

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)