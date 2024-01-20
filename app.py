from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Assuming you have a SQLite database file named 'your_database.db'
DATABASE = 'research.db'

@app.route('/')
def fetch_file_names():
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
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

    return render_template('home.html', file_names=file_names)


UPLOAD_FOLDER = 'static/posts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload')
def input_post():
    return render_template('upload.html')

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
        new_filename = secure_filename(f"p{post_id}{file_extension}")
        
        filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        # filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        
        text_desc="caption"
        user_id="person1"
        type="p"
        
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
    
if __name__ == '__main__':
    app.run(debug=True)
