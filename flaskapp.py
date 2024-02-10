from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Define a directory for storing uploaded files
UPLOAD_FOLDER = 'path/to/uploaded/files'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simulated database for storing users
# Structure: users = { 'username': {'first_name': '', 'last_name': '', 'email': '', 'password': ''} }
users = {}

@app.route('/')
def hello_world():
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Simple validation to check if user already exists
        if username in users:
            return 'User already exists!'
        # Save user data, excluding password for security (though storing unhashed password is insecure)
        users[username] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password  # Note: Never store plain passwords in a real app
        }

        # Handle file upload
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Store file path and word count in user's data
            with open(file_path, 'r') as f:
                file_content = f.read()
            word_count = len(file_content.split())
            users[username]['file_path'] = file_path
            users[username]['word_count'] = word_count

        return redirect(url_for('success', username=username))

    # Display registration form
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists and password matches
        user = users.get(username)
        if user and user['password'] == password:
            return redirect(url_for('success', username=username))
        else:
            return 'Invalid login credentials!'

    # Display login form
    return render_template('login.html')

@app.route('/success/<username>')
def success(username):
    user = users.get(username, {})
    if not user:
        return 'User not found!'

    # Display user details, excluding password
    return render_template('success.html', user=user)

@app.route('/download/<username>')
def download_file(username):
    user = users.get(username)
    if user and 'file_path' in user:
        return send_from_directory(directory=os.path.dirname(user['file_path']),
                                   filename=os.path.basename(user['file_path']),
                                   as_attachment=True)
    return 'File not found!'


if __name__ == '__main__':
        app.run(debug=True)
