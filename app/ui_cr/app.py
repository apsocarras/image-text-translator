"""
Application: image-text-translator - UI

Flask application that processes a user-uploaded image,
and then makes a call to the backend Cloud Function.

Author: Darren Lester
Created: June, 2024
"""
import os
import base64
from io import BytesIO
import requests
from flask import Flask, flash, request, render_template
from werkzeug.utils import secure_filename
import google.oauth2.id_token
from google.cloud import translate_v2 as translate
from PIL import Image

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
    flask_app.backend_func = os.environ.get('BACKEND_GCF', 'undefined')
    return flask_app

app = create_app()
for conf in app.config:
    app.logger.debug('%s: %s', conf, app.config[conf])
for lang in app.languages:
    app.logger.debug('%s: %s', lang, app.languages[lang])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename:str):
    """ Check if the filename is allowed. """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def entry():
    """ Render the upload form """
    message = "Upload your image!"
    to_lang = os.environ.get('TO_LANG', 'en')
    encoded_img = ""

    if request.method == 'POST': # Form has been posted
        app.logger.debug("Got POST")
        file = request.files.get('file')
        to_lang = request.form.get('to_lang')

        if file is None:
            flash('No file part.')
        elif file.filename == '':
            flash('No file selected for uploading.')
        elif not allowed_file(file.filename):
            filename = secure_filename(file.filename)
            flash(f'{secure_filename(filename)} is not a supported image format. Supported formats are: {ALLOWED_EXTENSIONS}')
        else:
            filename = secure_filename(file.filename)
            app.logger.debug("Got %s", filename)

            # We don't need to save the image. We just want to binary encode it.
            img = Image.open(file.stream)
            with BytesIO() as buf:
                img.save(buf, 'jpeg')
                image_bytes = buf.getvalue()
            encoded_img = base64.b64encode(image_bytes).decode()

            message = f"Got {secure_filename(filename)}. Feel free to upload a new image."
            func_response = make_authorized_post_request(app.backend_func,
                                                         app.backend_func,
                                                         encoded_img,
                                                         to_lang)
            app.logger.debug("Got response: %s", func_response)

    return render_template('index.html',
                           languages=app.languages,
                           message=message,
                           to_lang=to_lang,
                           img_data=encoded_img), 200

def make_authorized_post_request(endpoint:str, audience:str, image_data, to_lang:str):
    """
    Make a POST request to the specified HTTP endpoint by authenticating
    with the ID token obtained from the google-auth client library
    using the specified audience value.
    """

    # Cloud Functions uses your function's URL as the `audience` value
    # For Cloud Functions, `endpoint` and `audience` should be equal
    # ADC requires valid service account credentials
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json"
    }

    data = {
        "image_data": image_data,
        "to_lang": to_lang
    }

    # Send the HTTP POST request to the Cloud Function
    response = requests.post(endpoint, headers=headers, json=data, timeout=10)

    return response

if __name__ == '__main__':
    # Development only:
    # - python app.py
    # - python -m flask --app hello run --debug
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app. """
    server_port = os.environ.get('FLASK_RUN_PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')
