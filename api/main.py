from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from core.engine import load_framework, ai_assess
app=FastAPI(title='Ascendency Intelligence API',version='0.1.0')
class Evidence(BaseModel): name:str; text:str
class AssessmentRequest(BaseModel): criterion:str; evidence:List[Evidence]
@app.get('/health')
def health(): return {'status':'ok','version':'0.1.0'}
@app.get('/framework')
def framework(): return load_framework()
@app.post('/assess')
def assess(req:AssessmentRequest): return ai_assess(req.criterion,[e.model_dump() for e in req.evidence])
