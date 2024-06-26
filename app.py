from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flasgger import Swagger
import os, folium, mariadb
from time import sleep
from functools import wraps

while True:
    try:
        conn = mariadb.connect(
            user="root",
            password="example",
            host="db",
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

swagger = Swagger(app,template={
    "info": {
        "title": "wroclaw_crispy_places docs",
        "description": "REST api endopints"
    }
})

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
    cur.execute("""WITH ranked_users AS
                (SELECT u.nickname, COUNT(p.user_id) AS points, RANK() OVER (ORDER BY points DESC) AS position, u.id as id
                FROM user u
                LEFT JOIN user_poi p ON u.id = p.user_id
                GROUP BY u.id)
                SELECT * FROM ranked_users WHERE id = %s""", (session['id'],))
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

    return render_template('location.html',iframe=iframe, name=loc[1], address=loc[2], description=loc[3], percentage=percentage , been_here=been_here, comments=comments, location_id=location_id, nickname=nickname)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    return home()

#REST api
@app.route('/api/signin', methods=['POST'])
def api_signin():
    """
    Login to service
    ---
    tags:
      - Authentication
    parameters:
    - in: query
      name: login
      type: string
      required: true
    - in: query
      name: password
      type: string
      required: true
    responses:
        200:
            description: Succesfuly logged into service
            schema:
                type: object
                properties:
                    message:
                        example: Logged in
                        type: string
        401:
            description: Invalid credentials
            schema:
                type: object
                properties:
                    message:
                        example: Invalid credentials
                        type: string

    """
    login = request.args.get('login')
    password = request.args.get('password')
    if not login or not password:
        return jsonify({'message': 'Invalid credentials'}), 401

    cur.execute('SELECT id FROM user WHERE login = %s and password = %s',(login, password))
    acc = cur.fetchone()
    if acc:
        session['id']=acc[0]
        session['logged_in']=True
        return jsonify({'message': 'Logged in'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/signup', methods=['POST'])
def api_signup():
    """
    Register to service
    ---
    tags:
      - Authentication
    parameters:
      - in: query
        name: login
        type: string
        required: true
      - in: query
        name: nickname
        type: string
        required: true
      - in: query
        name: password
        type: string
        required: true
    responses:
        200:
            description: Succesfuly created an user
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: User created
        400:
            description: Missing some parameter
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Missing password
        409:
            description: User already exists
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: User exists
    """
    nickname = request.args.get('nickname')
    login = request.args.get('login')
    password = request.args.get('password')
    if not password:
        return jsonify({'message': 'Missing password'}), 400
    elif not login:
        return jsonify({'message': 'Missing login'}), 400
    elif not nickname:
        return jsonify({'message': 'Missing nickname'}), 400
    cur.execute('SELECT * FROM user WHERE nickname = %s OR login = %s',(nickname, login))
    acc = cur.fetchone()
    if acc:
        return jsonify({'message': 'User exists'}), 409
    else:
        cur.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)',(nickname, login, password))
        return jsonify({'message': 'User created'}), 200


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """
    Logout from service
    ---
    tags:
      - Authentication
    responses:
        200:
            description: Logged out
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Logged out
    """
    session.pop('logged_in', None)
    session.pop('id', None)
    return jsonify({'message': 'Logged out'}),200

@app.route('/api/location' , methods=['GET'])
def api_get_location():
    """
    Get informations about location
    ---
    tags:
      - Locations
    summary: Returns informations about location
    parameters:
    - in: query
      name: location_id
      type: string
      required: true
    responses:
        200:
            description: Returns location information succesfuly
            schema:
                type: object
                properties:
                    name:
                        type: string
                        example: ZOO Wrocław
                    address:
                        type: string
                        example: Zygmunta Wróblewskiego 1-5, 51-618
                    been_here:
                        type: string
                        example: Tak
                    percentage:
                        type: string
                        example: 50.0
                    comments:
                        type: array
                        items:
                            type: object
                            properties:
                                comment:
                                    type: string
                                    example: I love this place
                                user:
                                    example: Tester
                                    type: string
        400:
            description: Missing something in request
            schema:
                type: object
                properties:
                    message:
                        example: Missing location_id
                        type: string
        401:
            description: Unauthorized
            schema:
                type: object
                properties:
                    message:
                        example: Unauthorized
                        type: string

    """
    if not 'logged_in' in session:
        return jsonify({'message': "Unauthorized"}), 401
    location_id = request.args.get('location_id')
    if not location_id:
        return jsonify({'message': 'Missing location_id'}), 400

    cur.execute("SELECT * FROM user_poi WHERE user_id = %s AND poi_id = %s",(session['id'],location_id))
    loc = cur.fetchone();
    if not loc:
        return jsonify({'message': 'Unauthorized'}), 401

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
    comments = [{'comment': c[0], 'user': c[1]} for c in comments]

    cur.execute("""SELECT (v.users_visited * 100.0 / u.users_all) AS percent
                FROM
                    (SELECT COUNT(id) AS users_all FROM user) AS u,
                    (SELECT COUNT(user_id) AS users_visited FROM user_poi WHERE poi_id=%s) AS v;""",(location_id,))
    percentage = cur.fetchone()[0]
    return jsonify({'name':loc[1], 'address':loc[2], 'percentage':percentage, 'been_here':been_here, 'comments':comments})

@app.route('/api/location', methods=['POST'])
def api_post_location():

    """
    Put comment into location's discusion
    ---
    tags:
      - Locations
    parameters:
    - in: query
      name: location_id
      type: string
      required: true
    - in: query
      name: comment
      type: string
      required: true
    responses:
        200:
            description: Succesfuly commented under location
            schema:
                type: object
                properties:
                    message:
                        example: Comment succesfuly posted
                        type: string
        400:
            description: Missing data in request body
            schema:
                type: object
                properties:
                    message:
                        example: Missing location_id
                        type: string
        401:
            description: Unauthorized
            schema:
                type: object
                properties:
                    message:
                        example: Unauthorized
                        type: string
    """

    if not 'logged_in' in session:
        return jsonify({'message': "Unauthorized"}), 401
    location_id = request.args.get('location_id')
    if not location_id:
        return jsonify({'message': 'Missing location_id'}), 400

    cur.execute("SELECT * FROM user_poi WHERE user_id = %s AND poi_id = %s",(session['id'],location_id))
    loc = cur.fetchone();
    if not loc:
        return jsonify({'message': 'Unauthorized'}), 401

    comment = request.args.get('comment')
    if not comment:
        return jsonify({'message': 'Missing comment'}), 400

    cur.execute('INSERT INTO comments VALUES (NULL, %s)', (comment,))
    cur.execute('SELECT MAX(id) FROM comments')
    latest_id = cur.fetchone()[0]
    cur.execute('INSERT INTO user_comments_poi VALUES (%s, %s, %s);', (session['id'], location_id, latest_id))
    return jsonify({'message': 'Comment succesfuly posted'}), 200

@app.route('/api/scoreboard', methods=['GET'])
def api_scoreboard():
    """
    Get a ranking of users
    ---
    tags:
      - Users
    responses:
        200:
            description: Ranking of users
            schema:
                type: object
                properties:
                    rankings:
                        type: array
                        items:
                            type: object
                            properties:
                                place:
                                    type: integer
                                    example: 1
                                points:
                                    type: integer
                                    example: 1
                                user:
                                    type: string
                                    example: Tester
        401:
            description: Unauthorized request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Unauthorized
    """
    if not 'logged_in' in session:
        return jsonify({'message': 'Unauthorized'}), 401
    cur.execute("""SELECT u.nickname, COUNT(p.user_id) AS points, RANK() OVER (ORDER BY points DESC) AS position
                FROM user u
                LEFT JOIN user_poi p ON u.id = p.user_id
                GROUP BY u.id
                ORDER BY points DESC;""")
    rankings = cur.fetchall()
    rankings = [{'user': r[0], 'points': r[1], 'place': r[2]} for r in rankings]
    return jsonify({'rankings': rankings}), 200

@app.route('/api/scanner', methods=['POST'])
def api_scanner():
    """
    Add user to location based on his qr code
    ---
    tags:
      - Users
    parameters:
      - in: query
        name: qr_code
        type: string
        required: true
    responses:
        200:
            description: Location added to user
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Location added to user succesfully
        400:
            description: Missing qr_code
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Missing qr_code
        401:
            description: Unauthorized request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Unauthorized
        404:
            description: Location not found
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Location not found
    """
    if not 'logged_in' in session:
        return jsonify({'message': 'Unauthorized'}), 401
    qr_code = request.args.get('qr_code')
    if not qr_code:
        return jsonify({'message': 'Missing qr_code'}), 400
    cur.execute('SELECT id FROM poi WHERE name = %s',(qr_code,))
    loc = cur.fetchone()
    if loc:
        cur.execute('SELECT * FROM user_poi WHERE poi_id = %s AND user_id = %s',(loc[0],session['id']))
        if not cur.fetchone():
            cur.execute('INSERT INTO user_poi VALUES(%s,%s);',(loc[0],session['id']))
            cur.execute('INSERT INTO user_achievements VALUES(%s,%s)',(session['id'],loc[0]))
            return jsonify({'message': 'Location added to user succesfully'}), 200
        else:
            return jsonify({'message': 'Location already added to user'}), 200

    return jsonify({'message': 'Location not found'}), 404

@app.route("/api/profile", methods=['GET'])
def api_profile():
    """
    Get informations and achievements of logged in user
    ---
    tags:
      - Users
    responses:
        200:
            description: Informations about user that is logged in
            schema:
                type: object
                properties:
                    account:
                        type: object
                        properties:
                            place:
                                type: integer
                                example: 1
                            points:
                                type: integer
                                example: 1
                            user:
                                type: string
                                example: Tester
        401:
            description: Unauthorized request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Unauthorized
    """
    if not 'logged_in' in session:
        return jsonify({'message': 'Unauthorized'}), 401

    cur.execute("""WITH ranked_users AS
                (SELECT u.nickname, COUNT(p.user_id) AS points, RANK() OVER (ORDER BY points DESC) AS position, u.id as id
                FROM user u
                LEFT JOIN user_poi p ON u.id = p.user_id
                GROUP BY u.id)
                SELECT * FROM ranked_users WHERE id = %s""",(session['id'],))
    acc = cur.fetchone()
    acc = {'user': acc[0] , 'points': acc[1], 'place': acc[2]}

    cur.execute("""SELECT description
                FROM user_achievements ua
                JOIN user u
                ON ua.user_id = u.id
                JOIN achievements a
                ON a.id = ua.achievements_id
                WHERE ua.user_id= %s""",(session['id'],))
    achievements = cur.fetchall()
    achievements = [a[0] for a in achievements]
    return jsonify({'account': acc, 'achievements': achievements}), 200

if __name__ == "__main__":
    app.config['SECRET_KEY'] = os.urandom(13)
    app.run(debug=True,host='0.0.0.0', port=8000)
