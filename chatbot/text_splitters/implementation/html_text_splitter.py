import json

from django.db import models

from ..base_text_splitter import BaseTextSplitter
from langchain.text_splitter import HTMLHeaderTextSplitter


class HTMLTextSplitter(BaseTextSplitter):

    headers_to_split_on = models.JSONField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        extracted_headers_to_split_on = []
        for tag, value in json.loads(self.headers_to_split_on.value_to_string()):
            extracted_headers_to_split_on.append((tag, value))

        self.text_splitter = HTMLHeaderTextSplitter(headers_to_split_on=extracted_headers_to_split_on)

    def create_text_splits(self, data_to_split):
        return self.text_splitter.split_text(data_to_split)

