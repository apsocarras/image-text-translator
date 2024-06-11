# Testing

## Sample Curl Commands

### POSTing images

```bash
curl -X POST localhost:8080 \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/darren/localdev/gcp/image-text-translator/assets/test_images/ua_meme.jpg"

curl -X POST localhost:8080 \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/darren/localdev/gcp/image-text-translator/assets/test_images/fatrix.jpg"

curl -X POST localhost:8080 \
   -H "Content-Type: multipart/form-data" \
   -F "uploaded=@/home/darren/localdev/gcp/image-text-translator/assets/test_images/img7.jpg"

curl -X GET localhost:8080 -H "Content-Type: application/json" \
   -d '{"bucket":"Bob", "filename":"Whatevs"}'
```