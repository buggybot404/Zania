import json
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from .constants import PDF_FILE_EXTENSION, JSON_FILE_EXTENSION
from ..exception.chatbot_exception import ChatbotException


class FileUtil:

    @staticmethod
    def get_file_type(file):
        # Check if the file is a PDF or JSON based on the file extension
        file_name, file_extension = file.name.split('.')

        if file_extension.lower() == PDF_FILE_EXTENSION:
            return PDF_FILE_EXTENSION
        elif file_extension.lower() == JSON_FILE_EXTENSION:
            return JSON_FILE_EXTENSION
        else:
            return None

    @staticmethod
    def load_pdf_file_data(pdf_file):
        try:
            file_path = os.path.join(os.path.join(os.path.dirname
                                                  ('\\'.join(os.path.realpath(__file__).split('\\')[:-1])), 'temp'),
                                     'temp_data_feeder.pdf')

            # Write the content of the in-memory file to the temporary file
            with open(file_path, 'wb') as temp_file_out:
                temp_file_out.write(pdf_file.read())

            loader = PyPDFLoader(file_path)
            return loader.load_and_split()
        except Exception as e:
            # Handle the exception
            raise ChatbotException(exception_id="0003", exception=e, status_code=400)
        finally:
            file_path = os.path.join(os.path.join(os.path.dirname
                                                  (os.path.realpath(__file__)), '../temp'), 'temp_data_feeder.pdf')
            os.remove(file_path)

    @staticmethod
    def load_json_file_data(json_file):
        # Load JSON data from the JSON file
        try:
            return json.load(json_file)
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            raise ChatbotException(exception_id="0002", exception=e, status_code=400)

    @staticmethod
    def load_feeder_json_file_data(file):
        try:
            docs = []
            # Load JSON file
            data = json.load(file)

            # Iterate through 'pages'
            for content in data:
                answer = content['answer']
                metadata = {"question": content['content']}

                if answer is not None:
                    docs.append(Document(page_content=answer, metadata=metadata))

            return docs
        except Exception as e:
            raise ChatbotException(exception_id="0005", exception=e, status_code=400)
