import io,json,zipfile
from datetime import date,datetime,timedelta
import httpx
from app.core import Tender
URL='https://oeffentlichevergabe.de/api/notice-exports'
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
async def fetch(countries=None,days=3):
 out=[]
 async with httpx.AsyncClient(timeout=60,follow_redirects=True) as c:
  for n in range(1,days+1):
   day=(date.today()-timedelta(days=n)).isoformat();r=await c.get(URL,params={'pubDay':day,'format':'ocds.zip'})
   if r.status_code in (400,404):continue
   r.raise_for_status()
   with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    for fn in z.namelist():
     rel=(json.loads(z.read(fn)).get('releases') or [{}])[0];t=rel.get('tender') or {};ps=rel.get('parties') or [];buyer=next((p.get('name','') for p in ps if 'buyer' in p.get('roles',[])),'');supplier=next((p.get('name','') for p in ps if 'supplier' in p.get('roles',[])),'');v=t.get('value') or {};ocid=rel.get('ocid') or rel.get('id') or fn;url=f'https://oeffentlichevergabe.de/ui/de/notices/{ocid}'
     out.append(Tender('de:'+ocid,'germany','DEU',t.get('title') or ocid,buyer,v.get('amount'),v.get('currency','EUR'),dt((t.get('tenderPeriod') or {}).get('endDate')),t.get('status','active'),url,supplier,None,dt(rel.get('date')),t.get('description',''),ocid))
 return out
