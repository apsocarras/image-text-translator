# Testing

## Sample Curl Commands

### POSTing images, Local Dev

```bash
curl -X POST localhost:$FUNCTIONS_PORT \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@$HOME/localdev/gcp/image-text-translator/testing/images/ua_meme.jpg"

curl -X POST localhost:$FUNCTIONS_PORT \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@$HOME/localdev/gcp/image-text-translator/testing/images/fatrix.jpg"

curl -X POST localhost:$FUNCTIONS_PORT \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@$HOME/localdev/gcp/image-text-translator/testing/images/img7.jpg"

curl -X GET localhost:$FUNCTIONS_PORT -H "Content-Type: application/json" \
   -d '{"bucket":"Bob", "filename":"Whatevs"}'
```

### POSTimng images, GCP

```bash
export PROJECT_ID=$(gcloud config list --format='value(core.project)')
gcloud auth application-default login

curl -X POST $BACKEND_GCF \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: multipart/form-data" \
    -F "uploaded=@$HOME/localdev/gcp/image-text-translator/testing/images/ua_meme.jpg"
```