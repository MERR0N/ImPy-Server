import os, sqlite3, md5, random
from PIL import Image, ImageOps
from flask import Flask, request, render_template, send_file, redirect

host = "http://i.merron.ru/"  # change to you server
sqlite = sqlite3.connect('server.db3', check_same_thread=False)
sqlcur = sqlite.cursor()

UPLOAD_FOLDER = './uploads' # folder for uploads
THUMB_FOLDER = './uploads/t' # folder for thumbnails
GALLERY = '0b74f17c8b1d6e3ba9e24afea8be7de8' # id for public gallery


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMB_FOLDER'] = THUMB_FOLDER
app.config['GALLERY'] = GALLERY

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def welcome():
  return render_template('welcome.html')

@app.route('/<file>')
def img(file):
  file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
  if os.path.isfile(file_path):
    sqlcur.execute('UPDATE "main"."pic" SET views = views + 1 WHERE name = ?',(file,))
    sqlite.commit()
    return send_file(file_path, mimetype='image/jpeg')
  else: 
    return render_template('404.html'), 404
    
@app.route('/t/<file>')
def thumbimg(file):
  file_path = os.path.join(app.config['THUMB_FOLDER'], file)
  if os.path.isfile(file_path):
    return send_file(file_path, mimetype='image/jpeg')
  else: 
    return render_template('404.html'), 404
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    file = request.files['file']
    if file and allowed_file(file.filename) and request.form['key']:
      if request.form['key']!='public':
        key = request.form['key']
      else:
        key = app.config['GALLERY']
      filename = md5.new(str(random.random())+key).hexdigest()[:6]+"."+file.filename.rsplit('.', 1)[1]
      sqlcur.execute('INSERT INTO "main"."pic" ("key", "name") VALUES (?, ?)',(key, filename))
      sqlite.commit()
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      thumbnail(filename)
      return filename
  else:
    return render_template("upload.html")
    
@app.route('/list/<userkey>/')
@app.route('/list/<userkey>/<int:page>/')
def list_files(userkey, page=0, pfrom = 0, pto = 40):
  if (page > 0): pfrom = (page - 1)*pto
  sqlcur.execute('SELECT count(*) FROM "main"."pic" WHERE key = ?',(userkey,))
  count_pic = sqlcur.fetchall()
  count_page = (count_pic[0][0]//pto)+2
  
  sqlcur.execute('SELECT * FROM "main"."pic" WHERE key = ? LIMIT ?,?',(userkey,pfrom,pto))
  result = sqlcur.fetchall()
  if(result):
    return render_template('list.html', result=result, userkey=userkey, count_page = count_page)
  return render_template('404.html'), 404  

@app.route('/mlist/<userkey>/')
def mlist_files(userkey):
  sqlcur.execute('SELECT * FROM "main"."pic" WHERE key = ?',(userkey,))
  result = sqlcur.fetchall()
  if(result):
    list = ""
    for row in result:
      list += row[2]+":"
    return list.rstrip()
  return render_template('404.html'), 404  

@app.route('/gallery/')
def gallery(page=0, pfrom = 0, pto = 50):
  if (page > 0): pfrom = (page - 1)*pto
  sqlcur.execute('SELECT count(*) FROM "main"."pic" WHERE key = ?',(app.config['GALLERY'],))
  count_pic = sqlcur.fetchall()
  count_page = count_pic[0][0]//pto
  
  sqlcur.execute('SELECT * FROM "main"."pic" WHERE key = ? LIMIT ?,?',(app.config['GALLERY'],pfrom,pto))
  result = sqlcur.fetchall()
  if(result):
    return render_template('list.html', result=result, userkey='public',count_page = count_page)
  return render_template('404.html'), 404  

@app.route('/del/<userkey>/<filename>')
def delete_file(userkey,filename):
  sqlcur.execute('DELETE FROM "main"."pic" WHERE key = ? AND name = ?',(userkey,filename))
  sqlite.commit()
  os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  os.remove(os.path.join(app.config['THUMB_FOLDER'], filename))
  return 'ok'

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404  

def thumbnail(filename):
  file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  if os.path.isfile(file_path):
    ImageOps.fit(Image.open(file_path), (200,200), Image.ANTIALIAS).save(os.path.join(app.config['THUMB_FOLDER'], filename))

###
    
@app.route('/api/auth', methods=['GET', 'POST'])
def puushauth():
  return "0,%s,,0" % request.form['k']

@app.route('/api/hist', methods=['GET', 'POST'])
def puushhist():
  userkey = request.form['k']
  sqlcur.execute('SELECT * FROM "main"."pic" WHERE key = ? LIMIT 0,10',(userkey,))
  result = sqlcur.fetchall()
  if(result):
    list = "0\n"
    for row in result:
        list += str(row[0])+","+str(datetime.datetime.fromtimestamp(int(row[4])).strftime('%Y-%m-%d %H:%M:%S'))+","+str(host)+str(row[2])+","+str(row[2])+","+str(row[3])+",0\n"
        return list
  return ""  
  
@app.route('/api/up', methods=['GET', 'POST'])
def puushup():
  if request.method == 'POST':
    file = request.files['f']
    if file and allowed_file(file.filename):
      if request.form['k']!='public':
        key = request.form['k']
      else:
        key = app.config['GALLERY']
      filename = md5.new(str(random.random())+key).hexdigest()[:6]+"."+file.filename.rsplit('.', 1)[1]
      sqlcur.execute('INSERT INTO "main"."pic" ("key", "name") VALUES (?, ?)',(key, filename))
      sqlite.commit()
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      thumbnail(filename)
      return "0,"+host+filename+",190529312,0"
  else:
    return render_template("upload.html")

@app.route('/login/go/', methods=['GET', 'POST'])
def puushlogin():
  if request.args.get('k')!='':
    key = request.args.get('k')
    return redirect(host+"/list/"+key)
  return render_template('404.html'), 404  
###    
   
if __name__ == "__main__":
  app.run(host='localhost',port=3000)