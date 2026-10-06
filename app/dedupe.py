import hashlib,re,unicodedata
def norm(v):return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',str(v or '')).encode('ascii','ignore').decode().lower()).strip()
def ids(t):
 text=' '.join([t.id,t.procurement_id,t.url,t.title,t.description]);out=set()
 for p in [r'\b\d{6}-\d{4}\b',r'\bocds-[a-z0-9-]+\b',r'\bua-\d{4}-\d{2}-\d{2}-[a-z0-9-]+\b']:out.update(re.findall(p,text.lower()))
 return out
def fp(t):return hashlib.sha256('|'.join([t.country,norm(t.buyer),norm(t.title)[:180],t.deadline.date().isoformat() if t.deadline else '',str(round(t.value or 0,2)),t.currency]).encode()).hexdigest()
def duplicate(a,b):
 if ids(a)&ids(b):return True,'id'
 if fp(a)==fp(b):return True,'fingerprint'
 if a.country!=b.country:return False,''
 A=set(norm(a.title).split());B=set(norm(b.title).split());sim=len(A&B)/max(1,len(A|B));ok=sim>=.86 and norm(a.buyer)==norm(b.buyer) and (not a.deadline or not b.deadline or abs((a.deadline-b.deadline).days)<=2) and (not a.value or not b.value or abs(a.value-b.value)<=max(1,.01*max(a.value,b.value)))
 return ok,'fuzzy' if ok else ''
def merge(a,b):
 p=b if b.source!='ted' and a.source=='ted' else a;p.sources=sorted(set(a.sources or [a.source])|set(b.sources or [b.source]));p.duplicate_sources=[x for x in p.sources if x!=p.source];p.source_links={**(a.source_links or {a.source:a.url}),**(b.source_links or {b.source:b.url})};return p
