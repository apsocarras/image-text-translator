export PROJECT_ID=$(gcloud config list --format='value(core.project)')
export REGION=europe-west2
export FUNCTIONS_PORT=8081

echo "Environment variables configured:"
echo PROJECT_ID="$PROJECT_ID"
echo REGION="$REGION"
echo FUNCTIONS_PORT="$FUNCTIONS_PORT"