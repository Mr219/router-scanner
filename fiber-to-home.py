import requests,os,sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import subprocess,time

host=sys.argv[1]
ssid=sys.argv[2]
headers = { "Host" : host ,
"Connection" : "close",
"Cache-Control" : "max-age=0",
"Upgrade-Insecure-Requests" : "1",
"Origin" : "https://"+host+":80",
"Content-Type" : "application/x-www-form-urlencoded",
"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
"X-Requested-With" : "XMLHttpRequest",
"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
# "Sec-Fetch-Site" : "same-origin",
# "Sec-Fetch-Mode" : "navigate",
# "Sec-Fetch-User" : "?1",
"Accept-Encoding" : "gzip, deflate",
"Accept-Language" : "en-US,en;q=0.9,my;q=0.8",
"Sec-Fetch-Dest" : "document"
}
# cookie = {
# 	"Cookie" : "body:Language:english:id=-1"
# }
header = "-H 'Host: "+host+"'   -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'Origin: https://"+host+"' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'Referer: https://"+host+"/admin/login.asp' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,my;q=0.8' -H 'Connection: close'"
def run_cmd(cmd):
	# cmd1 = "curl -i -s -k  -X $'POST'  -H $'Host: 100.66.34.240' -H $'Content-Length: 24' -H $'Cache-Control: max-age=0' -H $'Upgrade-Insecure-Requests: 1' -H $'Origin: http://100.66.34.240' -H $'Content-Type: application/x-www-form-urlencoded' -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H $'Referer: http://100.66.8.72/admin/login.asp' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: en-US,en;q=0.9,my;q=0.8' -H $'Connection: close' --data-binary $'username=admin&psd=admin' $'http://100.66.34.240/boaform/admin/formLogin'"
	try:
	    out = subprocess.check_output(cmd,stderr=subprocess.STDOUT, shell=True)
	    res = 0    # no exception, exit status must be 0
	except subprocess.CalledProcessError as e:
		out = e.output
		res = e.returncode
	out = out.decode('utf8')
	# print(out)
	return out
def create_wlan():
	cmd2 = "curl -i -s -X 'POST' -H 'Content-Length: 24' "  +header+"  --data-binary 'wlanIdx=0&wl_disable1=ON&wl_band1=10&wl_ssid1="+ssid+"&TxRate1=0&wl_hide_ssid1=0&wl_access1=0&wl_limitstanum1=0&submit-url=%2Fadmin%2Fwlmultipleap.asp&save=Save%2FApply' 'http://"+host+"/boaform/admin/formWlanMultipleAP'"
	out = run_cmd(cmd2)
	if (out.find("Change setting successfully!")):
		#change wpa2 
		cmd3 = "curl -i -s -X 'POST' -H 'Content-Length: 266' "  +header+"  --data-binary 'wlanDisabled=OFF&isNmode=1&wpaSSID=1&security_method=6&auth_type=both&wepEnabled=ON&length0=1&format0=1&key0=*****&wpaAuth=psk&ciphersuite_t=1&wpa2ciphersuite_a=1&pskValue="+ssid+"&lst=&submit-url=%2Fnet_wlan_adv.asp&wlan_idx=undefined&wlan_idx2=222&pskFormat=0' 'http://"+host+"/boaform/admin/formWlEncrypt'"
		out = run_cmd(cmd3)
		# print(cmd3)
		if(out.find("301 Moved")):
			print("0")
		else:
			print("1")
def get_login_token():
	cmd1 = "curl -i -s -X 'POST' -H 'Content-Length: 24' "  +header+"  --data-binary 'username=admin&psd=admin' 'http://"+host+"/boaform/admin/formLogin'"
	out = run_cmd(cmd1)
	if (out.find("302 Moved") != -1 or out.find("have logined") != -1 ) :
		create_wlan()
	else:
		print("1")
# get_login_token()
try:
	get_login_token()
except:
	print("1")
#"+ssid+"


	# elif (out.find("have logined") != -1 ):
	# 	create_wlan()
