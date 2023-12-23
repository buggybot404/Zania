from ..base_text_splitter import BaseTextSplitter
from langchain.text_splitter import CharacterTextSplitter


class CharTextSplitter(BaseTextSplitter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=100, chunk_overlap=0)

    def create_text_splits(self, data_to_split):
        return self.text_splitter.split_text(data_to_split)

