from core.engine import load_framework, heuristic_assess
def test_framework():
    f=load_framework(); assert len(f['domains'])==4; assert len(f['maturity_levels'])==5
def test_missing():
    r=heuristic_assess('Are policies documented?',[]); assert r['score']==1 and r['status']=='Missing'
