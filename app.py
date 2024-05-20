from flask import Flask, session, render_template, request, redirect, url_for, jsonify
import os, folium
import mariadb
from time import sleep
from functools import wraps

while True:
    try:
        conn = mariadb.connect(
            user="root",
            password="example",
            host="127.0.0.1",
            port=3306,
            database="aplikacja_turystyczna",
            autocommit=True
        )
        break
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sleep(3)

cur = conn.cursor()
app = Flask(__name__)

def login_required(func):
    @wraps(func)
    def secure_function(*args,**kwargs):
        if 'id' not in session and 'logged_in' not in session:
            return redirect(url_for('app_login'))
        return func(*args, **kwargs)
    return secure_function

@app.route("/")
def home():
    if not session.get('logged_in'):
        return redirect(url_for('app_login'))
    else:
        return redirect(url_for('map'))

@app.route('/login', methods=['POST','GET'])
def app_login():
    if request.method == 'GET':
        return render_template('login.html')
    if session.get('logged_in'):
        return redirect(url_for('map'))
    if 'login' in request.form and 'password' in request.form:
        login = request.form['login']
        password = request.form['password']
        cur.execute('SELECT * FROM user WHERE login = %s and password = %s',(login, password))
        acc = cur.fetchone()
        if acc:
            session['logged_in'] = True
            session['id'] = acc[0]
    return home()

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' and 'nickname' in request.form and 'login' in request.form and 'password' in request.form:
        nickname = request.form['nickname']
        login = request.form['login']
        password = request.form['password']
        cur.execute('SELECT * FROM user WHERE nickname = %s OR login = %s',(nickname, login))
        acc = cur.fetchone()
        if acc:
            return render_template('register.html')
        elif not nickname or not login or not password:
            return render_template('register.html')
        else:
            cur.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)',(nickname, login, password))
            cur.execute('SELECT * FROM user WHERE login=%s',(login,))
            session['logged_in'] = True
            session['id'] = cur.fetchone()[0]
            return redirect(url_for('map'))
    return render_template('register.html')

@app.route("/map")
@login_required
def map():
    cur.execute("""SELECT p.id, p.name, p.latitude, p.longitude
                FROM poi p
                JOIN user_poi u on p.id = u.poi_id
                WHERE u.user_id = %s""",(session['id'],))
    loc = cur.fetchall()
    start_coords = (51.1, 17.03333)
    m = folium.Map(location = start_coords, zoom_start = 13)
    for l in loc:
        folium.Marker(location=[l[2],l[3]], popup = f'<a href=/location/{l[0]}>{l[1]}</a>').add_to(m)
    m.get_root().width = "100%"
    m.get_root().height = "100%"
    iframe = m.get_root()._repr_html_()
    return render_template('map.html', iframe=iframe)

@app.route("/scoreboard")
@login_required
def scoreboard():
    cur.execute("""SELECT u.nickname, COUNT(p.user_id) AS points, RANK() OVER (ORDER BY points DESC) AS position
                FROM user u
                LEFT JOIN user_poi p ON u.id = p.user_id
                GROUP BY u.id
                ORDER BY points DESC;""")
    rankings = cur.fetchall()
    return render_template("scoreboard.html",rankings=rankings)

@app.route("/profile")
@login_required
def profile():
    cur.execute("""SELECT u.nickname, COUNT(p.user_id) AS points, RANK() OVER (ORDER BY points DESC) AS position
                FROM user u
                LEFT JOIN user_poi p ON u.id = p.user_id
                WHERE u.id = %s
                GROUP BY u.id""",(session['id'],))
    acc = cur.fetchone()

    cur.execute("""SELECT description
                FROM user_achievements ua
                JOIN user u
                ON ua.user_id = u.id
                JOIN achievements a
                ON a.id = ua.achievements_id
                WHERE ua.user_id= %s""",(session['id'],))
    achievements = cur.fetchall()
    return render_template("profile.html",acc=acc, achievements=achievements)

@app.route("/scanner", methods=['POST', 'GET'])
@login_required
def scanner():
    if request.method == 'POST' and 'qr_code' in request.form:
        cur.execute('SELECT id FROM poi WHERE name = %s',(request.form['qr_code'],))
        loc = cur.fetchone()
        if loc:
            cur.execute('SELECT * FROM user_poi WHERE poi_id = %s AND user_id = %s',(loc[0],session['id']))
            if not cur.fetchone():
                cur.execute('INSERT INTO user_poi VALUES(%s,%s);',(loc[0],session['id']))
                cur.execute('INSERT INTO user_achievements VALUES(%s,%s)',(session['id'],loc[0]))
            return redirect(url_for('map'))
    return render_template("scanner.html")

@app.route("/location/<int:location_id>", methods=['POST','GET'])
@login_required
def location(location_id):
    cur.execute("SELECT * FROM user_poi WHERE user_id = %s AND poi_id = %s",(session['id'],location_id))
    if not cur.fetchone():
        return redirect(url_for('map'))
    if request.method == "POST" and 'comment' in request.form:
        cur.execute('INSERT INTO comments VALUES (NULL, %s)', (request.form['comment'],))
        cur.execute('SELECT MAX(id) FROM comments')
        latest_id = cur.fetchone()[0]
        cur.execute('INSERT INTO user_comments_poi VALUES (%s, %s, %s);', (session['id'], location_id, latest_id))
        return redirect(url_for('location', location_id=location_id))

    cur.execute("SELECT * FROM poi WHERE id = %s",(location_id,))
    loc = cur.fetchone()

    cur.execute("SELECT user_id FROM user_poi WHERE user_id = %s",(session["id"],))
    if cur.fetchone():
        been_here="Tak"
    else:
        been_here="Nie"

    cur.execute("SELECT nickname FROM user WHERE id = %s",(session["id"],))
    nickname = cur.fetchone()[0]

    cur.execute("""SELECT description AS comment, nickname
                    FROM comments
                    JOIN user_comments_poi
                    ON comments.id = user_comments_poi.comments_id
                    JOIN user
                    ON user_comments_poi.user_id = user.id
                    WHERE user_comments_poi.poi_id = %s""",(location_id,))
    comments = cur.fetchall()

    cur.execute("""SELECT (v.users_visited * 100.0 / u.users_all) AS percent
                FROM
                    (SELECT COUNT(id) AS users_all FROM user) AS u,
                    (SELECT COUNT(user_id) AS users_visited FROM user_poi WHERE poi_id=%s) AS v;""",(location_id,))
    percentage = cur.fetchone()[0]

    start_coords = (loc[4], loc[5])
    m = folium.Map(location = start_coords, zoom_start = 18)
    folium.Marker(location=[loc[4],loc[5]],popup=loc[1]).add_to(m)
    m.get_root().width = "100%"
    m.get_root().height = "100%"
    iframe = m.get_root()._repr_html_()

    return render_template('location.html',iframe=iframe, name=loc[1], address=loc[2], percentage=percentage , been_here=been_here, comments=comments, location_id=location_id, nickname=nickname)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(13)
    app.run(debug=True,host='0.0.0.0', port=8001, ssl_context='adhoc')
