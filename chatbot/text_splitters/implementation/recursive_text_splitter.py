from ..base_text_splitter import BaseTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ...exception.chatbot_exception import ChatbotException


class RecursiveTextSplitter(BaseTextSplitter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def create_text_splits(self, data_to_split):
        try:
            if isinstance(data_to_split, list):
                split = self.text_splitter.split_documents(data_to_split)
            else:
                split = self.text_splitter.split_text(data_to_split)
            return split
        except Exception as e:
            raise ChatbotException(exception_id="0007", exception=e, status_code=400)

