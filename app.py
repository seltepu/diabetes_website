from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

retinopathy_model = tf.keras.models.load_model('diabetic_retinopathy_classifier.keras')

retinopathy_classes = ['No DR', 'Mild DR', 'Severe DR']

users = {}

def preprocess_image(image_data):
    img = Image.open(io.BytesIO(image_data))
    img = img.resize((128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = tf.expand_dims(img_array, 0)
    return img_array

@app.route('/analyze_retina', methods=['POST'])
def analyze_retina():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'})

    try:
        image_data = file.read()
        processed_image = preprocess_image(image_data)
        
        predictions = retinopathy_model.predict(processed_image)
        predicted_class = retinopathy_classes[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]) * 100)
        
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        return jsonify({
            'prediction': predicted_class,
            'confidence': confidence,
            'image': image_base64
        })
    except Exception as e:
        return jsonify({'error': str(e)})

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

        if email in users:
            return render_template('signup.html', error_message='An account already exists with this email address.')

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

        user = users.get(email)
        if user and user['password'] == password:
            session['username'] = user['username'] 
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error_message='Invalid email or password. Please try again.')

    return render_template('login.html', error_message='')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)  
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)