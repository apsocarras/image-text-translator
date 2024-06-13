# Testing

## Sample Curl Commands

### POSTing images, Local Dev

```bash
curl -X POST localhost:8080 \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/darren/localdev/gcp/image-text-translator/testing/images/ua_meme.jpg"

curl -X POST localhost:8080 \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/darren/localdev/gcp/image-text-translator/testing/images/fatrix.jpg"

curl -X POST localhost:8080 \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/darren/localdev/gcp/image-text-translator/testing/images/img7.jpg"

curl -X GET localhost:8080 -H "Content-Type: application/json" \
   -d '{"bucket":"Bob", "filename":"Whatevs"}'
```

### POSTimng images, GCP

```bash
curl -X POST https://europe-west2-image-text-translator-425921.cloudfunctions.net/extract-and-translate \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: multipart/form-data" \
    -F "uploaded=@ua_meme.jpg"
```