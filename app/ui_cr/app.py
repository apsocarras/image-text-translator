"""
Application: image-text-translator - UI

Flask application that processes a user-uploaded image,
and then makes a call to the backend Cloud Function.

Author: Darren Lester
Created: June, 2024
"""
import os
from flask import Flask, flash, request, render_template
from werkzeug.utils import secure_filename
from google.cloud import translate_v2 as translate

def create_app():
    """ Create and configure the app """
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_mapping(
        SECRET_KEY='dev', # override with FLASK_SECRET_KEY env var
    )

    # Load envs starting with FLASK_
    # E.g. FLASK_SECRET_KEY, FLASK_PORT
    flask_app.config.from_prefixed_env()
    client = translate.Client()
    flask_app.languages = {lang['language']: lang['name'] for lang in client.get_languages()}
    return flask_app

app = create_app()
for conf in app.config:
    app.logger.debug(f'{conf}: {app.config[conf]}')
for lang in app.languages:
    app.logger.debug(f'{lang}: {app.languages[lang]}')

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
    """ Development only: 
      - python app.py
      - python -m flask --app hello run --debug
    When deploying to Cloud Run, a production-grade WSGI HTTP server,
    such as Gunicorn, will serve the app. """
    server_port = os.environ.get('FLASK_RUN_PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')
