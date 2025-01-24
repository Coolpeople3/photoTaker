from flask import Flask, render_template_string
import cv2
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Capture Photo</title>
    </head>
    <body>
        <h1>Welcome! Please go next.</h1>
        <form action="/capture" method="POST">
            <button type="submit">Next</button>
        </form>
        <h2> Copyright 2025 Hitarth Yagnik all rights reserved</h2>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/capture', methods=['POST'])
def capture_photo():
    # Get the absolute path of the script's directory (the folder containing the script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path for the 'photos' directory inside the same folder as the script
    photos_dir = os.path.join(script_dir, 'photos')

    # Start the camera (use the default camera, index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "Could not access the camera.", 500

    # Capture a single frame
    ret, frame = cap.read()

    if ret:
        # Ensure the 'photos' directory exists inside the script's folder
        os.makedirs(photos_dir, exist_ok=True)

        # Save the captured photo with a timestamp in the 'photos' folder
        photo_path = os.path.join(photos_dir, f"photo_{int(time.time())}.png")
        cv2.imwrite(photo_path, frame)

        # Release the camera
        cap.release()

        return f"Thank you for pressing next!"

    else:
        cap.release()
        return "Failed to capture photo.", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
