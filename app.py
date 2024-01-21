from flask import Flask, render_template, request, flash,get_flashed_messages,redirect
import sqlite3
import os

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'your_secret_key_here'

DATABASE = 'research.db'


@app.route('/',  methods=['POST','GET'])
def index():
    return render_template('index.html')

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
        UID=re+1

    return UID

# def fetch_file_names():
#     # Connect to the database
#     conn = sqlite3.connect('research.db')
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
#     return file_names

import sqlite3

def fetch_file_names():
    # Connect to the database
    conn = sqlite3.connect('research.db')
    cursor = conn.cursor()

    # Fetch file names and timestamps sorted by time
    cursor.execute('''
        SELECT users.name, posts.file_name, posts.time, posts.text_desc
        FROM posts
        JOIN users ON posts.user_id = users.user_id
        ORDER BY posts.time DESC
    ''')

    # Fetch all results into a list of tuples
    files = cursor.fetchall()

    # Close the database connection
    conn.close()

    return files

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
                
                files=fetch_file_names()
                return render_template('home.html',user_id=UID,lab_id=lab_id, files=files)
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
            return redirect("/Login")

        
        

@app.route('/Signup')
def Signup():
    return render_template('Signup.html')

@app.route('/Login')
def Login():
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

        cursor.execute('''
            INSERT INTO posts (text_desc, user_id, file_name, type)
            VALUES (?, ?, ?, ?)
        ''', (text_desc, user_id, new_filename, type))

        conn.commit()
        conn.close()  
        
        return "File uploaded successfully"

@app.route('/open_upload', methods=['POST'])
def open_upload():
    user_id = request.form.get('user_id')
    lab_id = request.form.get('lab_id')
    lab_id=int(lab_id)
    return render_template('upload.html', user_id=user_id, lab_id=lab_id)

@app.route('/open_research_list', methods=['POST'])
def open_research_list():
    # user_id = request.form['user_id']
    # lab_id = request.form['lab_id']
    user_id = request.form.get('user_id')
    lab_id = request.form.get('lab_id')
    lab_id=int(lab_id)
    
    conn = sqlite3.connect(DATABASE)  # Replace with your actual database file
    cursor = conn.cursor()

    # Fetch lab names from the labs table
    try:
        cursor.execute('SELECT lab_id, lab_name FROM labs')
        labs = [(int(row[0]), row[1]) for row in cursor.fetchall()]
        # print("Labs:", labs)
    except sqlite3.Error as e:
        labs = []
        print("Error fetching labs:", e)

    # Close the connection
    conn.close()
    # print(labs[0][0])
    # print(labs[1][0])
    # print(labs[2][0])
    return render_template('researchlist.html', user_id=user_id, lab_id=lab_id, labs=labs)


# @app.route('/Labss1', methods=['POST','GET'])
# def Labss1():
#     conn = sqlite3.connect('research.db')
#     cursor = conn.cursor()
#     file_namess=cursor.execute('''SELECT file_name FROM posts WHERE user_id IN (SELECT user_id FROM users WHERE lab_id=1)''' )
#     file_names=()
#     for x in file_namess:
#         file_names=x+file_names
#     UID=get_UID()-1

#     D=cursor.execute('''SELECT lab_id FROM users WHERE user_id=?''',(UID,))

#     for x in D:
#         lab_id=x[0]

#     print('cdscds',UID,lab_id)
#     return render_template('Labs1.html',User_id=UID,lab_id=lab_id,file_names=file_names)

# @app.route('/Labs1')
# def Labs1():
#     return render_template('Labs1.html')

@app.route('/open_research_lab', methods=['POST'])
def open_research_lab():
    # Extract user_id and lab_id from the form data
    print("Inside")
    user_id = request.form.get('user_id')
    lab_id = request.form.get('lab_id')
    lab_id=int(lab_id)
    lab_no = request.form.get('lab_no')
    lab_no=int(lab_no)
    lab_name=request.form.get('lab_name')
    # print(lab_no)
    # Add any logic to fetch data for the lab page based on user_id and lab_id
    # For example, you can query the database to get lab details

    # Render the lab page with the provided data
    # page_name='l'+str(lab_no)+'.html'
    # return render_template(page_name, user_id=user_id, lab_id=lab_id, lab_no=lab_no)

    conn = sqlite3.connect('research.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT users.name, posts.file_name, posts.time, posts.text_desc
        FROM posts
        JOIN users ON posts.user_id = users.user_id where lab_id={lab_no}
        ORDER BY posts.time DESC
    ''')
    # file_namess=cursor.execute(f'SELECT file_name FROM posts WHERE user_id IN (SELECT user_id FROM users WHERE lab_id={lab_no})' )
    # 
    files = cursor.fetchall()
    UID=get_UID()-1

    D=cursor.execute('''SELECT lab_id FROM users WHERE user_id=?''',(UID,))

    for x in D:
        lab_id=x[0]

    print('cdscds',UID,lab_id)
    return render_template('lab.html',User_id=UID,lab_id=lab_id,files=files, lab_no=lab_no,lab_name=lab_name)

@app.route('/home_nav', methods=['POST'])
def open_home_from_nav():
    # user_id = request.form['user_id']
    # lab_id = request.form['lab_id']
    user_id = request.form.get('user_id')
    lab_id = request.form.get('lab_id')
    lab_id=int(lab_id)
    
    files=fetch_file_names()
    return render_template('home.html',user_id=user_id,lab_id=lab_id, files=files)

if __name__ == '__main__':
    app.run(debug=True)
