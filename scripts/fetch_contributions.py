from __future__ import annotations
import json, os
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup
USERNAME=os.getenv("GITHUB_USERNAME","adityayedpalwar")
OUT=Path("data/contributions.json")
URL=f"https://github.com/users/{USERNAME}/contributions"
r=requests.get(URL,headers={"User-Agent":"github-profile-art/1.0"},timeout=30)
r.raise_for_status()
soup=BeautifulSoup(r.text,"html.parser")
days={}
for cell in soup.select("[data-date]"):
    d=cell.get("data-date")
    if d:
        try: days[d]=int(cell.get("data-level","0"))
        except ValueError: pass
if len(days)<300: raise RuntimeError(f"Only parsed {len(days)} cells; GitHub markup may have changed.")
active=sorted(d for d,v in days.items() if int(v)>0); aset=set(active)
current=0; cursor=date.today()
while cursor.isoformat() in aset: current+=1; cursor-=timedelta(days=1)
longest=run=0; prev=None
for d in active:
    dt=date.fromisoformat(d); run=run+1 if prev and (dt-prev).days==1 else 1; longest=max(longest,run); prev=dt
monthly=defaultdict(int)
for d,v in days.items(): monthly[d[:7]]+=int(v)
best=max(days.items(),key=lambda x:int(x[1]),default=(None,0))
payload={"username":USERNAME,"source":URL,"days":days,"stats":{"current_streak":current,"longest_streak":longest,"best_day":{"date":best[0],"level":int(best[1])},"active_days":len(active),"monthly_level_totals":dict(monthly)}}
OUT.parent.mkdir(exist_ok=True); OUT.write_text(json.dumps(payload,indent=2),encoding="utf-8")
