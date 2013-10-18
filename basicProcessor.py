# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:09:12 2013

@author: ep
"""

import pickle

data = []

D={}
tns = ['N','author','nsales','ncomments','prices','licenses','min_price','name','categories','kws']
for tn in tns:
  D[tn]=[]

f = open('main_results_copy.txt','r')
lines = f.readlines()
f.close()

SEP = '%%%%';

for line in lines:
  arr = line.split(SEP)  
  data.append(arr)
  
  D['N'].append(int(arr[0]))
  D['author'].append(arr[1])
  D['name'].append(arr[4])
  D['nsales'].append(int(arr[2]))
  D['ncomments'].append(int(arr[3]))
  tprices = map(int,arr[5].split(','))
  D['prices'].append(tprices)
  D['min_price'].append(min(tprices))
  D['licenses'].append(arr[6].split(','))
  D['categories'].append(arr[7].split('>'))
  D['kws'].append(arr[8].split(','))
  
with open('res_arraythingy.txt','w') as f:  
  pickle.dump(data,f)  

with open('res_Dthingy.txt','w') as f:
  pickle.dump(D,f)