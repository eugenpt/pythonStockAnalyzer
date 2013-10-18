# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 22:28:31 2013

@author: ep
"""

from mechanize import Browser
import lxml.html
import time
import requests
from random import randint
from Queue import Queue
from threading import Thread


pageQ = Queue()
for j in range(5185):
  pageQ.put(j)

pageDoneQ = Queue()

urlsQ = Queue()


def urlwriterFun():
  while(pageQ.empty()==False):
    if(urlsQ.empty()==False):
      f=open('graphicriverUrls.txt','a')
      while(urlsQ.empty()==False):
        f.write(urlsQ.get()+"\n")
      f.close()    

Reader = Thread(target = urlwriterFun)
Reader.setDaemon(True)
Reader.start()

def testPx(px):
  B=Browser()
  B.addheaders = [('User-agent', userAgents[randint(0,len(userAgents)-1)])]
  B.set_proxies(px)
  try:
    B.open('http://graphicriver.net/',timeout=5)
    pxQ.put(px)
    print(px['http']+"  ok")
    
    B.open('http://graphicriver.net/category/all',timeout=5)
  except:
    print(px['http']+"  error")
  page = pageQ.get()
  try:  
#    pass
#  finally:
    count=0
    while(count<5):
      O = B.open('http://graphicriver.net/category/all?page='+str(page),timeout=8)
      turls = lxml.html.document_fromstring(O.get_data()).xpath('//div[@class="item-info"]/h3/a/@href')
      for url in turls:
        urlsQ.put(url)
      print(str(page)+" got")  
      pageDoneQ.put(page)
      page = pageQ.get()
      count+=1
  except:  
    pageQ.put(page)
    print(str(page)+" error")
    #count_ok+=1
    #count_error+=1


while(pageQ.empty()==False):
  
  print('Getting proxy list..')
  R = requests.get('http://free-proxy-list.net/')
  doc =  lxml.html.document_fromstring(R.content)
  proxy_ips = doc.xpath('//tbody/tr/td[1]/text()')
  proxy_ports = doc.xpath('//tbody/tr/td[2]/text()')
  proxys = []
  
  for j in range(len(proxy_ips)):
    proxys.append({'http':'http://'+proxy_ips[j]+":"+proxy_ports[j]})
    
  print('done')  
  #print(proxys)
  
  print('Getting useragent list..')
  R = requests.get('http://adversari.es/assets/useragentlist.txt')
  userAgents = R.content.splitlines()
  print('done')
  
  count_error=0
  count_ok=0
  
  pxQ = Queue()
  
  
  
  
   
  
  print('testing proxies..') 
  Ths=[Thread(target=testPx,args=(px,)) for px in proxys]  
  
  for T in Ths:
    T.setDaemon(True)
    T.start()
  
  
  
  for T in Ths:
    T.join()
    
  #Reader.join()  
  print('done')  
    
  validProxies = []  
  while(pxQ.empty()==False):
    validProxies.append( pxQ.get())
    count_ok+=1
  
  
  count_error = len(proxys)-count_ok
  print("ok:"+str(count_ok))
  print("error:"+str(count_error))    
  
  pagesCount = 0;
  while(pageDoneQ.empty()==False):
    pagesCount+=1
    pageDoneQ.get()
  print("pages done: "+str(pagesCount))  
    
  #B = Browser;
