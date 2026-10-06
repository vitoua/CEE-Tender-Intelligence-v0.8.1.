from app.i18n import T
from app.core import Tender,Store
from datetime import datetime
def test_languages():assert set(T)=={'uk','pl','en','es'} and all(set(v)==set(T['en']) for v in T.values())
def test_links():
 s=Store();a=Tender('a','ted','DEU','SSD','B',1,'EUR',datetime(2026,12,1),url='https://a');b=Tender('b','germany','DEU','SSD','B',1,'EUR',datetime(2026,12,1),url='https://b');s.add('ted',[a]);s.add('germany',[b]);assert len(next(iter(s.data.values())).source_links)==2
