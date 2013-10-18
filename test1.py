# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 16:53:09 2013

@author: ep
"""

import urllib2
import re
import thread
import os.path

# from __future__ import print_function

from BeautifulSoup import BeautifulSoup

ts = 's'

commonURL = 'http://graphicriver.net/item/a/'

tNumStart = 4597556 #Svetka's stuff
tNumStart = 5502614 #another Svetka's stuff
tNumStart = 3349990
tNumStart = 1
tNumC = 1000000

tNumThreads = 100;

filename = './testfile.txt'

import time

start = time.time()
print "hello"

#busy = 0

f1=open('./testfile.txt', 'w+')

def testURL(threadName,url):
  try:
    R = urllib2.urlopen(url)
    #print(R.geturl())
    t = re.search("http:..([^/]+)/",R.geturl())
    domain = t.groups()[0] 
    if(domain!="graphicriver.net"):
      return
    
    soup = BeautifulSoup(R.read())   
    
    author = soup.findAll('a',{'rel':'author'})[0].getText()    
    
    name = soup.findAll('h1',{'class':'page-title'})[0].getText()
    
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
    
    numOfPurchases = int(soup.findAll('div',{'class':"sidebar-stats__box--sales"})[0].div.span.getText())
    
    #while(busy):
    #  pass
    
    #busy = 1  
    if(os.path.exists(filename)):
      f1=open(filename, 'a')
    else:
      f1=open(filename, 'w+')
    f1.write( threadName+"|"+author+"|"+name+"|"+str(price)+"|"+license_type+"|"+str(numOfPurchases)+"\n")
    f1.close()
    
    print(threadName+" N="+threadName)
    print(threadName+" domain: "+domain)
    print(threadName+" author: "+author)
    print(threadName+" name of the piece: "+name)
    print(threadName+" min price: "+str(price))
    print(threadName+" min price license type: "+license_type)
    print(threadName+" number of purchases: "+str(numOfPurchases))
    #busy=0
    
    
  except Exception:
    pass
  
tempN = tNumStart
while(tempN<tNumStart+tNumC):
  for tNum in range(tempN,tempN+tNumThreads):
    thread.start_new_thread(testURL,(""+str(tNum),commonURL+str(tNum),))  
  tempN=tempN+tNumThreads
  time.sleep(2)
  
    #print("Exception, assuming 404 not found")
end = time.time()
print(end - start)
print((end-start)/tNumC)