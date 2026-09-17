import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
from core.engine import load_framework, extract_text, ai_assess

st.set_page_config(page_title="Ascendency Intelligence", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');
:root{--navy:#06101f;--navy2:#09182c;--panel:#0b1c32;--gold:#e4bd68;--gold2:#f7d98b;--text:#f4f6fa;--muted:#94a3b8;--line:rgba(228,189,104,.20)}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:radial-gradient(circle at 78% 8%,rgba(42,73,111,.34),transparent 28%),radial-gradient(circle at 18% 95%,rgba(186,137,46,.10),transparent 25%),linear-gradient(145deg,#040b15 0%,#071426 52%,#05101d 100%);color:var(--text)}
[data-testid="stHeader"]{background:transparent}[data-testid="stSidebar"]{background:linear-gradient(180deg,#050d19,#071526);border-right:1px solid var(--line)}[data-testid="stSidebar"] *{color:#dbe4f0}.block-container{padding:1.3rem 2rem 3rem;max-width:1600px}
#MainMenu,footer{visibility:hidden}h1,h2,h3{letter-spacing:-.02em}h1{font-family:'Playfair Display',serif!important;font-weight:500!important}.gold{color:var(--gold2)}
.brand{padding:14px 4px 25px}.brand-mark{font-size:2rem;color:var(--gold);line-height:1}.brand-name{font-family:'Playfair Display',serif;font-size:1.38rem;letter-spacing:.13em;color:#f5d789}.brand-sub{font-size:.66rem;letter-spacing:.34em;color:#8795a9}
.hero{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:22px;padding:30px 34px;margin-bottom:20px;background:linear-gradient(120deg,rgba(10,28,50,.96),rgba(8,24,44,.80));box-shadow:0 24px 80px rgba(0,0,0,.25)}.hero:after{content:'';position:absolute;width:380px;height:380px;border-radius:50%;right:-80px;top:-260px;background:radial-gradient(circle,rgba(242,196,104,.19),transparent 68%)}.eyebrow{color:var(--gold);text-transform:uppercase;letter-spacing:.18em;font-size:.72rem;font-weight:700}.hero h1{font-size:2.35rem;margin:.35rem 0}.hero p{color:#9cacbf;margin:0;max-width:760px}
.kpi{min-height:150px;border:1px solid rgba(121,151,187,.18);border-radius:18px;padding:20px;background:linear-gradient(145deg,rgba(13,32,55,.94),rgba(7,22,40,.88));box-shadow:0 16px 40px rgba(0,0,0,.18);position:relative;overflow:hidden}.kpi:after{content:'';position:absolute;inset:auto -30px -60px auto;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,rgba(225,183,95,.11),transparent 70%)}.kpi-label{color:#aab6c5;font-size:.82rem}.kpi-value{font-family:'Playfair Display',serif;font-size:2.2rem;color:white;margin:.35rem 0}.kpi-note{font-size:.75rem;color:#6f8299}.kpi-accent{color:var(--gold)}
.section{border:1px solid rgba(121,151,187,.16);border-radius:20px;padding:20px 22px;background:linear-gradient(145deg,rgba(10,28,49,.91),rgba(6,20,37,.88));box-shadow:0 14px 42px rgba(0,0,0,.17);margin:10px 0 18px}.section-title{font-size:1.08rem;font-weight:700;color:#f6f8fb;margin-bottom:3px}.section-sub{font-size:.78rem;color:#7f91a7;margin-bottom:15px}
.pill{display:inline-block;padding:5px 10px;border:1px solid rgba(228,189,104,.28);border-radius:999px;color:#e9c97d;background:rgba(228,189,104,.08);font-size:.72rem;margin:2px}.priority{display:flex;gap:12px;align-items:center;padding:12px 2px;border-bottom:1px solid rgba(130,151,176,.12)}.priority-num{width:30px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,#f4d98e,#b88128);color:#071321;font-weight:800}.priority-text{font-size:.86rem;color:#e8edf4}.priority-meta{font-size:.7rem;color:#8191a5}
.stButton>button,.stDownloadButton>button{border-radius:10px!important;border:1px solid rgba(228,189,104,.45)!important;background:linear-gradient(135deg,#efd58d,#bd8b35)!important;color:#081321!important;font-weight:700!important;box-shadow:0 8px 24px rgba(190,137,43,.15)}.stButton>button:hover,.stDownloadButton>button:hover{border-color:#f6dc98!important;transform:translateY(-1px)}
[data-baseweb="select"]>div,.stTextInput input,.stTextArea textarea{background:#08192c!important;border-color:rgba(126,151,180,.22)!important;color:white!important;border-radius:10px!important}.stFileUploader section{background:rgba(8,25,44,.72)!important;border:1px dashed rgba(228,189,104,.32)!important;border-radius:14px}.stDataFrame{border:1px solid rgba(126,151,180,.15);border-radius:14px;overflow:hidden}
[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(13,32,55,.94),rgba(7,22,40,.88));border:1px solid rgba(121,151,187,.18);padding:16px;border-radius:16px}[data-testid="stMetricValue"]{font-family:'Playfair Display',serif;color:#f6d98d}.stTabs [data-baseweb="tab-list"]{gap:8px}.stTabs [data-baseweb="tab"]{background:#091a2e;border-radius:10px;padding:8px 16px}.stTabs [aria-selected="true"]{background:rgba(228,189,104,.12)!important;color:#f2d17f!important}
hr{border-color:rgba(126,151,180,.12)}
</style>
""", unsafe_allow_html=True)

F=load_framework()
if 'evidence' not in st.session_state: st.session_state.evidence=[]
if 'results' not in st.session_state: st.session_state.results={}
if 'validated' not in st.session_state: st.session_state.validated={}

st.sidebar.markdown("<div class='brand'><div class='brand-mark'>◢</div><div class='brand-name'>ASCENDENCY</div><div class='brand-sub'>INTELLIGENCE</div></div>",unsafe_allow_html=True)
page=st.sidebar.radio('Navigation',['Dashboard','Assessments','Evidence Library','AI Analysis','Executive Reports'],label_visibility='collapsed')
st.sidebar.markdown('---')
st.sidebar.markdown("<span class='pill'>MVP v0.2</span><br><br><small style='color:#718197'>Governed AI · Human validated<br>Enterprise intelligence</small>",unsafe_allow_html=True)

criteria=[(d,c) for d in F['domains'] for c in d['criteria']]
def result_rows():
    rows=[]
    for d,c in criteria:
        r=st.session_state.validated.get(c['id']) or st.session_state.results.get(c['id'])
        rows.append({'Domain':d['name'],'Criterion':c['title'],'Score':r.get('score') if r else None,'Status':r.get('status','Not assessed') if r else 'Not assessed','Validated':c['id'] in st.session_state.validated})
    return rows

def hero(title,subtitle):
    st.markdown(f"<div class='hero'><div class='eyebrow'>Enterprise Governance Intelligence</div><h1>{title}</h1><p>{subtitle}</p></div>",unsafe_allow_html=True)

def card(label,value,note=''):
    return f"<div class='kpi'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div><div class='kpi-note'>{note}</div></div>"

if page=='Dashboard':
    hero("From insight to <span class='gold'>impact.</span>","A governed intelligence layer turning enterprise evidence into traceable maturity decisions, priority gaps and executive action.")
    rows=result_rows(); done=[r for r in rows if r['Score']]; avg=sum(r['Score'] for r in done)/len(done) if done else 0; gaps=sum(1 for r in done if r['Score']<3)
    a,b,c,d=st.columns(4)
    a.markdown(card('Overall Maturity',f'{avg:.1f} / 5','Current validated enterprise maturity'),unsafe_allow_html=True)
    b.markdown(card('Evidence Library',str(len(st.session_state.evidence)),'Documents available for analysis'),unsafe_allow_html=True)
    c.markdown(card('Priority Gaps',str(gaps),'Criteria requiring management attention'),unsafe_allow_html=True)
    d.markdown(card('Human Validated',str(sum(r['Validated'] for r in rows)),'AI decisions reviewed by experts'),unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    left,right=st.columns([1.75,1])
    with left:
        st.markdown("<div class='section-title'>Maturity by Domain</div><div class='section-sub'>Current evidence-grounded maturity across assessment domains</div>",unsafe_allow_html=True)
        df=pd.DataFrame(done)
        if not df.empty: st.bar_chart(df.groupby('Domain')['Score'].mean(),height=310)
        else: st.info('Upload evidence and run an AI assessment to activate enterprise intelligence.')
    with right:
        st.markdown("<div class='section-title'>Assessment Progress</div><div class='section-sub'>Governed assessment lifecycle</div>",unsafe_allow_html=True)
        pct=int(100*len(done)/len(rows)) if rows else 0
        st.metric('Overall completion',f'{pct}%'); st.progress(pct/100)
        st.markdown("<div class='priority'><div class='priority-num'>✓</div><div><div class='priority-text'>Framework Setup</div><div class='priority-meta'>Assessment structure ready</div></div></div><div class='priority'><div class='priority-num'>2</div><div><div class='priority-text'>Evidence Collection</div><div class='priority-meta'>Upload policies, procedures and reports</div></div></div><div class='priority'><div class='priority-num'>3</div><div><div class='priority-text'>AI Analysis & Validation</div><div class='priority-meta'>Evidence-grounded human-in-the-loop review</div></div></div>",unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Assessment Portfolio</div><div class='section-sub'>Traceable status across all criteria</div>",unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

elif page=='Assessments':
    hero("Assessment <span class='gold'>workspace.</span>","Configure the organization, inspect the enterprise maturity framework and manage assessment scope.")
    c1,c2=st.columns(2); c1.text_input('Organization','Demo Organization'); c2.text_input('Assessment','Digital Transformation Maturity Assessment 2026')
    st.markdown("<span class='pill'>1 Initial</span><span class='pill'>2 Under Development</span><span class='pill'>3 Established</span><span class='pill'>4 Managed</span><span class='pill'>5 Optimized</span>",unsafe_allow_html=True)
    for d in F['domains']:
        with st.expander(f"◆  {d['name']}  ·  {len(d['criteria'])} criteria",expanded=False):
            for c in d['criteria']: st.markdown(f"**{c['title']}**  \n{c['question']}")

elif page=='Evidence Library':
    hero("Evidence <span class='gold'>library.</span>","Build a governed evidence base for policies, procedures, reports and operational proof.")
    files=st.file_uploader('Drop enterprise evidence here',type=['pdf','docx','txt','md'],accept_multiple_files=True)
    if st.button('Ingest evidence',type='primary') and files:
        existing={e['name'] for e in st.session_state.evidence}
        for f in files:
            if f.name not in existing: st.session_state.evidence.append({'name':f.name,'text':extract_text(f)})
        st.success(f'{len(files)} file(s) processed and indexed for assessment.')
    if not st.session_state.evidence: st.info('No evidence has been ingested yet. Add documents to begin evidence-grounded analysis.')
    for e in st.session_state.evidence:
        with st.expander(f"◫  {e['name']}"): st.write(e['text'][:4000] or 'No extractable text.')

elif page=='AI Analysis':
    hero("AI assessment & <span class='gold'>human validation.</span>","Ascendency analyzes only the supplied evidence. Every AI recommendation remains subject to expert review and approval.")
    labels={f"{d['name']} — {c['title']}":(d,c) for d,c in criteria}; choice=st.selectbox('Assessment criterion',list(labels)); d,c=labels[choice]; st.info(c['question'])
    if st.button('Run evidence-grounded assessment',type='primary'):
        with st.spinner('Reasoning across governed evidence...'): st.session_state.results[c['id']]=ai_assess(c['question'],st.session_state.evidence)
    r=st.session_state.results.get(c['id'])
    if r:
        a,b,cx=st.columns(3); a.metric('AI Maturity',f"{r['score']} / 5"); b.metric('Evidence Status',r['status']); cx.metric('Confidence',f"{100*r.get('confidence',0):.0f}%")
        st.markdown('### Assessment rationale'); st.write(r['rationale']); st.markdown('### Evidence provenance')
        for q in r.get('citations',[]): st.markdown(f"**{q['source']}**\n\n> {q['quote']}")
        st.markdown('### Human validation'); score=st.slider('Validated maturity score',1,5,int(r['score'])); options=['Supported','Partial','Missing','Requires Review']; status=st.selectbox('Validated evidence status',options,index=options.index(r['status']) if r['status'] in options else 3); note=st.text_area('Reviewer note',placeholder='Document expert rationale, exceptions or required remediation...')
        if st.button('Approve & record validation'):
            st.session_state.validated[c['id']]={**r,'score':score,'status':status,'reviewer_note':note}; st.success('Human-validated decision recorded.')

elif page=='Executive Reports':
    hero("Executive <span class='gold'>intelligence.</span>","Translate validated assessment evidence into management visibility, priority gaps and an actionable transformation narrative.")
    rows=result_rows(); done=[r for r in rows if r['Score']]
    if not done: st.warning('Complete at least one assessment criterion to generate executive intelligence.')
    else:
        df=pd.DataFrame(done); avg=df['Score'].mean(); gaps=df[df['Score']<3].sort_values('Score')
        a,b,c=st.columns(3); a.metric('Overall Maturity',f'{avg:.2f} / 5'); b.metric('Assessed Criteria',len(done)); c.metric('Priority Gaps',len(gaps))
        st.markdown('### Domain maturity'); st.bar_chart(df.groupby('Domain')['Score'].mean(),height=300); st.markdown('### Management priorities'); st.dataframe(gaps,use_container_width=True,hide_index=True)
        report=f"ASCENDENCY INTELLIGENCE — EXECUTIVE ASSESSMENT\nOrganization: Demo Organization\nOverall maturity: {avg:.2f}/5\n\n"+df.to_string(index=False)+"\n\nGovernance note: AI-assisted findings require human validation before management reliance."
        st.download_button('Download Executive Report',report,'ascendency_executive_report.txt','text/plain')
