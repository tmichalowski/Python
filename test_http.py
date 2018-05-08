#!/usr/bin/env python
import sys, urllib2, os, time, threading
from Queue import Queue
from termcolor import colored
q = Queue()
SITES = [
        "http://www.google.com",
        "http://www.wp.pl",
        "http://127.0.0.1:4880",
]


def get_url(url):
    try:
        response = urllib2.urlopen(url)
        code = response.getcode()
        return code
    except urllib2.HTTPError as e:
        return e.code
    except:
        return 0

def performer1():
    while True:
        webname_value = q.get()
        print "{0:30} {1:10}".format(webname_value,get_url(webname_value))
        q.task_done()

if __name__ == "__main__":

   os.system("clear")
   while 1:

      for i in SITES:
         q.put(i)
      for no_of_threads in range(10):
         t = threading.Thread(target=performer1)
         t.daemon=True
         t.start()
      q.join()
      time.sleep(5)
      os.system("clear")
