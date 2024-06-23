# Image Text Extract and Translation

## Overview

An application that allows a user to upload an image containing text. The text will be extracted, and translated as required. The translated text is returned.

This will make use of Google Cloud serverless components, and Google ML APIs.

### How It Works

1. A user uploads or pastes an image.
1. The image is processed, using Google Vision API. Any text is extracted.
1. The text is translated (if necessary) using Google Cloud Translation API.

### Example Use Case

- A user wants to translate a meme in Ukrainian, to English.

## Repo Structure

```text
└── image-text-translator
    ├── docs/
    |
    ├── infra-tf/               - Terraform for installing infra
    |
    ├── scripts/                - For environment setup and helper scripts
    |   └── setup.sh            - Setup helper script
    |
    ├── app/                    - The Application
    │   ├── ui_cr/                - Browser UI (Cloud Run)
    │   │   ├── static/             - Static content for frontend
    |   |   ├── templates/          - HTML templates for frontend
    |   |   ├── app.py              - The Flask application
    |   |   ├── requirements.txt    - The UI Python requirements
    |   |   ├── Dockerfile          - Dockerfile to build the Flask container
    |   |   └── .dockerignore       - Files to ignore in Dockerfile
    |   |
    │   └── backend_gcf/          - Backend (Cloud Function)
    │       ├── main.py             - The backend CF application
    │       └── requirements.txt    - The backend CF Python requirements
    |
    ├── testing/
    │   └── images/
    |
    ├── requirements.txt          - Python requirements for project local dev
    └── README.md                 - Repo README
```

## Architecture

![Architecture](docs/image-text-translator.png)

- UI:
  - Python Flask application, containerised.
  - Hosted in Cloud Run.
- Backend:
  - A Google Cloud Function, in Python.

## Setup

### Project Setup

- Create a Google Cloud project to host the application.
- Enable the necessary APIs.

```bash
# Enable necessary APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable eventarc.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable iamcredentials.googleapis.com
```

- Setup service account and assign roles:

```bash
export PROJECT_ID=<enter your project ID>
export SVC_ACCT=image-text-translator-sa
export SVC_ACCOUNT_EMAIL=$SVC_ACCT@$PROJECT_ID.iam.gserviceaccount.com

# Check we have the correct project selected
gcloud config set project $PROJECT_ID

# Attaching a user-managed service account is the preferred way to provide credentials to ADC for production code running on Google Cloud.
gcloud iam service-accounts create $SVC_ACCT

# Grant roles to the service account
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role=roles/run.admin

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role=roles/run.invoker

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role=roles/cloudfunctions.admin

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role=roles/cloudfunctions.invoker

# Grant the required role to the principal that will attach the service account to other resources.
gcloud iam service-accounts add-iam-policy-binding $SVC_ACCOUNT_EMAIL \
  --member="group:gcp-devops@my-org.com" \
  --role=roles/iam.serviceAccountUser

gcloud iam service-accounts add-iam-policy-binding $SVC_ACCOUNT_EMAIL \
  --member="group:gcp-devops@my-org.com" \
  --role=roles/iam.serviceAccountTokenCreator

# Ensure your account has access to deploy to Cloud Functions and Cloud run
# gcloud projects add-iam-policy-binding $PROJECT_ID \
#   --member="group:gcp-devops@my-org.com" \
#   --role roles/run.admin

# Use service account impersonation to create a local ADC file
gcloud auth application-default login
```

### Local Dev One Time Setup

```bash
# Cloud CLI installed in local Linux environment.
# See https://cloud.google.com/sdk/docs/install

# Install Google Cloud CLI packages for local dev
sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin kubectl google-cloud-cli-skaffold google-cloud-cli-minikube

# Setup Python in Gcloud CLI
# See https://cloud.google.com/python/docs/setup
# Create and activate a Python virtual environment

# Install the Python dependencies
python3 -m pip install -r requirements.txt
```

## Run with Every New Terminal Session

```bash
# From the image-text-translator directory
source ./scripts/setup.sh
```

## Function Backend

### Invoking

Two ways to call the function:

1. POST the image. E.g. 
   ```bash
   curl -X POST localhost:$FUNCTIONS_PORT -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/path/to/meme.jpg" \
   -F "to_lang=en"
   ```
1. Reference a bucket and filename. E.g.
   ```bash
   curl -X GET localhost:$FUNCTIONS_PORT -H "Content-Type: application/json" \
     -d '{"bucket":"Bob", "filename":"meme.jpg", "to_lang":"en}'
   ```

### Function Local Dev

```bash
# Run the function
cd app/backend_gcf
functions-framework --target extract_and_translate --debug --port $FUNCTIONS_PORT
```

### Testing

Run from another console:

```bash
gcloud auth application-default login  # Set default credentials 
source ./scripts/setup.sh # We need our env vars to be set in this console session

# Test the function
curl -X POST localhost:$FUNCTIONS_PORT -H "Content-Type: multipart/form-data" \
   -F "uploaded=@./testing/images/ua_meme.jpg"
```

### Deploying the Function with Gcloud

```bash
gcloud functions deploy extract-and-translate \
  --gen2 --max-instances 1 \
  --region europe-west2 \
  --runtime=python312 --source=. \
  --trigger-http --entry-point=extract_and_translate \
  --no-allow-unauthenticated

# Allow this function to be called by the service account
gcloud functions add-invoker-policy-binding extract-and-translate \
  --region=$REGION \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL"
```

The function is created with endpoint URL:

`https://<region>-<project-id>.cloudfunctions.net/extract-and-translate`

### Test Function in GCP

Syntax:

```bash
curl -X POST https://<region>-<project-id>.cloudfunctions.net/extract-and-translate \
     -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     -H "Content-Type: multipart/form-data" \
     -F "uploaded=@$HOME/path/to/meme.jpg" \
     -F "to_lang=en"
```

Sample:

```bash
./scripts/setup.sh

curl -X POST $BACKEND_GCF \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: multipart/form-data" \
    -F "uploaded=@./testing/images/ua_meme.jpg" \
    -F "to_lang=en"
```

## UI with Cloud Run

### Local Dev

To launch the Flask app:

```bash
cd app/ui_cr/
source ../../scripts/setup.sh  # Initialise vars if we're in a new terminal

# Run the Flask App
python app.py

# Or with the Flask command.
# This will automatically load any environment vars starting FLASK_
# The --debug tells Flask to automatically reload after any changes
# and to set the app.logger to debug.
python -m flask --app app run --debug
```

A sample VS Code launch configuration for the Flask app:

```json
{
    "configurations": [
        {
            "name": "Python Debugger: Flask",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "cwd": "${workspaceFolder}/app/ui_cr",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1",
                "FLASK_RUN_PORT": "8080"
            },
            "args": [
                "run",
                "--debug",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "autoStartBrowser": false
        },
        // Other configurations
    ]
}
```

```bash
gcloud functions add-invoker-policy-binding extract-and-translate \
  --member='serviceAccount:CALLING_FUNCTION_IDENTITY'
```