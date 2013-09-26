# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 16:53:09 2013

@author: ep
"""

import urllib2
import re



ts = 'http://graphicriver.net/item/seamless-hot-air-balloon-pattern/4597556'

commonURL = 'http://graphicriver.net/item/a/'

tNumStart = 4597556;
tNumC = 10;
import time

start = time.time()
print "hello"

for tNum in range(tNumStart,tNumStart+tNumC):
  print(commonURL+str(tNum))
  R = urllib2.urlopen(commonURL+str(tNum));
  ts = R.read();

end = time.time()
print end - start
print (end-start)/tNum