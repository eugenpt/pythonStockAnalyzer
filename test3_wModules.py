# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 17:49:34 2013

@author: ep
"""



"""

Idea:
  
  get proxies
  
  generate tasks (~5-20 per proxy)
  
  launch parallel workers (1 per proxy)
  
  errored links -> special queue
  
  retest special queue with new proxies

"""

import requests
import time
import random
import os.path
from Queue import Queue
from threading import Thread
from temp_getProxies_multi import getValidProxies
from stockPageGetInfo import getItemInfo

commonUrl = 'http://3docean.net/item/a/'

myDomains = ['graphicriver','activeden','audiojungle','themeforest',
             'videohive','3docean','codecanyon','photodune']

commonFilename = 'resultsFile_'
commonFileExt = '.txt'

reportFilename = "report.txt"

myDelim = '||||'

numberOfTests = 10

testNumsQ = Queue() #consists of two-elements arrays
errorredNumsQ = Queue()

resultsQs = [Queue() for domain in myDomains]

def randomURL():
  randomCharSource="1234567890---qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
  result = 'http://'+myDomains[random.randint(0,len(myDomains)-1)]+'.net/item/'
  temp = random.randint(4,20)
  for j in range(0,temp):
    result+=randomCharSource[random.randint(0,len(randomCharSource)-1)]
  result=result+'/'
  return result  
  

def testerFun(inputQ,errQ,proxy):
  while(inputQ.empty()==False):
    tNum = inputQ.get()
    if(tNum[1]>=numberOfTests):
      continue
    try:
#      pass
#    finally:
      url = randomURL()+str(tNum[0])
      print("R=responses.get('"+url+"',proxies="+str(proxy)+")")
      R = requests.get(url,proxies=proxy,timeout=4)
      tDomain = R.url[7:R.url.index('.net')]  
      tIX = myDomains.index(tDomain)      
      if(R.status_code==404):
        print(str(tNum[0])+" 404")
        temp = tNum
        temp[1]=temp[1]+1
        errQ.put(temp)
        pass #continue
      else:
      
        res = getItemInfo(R.content)
        res['num']=tNum
        res['domain']=tDomain
        
        resultsQs[tIX].put(res)
    except:
      temp = tNum
      temp[1]=temp[1]+1
      errQ.put(temp)

def resultsWriterFun(workerInputQ,qIX):
  while(workerInputQ.empty()==False):
    if(resultsQs[qIX].empty()==False):
      tf = open(commonFilename+myDomains[qIX]+commonFileExt,'a')
      while(resultsQs[qIX].empty()==False):
        res = resultsQs[qIX].get()
        tf.write(str(res['num'][0])+myDelim+
                 str(res['num'][1])+myDelim+
                 str(res['author'])+myDelim+
                 str(res['price'])+myDelim+
                 str(res['nop'])+myDelim+
                 str(res['date'])+myDelim+
                 str(res['lic_type'])+myDelim+
                 str(res['name'])+myDelim+
                 str(res['kws'])+"\n")
      tf.close()
    time.sleep(1)
  if(resultsQs[qIX].empty()==False):
    #tf = open(commonFilename+myDomains[qIX]+commonFileExt,'a')
    tf = open(commonFilename+"all"+commonFileExt,'a')
    while(resultsQs[qIX].empty()==False):
      res = resultsQs[qIX].get()
      tf.write(str(res['num'][0])+myDelim+
               str(res['num'][1])+myDelim+
               str(res['author'])+myDelim+
               str(res['price'])+myDelim+
               str(res['nop'])+myDelim+
               str(res['date'])+myDelim+
               str(res['lic_type'])+myDelim+
               str(res['name'])+myDelim+
               str(res['kws'])+"\n")
    tf.close()
    



nStart = 1
#nStart = 5502603


#
#  Read starting number 
#
# restart all files - temporary thing
for domain in myDomains:
  filename = commonFilename+domain+commonFileExt
  if(os.path.exists(filename)==False):
    open(filename,'w').close()
  else:
    f = open(filename,'r')
    
    for line in f:
      tnum = int(line[0:line.index(myDelim)])
      if(tnum>nStart):
        nStart = tnum
    
    f.close()

print("Starting from "+str(nStart))
print("")
print("")
time.sleep(2)



nPerProxy = 15


for j in range(0,100):
  count = 0
  S = time.time()
  #
  #  Getting proxies
  # 
  pxs = getValidProxies()
  random.shuffle(pxs)
  
  print('***********************************')
  print('found '+str(len(pxs))+" proxies")
  print('***********************************')
  
  #
  #  Putting all previous errored Nums bak into the game
  #
  
  while(errorredNumsQ.empty()==False):
    testNumsQ.put(errorredNumsQ.get())
    count+=1
  
  #
  #  Filling testing Q with new things to process (inluding number of tests already)
  #
  tc=count
  for j in range(nStart,nStart+nPerProxy*len(pxs)-tc+1):
    testNumsQ.put([j,0])
    count+=1
  
  nStart = nStart+nPerProxy*len(pxs)-tc+1
  print('***********************************')
  print('***********************************')
  print("new Start = "+str(nStart))
  print('***********************************')
  print('***********************************')
  time.sleep(2)
  #
  #  Starting testers (1 per proxy)
  #
  
  Ths = [Thread(target=testerFun,args=(testNumsQ,errorredNumsQ,px,)) for px in pxs]
  for T in Ths:
    T.setDaemon(True)
    T.start()
  
  print('***********************************')
  print('Started all workers')
  print('***********************************')
  #
  #  Starting Writers (1 per domain)
  #
  time.sleep(4)
  
  RThs = [Thread(target=resultsWriterFun,args=(testNumsQ,qIX,)) for qIX in range(0,len(myDomains))]
  for T in RThs:
    T.setDaemon(True)
    T.start()
  
  print('***********************************')
  print('Started all writers')
  print('***********************************')
    
  
  for T in Ths:
    T.join()
  
  print('***********************************')
  print('Joined all workers')
  print('***********************************')
    
  for T in RThs:
    T.join()
    
  print('***********************************')
  print('Joined all writers')
  print('***********************************')
  
  print("Errorred nums: "+str(errorredNumsQ.qsize()))
  print(str(count)+" done in "+str(time.time()-S)+"s")
  print('Error percentile: '+str(errorredNumsQ.qsize()*100.00/count)+"%")
  print(str(count/(time.time()-S))+"cps")
  
  report=open(reportFilename,'w')
  report.write("new Start = "+str(nStart))
  report.write('found '+str(len(pxs))+" proxies")
  report.write("Errorred nums: "+str(errorredNumsQ.qsize())+"\n")
  report.write(str(count)+" done in "+str(time.time()-S)+"s"+"\n")
  report.write('Error percentile: '+str(errorredNumsQ.qsize()*100.00/count)+"%"+"\n")
  report.write(str(count/(time.time()-S))+"cps"+"\n")
  report.close()  
  
  print("")
  print("")
  time.sleep(2)
  
for j in range(0,numberOfTests):
  print('***********************************')
  print("Starting final test #"+str(j+1)+"/"+str(numberOfTests))
  print('***********************************')
  pxs = getValidProxies()
  random.shuffle(pxs)
  print('***********************************')
  print('found '+str(len(pxs))+" proxies")
  print('***********************************')
  if(errorredNumsQ.empty()==False):
    while(errorredNumsQ.empty()==False):
      testNumsQ.put(errorredNumsQ.get())
    Ths = [Thread(target=testerFun,args=(testNumsQ,errorredNumsQ,px,)) for px in pxs]
    for T in Ths:
      T.setDaemon(True)
      T.start()
      
    time.sleep(2)
    
    RThs = [Thread(target=resultsWriterFun,args=(testNumsQ,qIX,)) for qIX in range(0,len(myDomains))]
    for T in RThs:
      T.setDaemon(True)
      T.start()
    for T in Ths:
      T.join()
      
    for T in RThs:
      T.join()
  print('***********************************')
  print("Finished: final test #"+str(j+1)+"/"+str(numberOfTests))
  print('***********************************')

print('***********************************')
print("All Finished")
print('***********************************')
