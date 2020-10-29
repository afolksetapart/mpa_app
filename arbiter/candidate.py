from google.cloud import vision


class Candidate():
    def __init__(self, preview_url):
        self.preview_url = preview_url
        self.labels = []
        self.text = None

    @staticmethod
    def api_error_handler(response):
        """Handles an error from the Google Vision API"""
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    @classmethod
    def evaluate(cls, uri):
        """Sends preview image to Google Vision API and retrieves labels and text(compiled)"""
        c = cls(preview_url=uri)
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = c.preview_url

        label_response = client.label_detection(image=image)
        text_response = client.text_detection(image=image)
        labels = label_response.label_annotations
        text = text_response.full_text_annotation

        label_list = [label.description for label in labels]
        compiled_text = ''.join(chr.lower()
                                for chr in text.text if chr.isalnum())

        print(label_list)
        print(compiled_text)

        if label_response.error.message:
            api_error_handler(label_response.error.message)
        elif text_response.error.message:
            api_error_handler(text_response.error.message)

        c.labels = label_list
        c.text = compiled_text

        return c
