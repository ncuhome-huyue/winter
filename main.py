from flask import Flask,jsonify,session,redirect,url_for,render_template,request,make_response
import re,time,json
from sqlite3 import *
import random
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = '~\xc8\xc6\xe0\xf3,\x98O\xa8z4\xfb=\rNd'

@app.route('/api/getbook',methods=['POST'])
def search(word,school,page_num,bo_ok_num):
    school_num = {'前湖校区':'01','前湖医学':'06','所有校区':'ALL','青山湖北区':'03','青山湖南区':'05','东湖校区':'02','院系资料室':'07','总管':'00'}
    num_ber = school_num[request.json('school')]
    page_url = 'http://210.35.251.243/opac/openlink.php'
    params_l = {
                'dept':num_ber,
                'title':request.json('word'),
                'doctype':'ALL',
                'lang_code':'ALL',
                'match_flag':'forward',
                'displaypg':'20',
                'showmode':'list',
                'orderby':'DESC',
                'sort':'CATA_DATE',
                'onlylendable':'no',
                'count':request.json('bo_ok_num'),
                'with_ebook':'on',
                'page':request.json('page_num'),
                }
    soup = requests.get( page_url , params = params_l )
    page_L_result = BeautifulSoup(soup.text,'lxml')
    titles_L = page_L_result.select('#search_book_list > li > h3')
    kejies_L = page_L_result.select('#search_book_list > li > p > span')
    booknums_L = page_L_result.select('strong.red')[0].get_text()
    z_L = []
    for ke_L in kejies_L:
        l = []
        all_m = ke_L.get_text(strip = True)
        sp = all_m.split('：')
        sp2 = sp[1].split('可')[0]
        left = sp[2] + '/' + sp2
        if int(sp[2]) != 0:
            whe = '可借'
        else:
            whe = '无书'
        l.append(left)
        l.append(whe)
        z_L.append(l)
    names_TPS_L = []
    for t in titles_L:
        name_TP = []
        all_t = t.get_text()
        split_title = all_t.split('.',1)[-1]
        book_name = split_title.split()
        nx = 0
        fi_book_na = ''
        while nx <= (len(book_name)-2):
            fi_book_na = fi_book_na + book_name[nx]
            nx =nx + 1
        name_TP.append(fi_book_na)
        name_TP.append(book_name[-1])
        names_TPS_L.append(name_TP)
    all_messages_book_L = []
    nnu = 0
    while nnu <= (len(names_TPS_L)-1):
        ms_book = []
        ms_book.append(names_TPS_L[nnu][0])
        ms_book.append(names_TPS_L[nnu][1])
        ms_book.append(z_L[nnu][0])
        ms_book.append(z_L[nnu][1])
        all_messages_book_L.append(ms_book)
        nnu = nnu + 1
    return jsonify({'data':all_messages_book_L})

@app.route('/api/postzancai',methods=['POST'])
def postzancai():
	if 'username' in session:
		conn = connect('sql/zan_and_cai.db')
		c = conn.cursor()
		c.execute(r"SELECT kind FROM COMPANY WHERE pl_id = '%s' AND fromID = '%s';"%(request.json('pl_id'),session.get('username')))
		kind = c.fetchall()
		if kind:
			conn.close()
			return jsonify({'state':'have'})
		else:
			post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			c.execute(r"INSERT INTO COMPANY VALUES ('%s','%s','%s','%s','%s')"%(request.json('pl_id'),request.json('kind'),request.json('book_id'),session.get('username'),post_time))
			conn.commit()
			conn.close()
			return jsonify({'state':'success'})
	else:
		return jsonify({'state':'error'})
	
@app.route('/api/postpinglun',methods=['POST'])
def postzancai():
	if 'username' in session:
		conn = connect('sql/pinglun.db')
		c = conn.cursor()
		post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		c.execute(r"INSERT INTO COMPANY VALUES ('%d','%s','%s','%s','%s',%d,%d)"%(time.time(),request.json('pl'),request.json('book_id'),session.get('username'),post_time,0,0))
		conn.commit()
		conn.close()
		return jsonify({'state':'success'})
	else:
		return jsonify({'state':'error'})

