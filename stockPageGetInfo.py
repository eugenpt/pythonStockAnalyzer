# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 13:11:38 2013

@author: ep
"""

#from BeautifulSoup import BeautifulSoup
import lxml.html

def getItemInfo(content):
  
  result={}
  doSoup=0 # lxml vs soup : 0.012s vs 0.87
  if(doSoup):
    pass
  else:
    doc = lxml.html.document_fromstring(content)
    
    result['name'] = doc.xpath('//*[@class="page-title"]/text()')[0].strip()
    result['author'] = doc.xpath('//*[@rel="author"]/text()')[0]
    result['nop'] = doc.xpath('//*[@class="sidebar-stats__box--sales"]/div/span/text()')[0]
    result['date'] = doc.xpath('//*[@class="attr-detail"]/text()')[0]
    result['kws'] = ','.join(doc.xpath('//ul[@itemprop="keywords"]//a/text()'))
    
    license_types = doc.xpath('//span[@class="price_in_dollars"]/@data-license')
    prices = doc.xpath('//span[@class="price_in_dollars"]/text()')
    #print(prices)
    
    if(prices and len(prices)>0):
      price = int(prices[0])
      lic = license_types[0]
      for j in range(0,len(prices)):
        if(int(prices[j])<price):
          price=int(prices[j])
          lic=license_types[j]
    else:
      price=-1
    #result['prices'] = prices    
    result['price'] = price
    result['lic_type'] = lic
        
  return result
  
#url='http://codecanyon.net/item/android-live-tv/5199544'
#url='http://audiojungle.net/item/cant-stop-moving/5693847'
#url='http://activeden.net/item/blue-flat-skin-for-jw6/5674180'
#url='http://videohive.net/item/bicycle-package-4/5683900'
#url='http://photodune.net/item/wooden-surface/3580063'
#url='http://3docean.net/item/chess/5706294'
#url='http://themeforest.net/item/lens-an-enjoyable-photography-wordpress-theme/5713452'
#url='http://graphicriver.net/item/seamless-hot-air-balloon-pattern/4597556'
#debug = 1
#import requests
#import re
#import time
#if(debug):
#  print('getting page..')
#  S = time.time()
#  R = requests.get(url,proxies={'http':'http://162.220.12.148:7808'})
#  ts = R.content
#  
#  
#  
#  print('page got in '+str(time.time()-S)+"s")
#  print('working..')
#  S = time.time()
#  res=getItemInfo(ts)
#  print('donein '+str(time.time()-S)+"s")
