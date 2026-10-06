from datetime import datetime,date,timedelta
import httpx
from app.core import Tender
URL='https://ezamowienia.gov.pl/mo-board/api/v1/notice'
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
def pick(x,*ks):
 for k in ks:
  if isinstance(x,dict) and x.get(k) not in (None,''):return x[k]
 return ''
async def fetch(countries=None,limit=200):
 attempts=[{}, {'page':0,'size':100},{'publicationDateFrom':(date.today()-timedelta(days=7)).isoformat(),'publicationDateTo':date.today().isoformat()}];last=''
 async with httpx.AsyncClient(timeout=45,follow_redirects=True,headers={'Accept':'application/json','User-Agent':'CEE-Tender-Intelligence/0.8.1'}) as c:
  for params in attempts:
   r=await c.get(URL,params=params)
   if r.status_code==200:break
   last=f'HTTP {r.status_code}: {r.text[:1000]}'
  else:raise RuntimeError('BZP API: '+last)
 body=r.json();rows=body if isinstance(body,list) else body.get('items') or body.get('data') or body.get('results') or body.get('content') or [];out=[]
 for x in rows[:limit]:
  rid=str(pick(x,'noticeNumber','noticeId','id','bzpNumber'));buyer=pick(x,'organizationName','contractingAuthorityName','buyerName','organization');buyer=pick(buyer,'name','organizationName') if isinstance(buyer,dict) else buyer;url=str(pick(x,'noticeUrl','url')) or f'https://ezamowienia.gov.pl/mo-client-board/bzp/notice-details/{rid}'
  out.append(Tender('pl:'+rid,'poland','POL',str(pick(x,'orderObject','title','noticeTitle','objectName') or rid),str(buyer),None,'PLN',dt(pick(x,'submissionDeadline','deadline')),str(pick(x,'noticeStatus','status') or 'active'),url,description=str(pick(x,'description','shortDescription')),procurement_id=rid))
 return out
