import unittest
from unittest.mock import MagicMock
from ..main import extract_and_translate, detect_text, translate_text
from google.cloud import vision
from google.cloud import translate_v2 as translate

class TestImageTextTranslator(unittest.TestCase):

    # def test_extract_and_translate_with_uploaded_file(self):
    #     with open("test_image.jpg", "rb") as f:
    #         test_image_data = f.read()

    #     # Mock the request object using MagicMock
    #     request_mock = MagicMock()
    #     request_mock.method = 'POST'
    #     request_mock.files = {"uploaded": io.BytesIO(test_image_data)}
    #     request_mock.form = {"to_lang": "es"}

    #     # Assuming detect_text and translate_text are working correctly
    #     # and mocking their responses for this test
    #     expected_detected_text = {"text": "Sample text", "src_lang": "en"}
    #     expected_translated_text = {"text": "Texto de ejemplo", "src_lang": "en", "to_lang": "es"}

    #     # Mock the responses from the Vision and Translate APIs
    #     vision.ImageAnnotatorClient.text_detection = MagicMock(return_value=MagicMock(text_annotations=[MagicMock(description=expected_detected_text["text"])]))
    #     translate.Client.detect_language = MagicMock(return_value={"language": expected_detected_text["src_lang"]})
    #     translate.Client.translate = MagicMock(return_value={"translatedText": expected_translated_text["text"]})

    #     response = extract_and_translate(request_mock)

    #     self.assertEqual(response, expected_translated_text["text"])

    def test_detect_text_with_text(self):
        """ Mock the response from the Vision API """
        test_text = "Sample text"
        vision.ImageAnnotatorClient.text_detection = MagicMock(return_value=MagicMock(text_annotations=[MagicMock(description=test_text)]))
        translate.Client.detect_language = MagicMock(return_value={"language": "en"})

        image_mock = MagicMock(spec=vision.Image)
        detected_text = detect_text(image_mock)

        self.assertEqual(detected_text["text"], test_text)

    def test_detect_text_without_text(self):
        """ Mock the response from the Vision API for no text detected """
        vision.ImageAnnotatorClient.text_detection = MagicMock(return_value=MagicMock(text_annotations=[]))
        translate.Client.detect_language = MagicMock(return_value={"language": "und"})

        image_mock = MagicMock(spec=vision.Image)
        detected_text = detect_text(image_mock)

        self.assertEqual(detected_text["text"], "")

    def test_translate_text(self):
        """ Mock the response from the Translate API """
        message = {"text": "Hola mundo", "src_lang": "es"}
        to_lang = "en"
        expected_translated_text = {"text": "Hello world", "src_lang": "es", "to_lang": "en"}

        # Mock the response from the Translate API
        translate.Client.translate = MagicMock(return_value={"translatedText": expected_translated_text["text"]})

        translated_text = translate_text(message, to_lang)

        self.assertEqual(translated_text, expected_translated_text)

    def test_translate_text_no_translation(self):
        message = {"text": "Hello world", "src_lang": "en"}
        to_lang = "en"
        expected_translated_text = {"text": "Hello world", "src_lang": "en", "to_lang": "en"}

        translated_text = translate_text(message, to_lang)

        self.assertEqual(translated_text, expected_translated_text)

if __name__ == "__main__":
    unittest.main()
