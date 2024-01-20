from flask import Flask, render_template, request, flash,get_flashed_messages,redirect
import sqlite3
import os

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Assuming you have a SQLite database file named 'your_database.db'
DATABASE = 'research.db'


# conn = sqlite3.connect('research.db')
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         username TEXT NOT NULL UNIQUE,
#         password TEXT NOT NULL,
#         email TEXT NOT NULL,
#         lab_id INTEGER,
#         FOREIGN KEY (lab_id) REFERENCES labs(lab_id)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS posts (
#         post_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         text_desc TEXT NOT NULL,
#         username TEXT NOT NULL,
#         file_name TEXT,
#         type TEXT,
#         FOREIGN KEY (username) REFERENCES users(username)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS labs (
#         lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         lab_name TEXT NOT NULL
#     )
# ''')
# conn.commit()
# conn.close()

@app.route('/',  methods=['POST','GET'])
def index():
    return render_template('index.html')
# @app.route('/')
# def fetch_file_names():
#     # Connect to the database
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     # Fetch file names sorted by time
#     cursor.execute('''
#         SELECT file_name FROM posts
#         ORDER BY time DESC
#     ''')

#     # Fetch all results into a list
#     result = cursor.fetchall()

#     # Close the database connection
#     conn.close()

#     # Extract file names from the result
#     file_names = [row[0] for row in result]

#     return render_template('home.html', file_names=file_names)

def get_UID():
    conn = sqlite3.connect('research.db')
    cursor = conn.cursor()
    user_id=cursor.execute('''SELECT MAX(user_id) FROM users''')
        
        # print(user_id)
    re=0
    for a in user_id:
        re=a[0]
        

    if re==None:
        UID=1
    else:
        # for x in user_id:
        #     for y in x:
        #         UID=y
        UID=re+1

    return UID

def fetch_file_names():
    # Connect to the database
    conn = sqlite3.connect('research.db')
    cursor = conn.cursor()

    # Fetch file names sorted by time
    cursor.execute('''
        SELECT file_name FROM posts
        ORDER BY time DESC
    ''')

    # Fetch all results into a list
    result = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Extract file names from the result
    file_names = [row[0] for row in result]
    return file_names

@app.route('/home',methods=['POST'])
def home():
        type=request.form['type']
        if type=="1":
            username = request.form['username']
            password = request.form['password']
            conn = sqlite3.connect('research.db')
            cursor = conn.cursor()

            passo = cursor.execute('''SELECT Password FROM users WHERE username=? ''', (username,))
            p = 0
            for x in passo:
                for y in x:
                    p = y
            
            
            if p != password or p == 0:
                flash('Login Unsuccessful! Try again')
                messages = get_flashed_messages()
                return render_template('Login.html', messages=messages)
            else:
                # Add a return statement for the successful login
                ul=cursor.execute('''SELECT user_id,lab_id FROM users WHERE username=? ''', (username,))
                for x in ul:
                    UID,lab_id=x
                
                file_names=fetch_file_names()
                return render_template('home.html',user_id=UID,lab_id=lab_id,file_names=file_names)
            conn.close()
        else:
            conn = sqlite3.connect('research.db')
            cursor = conn.cursor()

            name = request.form['name']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            lab_id = request.form['lab_id']  # Note: Use request.form['lab_id'] instead of request.form('lab_id')
            lab_id=int(lab_id)

            d = cursor.execute("SELECT Username FROM users")
            for x in d:
                for i in x:
                    if username == i:
                        flash('Username exists! Try a different one.')
                        messages = get_flashed_messages()
                        return render_template('Signup.html', messages=messages)

            UID=get_UID()
            

            sql = "INSERT INTO users VALUES (%d,'%s', '%s', '%s', '%s',%d)" % (int(UID), name, username, password, email, int(lab_id))
            cursor.execute(sql)
            conn.commit()
            conn.close()
            print(username)

            file_names=fetch_file_names()
            # return render_template('home.html')/
            return redirect("/Login")

        
        

