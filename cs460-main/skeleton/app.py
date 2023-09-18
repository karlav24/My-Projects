######################################
# author ben lawson <balawson@bu.edu>
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login
import itertools
#for image uploading
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cellogod93!'
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users")
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd
	return user

'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
			   <form action='login' method='POST'>
				<input type='text' name='email' id='email' placeholder='email'></input>
				<input type='password' name='password' id='password' placeholder='password'></input>
				<input type='submit' name='submit'></input>
			   </form></br>
		   <a href='/'>Home</a>
			   '''
	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file
	#change
	#
	#information did not match
	return "<a href='/login'>Try again</a>\
			</br><a href='/register'>or make an account</a>"

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return render_template('hello.html', message='Logged out')

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html')

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html', supress='True')

@app.route("/register", methods=['POST'])
def register_user():
	try:
		email=request.form.get('email')
		password=request.form.get('password')
		dob = request.form.get('dob')
		hometown = request.form.get('hometown')
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		gender = request.form.get('gender')

	except:
		print("couldn't find all tokens") #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		print(cursor.execute("INSERT INTO Users (email, password, dob, hometown, fname, lname, gender) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(email, password, dob, hometown, fname, lname, gender)))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('hello.html', name=email, message='Account Created!')
	else:
		print("couldn't find all tokens")
		return flask.redirect(flask.url_for('register'))

def getUsersPhotos(uid):
	cursor = conn.cursor()
	cursor.execute("""SELECT Pictures.imgdata, Pictures.picture_id, Pictures.caption, Pictures.album_id, Albums.aname, COUNT(Likes.user_id) AS num_likes
	FROM Pictures
	JOIN Albums ON Pictures.album_id = Albums.album_id
	LEFT JOIN Likes ON Pictures.picture_id = Likes.picture_id
	WHERE Pictures.user_id = '{0}'
	GROUP BY Pictures.picture_id""".format(uid))
	return cursor.fetchall() #NOTE return a list of tuples, [(imgdata, pid, caption), ...] 
	#chloe updated to [(imgdata, pid, caption, album_id, aname, num_likes), ...]

def getUsersAlbums(uid):
	cursor = conn.cursor()
	cursor.execute("""
        SELECT Albums.album_id, Albums.aname, MIN(Pictures.picture_id), MIN(Pictures.caption), MIN(Pictures.imgdata)
        FROM Albums
        LEFT JOIN (
            SELECT album_id, picture_id, caption, imgdata
            FROM Pictures
        ) AS Pictures ON Albums.album_id = Pictures.album_id
        WHERE Albums.user_id = '{0}'
		GROUP BY Albums.album_id, Albums.aname
    """.format(uid))
	return cursor.fetchall()

#gets specific content from one album, aname
def getUserAlbum(aid):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id, caption, Pictures.album_id, aname FROM Pictures JOIN Albums ON Pictures.album_id = Albums.album_id WHERE Pictures.album_id = '{0}'".format(aid))
	return cursor.fetchall() # return a list of tuples, [(imgdata, pid, caption), ...] 
	#chloe updated to [(imgdata, pid, caption, album_id, aname), ...])

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]
def getAIDfromaname(aname):
	cursor = conn.cursor()
	cursor.execute("SELECT album_id  FROM Albums WHERE aname = '{0}'".format(aname))
	return cursor.fetchone()[0]

def getanamefromAID(AID):
	cursor = conn.cursor()
	cursor.execute("SELECT aname FROM Albums WHERE album_id = '{0}'".format(AID))
	return cursor.fetchone()[0]

def getTAGidfromname(name):
	cursor = conn.cursor()
	cursor.execute("SELECT tag_id  FROM Tags WHERE name = '{0}'".format(name))
	return cursor.fetchone()[0]

def getUserFullName(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT fname, lname FROM Users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    return (result[0], result[1]) if result else None

def get_most_recent_picture_id_for_user(user_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(picture_id) FROM Pictures WHERE user_id = %s
    """, (user_id,))
    return cursor.fetchone()[0]

def getUserFriends(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT UID2, fname, lname FROM Friendship JOIN Users ON UID2 = Users.user_id WHERE UID1 = '{0}'".format(uid))
	return cursor.fetchall()

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)):
		#this means there are greater than zero entries with that email
		return False
	else:
		return True
#end login code

def getTop3Tags():
	cursor = conn.cursor()
	cursor.execute("SELECT Tags.name, COUNT(*) AS num_photos FROM Tagged INNER JOIN Tags ON Tagged.tag_id = Tags.tag_id GROUP BY Tagged.tag_id ORDER BY num_photos DESC LIMIT 3; ".format())
	return cursor.fetchall()


@app.route('/profile')
@flask_login.login_required
def protected():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile", albums = getUsersAlbums(uid), photos = getUsersPhotos(uid), toptags = getTop3Tags(),base64=base64 )

#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		caption = request.form.get('caption')
		aname = request.form.get('aname')
		tags = request.form.get('tags')
		tags_split = tags.split()
		photo_data =imgfile.read()
		cursor = conn.cursor()
		#create new album if album does not already exist 
		cursor.execute('''INSERT INTO Albums (aname, user_id) SELECT %s, %s WHERE NOT EXISTS (SELECT * FROM Albums WHERE aname = %s AND user_id = %s)''', (aname,uid,aname,uid))
		album_id = getAIDfromaname(aname)
		cursor.execute('''INSERT INTO Pictures (imgdata, user_id, caption, album_id) VALUES (%s, %s, %s, %s)''', (photo_data, uid, caption, album_id))
		conn.commit()
		most_recent_picture_id = get_most_recent_picture_id_for_user(uid)
		for name in tags_split:
			cursor = conn.cursor()
			#create new tag if tag does not already exist
			cursor.execute('''INSERT INTO Tags (name) SELECT %s WHERE NOT EXISTS (SELECT * FROM Tags WHERE name = %s)''', (name,name))
			tag_id = getTAGidfromname(name)
			cursor.execute('''INSERT INTO Tagged (picture_id, tag_id) VALUES (%s, %s)''', (most_recent_picture_id, tag_id))
			conn.commit()
		return render_template('hello.html', name=flask_login.current_user.id, message='Photo uploaded!', photos=getUsersPhotos(uid), albums=getUsersAlbums(uid), toptags = getTop3Tags(), base64=base64)
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		return render_template('upload.html')
#end photo uploading code
@app.route("/search", methods=['POST'])
def search():
	search_term = request.form['searchYourTags']
	search_tags = search_term.split(' ')
	if flask_login.current_user.is_authenticated:
		uid = getUserIdFromEmail(flask_login.current_user.id)
	else:
		uid = None
	if uid == None:
		return render_template('search.html', matching_photos=None, base64=base64, Message="Please login to search", uid = uid)
	placeholders = ', '.join(['%s'] * len(search_tags))
	query = f"""
        SELECT *
        FROM Pictures
        WHERE picture_id IN (
            SELECT picture_id
            FROM tagged
            WHERE tag_id IN (
                SELECT tag_id
                FROM tags
                WHERE name IN ({placeholders})
            )
            GROUP BY picture_id
            HAVING COUNT(DISTINCT tag_id) = {len(search_tags)}
        )
        AND user_id = %s
    """
	params = search_tags + [uid]
	cursor.execute(query, params)
	photos = cursor.fetchall()
	return render_template('search.html', matching_photos=photos, base64=base64, Message="No Photos match your search", uid = uid)


def searchmaylike(uid,tags):
	#print(tags)
	cursor = conn.cursor()

    #picture_ids that match all tags
	subquery = f"""
        SELECT picture_id
        FROM tagged
        JOIN tags ON tagged.tag_id = tags.tag_id
        WHERE tags.name IN ({','.join(['%s']*len(tags))})
        GROUP BY picture_id
        HAVING COUNT(DISTINCT tags.name) = {len(tags)}
    """

    #photos with correct user_id
	sql_query = f"""
        SELECT *
        FROM Pictures
        WHERE picture_id IN ({subquery})
        AND user_id != %s
    """
	cursor.execute(sql_query, tuple(tags) + (uid,))

	photos = cursor.fetchall()

	return photos

@app.route("/searchall", methods=['POST'])
def searchall():
	if 'clickedTag' in request.form:
		search_term = request.form['clickedTag']
		cursor = conn.cursor()
		cursor.execute("""
    	SELECT *
    	FROM Pictures
    	WHERE picture_id IN (
        SELECT picture_id
        FROM tagged
        WHERE tag_id IN (
            SELECT tag_id
            FROM tags
            WHERE name = %s
        ) 
		
    	)
		""", (search_term))

		photos = cursor.fetchall()
		return render_template('search.html', matching_photos=photos, base64=base64)
	else:
		search_term = request.form['searchALLTags']
		tags = search_term.split()

	
	cursor = conn.cursor()

    # Generate a subquery to find all picture_ids that match any of the tags
	subquery = "(" + " OR ".join(["tag_id IN (SELECT tag_id FROM tags WHERE name = %s)"] * len(tags)) + ")"

	cursor.execute(f"""
    SELECT *
    FROM Pictures
    WHERE picture_id IN (
        SELECT picture_id
        FROM tagged
        WHERE {subquery}
    )
    """, tuple(tags))

	photos = cursor.fetchall()

	return render_template('search.html', matching_photos=photos, base64=base64)
#default page
@app.route("/", methods=['GET'])
def hello():
	return render_template('hello.html', message='Welecome to Photoshare')

@app.route("/viewAlbum", methods=['POST', 'GET'])
def viewAlbum():
	aidtoview = request.form['viewAlbum']
	aname = getanamefromAID(aidtoview)
	photos = getUserAlbum(aidtoview)
	return render_template('viewAlbum.html', photos = photos, aname = aname, base64=base64)

@app.route("/friends", methods=['GET'])
def friends():
	if flask_login.current_user.is_authenticated:
		addFriend = True
		uid = getUserIdFromEmail(flask_login.current_user.id)
		friends = getUserFriends(uid)
		name = getUserFullName(uid)
		friend_recommendation = getfriendRecommendation(uid)
		for i in friend_recommendation:
			if uid in i:
				friend_recommendation.remove(i)
	else: 
		friends = None
		uid = None
		real = None
		addFriend = False
	return render_template('friends.html', friends = friends, uid = uid, addFriend = addFriend, recommendations = friend_recommendation, base64=base64)

@app.route("/searchUsers", methods=['POST'])
def searchUsers():
	if flask_login.current_user.is_authenticated:
		uid = getUserIdFromEmail(flask_login.current_user.id)
		friends = getUserFriends(uid)
	else: 
		friends = None
	
	if request.method == 'POST':
		search_term = request.form['searchUsers']
		cursor = conn.cursor()
		cursor.execute("""
		SELECT fname, lname, user_id
		FROM Users
		WHERE fname = %s 
		""", (search_term))
		userSearch = cursor.fetchall()
		return render_template('friends.html',friends = friends,userSearch = userSearch,  addFriend = True)

@app.route("/addFriend", methods=['POST'])
def addFriend():
	if flask_login.current_user.is_authenticated:
		uid = getUserIdFromEmail(flask_login.current_user.id)
		friends = getUserFriends(uid)
		addFriend = True
		search_term = request.form['friendButton']
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO Friendship (UID1, UID2) 
			VALUES (%s, %s) 
			ON DUPLICATE KEY UPDATE UID1=UID1
			""", (uid, search_term))
		conn.commit()
	else: 
		friends = None
		addFriend = False

	
	return render_template('friends.html', friends=friends, addFriend = addFriend, uid = uid)

@app.route("/like", methods=['POST', 'GET'])
def like():
    if flask_login.current_user.is_authenticated:
        uidl = getUserIdFromEmail(flask_login.current_user.id)
    else:
        uidl = None
    
    likepid = request.form['like']
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO likes (user_id, picture_id) VALUES (%s, %s) ", (uidl, likepid))
    conn.commit()

    cursor2 = conn.cursor()
    cursor2.execute("""
           SELECT user_id
           FROM Pictures
           WHERE picture_id = %s
           """, (likepid))
    search_term = cursor2.fetchone()[0]
    
    cursor3 = conn.cursor()
    cursor3.execute("""
           SELECT fname, lname
           FROM Users
           WHERE user_id = %s 
           """, (search_term,))
    visitingname = cursor3.fetchone()

    photos = getUsersPhotos(search_term)

    cursor4 = conn.cursor()
    cursor4.execute("""
           SELECT comment_id, picture_id, comment_text, Users.fname, Users.lname
           FROM Comments JOIN Users ON Comments.user_id = Users.user_id
           WHERE picture_id = %s
           ORDER BY comment_id ASC
           """, (likepid,))
    rows = cursor4.fetchall()
    photo_comments = {likepid:[(row[2], row[3], row[4]) for row in rows] for likepid in [row[1] for row in rows]}

    return render_template('visitaccount.html', uid=uidl, search_term=search_term, photos=photos, albums=getUsersAlbums(search_term), visitingname=visitingname, base64=base64, photo_comments=photo_comments)

@app.route("/visitaccount", methods=['POST', 'GET'])
def visitaccount():
	if flask_login.current_user.is_authenticated:
		uid = getUserIdFromEmail(flask_login.current_user.id)
	else:
		uid = None
	search_term = request.form['clickedAccount']

	if str(uid).strip() == search_term.strip():
		return render_template('errorscreen.html')
	cursor = conn.cursor()
	cursor.execute("""
       SELECT fname, lname
       FROM Users
       WHERE user_id = %s 
       """, (search_term))
	visitingname= cursor.fetchone()
	picture = request.form.get('picture')
	cursor = conn.cursor()
	cursor.execute("""
        SELECT Comments.comment_text, Comments.picture_id, Users.fname, Users.lname
        FROM Comments JOIN Users ON Comments.user_id = Users.user_id
        WHERE Comments.picture_id = %s
    """, (picture,))
	rows = cursor.fetchall()
	photo_comments = {pid: [(row[0], row[2], row[3]) for row in rows] for pid in [row[1] for row in rows]}
	#print(search_term)
	photos = getUsersPhotos(search_term)
	#print(photos)
	return render_template('visitaccount.html', uid = uid, photo_comments = photo_comments, search_term = search_term, photos = photos, albums = getUsersAlbums(search_term), visitingname = visitingname, base64=base64)

@app.route("/pdelete", methods=['POST', 'GET'])
def pdelete():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	p_id = request.form['pdelete']
	cursor = conn.cursor()
	cursor.execute("""
        DELETE FROM Pictures WHERE picture_id = %s;
    """, (p_id))
	conn.commit()
	return render_template('hello.html', name=flask_login.current_user.id, message='Photo Deleted', photos=getUsersPhotos(uid), albums=getUsersAlbums(uid), toptags = getTop3Tags(), base64=base64)

@app.route("/adelete", methods=['POST', 'GET'])
def adelete():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	a_id = request.form['adelete']
	
	cursor = conn.cursor()
	cursor.execute("""
        DELETE FROM Albums WHERE album_id = %s;
    """, (a_id))
	conn.commit()
	return render_template('hello.html', name=flask_login.current_user.id, message='Album Deleted', photos=getUsersPhotos(uid), albums=getUsersAlbums(uid), toptags = getTop3Tags(), base64=base64)

@app.route("/you_may_also_like", methods=['POST', 'GET'])
def you_may_also_like():

	if flask_login.current_user.is_authenticated:
		uid = getUserIdFromEmail(flask_login.current_user.id)
	else:
		return render_template('register.html',  supress='False')
	uid = getUserIdFromEmail(flask_login.current_user.id)
	cursor = conn.cursor()
	cursor.execute("""SELECT Tags.name, Tags.tag_id, COUNT(*) AS num_photos 
	FROM Tagged 
	INNER JOIN Tags ON Tagged.tag_id = Tags.tag_id 
	INNER JOIN Pictures ON Tagged.picture_id = Pictures.picture_id 
	WHERE Pictures.user_id = '{0}'
	GROUP BY Tagged.tag_id ORDER BY num_photos DESC LIMIT 3; """.format(uid))
	t3 = cursor.fetchall()
	allphotos3 = []
	allphotos2 = []
	allphotos1 = []

	if(len(t3)<3):
		notenoughtags = True
	else:
		tags3 = [t3[0][0], t3[1][0], t3[2][0]]
		tags2_1 = [t3[0][0], t3[1][0]] #ab
		tags2_2 = [t3[0][0], t3[2][0]] #ac
		tags2_3 = [t3[1][0], t3[2][0]] #bc
		tags1_1 = [t3[0][0]]
		tags1_2 = [t3[1][0]]
		tags1_3 = [t3[2][0]]
		notenoughtags = False
		allphotos3 = [*searchmaylike(uid,tags3)]
		allphotos2 = [*searchmaylike(uid,tags2_1), *searchmaylike(uid,tags2_2), *searchmaylike(uid,tags2_3)]
		allphotos1 = [*searchmaylike(uid,tags1_1), *searchmaylike(uid,tags1_2), *searchmaylike(uid,tags1_3)]
		#print(allphotos[0][0])
		discovered = set()
		
		for photo in allphotos3.copy():
				if(photo[0] in discovered):
					allphotos3.remove(photo)
				else:
					discovered.add(photo[0])

		for photo in allphotos2.copy():
				if(photo[0] in discovered):
					allphotos2.remove(photo)
				else:
					discovered.add(photo[0])

		for photo in allphotos1.copy():
				if(photo[0] in discovered):
					allphotos1.remove(photo)
				else:
					discovered.add(photo[0])
		
	if not allphotos3 and not allphotos2 and not allphotos1:
		notenoughtags = True

	#print(allphotos3[0][0])
	#print(allphotos3)
	return render_template("you_may_also_like.html", allphotos3 = allphotos3, allphotos2 = allphotos2, allphotos1=allphotos1, t3=t3, notenoughtags=notenoughtags, base64=base64)


@app.route("/comment", methods=['POST', 'GET'])
def comment():
    comment = request.form.get('comment')
    picture = request.form.get('picture')
    cursor = conn.cursor()
    if flask_login.current_user.is_authenticated:
        uid = getUserIdFromEmail(flask_login.current_user.id)
    else:
        uid = None

    cursor.execute("""
        INSERT INTO Comments (comment_text, picture_id, user_id)
        VALUES (%s, %s, %s)
    """, (comment, picture, uid))
    conn.commit()

    # Update the photo_comments dictionary with the new comment
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.comment_text, c.picture_id, COALESCE(u.fname, 'Anonymous'), COALESCE(u.lname, '')
    FROM Comments c LEFT JOIN Users u ON c.user_id = u.user_id
    WHERE c.picture_id = %s
    """, (picture,))
    rows = cursor.fetchall()
    photo_comments = {pid: [(row[0], row[2], row[3]) for row in rows] for pid in [row[1] for row in rows]}

    # Render the visitaccount template with the updated comments
    if flask_login.current_user.is_authenticated:
        uid = getUserIdFromEmail(flask_login.current_user.id)
    else:
        uid = None
    search_term = request.form['clickedAccount']

    if str(uid).strip() == search_term.strip():
        return render_template('errorscreen.html')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fname, lname
        FROM Users
        WHERE user_id = %s 
    """, (search_term,))
    visitingname = cursor.fetchone()
    photos = getUsersPhotos(search_term)
    albums = getUsersAlbums(search_term)

    return render_template('visitaccount.html', uid=uid, search_term=search_term, photos=photos, albums=albums, visitingname=visitingname, base64=base64, photo_comments=photo_comments, getUserFullName=getUserFullName)

@app.route("/commentSearch", methods=['POST', 'GET'])
def commentSearch():
	comment_val = request.form['commentSearch']
	cursor = conn.cursor()
	cursor.execute("""
    SELECT u.user_id, u.fname, u.lname, COUNT(*) AS num_comments 
    FROM Comments c 
    JOIN Users u ON c.user_id = u.user_id 
    WHERE c.comment_text = %s
    GROUP BY c.user_id 
    ORDER BY num_comments DESC
	""", (comment_val,))
	rows = cursor.fetchall()
	return render_template('commentSearch.html', topCommenters = rows)
# Get the user's friends
@app.route("/friend_recommendation")
def getfriendRecommendation(uid):
	cursor = conn.cursor()
	cursor.execute("""
    	SELECT UID2 FROM friendship WHERE UID1 = %s
    """, (uid,))
	friends = cursor.fetchall()
	recommended_names = []
	save = []
	friends = [friend[0] for friend in friends]
	cursor = conn.cursor()
	if friends:
		cursor.execute("""
		SELECT UID2 FROM friendship WHERE UID1 IN %s AND UID2 NOT IN %s
	""", (tuple(friends), friends))
		fofs = cursor.fetchall()
		fofs = [fof[0] for fof in fofs]
		fof_counts = {}
		for fof in fofs:
			cursor = conn.cursor()
			cursor.execute("""
			SELECT COUNT(*) AS count FROM friendship WHERE UID1 IN %s AND UID2 = %s
		""", (tuple(friends), fof))
			count = cursor.fetchone()[0]
			fof_counts[fof] = count

		# Sort the fofs by the number of times they appear in the list of friends of friends
		sorted_fofs = sorted(fof_counts.items(), key=lambda x: x[1], reverse=True)

		# Get the recommended friends
		recommended_friends = [fof[0] for fof in sorted_fofs]
		save = [fof[0] for fof in sorted_fofs]
		# Get the names of the recommended friends
		cursor.execute("""
		SELECT fname, lname FROM Users WHERE user_id IN %s
		""", (tuple(recommended_friends),))
		recommended_names = [(user[0], user[1]) for user in cursor.fetchall()]
		for i in range(len(recommended_names)):
			recommended_names[i] = recommended_names[i][0] + " " + recommended_names[i][1], save[i] 
	return (recommended_names)

if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port=5000, debug=True)
