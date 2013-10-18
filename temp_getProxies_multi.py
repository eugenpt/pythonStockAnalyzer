# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:06:04 2013

@author: ep
"""

import requests
from BeautifulSoup import BeautifulSoup
import lxml.html
import re
import time
from Queue import Queue
from threading import Thread
from random import randint


# only anonimous
pUrl='http://proxy-list.org/ru/index.php?pp=any&pt=2&pc=any&ps=any#proxylist'

#any proxies
pUrl='http://proxy-list.org/ru/index.php?pp=any&pt=any&pc=any&ps=any#proxylist'

pUrls = ['http://proxy-list.org/ru/index.php',
         'http://proxy-list.org/ru/index.php?sp=20',
         'http://proxy-list.org/ru/index.php?sp=40',
         'http://proxy-list.org/ru/index.php?sp=60',
         'http://proxy-list.org/ru/index.php?sp=80',
         'http://proxy-list.org/ru/index.php?sp=100']
         
myDomains = ['graphicriver','activeden','audiojungle','themeforest',
             'videohive','3docean','codecanyon','photodune']
             
testUrls = ['http://'+domain+'.net/' for domain in myDomains]             
         
pxsToTestQ = Queue()
            
  
def getProxiesListFromDB(url):
  print("queueing "+url)
  R = requests.get(url)
  doSoup=0
  if(doSoup):
    soup = BeautifulSoup(R.content)
    table = soup.find('table',{'width':'488'})
    rows = table.findAll('tr')
    for j in range(1,len(rows)):
      pxsToTestQ.put({'http':'http://'+rows[j].find('td').getText()})
  else:
    doc = lxml.html.document_fromstring(R.content)
    for addr in doc.xpath('//table[@width="488"]//tr/td[1]/text()'):
      pxsToTestQ.put({'http':'http://'+addr})
#S=time.time()
workPxsQ= Queue()

def testProxy(px):
  print("Testing: "+px['http'])  
  try:
    tempR = requests.get(testUrls[randint(0,len(testUrls))],proxies=px,timeout=2)
    workPxsQ.put(px)
    print("OK  time: "+str(tempR.elapsed.total_seconds()))
  except:
    print("some error..")

def getValidProxies():
  Ths = [Thread(target = getProxiesListFromDB,args=(url,)) for url in pUrls] 

  for T in Ths:
    T.setDaemon(True)
    T.start()

  for T in Ths:
    T.join()


#print("Time elapsed: "+str(time.time()-S)+"s")
#print("Approximate count proxies to test: "+str(pxsToTestQ.qsize()))
  
  proxyListsUrls = ['http://newscatcher.ru/files/exe/unchecked.txt',
                    'http://www.hotels4all.org/Proxies.txt',
                    'http://webanet.ucoz.ru/proxy/proxylist_at_01.09.2013.txt']    
  for proxyListUrl in proxyListsUrls:
    try:
      print("quering "+proxyListUrl)
      R = requests.get(proxyListUrl)
      tpxs=R.content.splitlines()
      for px in tpxs:
        pxsToTestQ.put({'http':'http://'+px})
    except:
      print("some error..")
      pass

  Ths=[]
  
  while(pxsToTestQ.empty()==False):
    Ths.append(Thread(target=testProxy,args=(pxsToTestQ.get(),)))
    Ths[len(Ths)-1].setDaemon(True)
  
  for T in Ths:
    T.start()
  
  for T in Ths:
    T.join()


  res =[]  
    
  while(workPxsQ.empty()==False):
    temp = workPxsQ.get()
    res.append(temp)
    print("adding "+temp['http'])
    
  print("getValidProxies done")
  res.append({'http':'http://194.141.102.254:8080'})  
  res.append({'http':'http://219.143.228.155:1080'})  
  res.append({'http':'http://94.154.28.241:8090'})  
  
  return res  