@app.route('/api/getpinglun/<string:bookID>')
def getpinglun(bookID):
	if 'username' in session:
		conn = connect('sql/pinglun.db')
		c = conn.cursor()
		c.execute(r"SELECT pl_id,pl,fromID,time,zan,cai FROM COMPANY WHERE bookID = '%s';"%(bookID))
		pl_content = c.fetchall()
		conn.close()
		conn = connect('sql/zan_and_cai.db')
		c = conn.cursor()
		for x in range(pl_content):
			c.execute(r"SELECT kind FROM COMPANY WHERE pl_id = '%s' AND fromID = '%s';"%(pl_content[x][0],session.get('username')))
			kind = c.fetchall()
			if kind:
				pl_content[x].append(kind[0][0])
			else:
				pl_content[x].append(None)
		conn.close()
		return jsonify({'data':pl_content})
	else:
		return jsonify({'state':'error'})

@app.route('/api/postzancai',methods=['POST'])
def postzancai():
	if 'username' in session:
		conn = connect('sql/zan_and_cai.db')
		c = conn.cursor()
		c.execute(r"SELECT kind FROM COMPANY WHERE pl_id = '%s' AND fromID = '%s';"%(request.json('pl_id'),session.get('username')))
		kind = c.fetchall()
		if kind:
			conn.close()
			return jsonify({'state':'have'})
		else:
			post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			c.execute(r"INSERT INTO COMPANY VALUES ('%s','%s','%s','%s','%s')"%(request.json('pl_id'),request.json('kind'),request.json('book_id'),session.get('username'),post_time))
			conn.commit()
			conn.close()
			return jsonify({'state':'success'})
	else:
		return jsonify({'state':'error'})

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
	resp = make_response(picture.content)
	resp.set_cookie('PHPSESSID', cookie)
	return resp

@app.route('/api/login',methods=['POST'])
def login():
        s = requests.Session()
        jar = requests.cookies.RequestsCookieJar()
        jar.set('PHPSESSID',request.cookies.get('PHPSESSID'),domain='210.35.251.243',path='/')
        loginurl = "http://210.35.251.243/reader/redr_verify.php"
        payload = {"number":request.json['username'],"passwd":request.json['password'],"captcha":request.json["yanzheng"],"select":"cert_no","retrunUrl":""}
        login = s.post(loginurl , data = payload , cookies=jar)
        napage = s.get("http://210.35.251.243/reader/redr_info.php", cookies=jar)
        na = BeautifulSoup(napage.text,'html.parser')
        library_name = na.find("span",{"class":"profile-name"}).get_text()
        if library_name is not None:
                session['username'] = request.json['username']
                return jsonify({'status':'success','name':library_name})
        else:
                return jsonify({'status':'error'})

@app.route('/api/readnum')
def readnum():
	if request.cookies.get('PHPSESSID'):
		s = requests.Session()
		jar = requests.cookies.RequestsCookieJar()
		jar.set('PHPSESSID',request.cookies.get('PHPSESSID'),domain='210.35.251.243',path='/')
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
	if request.cookies.get('PHPSESSID'):
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
	if request.cookies.get('PHPSESSID'):
		s = requests.Session()
		jar = requests.cookies.RequestsCookieJar()
		jar.set('PHPSESSID',request.cookies.get('PHPSESSID'),domain='210.35.251.243',path='/')
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
	
@app.route('/api/getnowbook')
def getnowbook():
	if request.cookies.get('PHPSESSID'):
		s = requests.Session()
		jar = requests.cookies.RequestsCookieJar()
		jar.set('PHPSESSID',request.cookies.get('PHPSESSID'),domain='210.35.251.243',path='/')
		hisurl = "http://210.35.251.243/reader/book_lst.php"
		hispage = s.get(hisurl,cookies=jar)
		hismess = BeautifulSoup(hispage.text,'lxml')
		hisbooks = hismess.find_all("a",{"class":"blue"})
		cz = hismess.find_all("input",{"class":"btn btn-success"})
		ln = 0
		lm = 1
		book_date = []
		while ln < len(hisbooks):
			newl = []
			newl.append(hisbooks[ln].get_text())
			newl.append(tag_list[lm])
			if cz[ln].attrs['value'] == '续借':
				newl.append('未续借')
			else:
				newl.append(cz[ln].attrs['value'])
			book_date.append(newl)
			ln = ln + 1
			lm = lm + 3
		return jsonify({'data':book_date})
	else:
		return jsonify({'status':'error'})

@app.route('/api/getmycollection')
def getmycollection():
       if 'username' in session:
              conn = connect('collection.db')
              c = conn.cursor()
              c.execute(r"SELECT bookname,bookID FROM COMPANY WHERE usernameID = '%s'"%(session.get('username')))
              data = c.fetchall()
              conn.close()
              return jsonify({'data':data})
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
if __name__ == '__main__':
    app.run()

