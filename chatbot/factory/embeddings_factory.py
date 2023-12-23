from langchain_community.embeddings import OpenAIEmbeddings

from ..utils.constants import OPEN_AI_EMBEDDING
from ..exception.chatbot_exception import ChatbotException


class EmbeddingsFactory:

    @staticmethod
    def get_embedding(embedding_name):
        if embedding_name == OPEN_AI_EMBEDDING:
            return OpenAIEmbeddings()
        else:
            raise ChatbotException(exception_id="0008", exception=Exception("Invalid Embedding Requested"), status_code=400)
        # Configure for different embeddings if required
