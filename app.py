from flask import Flask, session, render_template, request
import os, folium

app = Flask(__name__)

@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Jesteś zalogowany"

@app.route('/login', methods=['POST'])
def app_login():
    # Tymczasowy użytkownik, kiedy będzie możliwość zostanie to połączone z bazą
    if request.form['login'] == 'admin' and request.form['password'] == 'admin':
        session['logged_in'] = True
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

if __name__ == "__main__":
    app.secret_key = os.urandom(13)
    app.run(debug=True,host='0.0.0.0', port=8000, ssl_context='adhoc')
