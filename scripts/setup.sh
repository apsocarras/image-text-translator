export PROJECT_ID=$(gcloud config list --format='value(core.project)')
export REGION=europe-west2
export FUNCTIONS_PORT=8081

export FLASK_SECRET_KEY=secret-1234
export FLASK_RUN_PORT=8080

echo "Environment variables configured:"
echo PROJECT_ID="$PROJECT_ID"
echo REGION="$REGION"
echo FUNCTIONS_PORT="$FUNCTIONS_PORT"
echo FLASK_RUN_PORT="$FLASK_RUN_PORT"