@app.route('/Signup')
def Signup():
        # conn = sqlite3.connect('research.db')
        # cursor = conn.cursor()

        # name = request.form['name']
        # email = request.form['email']
        # username = request.form['username']
        # password = request.form['password']
        # lab_id = request.form['lab_id']  # Note: Use request.form['lab_id'] instead of request.form('lab_id')
        # lab_id=int(lab_id)

        # d = cursor.execute("SELECT Username FROM users")
        # for x in d:
        #     for i in x:
        #         if username == i:
        #             flash('Username exists! Try a different one.')
        #             messages = get_flashed_messages()
        #             return render_template('Signup.html', messages=messages)

        # UID=get_UID()
        

        # sql = "INSERT INTO users VALUES (%d,'%s', '%s', '%s', '%s',%d)" % (int(UID), name, username, password, email, int(lab_id))
        # cursor.execute(sql)
        # conn.commit()
        # conn.close()
        # print(username)

        # file_names=fetch_file_names()

        # # Pass lab_id as a parameter to 'home.html'
        # return render_template('home.html', lab_id=lab_id,user_id=UID,file_names=file_names)

    # Handle GET requests
    return render_template('Signup.html')

@app.route('/Login')
def Login():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     conn = sqlite3.connect('research.db')
    #     cursor = conn.cursor()

    #     passo = cursor.execute('''SELECT Password FROM users WHERE username=? ''', (username,))

    #     p = 0
    #     for x in passo:
    #         for y in x:
    #             p = y
        

    #     if p != password or p == 0:
    #         flash('Login Unsuccessful! Try again')
    #         messages = get_flashed_messages()
    #         return render_template('Login.html', messages=messages)
    #     else:
    #         # Add a return statement for the successful login
    #         ul=cursor.execute('''SELECT user_id,lab_id FROM users WHERE username=? ''', (username,))
    #         for x in ul:
    #             UID,lab_id=x
            
    #         file_names=fetch_file_names()
    #         return render_template('home.html',user_id=UID,lab_id=lab_id,file_names=file_names)
    #     conn.close()
    # Handle GET requests
    return render_template('Login.html')


UPLOAD_FOLDER = 'static/posts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload')
def input_post():
    return render_template('upload.html')

def classify_file_type(file_extension):
    photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.webm']

    if file_extension.lower() in photo_extensions:
        return 'p'
    elif file_extension.lower() in video_extensions:
        return 'v'

@app.route('/upload_post', methods=['POST'])  
def upload():
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch the post_id of the last entry in the 'posts' table
    cursor.execute('''
        SELECT post_id FROM posts
        ORDER BY time DESC
        LIMIT 1
    ''')

    # Fetch the result
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Extract post_id from the result, if any
    post_id = result[0] if result else 0
    post_id+=1
    
    
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file"
    
    if file:
        
        from werkzeug.utils import secure_filename
        original_filename, file_extension = os.path.splitext(file.filename)
        type=classify_file_type(file_extension)
        new_filename = secure_filename(f"{type}{post_id}{file_extension}")
        
        filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        # filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        
        text_desc=request.form['description']
        user_id=request.form['user_id']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Insert a new row into the 'posts' table
        cursor.execute('''
            INSERT INTO posts (text_desc, username, file_name, type)
            VALUES (?, ?, ?, ?)
        ''', (text_desc, user_id, new_filename, type))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()  
        
        return "File uploaded successfully"

@app.route('/open_upload', methods=['POST'])
def open_upload():
    # Retrieve variables from the request
    user_id = request.form['user_id']
    lab_id = request.form['lab_id']
    # variable2 = request.args.get('variable2', 'default_value2')

    # Render post.html with variables
    return render_template('upload.html', user_id=user_id, lab_id=lab_id)


if __name__ == '__main__':
    app.run(debug=True)
