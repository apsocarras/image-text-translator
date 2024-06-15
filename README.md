# Image Text Extract and Translation

## Overview

An application that allows a user to upload an image containing text. The text will be extracted, and translated as required. The translated text is returned.

### How It Works

1. A user uploads or pastes an image.
1. The image is processed, using Google Vision API. Any text is extracted.
1. The text is translated (if necessary) using Google Cloud Translation API.

### Example Use Case

- A user wants to translate a meme in Ukrainian, to English.

## Repo Structure

```text
└── image-text-translator
    ├── docs
    ├── infra-tf              - Terraform for installing infra
    ├── app                   - The Application
    │   ├── ui-cr               - Browser UI (Cloud Run)
    │   │   └── ...
    │   └── backend-gcf         - Backend (Cloud Function)
    │       └── ...
    ├── testing
    │   └── images
    └── README.md
```


## Architecture

![Architecture](docs/image-text-translator.png)

- UI:
  - Python Flask application, containerised.
  - Hosted in Cloud Run.
- Backend:
  - A Google Cloud Function, in Python.

## Local Dev Setup

```bash
# Cloud CLI installed in local Linux environment.
# See https://cloud.google.com/sdk/docs/install

# Setup Python in Gcloud CLI
# See https://cloud.google.com/python/docs/setup
# Create and activate a Python virtual environment

# Setup for local Cloud Run dev
sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin kubectl google-cloud-cli-skaffold google-cloud-cli-minikube

# Set up envs
export PROJECT_ID=$(gcloud config list --format='value(core.project)')
export REGION=europe-west2

# Set default credentials for making API calls from local dev environment
gcloud auth application-default login
```

## Function Backend

### Invoking

Two ways to call the function:

1. POST the image. E.g. 
   curl -X POST localhost:8080 -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/path/to/meme.jpg"
1. Reference a bucket and filename. E.g.
   curl -X GET localhost:8080 -H "Content-Type: application/json" \
     -d '{"bucket":"Bob", "filename":"meme.jpg"}'

### Function Local Dev

```bash
cd app/backend-gcf

# Install Google Cloud SDKs and other requirements (in appropriate folder)
pip install -r requirements.txt

# Allow local Cloud Functions dev using the framework
# (This is automatically included when deploying in GCP.)
pip install functions-framework

# Run the function
functions-framework --target extract_and_translate --debug

# test, from another console, e.g.
curl -X POST localhost:8080 -H "Content-Type: multipart/form-data" \
   -F "uploaded=@$HOME/path/to/meme.jpg"
```

### Deploying the Function with Gcloud

```bash
gcloud functions deploy extract-and-translate \
  --gen2 --max-instances 1 \
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
     -F "uploaded=@$HOME/path/to/meme.jpg"
```

Sample:

```bash
gcloud auth application-default login
export PROJECT_ID=$(gcloud config list --format='value(core.project)')
export REGION=europe-west2

curl -X POST https://$REGION-$PROJECT_ID.cloudfunctions.net/extract-and-translate \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: multipart/form-data" \
    -F "uploaded=@$HOME/localdev/gcp/image-text-translator/testing/images/ua_meme.jpg"
```

## UI with Cloud Run

```bash
```