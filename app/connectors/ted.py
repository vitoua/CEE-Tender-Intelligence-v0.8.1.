from datetime import datetime
import httpx
from app.core import Tender
URL='https://api.ted.europa.eu/v3/notices/search'
def first(v):
 if isinstance(v,dict):return first(next(iter(v.values()),''))
 if isinstance(v,list):return first(v[0]) if v else ''
 return str(v or '')
def dt(v):
 try:return datetime.fromisoformat(first(v)[:10])
 except:return None
async def fetch(countries=None,limit=200):
 fields=['publication-number','notice-title','buyer-name','buyer-country','total-value','total-value-cur','deadline','description-proc'];payload={'query':'FT~"SSD" OR FT~"NVMe" OR FT~"DDR4" OR FT~"DDR5" OR FT~"memory card"','fields':fields,'page':1,'limit':limit,'scope':'ALL','paginationMode':'PAGE_NUMBER','onlyLatestVersions':True}
 async with httpx.AsyncClient(timeout=45) as c:r=await c.post(URL,json=payload);r.raise_for_status();rows=r.json().get('notices',[])
 out=[]
 for x in rows:
  co=first(x.get('buyer-country'))[:3] or 'EU'
  if countries and co not in countries:continue
  n=first(x.get('publication-number'));url=f'https://ted.europa.eu/en/notice/-/detail/{n}';out.append(Tender('ted:'+n,'ted',co,first(x.get('notice-title')) or n,first(x.get('buyer-name')),None,first(x.get('total-value-cur')),dt(x.get('deadline')),'active',url,description=first(x.get('description-proc')),procurement_id=n))
 return out
