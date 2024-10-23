from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Sample user data for demonstration purposes
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        diabetes_type = request.form.get('diabetes_type')

        # Check if email already exists
        if email in users:
            return render_template('signup.html', error_message='An account already exists with this email address.')

        # Register the new user
        users[email] = {
            'username': username,
            'password': password,
            'diabetes_type': diabetes_type
        }
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', error_message='')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate user credentials
        user = users.get(email)
        if user and user['password'] == password:
            session['username'] = user['username']  # Store username in session
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error_message='Invalid email or password. Please try again.')

    return render_template('login.html', error_message='')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect if not logged in
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)