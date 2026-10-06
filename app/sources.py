COUNTRIES={'DEU':'Germany','ESP':'Spain','FRA':'France','ITA':'Italy','POL':'Poland','UKR':'Ukraine','CZE':'Czechia','SVK':'Slovakia','ROU':'Romania','LTU':'Lithuania','LVA':'Latvia','EST':'Estonia','SVN':'Slovenia','AUT':'Austria','BEL':'Belgium','BGR':'Bulgaria','HRV':'Croatia','HUN':'Hungary','NLD':'Netherlands','PRT':'Portugal','SWE':'Sweden'}
def sources_for(c):
 c=set(c);o=[];eu=sorted(c-{'UKR'});o+= [('ted',eu)] if eu else [];o += [('prozorro',['UKR'])] if 'UKR' in c else [];o += [('germany',['DEU'])] if 'DEU' in c else [];o += [('poland',['POL'])] if 'POL' in c else [];return o
