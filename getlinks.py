import urllib2
import re
import MySQLdb
from StringIO import StringIO
import gzip
import zlib
from bs4 import BeautifulSoup
from datetime import date


def get_sitemap_url(url):
		response=urllib2.urlopen(url)
		content=response.read()
		sitemap_list=re.findall('http://.+',content)
		return sitemap_list

#db=MySQLdb.connect('localhost','root','','productbase')
#cursor=db.cursor()
count=0
sitemap_list=get_sitemap_url('http://www.flipkart.com/robots.txt')
for item in sitemap_list:
		response=urllib2.urlopen(item)
		content=response.read()
		todaydate=date.today().isoformat()
		sitemap_xml=re.findall('http://www\.flipkart\.com/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.gz',content)  #modify this with beautiful soup
		for url in sitemap_xml:
			print url
			request=urllib2.Request(url)
			request.add_header('Accept-Encoding','gzip,deflate')
			response=urllib2.urlopen(request)
			if response.info().get('Content-Encoding') =='gzip':
				 buf =StringIO(response.read())
				 f=gzip.GzipFile(fileobj=buf,mode='rb')
				 data=f.read()
				 xmlfile=zlib.decompress(data,zlib.MAX_WBITS | 16)
				 soup=BeautifulSoup(xmlfile)
				 product_url_list=soup.find_all('url')
				 for url in product_url_list:
						 #print url.loc.string
						 count=count+1
						 #print count
						 #cursor.execute("INSERT INTO crawllist(url,last_modified,date_added,crawled,analyzed,linkadded) values('%s','%s','%s','%s','%s','%s')" % (url.loc.string,url.lastmod.string,todaydate,'0','0','1'))
				 #db.commit()