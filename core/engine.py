from __future__ import annotations
import json, os, re
from pathlib import Path
from typing import List, Dict, Any

BASE = Path(__file__).resolve().parents[1]

def load_framework():
    return json.loads((BASE/'data'/'demo_framework.json').read_text())

def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()
    if name.endswith('.pdf'):
        from pypdf import PdfReader
        from io import BytesIO
        return '\n'.join((p.extract_text() or '') for p in PdfReader(BytesIO(raw)).pages)
    if name.endswith('.docx'):
        from docx import Document
        from io import BytesIO
        return '\n'.join(p.text for p in Document(BytesIO(raw)).paragraphs)
    return raw.decode('utf-8', errors='ignore')

def heuristic_assess(question: str, evidence: List[Dict[str,str]]) -> Dict[str,Any]:
    text = ' '.join(e.get('text','') for e in evidence).lower()
    terms = [w for w in re.findall(r'[a-z]{5,}', question.lower()) if w not in {'through','defined','demonstrably','enterprise','systematically','documented','supported'}]
    hits = sorted({t for t in terms if t in text})
    coverage = min(1.0, len(hits)/max(3, len(set(terms))))
    if not evidence or len(text.strip()) < 80: score, status = 1, 'Missing'
    elif coverage < .25: score, status = 2, 'Partial'
    elif coverage < .55: score, status = 3, 'Supported'
    elif coverage < .8: score, status = 4, 'Supported'
    else: score, status = 5, 'Supported'
    snippets=[]
    for e in evidence:
        t=e.get('text','').replace('\n',' ')
        if t: snippets.append({'source':e.get('name','Evidence'),'quote':t[:280]})
    return {'score':score,'status':status,'confidence':round(.45+.45*coverage,2),'rationale':f'Evidence coverage matched {len(hits)} relevant assessment concepts. Human validation is required.','citations':snippets[:3]}

def ai_assess(question: str, evidence: List[Dict[str,str]]) -> Dict[str,Any]:
    key=os.getenv('OPENAI_API_KEY')
    if not key: return heuristic_assess(question,evidence)
    try:
        from openai import OpenAI
        client=OpenAI(api_key=key)
        prompt={"criterion":question,"evidence":[{"source":e['name'],"text":e['text'][:12000]} for e in evidence],"scale":{"1":"Initial","2":"Under Development","3":"Established","4":"Managed","5":"Optimized"}}
        r=client.responses.create(model=os.getenv('OPENAI_MODEL','gpt-5-mini'),input='Assess only from supplied evidence. Return JSON with score integer 1-5, status Supported/Partial/Missing/Requires Review, confidence 0-1, rationale, citations [{source,quote}]. No unsupported claims.\n'+json.dumps(prompt))
        txt=r.output_text.strip().removeprefix('```json').removesuffix('```').strip()
        return json.loads(txt)
    except Exception:
        return heuristic_assess(question,evidence)
