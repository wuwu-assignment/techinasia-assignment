#explore url
import json
import requests 

new=open('validURL.txt','w')
url= 'https://www.techinasia.com/wp-json/techinasia/2.0/posts?'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}

for i in range(1,10001):
	print(i) 
	pageurl = url+'page='+str(i)
	response= requests.get(pageurl,headers=header)
	if response.status_code==200:
		new.write(str(i)+'\n')
new.close() 