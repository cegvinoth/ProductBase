import urllib2
import threading
import time
import re
import MySQLdb
from StringIO import StringIO
import gzip
import zlib
from bs4 import BeautifulSoup
import requests
from datetime import date
import os

db=MySQLdb.connect("localhost","root","","productbase")
cursor=db.cursor()

class crawlThread(threading.Thread):
	def __init__(self,threadID,name,url,last_modified):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.last_modified =last_modified
		self.name = name
		self.url = url

	def run(self):
		print str(self.threadID)+' starting download: '+self.url+'\n'
		response = download_page(self.threadID,self.url,self.last_modified)
		print str(self.threadID)+' downloaded '+self.url+'\n'

def download_page(id,url,last_modified):
	try:
		response=requests.get(url,allow_redirects=False)
		content=response.text
		todaydate=date.today().isoformat()
		if not os.path.exists(todaydate):
			os.makedirs(todaydate)
		file_open=open(todaydate+'/'+url.replace('/','-')+'.html','w')
		file_open.write(content)
		file_open.close()
		db=MySQLdb.connect("localhost","root","","productbase")
		cursor=db.cursor()
		cursor.execute("update crawllist set linkadded=0,crawled=1,date_downloaded='%s' where id=%s" %(todaydate,id))
		db.commit()
		db.close()
		print url
	except urllib2.URLError as e:
		print e.reason
		return -1
	return 1


def get_sitemap_url(url):
		response=urllib2.urlopen(url)
		content=response.read()
		sitemap_list=re.findall('http://.+',content)
		return sitemap_list

print 'Download webpages'
cursor.execute("select id,url,last_modified from crawllist where linkadded=1")
resultset=cursor.fetchall()
for row in resultset:
		r=row[1]
		time.sleep(1)
		thread=crawlThread(row[0],r,r,row[2])
		thread.start()
