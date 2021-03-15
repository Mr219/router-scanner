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
"Sec-Fetch-Site" : "same-origin",
"Sec-Fetch-Mode" : "navigate",
"Sec-Fetch-User" : "?1",
"Accept-Encoding" : "gzip, deflate",
"Accept-Language" : "en-US,en;q=0.9,my;q=0.8",
"Sec-Fetch-Dest" : "document"
}
# cookie = {
# 	"Cookie" : "body:Language:english:id=-1"
# }
session = requests.Session()

def get_login_token():
	url = 'https://'+host+':80/asp/GetRandCount.asp'
	data1 = {}
	x = requests.post(url, data = data1,headers = headers, verify=False)
	login_token = x.text
	login_token = login_token.replace("ï»¿","")
	# print(login_token)
	login_cookie(login_token)

def get_wlan_token(cookies):
	cmd2 = "curl -i -s -k -X 'GET' "  + " -b '"+cookies+":Language:english:id=1' 'https://"+host+":80/html/amp/wlanbasic/WlanBasic.asp'"	
	out2 = run_cmd(cmd2)
	out2 = out2.split("hwonttoken")[1]
	token = out2.split('"')[2]
	return token

def run_cmd(cmd):
	try:
	    out = subprocess.check_output(cmd,stderr=subprocess.STDOUT, shell=True)
	    res = 0    # no exception, exit status must be 0
	except subprocess.CalledProcessError as e:
		out = e.output
		res = e.returncode
	out = out.decode('utf8')
	return out
