from flask import Flask, session, render_template, request, redirect, url_for
import os, folium
import mariadb

try:
    conn = mariadb.connect(
        user="root",
        password="example",
        host="127.0.0.1",
        port=3306,
        database="aplikacja_turystyczna")
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
        cur.execute(f'SELECT * FROM user WHERE login = \'{request.form['login']}\' and password = \'{request.form['password']}\'')
        acc = cur.fetchone()
        if acc:
            session['logged_in'] = True
            session['id'] = acc[0]
    return home()

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
    return render_template("scoreboard.html")

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
    app.run(debug=True,host='0.0.0.0', port=8001, ssl_context='adhoc')
