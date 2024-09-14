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
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.cloud import translate_v2 as translate
from PIL import Image, UnidentifiedImageError

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
# for lang in app.languages:
#     app.logger.debug('%s: %s', lang, app.languages[lang])

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
    translation = ""

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
            flash(f'{secure_filename(filename)} is not a supported image format. '
                  f'Supported formats are: {ALLOWED_EXTENSIONS}')
        else:
            filename = secure_filename(file.filename)
            app.logger.debug("Got %s", filename)
            app.logger.debug("Translating to %s", to_lang)

            # We don't need to save the image. We just want to binary encode it.
            try:
                img = Image.open(file.stream)
                with BytesIO() as buf:
                    if img_format := img.format: # e.g. JPEG, GIF, PNG
                        img.save(buf, img_format.lower())
                        content_type = f"image/{img_format.lower()}"
                        image_bytes = buf.getvalue()
                        encoded_img = base64.b64encode(image_bytes).decode()
                    else:
                        flash('Unable to determine image format.')
            except UnidentifiedImageError:
                # This will happen if we resubmit the form
                flash('Unable to process image.')

            if encoded_img:
                message = f"Processed <{secure_filename(filename)}>. Feel free to upload a new image."
                func_response = make_authorized_post_request(endpoint=app.backend_func,
                                        image_data=image_bytes, to_lang=to_lang,
                                        filename=filename, content_type=content_type)
                app.logger.debug("Function response code: %s", func_response.status_code)
                app.logger.debug("Function response text: %s", func_response.text)
                translation = func_response.text
            else:
                app.logger.error("Image encoding failed.")                

    app.logger.debug(f"Final translation: {translation}")
    return render_template('index.html',
                           languages=app.languages,
                           message=message,
                           to_lang=to_lang,
                           img_data=encoded_img,
                           translation=translation), 200

def make_authorized_post_request(endpoint:str,
                                 image_data, to_lang:str,
                                 filename:str, content_type:str):
    """
    Make a POST request to the specified HTTP endpoint by authenticating with the ID token
    obtained from the google-auth client library using the specified audience value.
    Expects the image_data to be a bytes representation of the image.
    """
    if endpoint == "undefined":
        raise ValueError("Unable to retrieve Function endpoint.")

    # Cloud Functions uses your function's URL as the `audience` value
    # For Cloud Functions, `endpoint` and `audience` should be equal
    # ADC requires valid service account credentials
    audience = endpoint
    auth_req = GoogleAuthRequest()

    # Requests OAuth 2.0 access token for the service identity
    # from the instance metadata server or with local ADC. E.g.
    # export GOOGLE_APPLICATION_CREDENTIALS=/path/to/svc_account.json
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    headers = {
        "Authorization": f"Bearer {id_token}",
        # "Content-Type": "multipart/form-data" # Let requests library decide on the content-type
    }

    files = {
        "uploaded": (filename, image_data, content_type),
        "to_lang": (None, to_lang)
    }

    # Send the HTTP POST request to the Cloud Function
    response = requests.post(endpoint, headers=headers, files=files, timeout=10)

    return response

if __name__ == '__main__':
    # Development only:
    # - python app.py
    # - python -m flask --app hello run --debug
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app. """
    server_port = os.environ.get('FLASK_RUN_PORT', '8080')
    app.run(port=server_port, host='0.0.0.0')
