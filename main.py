from flask import Flask,jsonify,session,redirect,url_for,render_template,request
import re,time
from sqlite3 import *
import random
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = '~\xc8\xc6\xe0\xf3,\x98O\xa8z4\xfb=\rNd'


@app.route('/api/getpinglun/<string:bookID>')
def getpinglun(bookID):
	conn = connect('sql/pinglun.db')
	c = conn.cursor()
	c.execute(r"SELECT pl,fromID,time,zan,cai FROM COMPANY WHERE bookID = '%s';"%(bookID))
	pl_content = c.fetchall()
	conn.close()
	return jsonify({'data':pl_content})

@app.route('/api/getbangdan_collection')
def bangdan_collection():
	conn = connect('sql/collection.db')
	c = conn.cursor()
	c.execute(r"SELECT DISTINCT bookID,count(*) AS count FROM COMPANY GROUP BY bookID ORDER BY count DESC LIMIT 10;")
	bangdan_c = c.fetchall()
	conn.close()
	return jsonify({'bangdan_collection':bangdan_c})

@app.route('/api/getbangdan_pinglun')
def bangdan_pinglun():
	conn = connect('sql/pinglun.db')
	c = conn.cursor()
	c.execute(r"SELECT DISTINCT bookID,count(*) AS count FROM COMPANY GROUP BY bookID ORDER BY count DESC LIMIT 10;")
	bangdan_c = c.fetchall()
	conn.close()
	return jsonify({'bangdan_collection':bangdan_c})

@app.route('/api/getyanzheng')
def getyanzheng():
	s = requests.Session()
	picture = s.get("http://210.35.251.243/reader/captcha.php")
	cookie = requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']
	session['PHPSESSID'] = cookie
	return picture.content

@app.route('/api/login',methods=['POST'])
def login():
	s = requests.Session()
	jar = requests.cookies.RequestsCookieJar()
	jar.set('PHPSESSID',session.get('PHPSESSID'),domain='210.35.251.243',path='/')
	loginurl = "http://210.35.251.243/reader/redr_verify.php"
	payload = {"number":request.form.get('username'),"passwd":request.form.get('password'),"captcha":request.form.get('yanzheng'),"select":"cert_no","returnUrl":""}
	login = s.post(loginurl , data = payload , cookies=jar)
	napage = s.get("http://210.35.251.243/reader/redr_info.php", cookies=jar)
	na = BeautifulSoup(napage.text,'lxml')
	library_name = na.find("span",{"class":"profile-name"}).get_text()
	if library_name is not None:
		return jsonify({'status':'success','name':library_name})
	else:
		return jsonify({'status':'error'})

@app.route('/api/readnum')
def readnum():
	if 'PHPSESSID' in session：
		s = requests.Session()
		jar = requests.cookies.RequestsCookieJar()
		jar.set('PHPSESSID',session.get('PHPSESSID'),domain='210.35.251.243',path='/')
		rnum = s.get('http://210.35.251.243/reader/book_hist.php',cookies=jar)
		mess = BeautifulSoup(rnum.text,'lxml')
		booknums = mess.find_all("td",{"bgcolor":"#FFFFFF","class":"whitetext","width":"5%"})
		if booknum:
			booknum = booknums[-1].get_text()
			return jsonify({'booknum':booknum})
		else:
			return jsonify({'booknum':0})
	else:
    		return jsonify({'status':'error'})

@app.route('/api/getpercent')
def getpercent():
	if 'PHPSESSID' in session：
		s = requests.Session()
		jar = requests.cookies.RequestsCookieJar()
		jar.set('PHPSESSID',session.get('PHPSESSID'),domain='210.35.251.243',path='/')
		rhomeurl = "http://210.35.251.243/reader/redr_info.php"
		homepage = s.get(homeurl,cookies=jar)
		pagemess = BeautifulSoup(homepage.text,'lxml')
		percent = pagemess.find("h2",{"class":"h2"}).find("span",{"class":"Num"}).get_text()
    		return jsonify({'percent':percent})
    	else:
    		return jsonify({'status':'error'})

@app.route('/api/gettime')
def gettime():
	if 'PHPSESSID' in session：
		s = requests.Session()
		jar = requests.cookies.RequestsCookieJar()
		jar.set('PHPSESSID',session.get('PHPSESSID'),domain='210.35.251.243',path='/')
		hisurl = "http://210.35.251.243/reader/book_lst.php"
		hispage = s.get(hisurl,cookies=jar)
		hismess = BeautifulSoup(hispage.text,'lxml')
		date_tag_list = hismess.find_all("td",{"class":"whitetext","width":"13%"})
		tag_list = []
		for char in date_tag_list:
			tag_list.append(char.get_text())
			z = 1
		str_date_list = []
		while z <= len(tag_list)-1:
			str_date = tag_list[z]
			str_date_list.append(str_date.split("-"))
			z = z+3
		day_list = []
		for l in str_date_list:
			t = datetime.datetime(int(l[0]),int(l[1]),int(l[2]),0,0,0)
			limit_time = time.mktime(t.timetuple())
			nowtime = time.time()
			ti = limit_time - nowtime
			day = ti//86400
			day_list.append(int(day))
		if day_list:
			min_time = day_list[0]
			for x in day_list[1:]:
				if x < min_time:
					min_time = x
			return jsonify({'time':min_time})
		else:
			return jsonify({'time':None})
	else:
		return jsonify({'status':'error'})

@app.route('/web/<string:web>')
def index(web):
    return render_template(web)

@app.route('/css/<string:css>')
def css(css):
	f.open('css/' + css,"rb")
	a = f.read()
	f.close()
	return a

@app.route('/js/<string:js>')
def js(js):
	f.open('js/' + js,"rb")
	a = f.read()
	f.close()
	return a

if __name__ == '__main__':
    app.run()
