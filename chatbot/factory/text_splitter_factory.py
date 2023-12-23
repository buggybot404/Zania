from ..exception.chatbot_exception import ChatbotException
from ..text_splitters.implementation.character_text_splitter import CharTextSplitter
from ..text_splitters.implementation.html_text_splitter import HTMLTextSplitter
from ..text_splitters.implementation.recursive_text_splitter import RecursiveTextSplitter
from ..utils.constants import CHARACTER_TEXT_SPLITTER, RECURSIVE_CHARACTER_TEXT_SPLITTER, \
    HTML_TEXT_SPLITTER


class TextSplitterFactory:
    @staticmethod
    def get_text_splitter(text_splitter_name, **kwargs):
        if text_splitter_name == CHARACTER_TEXT_SPLITTER:
            return CharTextSplitter()
        elif text_splitter_name == RECURSIVE_CHARACTER_TEXT_SPLITTER:
            return RecursiveTextSplitter()
        elif text_splitter_name == HTML_TEXT_SPLITTER:
            return HTMLTextSplitter(**kwargs)
        else:
            raise ChatbotException(exception_id="0006", exception=Exception("Invalid Text Splitter Requested"),
                                   status_code=400)
