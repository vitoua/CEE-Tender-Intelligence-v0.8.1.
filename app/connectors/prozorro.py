from datetime import datetime
import httpx
from app.core import Tender
BASE='https://public-api.prozorro.gov.ua/api/2.5/tenders'
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
async def fetch(countries=None,limit=200):
 out=[]
 async with httpx.AsyncClient(timeout=45,follow_redirects=True) as c:
  feed=await c.get(BASE,params={'limit':limit,'descending':1});feed.raise_for_status()
  for row in feed.json().get('data',[]):
   r=await c.get(f"{BASE}/{row['id']}");r.raise_for_status();x=r.json().get('data',{});tid=x.get('tenderID',row['id']);v=x.get('value') or {};p=x.get('tenderPeriod') or {};a=next((a for a in x.get('awards',[]) if a.get('status')=='active'),{});sup=(a.get('suppliers') or [{}])[0]
   out.append(Tender('prozorro:'+tid,'prozorro','UKR',x.get('title') or tid,(x.get('procuringEntity') or {}).get('name',''),v.get('amount'),v.get('currency',''),dt(p.get('endDate')),x.get('status',''),f'https://prozorro.gov.ua/tender/{tid}',sup.get('name',''),(a.get('value') or {}).get('amount'),dt(a.get('date')),x.get('description',''),tid))
 return out
