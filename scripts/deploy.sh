#!/bin/bash 

# From backend-gcf folder 
cd /Users/alex/tutorials/image-text-translator/app/backend_gcf
gcloud functions deploy extract-and-translate \
  --gen2 --max-instances 1 \
  --region $REGION \
  --runtime=python312 --source=. \
  --trigger-http --entry-point=extract_and_translate \ 
  --no-allow-unauthenticated \
  --service-account=$SVC_ACCOUNT_EMAIL

gcloud functions add-invoker-policy-binding extract-and-translate \
  --region=$REGION \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL"

