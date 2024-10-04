################################################################
# One-time creation of sa account for our application services #
################################################################

# First, authenticate as a user who can create service accounts
# gcloud auth login

# Check correct project is selected
# gcloud config list project
# export PROJECT_ID=<enter your project ID>
# gcloud config set project $PROJECT_ID

# If these are not already set...
export SVC_ACCOUNT=image-text-translator-sa
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

# Attaching a user-managed service account is the preferred way to
# provide credentials to ADC for production code running on Google Cloud
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
# Grant roles to our developer account, for deploying #
#######################################################

export MY_ORG=<enter your org domain>

# Grant the required role to the principal
# that will attach the service account to other resources.
# Here we assume your developer account is a member of the gcp-devops group.
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="group:gcp-devops@$MY_ORG" \
  --role=roles/iam.serviceAccountUser

# Allow service account impersonation
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="group:gcp-devops@$MY_ORG" \
  --role=roles/iam.serviceAccountTokenCreator

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="group:gcp-devops@$MY_ORG" \
   --role roles/cloudfunctions.admin

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="group:gcp-devops@$MY_ORG" \
   --role roles/run.admin