import sqlite3, datetime
from flask import Blueprint, request
puush = Blueprint('puush', __name__)
host = "http://img.merron.ru/"
sqlite = sqlite3.connect('server.db3', check_same_thread=False)
sqlcur = sqlite.cursor()


@puush.route('/api/auth', methods=['GET', 'POST'])
def puushauth():
  return "0,%s,,0" % request.form['k']

@puush.route('/api/hist', methods=['GET', 'POST'])
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
  
@puush.route('/api/up', methods=['GET', 'POST'])
def puushup():
  if request.method == 'POST':
    file = request.files['f']
    if file and allowed_file(file.filename):
      if request.form['k']!='public':
        key = request.form['k']
      else:
        key = app.config['GALLERY']
      filename = md5.new(str(random.random())+key).hexdigest()[:16]+"."+file.filename.rsplit('.', 1)[1]
      sqlcur.execute('INSERT INTO "main"."pic" ("key", "name") VALUES (?, ?)',(key, filename))
      sqlite.commit()
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      thumbnail(filename)
      return "0,"+host+filename+",190529312,0"
  else:
    return render_template("upload.html")