def login_cookie(login_token):
	header = "-H 'Host: "+host+":80' -H 'Connection: close' -H 'Content-Length: 93' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'Origin: https://"+host+":80' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Dest: document' -H 'Referer: https://"+host+":80/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,my;q=0.8'"
	cmd1 = "curl -i -s -k -X 'POST' " + header + " -b 'Cookie=body:Language:english:id=-1' --data-binary 'UserName=telecomadmin&PassWord=YWRtaW50ZWxlY29t&x.X_HW_Token="+login_token+"' 'https://"+host+":80/login.cgi'"
	# print(cmd1)
	out = run_cmd(cmd1)
	out= out.split(':')
	cookies = out[1]
	# print(cookies)
	token = get_wlan_token(cookies)
	cmd21 = "curl -i -s -k -X 'POST' " +  " -b '"+cookies+":Language:english:id=1'  --data-binary 'InternetGatewayDevice.LANDevice.1.WLANConfiguration.2=&x.X_HW_Token=" +token+"' 'https://"+host+":80/html/amp/wlanbasic/del.cgi?RequestFile=html/amp/wlanbasic/WlanBasic.asp'"
	try:
		out21 = run_cmd(cmd21)
		# print(out21)
		token = get_wlan_token(cookies)
		cmd22 = cmd21 = "curl -i -s -k -X 'POST' " +  " -b '"+cookies+":Language:english:id=1'  --data-binary 'InternetGatewayDevice.LANDevice.1.WLANConfiguration.3=&x.X_HW_Token=" +token+"' 'https://"+host+":80/html/amp/wlanbasic/del.cgi?RequestFile=html/amp/wlanbasic/WlanBasic.asp'"
		out22 = run_cmd(cmd22)
		token = get_wlan_token(cookies)
		cmd3 = "curl -i -s -k -X 'POST' "  +header+ " -b '"+cookies+":Language:english:id=1'  --data-binary 'y.Enable=1&y.SSIDAdvertisementEnabled=1&y.WMMEnable=1&y.SSID="+ssid+"&y.X_HW_AssociateNum=32&x.X_HW_Token=" +token+"' 'https://"+host+":80/html/amp/wlanbasic/add.cgi?y=InternetGatewayDevice.LANDevice.1.WLANConfiguration&RequestFile=html/amp/wlanbasic/WlanBasic.asp'"
		# print(token)
	except:
		# print("not delete")
		token = get_wlan_token(cookies)
		cmd3 = "curl -i -s -k -X 'POST' "  +header+ " -b '"+cookies+":Language:english:id=1'  --data-binary 'y.Enable=1&y.SSIDAdvertisementEnabled=1&y.WMMEnable=1&y.SSID="+ssid+"&y.X_HW_AssociateNum=32&x.X_HW_Token=" +token+"' 'https://"+host+":80/html/amp/wlanbasic/add.cgi?y=InternetGatewayDevice.LANDevice.1.WLANConfiguration&RequestFile=html/amp/wlanbasic/WlanBasic.asp'"
		# print(cmd3)
	out3 = run_cmd(cmd3)
	time.sleep(1)
	token = get_wlan_token(cookies)
	cmd4 = "curl -i -s -k -X 'POST' " + " -b '"+cookies+":Language:english:id=1'  --data-binary 'y.Enable=1&y.SSIDAdvertisementEnabled=1&y.SSID="+ssid+"&y.X_HW_AssociateNum=32&y.BeaconType=WPAand11i&y.X_HW_WPAand11iAuthenticationMode=PSKAuthentication&y.X_HW_WPAand11iEncryptionModes=TKIPandAESEncryption&k.PreSharedKey="+ssid+"&y.X_HW_GroupRekey=3600&z.Enable=0&z.X_HW_ConfigMethod=PushButton&w.SsidInst=2&w.SSID="+ssid+"&w.Enable=1&w.Standard=11bgn&w.BasicAuthenticationMode=None&w.BasicEncryptionModes=TKIPandAESEncryption&w.WPAAuthenticationMode=EAPAuthentication&w.WPAEncryptionModes=TKIPandAESEncryption&w.IEEE11iAuthenticationMode=EAPAuthentication&w.IEEE11iEncryptionModes=TKIPandAESEncryption&w.MixAuthenticationMode=PSKAuthentication&w.MixEncryptionModes=TKIPandAESEncryption&w.BeaconType=WPAand11i&w.WEPEncryptionLevel=104-bit&w.WEPKeyIndex=1&w.Key="+ssid+"&x.X_HW_Token=" +token+"' 'https://"+host+":80/html/amp/wlanbasic/set.cgi?w=InternetGatewayDevice.X_HW_DEBUG.AMP.WifiCoverSetWlanBasic&y=InternetGatewayDevice.LANDevice.1.WLANConfiguration.2&z=InternetGatewayDevice.LANDevice.1.WLANConfiguration.2.WPS&k=InternetGatewayDevice.LANDevice.1.WLANConfiguration.2.PreSharedKey.1&RequestFile=html/amp/wlanbasic/WlanBasic.asp'"
	out4 = run_cmd(cmd4)
	token = get_wlan_token(cookies)
	cmd5 = "curl -i -s -k -X 'POST' " +  " -b '"+cookies+":Language:english:id=1'  --data-binary 'y.Enable=1&y.SSIDAdvertisementEnabled=1&y.SSID="+ssid+"&y.X_HW_AssociateNum=32&y.BeaconType=WPAand11i&y.X_HW_WPAand11iAuthenticationMode=PSKAuthentication&y.X_HW_WPAand11iEncryptionModes=TKIPandAESEncryption&k.PreSharedKey="+ssid+"&y.X_HW_GroupRekey=3600&z.Enable=0&z.X_HW_ConfigMethod=PushButton&w.SsidInst=2&w.SSID="+ssid+"&w.Enable=1&w.Standard=11bgn&w.BasicAuthenticationMode=None&w.BasicEncryptionModes=TKIPandAESEncryption&w.WPAAuthenticationMode=EAPAuthentication&w.WPAEncryptionModes=TKIPandAESEncryption&w.IEEE11iAuthenticationMode=EAPAuthentication&w.IEEE11iEncryptionModes=TKIPandAESEncryption&w.MixAuthenticationMode=PSKAuthentication&w.MixEncryptionModes=TKIPandAESEncryption&w.BeaconType=WPAand11i&w.WEPEncryptionLevel=104-bit&w.WEPKeyIndex=1&w.Key="+ssid+"&x.X_HW_Token=" +token+"' 'https://"+host+":80/html/amp/wlanbasic/set.cgi?w=InternetGatewayDevice.X_HW_DEBUG.AMP.WifiCoverSetWlanBasic&y=InternetGatewayDevice.LANDevice.1.WLANConfiguration.2&z=InternetGatewayDevice.LANDevice.1.WLANConfiguration.2.WPS&k=InternetGatewayDevice.LANDevice.1.WLANConfiguration.2.PreSharedKey.1&RequestFile=html/amp/wlanbasic/WlanBasic.asp'"
try:
	get_login_token()
	print("0")
except:
	print("1")
