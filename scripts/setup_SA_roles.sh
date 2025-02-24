#!/bin/bash 

export SVC_ACCOUNT="image-text-translator-sa"
export PROJECT_ID="wck-source"
export SVC_ACCOUNT_EMAIL="$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $SVC_ACCOUNT 

######################################
# Grant roles to the service account #
######################################

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role=roles/run.invoker

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role=roles/cloudfunctions.invoker

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/cloudtranslate.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/serviceusage.serviceUsageAdmin"

#######################################################
# Grant roles to your user account for deploying      #
#######################################################

export MY_EMAIL=asocarras@worldcentralkitchen.org
export PROJECT_ID=wck-source

# Grant the required role to the principal
# that will attach the service account to other resources.
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$MY_EMAIL" \
  --role=roles/iam.serviceAccountUser

# Allow service account impersonation
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$MY_EMAIL" \
  --role=roles/iam.serviceAccountTokenCreator

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="user:$MY_EMAIL" \
   --role=roles/cloudfunctions.admin

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="user:$MY_EMAIL" \
   --role=roles/run.admin

#######################################################
# Get service account JSON for local development      #
#######################################################

gcloud iam service-accounts keys create ~/.config/gcloud/$SVC_ACCOUNT.json \
  --iam-account=$SVC_ACCOUNT_EMAIL 

export GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/$SVC_ACCOUNT.json