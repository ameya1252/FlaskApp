from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
import os

# Initialize Flask application
web_app = Flask(__name__, template_folder='/var/www/html/flask_project/templates')
web_app.config['SECRET_KEY'] = 'unique_secret_key'  # secret key

# Home route
@web_app.route('/')
def home():
    return render_template('home.html')

# Function to calculate the number of words in a file
def word_counter(filepath):
    with open(filepath, 'r') as file_content:
        content = file_content.read()
        return len(content.split())

# Route for user registration
@web_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract form data
        user_name = request.form['username']
        user_password = request.form['password']
        user_first_name = request.form['firstName']
        user_last_name = request.form['lastName']
        user_email = request.form['email']

        # Process file upload for word counting
        file_upload = request.files['fileUpload']
        if file_upload:
            # Save the uploaded file
            save_path = os.path.join('/var/www/html/flask_project/uploads', file_upload.filename)
            file_upload.save(save_path)

            # Perform word count
            total_words = word_counter(save_path)

            # Save user data in session
            session['user_name'] = user_name
            session['user_password'] = user_password
            session['user_first_name'] = user_first_name
            session['user_last_name'] = user_last_name
            session['user_email'] = user_email
            session['total_words'] = total_words
            session['save_path'] = save_path

            # Navigate to confirmation page
            return redirect(url_for('signup_success'))

    return render_template('signup.html')

# Login functionality
@web_app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        login_username = request.form['username']
        login_password = request.form['password']

        # Validate credentials
        if login_username == session.get('user_name') and login_password == session.get('user_password'):
            return redirect(url_for('signup_success'))
        else:
            # Handle invalid login
            pass  # Add your error handling or redirection here

    return render_template('login.html')

# Signup success page
@web_app.route('/signup-success')
def signup_success():
    # Fetch session data
    data = {key: session.get(key) for key in ['user_name', 'user_password', 'user_first_name', 'user_last_name', 'user_email', 'total_words']}
    return render_template('signup_success.html', **data)

# File download route
@web_app.route('/download/<path:filename>')
def file_download(filename):
    return send_from_directory('/var/www/html/flask_project/uploads', filename)

# Main entry
if __name__ == '__main__':
    web_app.run(debug=True, host='127.0.0.1', port=5001)
