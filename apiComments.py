import json
import requests 

#load the posts data
txtData = open('postsPage1to30.txt','r').read()

#There are 30 pages. Each page contains multiple posts
txtByPage = txtData.split('_My_Page_Separator_')

#We use a list to store the ids 
ids=[] #each element is an id
for item in txtByPage:
	js = json.loads(item) 
	for post in js['posts']:
		ids.append(post['id'])

new = open('comments.txt','w') 

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}

for i in ids:
	print(i) 
	pageurl = url= 'https://www.techinasia.com/wp-json/techinasia/2.0/posts/'+i+'/comments'

	response= requests.get(pageurl,headers=header)
	# print(response) 
	data=response.text
	new.write(data) 
	new.write('_My_Separator_')
new.close() 