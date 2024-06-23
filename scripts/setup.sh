export PROJECT_ID=$(gcloud config list --format='value(core.project)')
export REGION=europe-west2
export GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json

# Functions
export FUNCTIONS_PORT=8081
export BACKEND_GCF=https://$REGION-$PROJECT_ID.cloudfunctions.net/extract-and-translate

# Flask
export FLASK_SECRET_KEY=secret-1234
export FLASK_RUN_PORT=8080

echo "Environment variables configured:"
echo PROJECT_ID="$PROJECT_ID"
echo REGION="$REGION"
echo GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_APPLICATION_CREDENTIALS"
echo BACKEND_GCF="$BACKEND_GCF"
echo FUNCTIONS_PORT="$FUNCTIONS_PORT"
echo FLASK_RUN_PORT="$FLASK_RUN_PORT"


