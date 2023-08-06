[![proxyCheck](https://img.shields.io/pypi/v/proxyCheck-mp?style=for-the-badge)](https://pypi.org/project/proxyCheck-mp/)
[![Python3](https://img.shields.io/pypi/pyversions/proxyCheck-mp?style=for-the-badge)](https://www.python.org/downloads/release/python-396/)
[![proxyCheck](https://img.shields.io/github/languages/code-size/IMaresaLI/Proxy_Checker?style=for-the-badge)](https://pypi.org/project/proxyCheck-mp/)
[![proxyCheck](https://img.shields.io/pypi/l/proxyCheck-mp?style=for-the-badge)](https://github.com/IMaresaLI/Proxy_Checker/blob/lastversion/LICENSE)

# Proxy Checker Mp

# How to use ?

## 1-) Module Install and Import
 - **Install Module**
```python
pip install proxyCheck-mp
```
```python
pip3 install proxyCheck-mp
```
- **Import Module**
```python
from proxyChecker import ProxyController
```
## 2-) proxyController class must be called.
```python
prxCont = ProxyController()
```
## 3-) User-agent default value and reassign.

**Default Value ;**
```python
getDefaultUseragent() --> "windows" 
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
```
**Assigning a new value ;**
```python
prxCont = ProxyController()
#First method
prxCont.userAgent = 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

#Second method
prxCont.userAgent = getDefaultUseragent("linux") --> linux user-agent
#Operating systems defined in the getDefaultUseragent() method. --> Windows,Linux,Macos,Android,Iphone,Ipad,Ipod

#Third method
prxCont.userAgent = randomUserAgent() --> a random user-agent
# When this method calls, it fetches a random user agent from the Eight Thousand-element list.
```
## 3-) The proxyControl method bound to the proxyController class must be called.
### prxCont.proxyControl(proxys , url , timeout , max_redirects, details)
```
Parameter Details ;
proxies  -> Proxies parameter must be list or str. (List or String)
url	-> Give url to check proxy. (https-http) Default = https://www.google.com
timeout -> Set a waiting time to connect. Default timeout = (3.05,27) >> (connect,read)
max_redirects -> Determines whether redirects are used. Default max_redirects = (False,300) >> (use,value)
details -> Information message about whether the proxy is working or not. (True or False) Default = True
```
## 4-) Output - Successfull
```python
prxCont = ProxyController()
prxCont.userAgent = prxCont.randomUserAgent()

# Singular
proxy = "125.99.157.238:5678"
print(prxCont.proxyControl(proxy))

#output _> 
	Protocol : socks4 - Connection Successfull - 125.99.157.238:5678
	ProxyIp : 125.99.157.238 -- ProxyType : IPv4 -- Country : India -- Region : Telangana -- AvagereTimeOut : 2.07sn
	Your User-Agent = Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.13 (KHTML, like Gecko) RockMelt/0.9.48.59 Chrome/9.0.597.107 Safari/534.13
	Proxy check completed.
	125.99.157.238:5678
	
print(prxCont.proxyControl(proxyList,detail=False))
#output2 _>
	Proxy check completed.
	125.99.157.238:5678

# Multiple
proxies = ["37.238.136.12:5678","158.69.225.124:2021","64.235.204.107:8080","148.72.65.230:37704","20.47.108.204:8888"]
print(prxCont.proxyControl(proxies))

#output _> 
	Protocol : http - The connection is unstable - 37.238.136.12:5678
	ProxyIp : 37.238.136.12 -- ProxyType : IPv4 -- Country : Iraq -- Region : Baghdad Governorate -- AvagereTimeOut : 1.97sn
	Your User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36
	Protocol : socks4 - Connection Successfull - 37.238.136.12:5678
	Protocol : http - The connection is unstable - 158.69.225.124:2021
	ProxyIp : 158.69.225.124 -- ProxyType : IPv4 -- Country : Canada -- Region : Québec -- AvagereTimeOut : 17.56sn
	Your User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36
	Protocol : socks4 - Connection Successfull - 158.69.225.124:2021
	Protocol : http - The connection is unstable - 64.235.204.107:8080
	Protocol : socks4 - The connection is unstable - 64.235.204.107:8080
	Protocol : socks5 - The connection is unstable - 64.235.204.107:8080
	Protocol : http - The connection is unstable - 148.72.65.230:37704
	ProxyIp : 148.72.65.230 -- ProxyType : IPv4 -- Country : United States -- Region : Virginia -- AvagereTimeOut : 2.68sn
	Your User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36
	Protocol : socks4 - Connection Successfull - 148.72.65.230:37704
	ProxyIp : 52.188.146.128 -- ProxyType : IPv4 -- Country : United States -- Region : Virginia -- AvagereTimeOut : 1.09sn
	Your User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36
	Protocol : http - Connection Successfull - 20.47.108.204:8888

	Proxy check completed.
	['37.238.136.12:5678','125.99.157.238:5678','148.72.65.230:37704','20.47.108.204:8888']
	
print(prxCont.proxyControl(proxyList,detail=False))
#output2 _>
	Proxy check completed.
	['37.238.136.12:5678','125.99.157.238:5678','148.72.65.230:37704','20.47.108.204:8888']

```
## 4-) Output - UnSuccessful
```python
prxCont = ProxyController()
proxyList = ["0.0.0.0:18","1.1.1.1:80","11.11.11.11:8080"]
prxCont.proxyControl(proxyList)
#output _> 
	Protocol : http - The connection is unstable - 0.0.0.0:18
	Protocol : socks4 - The connection is unstable - 0.0.0.0:18
	Protocol : socks5 - The connection is unstable - 0.0.0.0:18
	Protocol : http - The connection is unstable - 1.1.1.1:80
	Protocol : socks4 - The connection is unstable - 1.1.1.1:80
	Protocol : socks5 - The connection is unstable - 1.1.1.1:80
	Protocol : http - The connection is unstable - 11.11.11.11:8080
	Protocol : socks4 - The connection is unstable - 11.11.11.11:8080
	Protocol : socks5 - The connection is unstable - 11.11.11.11:8080
	Proxy check completed.
	None of the proxies you provided are working.
	
prxCont.proxyControl(proxyList,detail=False)
#output2 _>
	Proxy check completed.
	None of the proxies you provided are working.
```