# Ascendency Intelligence MVP v0.1
Enterprise Governance Intelligence demo: evidence ingestion → AI assessment → human validation → maturity dashboard → executive report.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```
Optional API:
```bash
uvicorn api.main:app --reload --port 8000
```

## AI
Without `OPENAI_API_KEY`, the app uses a deterministic heuristic demo assessor. With a key, it uses an evidence-only LLM assessment with citations and human validation.

## Supabase
Run `sql/schema.sql` in Supabase SQL Editor. v0.1 UI uses session state so it can be demonstrated immediately; persistence is the next integration step.

## Data boundary
The included framework is anonymized for demonstration. No organization name is present in the demo dataset. Do not represent demo outputs as actual customer findings or product traction.
