# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 18:41:34 2013

@author: ep
"""
#set PYTHONIOENCODING=utf_8

from mechanize import Browser
import lxml.html
import time
import requests
from random import randint
import random
from Queue import Queue
from threading import Thread
import urllib2
import os
import re

print("Getting UserAgents..")
R = requests.get('http://adversari.es/assets/useragentlist.txt')
userAgents = R.content.splitlines()
print("done, found "+str(len(userAgents))+" user agents")

print("Getting starting pages..")

B = Browser()
B.addheaders = [('User-agent', userAgents[randint(0,len(userAgents)-1)])]
#B.set_proxies({'http':'http://5.187.2.148:3128'})
B.set_handle_robots( False )
B.open('http://www.google.com/')
R = B.open('http://graphicriver.net/')
L = B.find_link(text='All Items')

print('done')

#return
SEP = '%%%%';

pageN = 903

print('removing page and error file(s)')
for filename in os.listdir('.'):
  if((filename.startswith('page_')) or (filename.startswith('error'))):
    os.remove(filename)
    #break
print('done')  


if(pageN!=1):
  print('pageN = '+str(pageN)+', not 1, opening next page')  
  B.open('http://graphicriver.net/category/all?page='+str(pageN+1))
  L = B.find_link(text=str(pageN))
  print('done')
  
tf = open('page_'+str(pageN)+'.txt','w')
tf.close()
while(1):
  #O = B.open('http://graphicriver.net/category/all?page='+str(page),timeout=8)
  try:
    R2 = B.follow_link(L)
    turls = lxml.html.document_fromstring(R2.get_data()).xpath('//div[@class="item-info"]/h3/a/@href')
    print('found '+str(len(turls))+' urls')
    f=open('graphicriver_urls_3.txt','a')
    for url in turls:
      #print(url)
      f.write(url+'\n')
    f.close()  
    
    for url in turls:
      #print(url)
      Ns = re.findall('([0-9]+)\?',url)[0]
      print('trying to get '+Ns)
      try:
        R = B.open(url)
      except urllib2.HTTPError, err:
        if ((err.code == 404)):
          print('404')
          continue
        else:
          print('HTTP error while loading page, not 404')
          print('lowering pageN')
          os.rename('page_'+str(pageN)+'.txt','page_'+str(pageN-1)+'.txt')
          pageN = pageN-1;
          print('sleeping 10')
          time.sleep(10)
          print('restarting page')
          break
      except:
        print('Error, not HTTP')
        f=open('error_notHTTP_in_page.log','a')
        f.write('damn it, I have an error on page '+str(pageN)+" url#"+Ns)
        f.close()
        raise  
      #print('done')
      doc = lxml.html.document_fromstring(R.get_data())
      #print('Going back..')
      B.back()
      #print('done')
      categories='>'.join(doc.xpath('//span[@itemprop="genre"]/a/text()'))
      kws = ','.join(doc.xpath('//ul[@itemprop="keywords"]/li/a/text()'))
      author = doc.xpath('//a[@rel="author"]/text()')[0]
      nPurchases = re.findall(':([0-9]+)',doc.xpath('//meta[@itemprop="interactionCount"]/@content')[0])[0]
      nComments = doc.xpath('//div[@class="sidebar-stats__box--comments"]/div/a/span/text()')[0]
      name = doc.xpath('//h1[@itemprop="name"]/text()')[0].strip()
      lic_types=','.join(doc.xpath('//span[@class="price"]/span[@class="price_in_dollars"]/@data-license'))
      prices = ','.join(doc.xpath('//span[@class="price"]/span[@class="price_in_dollars"]/text()'))
      print('parsed all info, writing to file..')
      f=open('main_results.txt','a')
      f.write(Ns+SEP)
      f.write(author+SEP)
      f.write(nPurchases+SEP)
      f.write(nComments+SEP)
      f.write(name.encode('ascii','ignore')+SEP)
      f.write(prices+SEP)
      f.write(lic_types+SEP)
      f.write(categories+SEP)
      f.write(kws+"\n")
      f.close();
      #print('done')
      rtime = 0.25+random.random()*1.75
      print('sleeping '+str(rtime)+'s')
      time.sleep(rtime)  
      #print('done')
    
    rtime = 0.5+random.random()*1
    print('sleeping '+str(rtime)+'s')
    time.sleep(rtime)  
    print('done')
    os.rename('page_'+str(pageN)+'.txt','page_'+str(pageN+1)+'.txt')
    pageN = pageN + 1
  except:
    print('Error')
    f=open('error_unexpected.log','a')
    f.write('damn it, I have an error on page '+str(pageN))
    f.close()
    raise
    
  if(random.random()<0.7):
    while(1):
      try:
        print('restarting Browser..')
        B = Browser()
        B.addheaders = [('User-agent', userAgents[randint(0,len(userAgents)-1)])]
        #B.set_proxies({'http':'http://5.187.2.148:3128'})
        B.set_handle_robots( False )
        print('opening start page')
        R = B.open('http://graphicriver.net/')
        print('following All Items link..')
        R = B.follow_link(text='All Items')
        print('opening page pageN-1('+str(pageN-1)+')..')
        R = B.open('http://graphicriver.net/category/all?page='+str(pageN-1))
        print('done')
        break
      except urllib2.HTTPError, err:
        if err.code == 404:
          print('404')
          time.sleep(10)
          continue
        else:
          print('Error not404_in_restart')
          f=open('error_not404_in_restart.log','a')
          f.write('damn it, I have an error on page '+str(pageN))
          f.close()
          raise  
      except:
        print('Browser Error')
        f=open('error_browser.log','a')
        f.write('damn it, I have an error on page '+str(pageN))
        f.close()
        raise
  try:
    L = B.find_link(text=str(pageN))
  except:
    print('Error')
    f=open('error.log','a')
    f.write('damn it, I have an error on page '+str(pageN))
    f.close()
    raise
  
  print('found link to page '+str(pageN))
#  if(pageN==3):
#    break

#B.open('http://graphicriver.net/category/all')

