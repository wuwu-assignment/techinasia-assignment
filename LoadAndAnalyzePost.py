#load and analyze text
import json
import pandas as pd
import numpy as np 
from textblob import TextBlob 
import re

#load the posts data
txtData = open('postsPage1to30.txt','r').read()

#There are 30 pages. Each page contains multiple posts
txtByPage = txtData.split('_My_Page_Separator_')

#We use a list to store the posts
posts=[] #each element is a post
for item in txtByPage:
	js = json.loads(item) 
	for post in js['posts']:
		posts.append(post)

print('Every post contains following fields:')
print(posts[0].keys())

# Note that in the content of each post, there're many html tags
# This function will clean the text by removing '\n' and html tags such as <div>
###############################
def cleanText(tx):
	#tx is a single string
	result = re.sub(r'<[^>]+>','',tx)
	result = re.sub(r'\n','',result) 
	return result 
###############################

print('This is a piece of content before cleaning:')
print(posts[0]['content'][:300].encode('ascii',errors='ignore'))

for item in posts:
	item['content']=cleanText(item['content'])

print('This is the same content after cleaning:')
print(posts[0]['content'][:300].encode('ascii',errors='ignore'))


#We compute average read time
meanReadTime = np.mean([float(item['read_time']) for item in posts])
maxReadTime = max([float(item['read_time']) for item in posts])
print('The average reading time for posts is %8.2f minutes.'% (round(meanReadTime,2)) )
print('The longest reading time for posts is %8.2f minutes.'% (round(maxReadTime,2)))

#We compute average number of comments
meanComment = np.mean([float(item['comment_count']) for item in posts])
maxComment = max([float(item['comment_count']) for item in posts])
print('The average number of comments for posts is %8.2f.'% (round(meanComment,2)) )
print('The largest number of comments for posts is %8.2f.'% (round(maxComment,2)) )

# d={'id':[item['id'] for item in posts], 'title':[item['title'] for item in posts]}
# df = pd.DataFrame(data=d)
# print(df.iloc[0]['title'])

#Now, we want to find the most frenquent nouns in title.

#We define a function which can find the most frequent nouns in a text.
################################
def mostFrequentNoun100(tx):
	#tx is a single string
	blob = TextBlob(tx)
	frequency = blob.np_counts
	frequency_high2low = sorted(frequency,key=frequency.get,reverse=True)
	print([item +':'+str(frequency[item]) for item in frequency_high2low[:100]])
	return 
#################################

#We consider the titles for all posts
allTitle = ' '.join([item['title'] for item in posts])

#Find the most frequent nouns.
print('These are the most frequent nouns in title found by textblob, together with their frequency.') 
mostFrequentNoun100(allTitle) 

#We can also use the same method to find most frequent nouns in content part.
# allContent = ' '.join([item['content'] for item in posts])
# print('These are the most frequent nouns in content found by textblob, together with their frequency.') 
# mostFrequentNoun100(allContent)

#Analyze the sentiment of each post
sentimentList = [TextBlob(item['content']).sentiment for item in posts]
polarityList = [item.polarity for item in sentimentList]
subjectivityList = [item.subjectivity  for item in sentimentList]

meanPol = np.mean(polarityList)
print('The average polarity score is %8.4f.' % (meanPol))
positive = [item for item in polarityList if item>0]
positive = len(positive)/len(polarityList)
print('%8.2f percent of posts have a positive polarity score.'% (round(positive*100)))

meanSub = np.mean(subjectivityList)
print('The average subjectivity score is %8.4f.'% (meanSub) )
objective = [item for item in subjectivityList if item<0.5]
objective = len(objective)/len(subjectivityList)
print('%8.2f percent of posts are of objective type.'% (round(objective*100)) ) 

#load file
txtData = open('comments.txt','r').read()
txtByPage = txtData.split('_My_Separator_')[:-1]

#We use a dictionary to store the comments
comments={} #each element is a post
for item in txtByPage:
	if re.search(r'post":"[^"]+',item):
		postID = re.search(r'post":"[^"]+',item).group()[7:]
		commentList = re.findall(r'content":"[^"]+',item)
		commentList = [c[10:] for c in commentList]
		comments[postID]=' '.join(commentList)
		comments[postID] = cleanText(comments[postID]) 

#Is there a correlation between number of comments and length of content
x=[len(item['content']) for item in posts]
y=[int(item['comment_count']) for item in posts]
print('correlation between length of content and no. comments:')
print(np.corrcoef(x,y))

#Is there a correlation between number of comments and positivity?
x=[len(item['content']) for item in posts]
y=polarityList[:] 
print('correlation between content positivity and no. comments:')
print(np.corrcoef(x,y))

#Is there a correlation between number of comments and objectivity?
x=[len(item['content']) for item in posts]
y=subjectivityList[:] 
print('correlation between content subjectivityList and no. comments:')
print(np.corrcoef(x,y))


#Now we consider this question:
#Is there a correlation between nouns in title and number of comments?
#What is the positivity of comments?

###############################
#This function finds all posts who has the keyword in its title
#and return the average number of comments in these posts
#together with the average polarity of comments
def keywordComment(keyword):	
	totalPost=0
	totalComment=0
	pol=0
	for post in posts:
		if keyword.lower() in post['title'].lower():
			totalComment+= post['comment_count']
			totalPost+=1
			postID = post['id']
			com = comments.get(postID,'')
			pol+= TextBlob(com).sentiment.polarity
	if totalPost==0:
		return {'average no. comments':0, 'average polarity':0}
	else:
		return {'average no. comments':totalComment/totalPost ,'average polarity': pol/totalPost} 
################################

print('china',keywordComment('china'))
print('singapore',keywordComment('singapore'))
print('japan',keywordComment('japan'))
print('jack ma',keywordComment('jack ma'))
print('grab',keywordComment('grab')) 
print('facebook',keywordComment('facebook'))
print('go-jek',keywordComment('go-jek'))
print('didi',keywordComment('didi'))
print('google',keywordComment('google'))

for post in posts:
	if int(post['comment_count'])==74:
		print(post['title']) 