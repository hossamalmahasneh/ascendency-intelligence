import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
from core.engine import load_framework, extract_text, ai_assess

st.set_page_config(page_title='Ascendency Intelligence', page_icon='◆', layout='wide')
st.markdown('''<style>
.block-container{padding-top:1.5rem}.hero{padding:22px 26px;border:1px solid #27364d;border-radius:18px;background:linear-gradient(135deg,#071426,#10223b);color:white}.gold{color:#d6b25e}.card{border:1px solid #dfe5ec;border-radius:14px;padding:14px;margin:5px 0}.small{opacity:.72;font-size:.88rem}
</style>''',unsafe_allow_html=True)
F=load_framework()
if 'evidence' not in st.session_state: st.session_state.evidence=[]
if 'results' not in st.session_state: st.session_state.results={}
if 'validated' not in st.session_state: st.session_state.validated={}

st.markdown('<div class="hero"><h2>Ascendency <span class="gold">Intelligence</span></h2><div>Enterprise Governance Intelligence · Demo Organization</div><div class="small">Evidence-grounded assessment · Human validation · Executive intelligence</div></div>',unsafe_allow_html=True)
page=st.sidebar.radio('Workspace',['Dashboard','Assessment Setup','Evidence Workspace','AI Assessment','Executive Report'])
st.sidebar.caption('MVP v0.1 · anonymized demo framework')

criteria=[(d,c) for d in F['domains'] for c in d['criteria']]
def result_rows():
    rows=[]
    for d,c in criteria:
        r=st.session_state.validated.get(c['id']) or st.session_state.results.get(c['id'])
        rows.append({'Domain':d['name'],'Criterion':c['title'],'Score':r.get('score') if r else None,'Status':r.get('status','Not assessed') if r else 'Not assessed','Validated':c['id'] in st.session_state.validated})
    return rows

if page=='Dashboard':
    rows=result_rows(); done=[r for r in rows if r['Score']]
    avg=sum(r['Score'] for r in done)/len(done) if done else 0
    c1,c2,c3,c4=st.columns(4); c1.metric('Overall maturity',f'{avg:.2f}/5'); c2.metric('Criteria assessed',f'{len(done)}/{len(rows)}'); c3.metric('Evidence files',len(st.session_state.evidence)); c4.metric('Human validated',sum(r['Validated'] for r in rows))
    st.subheader('Domain maturity')
    df=pd.DataFrame(done)
    if not df.empty: st.bar_chart(df.groupby('Domain')['Score'].mean())
    else: st.info('Upload evidence and run an AI assessment to populate the dashboard.')
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
elif page=='Assessment Setup':
    st.header('Assessment Setup'); st.text_input('Organization','Demo Organization'); st.text_input('Assessment','Digital Transformation Maturity Assessment 2026')
    for d in F['domains']:
        with st.expander(f"{d['name']} · {len(d['criteria'])} criteria",expanded=True):
            for c in d['criteria']: st.markdown(f"**{c['title']}** — {c['question']}")
    st.caption('Maturity scale: 1 Initial · 2 Under Development · 3 Established · 4 Managed · 5 Optimized')
elif page=='Evidence Workspace':
    st.header('Evidence Workspace'); files=st.file_uploader('Upload policies, procedures, reports or evidence',type=['pdf','docx','txt','md'],accept_multiple_files=True)
    if st.button('Ingest evidence',type='primary') and files:
        existing={e['name'] for e in st.session_state.evidence}
        for f in files:
            if f.name not in existing: st.session_state.evidence.append({'name':f.name,'text':extract_text(f)})
        st.success(f'{len(files)} file(s) processed.')
    for e in st.session_state.evidence:
        with st.expander(e['name']): st.write(e['text'][:3000] or 'No extractable text.')
elif page=='AI Assessment':
    st.header('AI Assessment & Human Validation'); labels={f"{d['name']} — {c['title']}":(d,c) for d,c in criteria}; choice=st.selectbox('Criterion',list(labels)); d,c=labels[choice]; st.info(c['question'])
    if st.button('Run evidence-grounded assessment',type='primary'):
        with st.spinner('Assessing evidence...'): st.session_state.results[c['id']]=ai_assess(c['question'],st.session_state.evidence)
    r=st.session_state.results.get(c['id'])
    if r:
        a,b,cx=st.columns(3); a.metric('AI maturity',f"{r['score']}/5"); b.metric('Evidence status',r['status']); cx.metric('Confidence',f"{100*r.get('confidence',0):.0f}%")
        st.write(r['rationale']); st.subheader('Evidence citations')
        for q in r.get('citations',[]): st.markdown(f"**{q['source']}**\n\n> {q['quote']}")
        score=st.slider('Validated maturity score',1,5,int(r['score'])); status=st.selectbox('Validated status',['Supported','Partial','Missing','Requires Review'],index=['Supported','Partial','Missing','Requires Review'].index(r['status']) if r['status'] in ['Supported','Partial','Missing','Requires Review'] else 3)
        note=st.text_area('Reviewer note')
        if st.button('Approve human validation'):
            st.session_state.validated[c['id']]={**r,'score':score,'status':status,'reviewer_note':note}; st.success('Validated decision saved to the assessment record.')
elif page=='Executive Report':
    st.header('Executive Report'); rows=result_rows(); done=[r for r in rows if r['Score']]
    if not done: st.warning('No assessment results yet.')
    else:
        df=pd.DataFrame(done); avg=df['Score'].mean(); st.metric('Overall maturity',f'{avg:.2f}/5'); st.bar_chart(df.groupby('Domain')['Score'].mean()); st.subheader('Priority gaps'); gaps=df[df['Score']<3].sort_values('Score'); st.dataframe(gaps,use_container_width=True,hide_index=True)
        report=f"ASCENDENCY INTELLIGENCE — EXECUTIVE ASSESSMENT\nOrganization: Demo Organization\nOverall maturity: {avg:.2f}/5\n\n"+df.to_string(index=False)+"\n\nPriority: validate all AI assessments before management use."
        st.download_button('Download executive report',report,'ascendency_executive_report.txt','text/plain')
