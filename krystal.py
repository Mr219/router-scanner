import os,sys,platform,requests
from multiprocessing import Pool
from sys import exit
from datetime import datetime

net = input("Enter the Network Address: ")
net1= net.split('.')
a = '.'

net2 = net1[0] + a + net1[1] + a 
st1 = 0   # 10.10.*  start
en1 = 255  # 10.10.*  end
en1 = en1 + 1
st2 = 1 # 10.10.10.*  start
en2 = 255 # 10.10.10.* end
en2 = en2 + 1
oper = platform.system()
links = []
error = []

t1 = datetime.now()
print ("Scanning in Progress:")

def scan(url):
   try:
      print('\r'+url+ '/index.html     ',end=' ',flush=True)
      r = requests.get(url+ '/index.html',timeout=2)
      r.raise_for_status()
      rs=r.text
      if (rs.find('window.location=') != -1): 
         print ("\rHuawei Router : "+ url+"/index.html")
         # huawei.append(url)
      else:
         print ("\rOther Router : " + url)
   except requests.exceptions.HTTPError as errb:
      ra = requests.get(url,timeout=2)
      rx=ra.text
      if (rx.find('RouterOS') != -1): 
         print ("\rmikrotik : "+ url)
         # mikrotik.append(url)
      else:
         print ("\rOther Router : " + url)
   except requests.exceptions.ConnectionError as errc:
      error.append(url)
   except requests.exceptions.Timeout as  errt:
      error.append(url)

def bb(net3):
   for ip in range(st2,en2):
      addr = net3 + str(ip)
      url = "http://" + addr 
      links.append(url)
def aa():
   for ip in range(st1,en1):
      net3 = net2  + str(ip) + '.' 
      bb(net3)
aa()
def do():
    p = Pool(processes=250)
    try:
        p.map(scan, links)
        p.close()
    except KeyboardInterrupt:
        print('got ^C while pool mapping, terminating the pool')
        p.terminate()
        print('\r[!] Good Bye J3rry')
        sys.exit()
    finally:
        p.join()
if __name__ == "__main__":
   try:
      do()
   except KeyboardInterrupt:
      sys.exit()
   t2 = datetime.now()
   total = t2 - t1
   print ("Scanning completed in: ",total)
