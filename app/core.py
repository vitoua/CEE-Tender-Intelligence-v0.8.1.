from dataclasses import dataclass,field
from datetime import datetime
from collections import defaultdict
@dataclass
class Tender:
 id:str;source:str;country:str;title:str;buyer:str='';value:float|None=None;currency:str='';deadline:datetime|None=None;status:str='active';url:str='';winner:str='';award_value:float|None=None;award_date:datetime|None=None;description:str='';procurement_id:str='';sources:list[str]=field(default_factory=list);duplicate_sources:list[str]=field(default_factory=list);source_links:dict[str,str]=field(default_factory=dict)
class Store:
 def __init__(self):self.data={};self.runs=[]
 def add(self,s,rows):
  from app.dedupe import duplicate,merge
  added=dupes=0
  for x in rows:
   x.sources=x.sources or [x.source];x.source_links=x.source_links or ({x.source:x.url} if x.url else {});hit=None
   for k,y in self.data.items():
    if duplicate(y,x)[0]:hit=k;break
   if hit is None:self.data[x.id]=x;added+=1
   else:self.data[hit]=merge(self.data[hit],x);dupes+=1
  self.runs.insert(0,{'source':s,'status':'ok','count':len(rows),'added':added,'duplicates':dupes,'error':''})
 def error(self,s,e):self.runs.insert(0,{'source':s,'status':'error','count':0,'added':0,'duplicates':0,'error':str(e)})
 def countries(self):return sorted({x.country for x in self.data.values() if x.country})
store=Store()
def active(x):return (x.status or '').lower() not in {'complete','completed','awarded','cancelled','canceled','closed'} and (not x.deadline or x.deadline>=datetime.utcnow())
def analytics(rows):
 g=defaultdict(lambda:{'wins':0,'total':0.0})
 for x in rows:
  if x.winner:g[x.winner]['wins']+=1;g[x.winner]['total']+=x.award_value if x.award_value is not None else (x.value or 0)
 total=sum(v['total'] for v in g.values());return [{'winner':k,**v,'share':v['total']/total*100 if total else 0} for k,v in g.items()]
