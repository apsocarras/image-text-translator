# Image Text Extract and Translation

## Overview

An applicatin that allows a user to upload an image containing text.
The text will be extracted, and translated as required.
The translated text is returned.

### How It Works

1. A user uploads or pastes an image.
1. The image is processed, using Google Vision API. Any text is extracted.
1. The text is translated (if necessary) using Google Cloud Translation API.

### Example Use Case

- A user wants to translate a meme in Ukrainian, to English.

## Architecture

![Architecture](docs/image-text-translator.png)

- Frontend:
  - In Python and containerised.
  - Hosted in Cloud Run.
- Backend:
  - A Google Cloud Function, in Python.

## Function Design

Two ways to call the function:

1. POST the image. E.g. 
   curl -X POST localhost:8080 -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/path/to/meme.jpg"
1. Reference a bucket and filename. E.g.
   curl -X GET localhost:8080 -H "Content-Type: application/json" \
     -d '{"bucket":"Bob", "filename":"meme.jpg"}'

## For Local Dev

```bash
# Cloud CLI installed in local Linux environment.
# Create and activate Python env

# Set up envs
export PROJECT_ID=$(gcloud config list --format='value(core.project)')

# Set default credentials for making API calls from local dev environment
gcloud auth application-default login

# Allow local Cloud Functions dev using the framework
# (This is automatically included when deploying in GCP.)
pip install functions-framework

# Install Google Cloud SDKs and other requirements (in appropriate folder)
pip install -r requirements.txt

# Run the function
functions-framework --target extract_and_translate --debug

# test, from another console, e.g.
curl -X POST localhost:8080 -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/path/to/meme.jpg"
```

## Deploying the Function with Gcloud

```bash
gcloud functions deploy extract-and-translate \
  --gen2 \
  --region europe-west2 \
  --runtime=python312 --source=. \
  --trigger-http --entry-point=extract_and_translate \
  --no-allow-unauthenticated
```

The function is created with endpoint URL:

`https://europe-west2-<project-id>.cloudfunctions.net/extract-and-translate`

### Test Function in GCP

Syntax:

```bash
curl -X POST https://europe-west2-<project-id>.cloudfunctions.net/extract-and-translate \
     -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     -H "Content-Type: multipart/form-data" \
     -F "uploaded=@/home/path/to/meme.jpg"
```

Sample:

```bash
curl -X POST https://europe-west2-image-text-translator-425921.cloudfunctions.net/extract-and-translate \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: multipart/form-data" \
    -F "uploaded=@ua_meme.jpg" 
```