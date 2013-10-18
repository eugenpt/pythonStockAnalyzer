# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 18:41:34 2013

@author: ep
"""


from mechanize import Browser
import lxml.html
import time
import requests
from random import randint
import random
from Queue import Queue
from threading import Thread
import os

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
pageN = 2365

print('removing page and error file(s)')
for filename in os.listdir('.'):
  if((filename.startswith('page_')) or (filename.startswith('error_'))):
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
    f=open('graphicriver_urls_2.txt','a')
    for url in turls:
      #print(url)
      f.write(url+'\n')
    f.close()  
    rtime = 1.5+random.random()*4
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
    break

  try:
    if(random.random()<0.05):
      print('restarting Browser..')
      B = Browser()
      B.addheaders = [('User-agent', userAgents[randint(0,len(userAgents)-1)])]
      #B.set_proxies({'http':'http://5.187.2.148:3128'})
      B.set_handle_robots( False )
      print('opening start page')
      R = B.open('http://graphicriver.net/')
      print('following All Items link..')
      B.follow_link(text='All Items')
      print('opening page pageN-1('+str(pageN-1)+')..')
      B.open('http://graphicriver.net/category/all?page='+str(pageN-1))
      print('done')
  except:
    print('Browser Error')
    f=open('error_browser.log','a')
    f.write('damn it, I have an error on page '+str(pageN))
    f.close()
    break
  
  try:
    L = B.find_link(text=str(pageN))
  except:
    print('Error')
    f=open('error.log','a')
    f.write('damn it, I have an error on page '+str(pageN))
    f.close()
    break
  
  print('found link to page '+str(pageN))
#  if(pageN==3):
#    break

#B.open('http://graphicriver.net/category/all')

