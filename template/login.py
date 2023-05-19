from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import cv2

app = Flask(__name__)

# Initialize the speech recognition module
r = sr.Recognizer()

# Initialize the eye recognition module
face_cascade = cv2.CascadeClassifier(r'F:\admin\haarcascade\haarcascade_eye.xml')

# Load admin data from a user database or other storage
admin_voice_data = 'Anirudh'
admin_eye_data = 'admin eye data'

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        voice_text = recognize_voice()
        eye_image = capture_eye_image()
        
        if username == 'admin' and password == 'admin123' and voice_text == admin_voice_data and verify_eye(eye_image):
            return jsonify({'message': 'Access granted as admin'})
        else:
            return jsonify({'message': 'Access denied'})

    return render_template('login.html')

# Voice recognition function
def recognize_voice():
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("Recognized voice:", text)
            return text
        except sr.UnknownValueError:
            print("Unable to recognize voice.")
            return None

# Eye verification function
def verify_eye(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eyes = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(eyes) > 0:
        print("Eyes detected.")
        return True
    else:
        print("Eyes not detected.")
        return False

# Function to capture an image for eye verification
def capture_eye_image():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    cap.release()
    return frame

if __name__ == '__main__':
    app.run(debug=True)
