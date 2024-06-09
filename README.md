# Image Text Extract and Translation

## Example Use Case

- A user wants to translate a meme in Ukrainian, to English.

## Application Overview

A simple application that:

- Allows a user to upload or paste an image.
- The image is processed, probably using Google Vision API. Any text is extracted.
- The text is translated (if necessary) using Google Cloud Translation API.

## Architecture

- Frontend:
  - In Python and containerised.
  - Hosted in Cloud Run.
- Backend:
  - A Google Cloud Function, in Python.

