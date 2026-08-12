
import re
from difflib import SequenceMatcher

def normalize(t):
    t=re.sub(r"[^a-z0-9'\s]","",t.lower().strip())
    return re.sub(r"\s+"," ",t)

def score_transcript(target,heard):
    a,b=normalize(target),normalize(heard)
    score=round(SequenceMatcher(None,a,b).ratio()*100) if a else 0
    aw,bw=a.split(),b.split()
    missing=[w for w in aw if not any(SequenceMatcher(None,w,x).ratio()>=0.78 for x in bw)]
    return score,missing
