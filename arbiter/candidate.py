from google.cloud import vision


class Candidate():
    def __init__(self, preview_url):
        self.preview_url = preview_url
        self.labels = []
        self.text = None

    @staticmethod
    def api_error_handler(response):
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    @classmethod
    def evaluate(cls, uri):
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        label_response = client.label_detection(image=image)
        text_response = client.text_detection(image=image)
        labels = label_response.label_annotations
        text = text_response.full_text_annotation

        label_list = [label.description for label in labels]
        compiled_text = ''.join(chr.lower()
                                for chr in text.text if chr.isalnum())

        if label_response.error.message:
            api_error_handler(label_response.error.message)
        elif text_response.error.message:
            api_error_handler(text_response.error.message)

        candidate = cls(preview_url=uri, labels=label_list, text=compiled_text)
