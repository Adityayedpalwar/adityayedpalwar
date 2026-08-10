from __future__ import annotations
import json
from datetime import date,timedelta
from pathlib import Path
p=json.loads(Path("data/contributions.json").read_text(encoding="utf-8")); days,stats=p["days"],p["stats"]
pal=["#161b22","#0e4429","#006d32","#26a641","#39d353","#69f0a0"]
today=date.today(); start=today-timedelta(days=364); start-=timedelta(days=(start.weekday()+1)%7)
cells=[]
for w in range(53):
    for d in range(7):
        dt=start+timedelta(days=w*7+d); level=max(0,min(5,int(days.get(dt.isoformat(),0))))
        x,y=34+w*16,58+d*16
        cells.append('<rect x="%d" y="%d" width="12" height="12" rx="3" fill="%s" class="cell" style="animation-delay:%.3fs"><title>%s · level %d</title></rect>'%(x,y,pal[level],(w+d)*.018,dt.isoformat(),level))
legend=''.join('<rect x="%d" y="176" width="12" height="12" rx="3" fill="%s"/>'%(69+i*18,c) for i,c in enumerate(pal))
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="740" height="245" viewBox="0 0 740 245"><style>@keyframes reveal { from { opacity:0; transform:translateY(-5px); } to { opacity:1; transform:translateY(0); } } .cell { opacity:0; animation:reveal .34s ease-out forwards; }</style><rect width="100%" height="100%" rx="18" fill="#0b0a0f"/><rect x="1" y="1" width="738" height="243" rx="17" fill="none" stroke="#302a3b"/><text x="22" y="28" fill="#b88cff" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14">contributions</text><text x="718" y="28" text-anchor="end" fill="#777080" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11">%s · live</text>%s<text x="34" y="185" fill="#777080" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">Less</text>%s<text x="177" y="185" fill="#777080" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">More</text><text x="22" y="218" fill="#777080" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10">current: %dd · longest: %dd · active days: %d</text></svg>'''%(p["username"],''.join(cells),legend,stats["current_streak"],stats["longest_streak"],stats["active_days"])
Path("contrib-heatmap.svg").write_text(svg,encoding="utf-8")
