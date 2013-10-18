# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 16:53:09 2013

@author: ep
"""

import urllib2
import re
import thread
import os.path

import Queue
from Queue import Queue
import threading
from threading import Thread

from BeautifulSoup import BeautifulSoup

import requests



ts = 's'

myDelim = '||||'

commonURL = 'http://graphicriver.net/item/a/'

tNumStart = 4597556 #Svetka's stuff
tNumStart = 5502614 #another Svetka's stuff
tNumStart = 3349990
tNumStart = 1

filename = './testfile.txt'
#filename = './tempfile.txt'

if(os.path.exists(filename)):
  f = open(filename,'r')
  for line in f:
    n1 = line.find(myDelim)
    n2 = line.find(myDelim,n1+1)
    if(n1>=0 and n2>=0):
      tN = int(line[(n1+len(myDelim)):(n2)])
      if(tNumStart<tN):
        tNumStart=tN
        print(tNumStart)
  f.close()

tNumStart=tNumStart+1  





tNumC = 1000000

tNumThreads = 300;


import time

start = time.time()
print "hello"

#busy = 0

qOut = Queue()
qURL = Queue()
qLog = Queue()

#f1=open('./testfile.txt', 'w+')

def testURL(threadName,proxie):
  while(1):
    if(qURL.empty()):
      print("No URLs")
      return
    if(os.path.exists('stop.txt')):
      print("stop file detected")
      return
    try:
      #print(threadName+" qURL size = "+str(qURL.qsize()))
      tNums = qURL.get()
      #qLog.put(tNums)
      url = commonURL+tNums
      #print(threadName+" "+url)
      print(threadName+" t "+tNums)
      R = R=requests.get(url)
      #print(threadName+" g "+tNums)
      #print(R.geturl())
      #print(threadName+" "+R.geturl())
      t = re.search("http:..([^/]+)/",R.geturl())
      domain = t.groups()[0] 
      if(domain!="graphicriver.net"):
        #print(threadName+" m "+tNums)
        #print("Not graphicriver")
        continue
      
      soup = BeautifulSoup(R.content())   
      
      author = soup.find('a',{'rel':'author'}).getText()    
      
      name = soup.find('h1',{'class':'page-title'}).getText()
      
      priceTemp = soup.findAll('span',{'class':"price_in_dollars"})
      license_type = ''
      if(len(priceTemp)>0):
        price=1000;
        for tag in priceTemp:
          temp = int(tag.getText());
          if(temp<price):
            price=temp
            license_type = tag.attrMap['data-license']
          else:
            pass
      else:
        price = -1
      
      #print("bbb")
      numOfPurchases = int(soup.findAll('div',{'class':"sidebar-stats__box--sales"})[0].div.span.getText())
  
      dateCreated = soup.find('td',{'class':'attr-detail'}).getText()
      
      keywords = ''
      kTag = soup.find('ul',{'itemprop':'keywords'})
      if(kTag):
        for tag in kTag.findAll('a'):
          keywords = keywords+tag.getText()+','
      
      #print(threadName+" N="+threadName+" a="+author+" n="+name)
      qOut.put(threadName+myDelim+tNums+myDelim+author+myDelim+name+myDelim+str(price)+myDelim+license_type+myDelim+str(numOfPurchases)+myDelim+dateCreated+myDelim+keywords+"\n")    
      #print(threadName+" r "+tNums)
    except Exception:
      #print(threadName+" ng "+tNums)
      pass

def writeResults():
  tempTime = time.time();
  count=0;
  while(1):
    #print("qURL size = "+str(qURL.qsize()))
    while(qOut.empty()):
      print("qOut is empty")
      if(qURL.empty()):
        print("qURL is empty!")
        return
      if(os.path.exists('stop.txt')):
        print("stop file detected")
        return
      time.sleep(1) 
    #count=count+1
    #if(time.time()-tempTime > 2):
    #  print("Done "+str(count/(time.time()-tempTime))+" cps")
    #  tempTime = time.time()
    f1=open(filename, 'a')
    while(qOut.empty()==False):
      ts=qOut.get()
      f1.write(ts)
    f1.close()
    #f2=open('E:\EP\Stuff\Git\pythonStockAnalyzer\log.txt','a')
    #while(qLog.empty()==False):
    #  tDone = qLog.get()
    #  f2.write(tDone+"\n")
    #f2.close()  
    



for tNum in range(tNumStart,tNumStart+tNumC):
  qURL.put(str(tNum))  
  
print("qURL size = "+str(qURL.qsize()))  

T = [ Thread(target=testURL,args=[str(i),]) for i in range(0,tNumThreads)]
for j in range(0,tNumThreads):
  T[j].daemon = True
  T[j].start()

Tr=Thread(target=writeResults)
Tr.daemon = True
Tr.start()  
  
for j in range(0,tNumThreads):
  T[j].join()
Tr.join()

  
    #print("Exception, assuming 404 not found")
end=time.time()

print("Time total: "+str(end - start)+"s")
print("Count per second: "+str(tNumC*1.0/(end-start)))

print("All ended")