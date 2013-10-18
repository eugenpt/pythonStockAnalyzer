# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:06:04 2013

@author: ep
"""

import requests
from BeautifulSoup import BeautifulSoup
import re
import time

S=time.time()

# only anonimous
pUrl='http://proxy-list.org/ru/index.php?pp=any&pt=2&pc=any&ps=any#proxylist'

#any proxies
pUrl='http://proxy-list.org/ru/index.php?pp=any&pt=any&pc=any&ps=any#proxylist'

R = requests.get(pUrl)

soup = BeautifulSoup(R.content)

table = soup.find('table',{'width':'488'})

rows = table.findAll('tr')

pxs = [{'http':'http://'+rows[j].find('td').getText()} for j in range(1,len(rows))]

print("Time elapsed: "+str(time.time()-S)+"s")
  
workPxs = [];  
  
for j in range(0,len(pxs)):
  print("Testing: "+pxs[j]['http'])  
  try:
    tempR = requests.get('http://graphicriver.net',proxies=pxs[j],timeout=2)
    workPxs.append(pxs[j])
    print("time: "+str(tempR.elapsed.total_seconds()))
  except:
    print("some error..")

for j in range(0,len(workPxs)):
  print(workPxs[j]['http'])  

