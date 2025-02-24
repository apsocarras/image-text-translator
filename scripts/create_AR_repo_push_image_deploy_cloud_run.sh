#!/bin/bash 

## Create AR Repo 
gcloud artifacts repositories create image-text-translator-artifacts \
  --repository-format=docker \
  --location=$REGION \
  --project=$PROJECT_ID

## Create Docker Image 
export IMAGE_NAME=$REGION-docker.pkg.dev/$PROJECT_ID/image-text-translator-artifacts/image-text-translator-ui

# configure Docker to use the Google Cloud CLI to authenticate requests to Artifact Registry.
gcloud auth configure-docker $REGION-docker.pkg.dev

# Build the image and push it to Artifact Registry
# Run from the ui_cr folder
gcloud builds submit --tag $IMAGE_NAME:v0.1 .

## Deploy to Cloud Run 
export RANDOM_SECRET_KEY=$(openssl rand -base64 32)

gcloud run deploy image-text-translator-ui \
  --image=$IMAGE_NAME:v0.1 \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --max-instances=1 \
  --service-account=$SVC_ACCOUNT_EMAIL \
  --set-env-vars BACKEND_GCF=$BACKEND_GCF,FLASK_SECRET_KEY=$RANDOM_SECRET_KEY