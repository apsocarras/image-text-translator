"""
A sample Hello World server.
"""
import os

from flask import Flask, flash, request, render_template
from werkzeug.utils import secure_filename

def create_app():
    """ Create and configure the app """
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_mapping(
        SECRET_KEY='dev', # override with FLASK_SECRET_KEY env var
    )

    # Load envs starting with FLASK_
    # E.g. FLASK_SECRET_KEY
    flask_app.config.from_prefixed_env()
    return flask_app

app = create_app()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename:str):
    """ Check if the filename is allowed. """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def entry():
    """ Render the upload form """
    message = "Upload your image!"
    to_lang = os.environ.get('TO_LANG', 'en')

    if request.method == 'POST':
        app.logger.debug("Got POST")
        file = request.files.get('file')

        # check if the post request has the file part
        if file is None:
            flash('No file part')
        elif file.filename == '':
            flash('No selected file')
        elif not allowed_file(file.filename):
            filename = secure_filename(file.filename)
            flash(f'{secure_filename(filename)} is not a supported image format')
        else:
            filename = secure_filename(file.filename)
            message = f"Got {secure_filename(filename)}. Feel free to upload a new image."

    return render_template('index.html', message=message, to_lang=to_lang)

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    # todo: resolve debug setting
    app.run(debug=False, port=server_port, host='0.0.0.0')
