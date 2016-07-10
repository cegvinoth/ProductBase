from bs4 import BeautifulSoup
import MySQLdb

db=MySQLdb.connect('localhost','root','','productbase')
cursor=db.cursor()
cursor.execute("select url,date_downloaded,id from crawllist where crawled=1")
resultset=cursor.fetchall()
for row in resultset:
   try:
	pagedate=row[1]
	rowid=row[2]
	rowurl=row[0]
	data=open(str(pagedate)+'/'+rowurl.replace('/','-')+'.html','r').read()
	soup=BeautifulSoup(data)
	product_name=soup.title.string
	img=soup.find('meta',attrs={'name':'og_image'})
	imgurl=img['content']
	url=soup.find('meta',attrs={'name':'og_url'})
	product_url=url['content']
	price=soup.find('span',attrs={'class':'selling-price omniture-field'})
	product_price=price.string
	product_price=(product_price.replace('Rs. ','')).strip()
	cursor.execute("insert into pricelist(producturl,imageurl,price,productname,price_date) values('%s','%s','%s','%s','%s')" % (product_url,imgurl,product_price,product_name,pagedate))
	cursor.execute("update crawllist set crawled=0,analyzed=1 where id='%s'" %(rowid))
	print product_name+" :: "+product_price
	db.commit()
   except Exception as e:
	  print str(e)