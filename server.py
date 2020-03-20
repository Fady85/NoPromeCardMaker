from flask import (
    Flask, 
    make_response,
    render_template, 
    request, 
    redirect, 
    url_for,
    session as login_session
)
import os
import hmac
import time
import hashlib
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import pymysql.cursors

# app config
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jJHVDmN]LWX/,?RT'
app.debug = True
secret = b"s"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

USERNAME="flask"
PASSWORD="testing"
DATABASE="noprom"
HOST="localhost"
PORT="3306"
SOCKET="/var/run/mysqld/mysqld.sock"
"""maybe also use this? cursorclass=pymysql.cursors.DictCursor much cleaner
https://stackoverflow.com/questions/51235999/"""
user_ins = user(username=USERNAME, password=PASSWORD, database=DATABASE,host=HOST ,port=PORT,socket=SOCKET)
# returns a hash for given function
def haaash(w):
    h = hashlib.md5(w)
    x = h.hexdigest().encode('utf-8')
    h = hashlib.md5(x)
    return h.hexdigest()
####
# create secure value for a given value
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val.encode('utf-8')).hexdigest().encode('utf-8'))
####
# check if the secure value is valid or not
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
    else:
        return None
####
# check file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
####
@app.errorhandler(404)
def not_found(error=None):
    #do some error reporting and stuff
    return "404 Not found"

# Home Page
@app.route('/')
def home():
    return render_template('index.html')
####
"""maybe use the @login_required method instead?"""
@app.route('/login', methods=['GET']) 
def loginG():
    return render_template("login.html",alert="")
        

@app.route('/login', methods=['POST']) 
def login():
    if 'username' in request.form and 'password' in request.form:
        user = user_ins.login(
            password=haaash(str(request.form['password']).encode('utf-8')), 
            username=request.form['username']
        )
    if user:
        login_session['id'] = user[0]
        login_session['username'] = user[1]
        login_session['type'] = user[3]
        resp = make_response(redirect('/create_card'))
        resp.set_cookie('username', make_secure_val(user[1]))
        return resp
    else:
        return render_template("login.html",alert="Failed to login")

@app.route('/logout', methods=['GET'])
def logout():   
    login_session.clear()
    respond = make_response(redirect('/'))
    respond.set_cookie('username', '', expires=0)
    return respond

@app.route('/signup', methods=['POST'])
def panelUsers():
    name=request.form["name"]
    password=haaash(request.form["password"])
    email=request.form["email"]
    adU=user.addUser(email,name,password)
    if adU:
        return redirect("/login")
    else:
        return render_template("signup.html",alert="User Already Exists")

@app.route('/signup', methods=['GET'])
def panelUsers():
    return render_template("signup.html",alert="")
  
def handleImage(r):
    #handleImage(request.files['image'])
    if allowed_file(r.filename):
        file = r
        filename = secure_filename(r.filename)
        partnersLogospath='/static/img/products/'
        if os.path.exists(os.path.join(APP_ROOT + partnersLogospath, filename)):
            os.remove(os.path.join(APP_ROOT + partnersLogospath, filename))
        file.save(os.path.join(APP_ROOT + partnersLogospath, filename))
        FinalPath = 'img/products/' + filename
        return FinalPath
    else:
        return False

@app.route("/sitemap")
@app.route("/sitemap/")
def sitemap():
    links=[[url_for('home'),"index"]]
    resp=""
    for i in post_ins.getPosts():
        links.append([url_for('post',t=urlFromName(i[0])),i[0]])
    for i in product_ins.getProducts():
        links.append([url_for('products',product_id=i[0]),i[1]])
    for i in links:
        resp+="<a href={0}>{0}</a><br>".format(i[0],i[1])

    return resp
@app.route("/robots.txt")
@app.route("/robots.txt/")
def robots():
    return open("static/robots.txt",'r').read()
# Main Function To Run the App
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded = True)
