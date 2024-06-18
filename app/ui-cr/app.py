"""
A sample Hello World server.
"""
import os

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# pylint: disable=C0103
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """ Check if the filename is allowed. """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def hello():
    print("Hello")
    message = "Upload your image!"
    to_lang = os.environ.get('TO_LANG', 'en')

    if request.method == 'POST':
        print("Got POST")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            message = "No file part! Upload your image!"
        else:
            file = request.files['file']
            # If the user does not select a file, 
            # the browser submits an empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                message = "No file! Upload your image!"
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                message = f"Got {filename}. Upload your image!"
            else:
                filename = secure_filename(file.filename)
                message = f"{filename} not an allowed image type. Upload your image!"

    return render_template('index.html',
        message=message,
        to_lang=to_lang)

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')
