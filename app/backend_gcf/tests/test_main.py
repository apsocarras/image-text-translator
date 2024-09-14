import pytest
from unittest.mock import patch, MagicMock # To mock external API calls
from flask import Flask, request # To simulate HTTP requests
from io import BytesIO

# Import the function from main.py
from backend_gcf.main import extract_and_translate

@pytest.fixture
def app():
    """ Fixture for Flask app context, for creating HTTP requests """
    app = Flask(__name__)
    return app

# Use patch to replace the Google clients with mock objects
@patch('backend_gcf.main.vision_client')
@patch('backend_gcf.main.translate_client')
def test_extract_and_translate_with_posted_image(mock_translate_client, mock_vision_client, app: Flask):
    with app.test_request_context(
        method='POST',
        data={
            'uploaded': (BytesIO(b'sample image data'), 'test_image.jpg'),
            'to_lang': 'en'
        },
        content_type='multipart/form-data'
    ):
        # Mock Vision API response
        mock_vision_client.text_detection.return_value = MagicMock(
            text_annotations=[MagicMock(description="Put a glass of rice and three glasses of water in a saucepan")]
        )

        # Mock Translate API response
        mock_translate_client.detect_language.return_value = {"language": "uk"}
        mock_translate_client.translate.return_value = {"translatedText": "Put a glass of rice and three glasses of water in a saucepan"}

        # Call the function - the request object is the one simulated in test_request_context
        response = extract_and_translate(request)

        # Check the result
        assert response == "Put a glass of rice and three glasses of water in a saucepan"
