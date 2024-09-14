import os
import pytest
import logging
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image

@pytest.fixture
def app():
    """Flask test app configuration with logging enabled."""
    from ui_cr.app import app  # Import the app
    app.config['TESTING'] = True
    app.logger.setLevel(logging.DEBUG)  # Enable debug logging
    
    # Enable Flask's logger propagation to the root logger
    app.logger.propagate = True

    return app

@pytest.fixture
def client(app):
    """Fixture to create a test client for the Flask app."""
    return app.test_client()

@patch('ui_cr.app.make_authorized_post_request')
def test_entry_post_valid_image(mock_make_post_request, client, app):
    """Test the POST request with a valid image and form."""

    # Create a test image and save it to a BytesIO object
    img_io = BytesIO()
    test_image = Image.new('RGB', (10, 10), color='red')
    test_image.save(img_io, format='JPEG')
    img_io.seek(0)  # Move to the start of the BytesIO object

    # Ensure the BACKEND_GCF environment variable is set for this test
    backend_gcf = os.environ.get('BACKEND_GCF', 'undefined')
    app.logger.debug(f"BACKEND_GCF: {backend_gcf}")

    # Mocking the response from the backend function
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Test translated text"
    mock_make_post_request.return_value = mock_response

    # Create a mock image file to simulate form data
    img_data = (img_io, 'test_image.jpg')

    # Send POST request
    response = client.post(
        '/',
        data={'file': img_data, 'to_lang': 'en'},
        content_type='multipart/form-data'
    )

    # Check the response status
    assert response.status_code == 200

    # Debugging logs
    app.logger.debug(f"Test response data: {response.data}")

    # Check if the mock function was called, ensuring the image was processed correctly
    try:
        mock_make_post_request.assert_called_once()
        called_args, called_kwargs = mock_make_post_request.call_args

        # Check that the arguments are as expected
        assert called_kwargs['endpoint'] == backend_gcf
        assert called_kwargs['to_lang'] == 'en'
        assert called_kwargs['filename'] == 'test_image.jpg'
        assert called_kwargs['content_type'] in ['image/jpeg', 'image/png']
        
        # Optionally check that image_data is not empty
        assert called_kwargs['image_data'], "Image data is empty"

        # Add additional check for content length
        assert len(called_kwargs['image_data']) > 0, "Image data length is zero"
        
        # Log the mock function call arguments
        app.logger.debug(f"make_authorized_post_request called with: {called_kwargs}")

    except AssertionError as e:
        app.logger.error(f"make_authorized_post_request was not called correctly: {str(e)}")
        raise e

    # Check that there are no flash error messages
    assert b"No file selected for uploading." not in response.data
    assert b"Unable to process image." not in response.data
    assert b"Unsupported image format." not in response.data

    # Check for the translation text in the response
    assert b"Test translated text" in response.data
