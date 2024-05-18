from flask import Flask, session, render_template, request, redirect, url_for
import os, folium
import mariadb

try:
    conn = mariadb.connect(
        user="root",
        password="example",
        host="127.0.0.1",
        port=3306,
        database="aplikacja_turystyczna",
        )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
cur = conn.cursor()
app = Flask(__name__)

@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for('map'))

@app.route('/login', methods=['POST'])
def app_login():
    # Tymczasowy użytkownik, kiedy będzie możliwość zostanie to połączone z bazą
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
        cur.execute(f'SELECT * FROM user WHERE nickname = %s OR login = %s',(nickname, login))
        acc = cur.fetchone()
        if acc:
            return render_template('register.html')
        elif not nickname or not login or not password:
            return render_template('register.html')
        else:
            cur.execute(f'INSERT INTO user VALUES (NULL, %s, %s, %s)',(nickname, login, password))
            cur.execute(f'SELECT * FROM user WHERE login=%s',(login,))
            session['logged_in'] = True
            session['id'] = cur.fetchone()[0]
            return redirect(url_for('map'))
    return render_template('register.html')
# Powiąż to z map.html
@app.route("/map")
def map():
    start_coords = (51.1, 17.03333)
    m = folium.Map(location = start_coords, zoom_start = 13)
    m.get_root().width = "100%"
    m.get_root().height = "100%"
    iframe = m.get_root()._repr_html_()
    return render_template('map.html', iframe=iframe)

# szybkie podpięcie po możliwość podglądu strony; do edycji
@app.route("/scoreboard")
def scoreboard():
    cur.execute("""
        SELECT u.nickname, COUNT(p.user_id) AS points, RANK() OVER (ORDER BY points DESC) AS position
        FROM user_poi p
        JOIN user u ON u.id = p.user_id
        GROUP BY u.id
        ORDER BY points DESC;""")
    rankings = cur.fetchall()
    for rank in rankings:
        print(rank)
    return render_template("scoreboard.html",rankings=rankings)

# szybkie podpięcie po możliwość podglądu strony; do edycji
@app.route("/profile")
def profile():
    return render_template("profile.html")

# szybkie podpięcie po możliwość podglądu strony; do edycji
@app.route("/scanner")
def scanner():
    return render_template("scanner.html")

# szybkie podpięcie po możliwość podglądu strony; do edycji
@app.route("/location")
def location():
    start_coords = (51.1, 17.03333) # coordy adekwatne do klikniętego markera
    m = folium.Map(location = start_coords, zoom_start = 13)
    m.get_root().width = "100%"
    m.get_root().height = "100%"
    iframe = m.get_root()._repr_html_()
    return render_template('location.html', iframe=iframe)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(13)
    app.run(debug=True,host='0.0.0.0', port=8000, ssl_context='adhoc')
