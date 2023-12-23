import json
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..exception.chatbot_exception import ChatbotException
from ..views import create_vector_store


class ChatBotTestCase(TestCase):

    def setUp(self):
        self.questions_file = SimpleUploadedFile("questions.json",
                                                 b'{"questions": [{"question": "What is your name?"}]}')
        self.data_feeder_file = SimpleUploadedFile("feeder.json", b'[{"content": "dummy_data", "answer": "dummy_ans"}]')

    def tearDown(self):
        self.questions_file.close()
        self.data_feeder_file.close()

    @patch('chatbot.views.Chroma.from_documents')
    @patch('chatbot.factory.embeddings_factory.EmbeddingsFactory.get_embedding')
    @patch('chatbot.views.generate_answers_for_bot')
    def test_generate_chatbot_answers_should_succeed(self, mock_get_embedding, mock_from_documents,
                                                     mock_generate_answers_for_bot):
        mock_get_embedding.return_value = 'mock_embedding_result'
        mock_from_documents.return_value = 'mock_vector_store_result'
        mock_generate_answers_for_bot.return_value = '[("dummy_q": "dummy_ans")]'

        url = reverse('generate_chatbot_response')
        response = self.client.post(
            url,
            {
                "questions_set": self.questions_file,
                "data_feeder": self.data_feeder_file,
            },
        )

        # Assertions for the response
        self.assertEqual(response.status_code, 200)

    @patch('chatbot.views.Chroma.from_documents')
    @patch('chatbot.factory.embeddings_factory.EmbeddingsFactory.get_embedding')
    @patch('chatbot.views.generate_answers_for_bot')
    def test_generate_chatbot_answers_should_succeed_for_pdf_file(self, mock_get_embedding, mock_from_documents,
                                                                  mock_generate_answers_for_bot):
        mock_get_embedding.return_value = 'mock_embedding_result'
        mock_from_documents.return_value = 'mock_vector_store_result'
        mock_generate_answers_for_bot.return_value = '[("dummy_q": "dummy_ans")]'

        url = reverse('generate_chatbot_response')
        response = self.client.post(
            url,
            {
                "questions_set": self.questions_file,
                "data_feeder": SimpleUploadedFile("feeder.pdf",
                                                  b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 50 >>\nstream\nBT /F1 12 Tf 0 0 Td (Hello, World!) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000089 00000 n \n0000000145 00000 n \n0000000270 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n351\n%%EOF',
                                                  content_type="application/pdf"),
            },
        )

        self.assertEqual(response.status_code, 200)

    @patch('chatbot.views.Chroma.from_documents')
    @patch('chatbot.factory.embeddings_factory.EmbeddingsFactory.get_embedding')
    @patch('chatbot.views.generate_answers_for_bot')
    def test_generate_chatbot_answers_should_fail_for_invalid_pdf_file(self, mock_get_embedding, mock_from_documents,
                                                                       mock_generate_answers_for_bot):
        mock_get_embedding.return_value = 'mock_embedding_result'
        mock_from_documents.return_value = 'mock_vector_store_result'
        mock_generate_answers_for_bot.return_value = '[("dummy_q": "dummy_ans")]'

        url = reverse('generate_chatbot_response')
        response = self.client.post(
            url,
            {
                "questions_set": self.questions_file,
                "data_feeder": SimpleUploadedFile("feeder.pdf", b'test data'),
            },
        )
        response_data = json.loads(response.content.decode('utf-8'))
        # Assertions for the response
        self.assertEqual(response_data.get('code'), '0003')
        self.assertEqual(response_data.get('error'), 'ERROR_LOADING_PDF_FILE_DATA')

    @patch('chatbot.views.create_vector_store')
    @patch('chatbot.views.generate_answers_for_bot')
    def test_generate_chatbot_answers_failed_on_answer_generation(self, mock_generate_answers_for_bot,
                                                                  mock_create_vector_store):
        mock_create_vector_store.return_value = 'mock_vector_store'
        mock_generate_answers_for_bot.side_effect = ChatbotException('0010', 'Mocked exception', '500')

        url = reverse('generate_chatbot_response')

        response = self.client.post(
            url,
            {
                "questions_set": self.questions_file,
                "data_feeder": self.data_feeder_file,
            },
        )
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response_data.get('code'), '0010')
        self.assertEqual(response_data.get('error'), 'FAILED_TO_GENERATE_RESPONSE')

    def test_generate_chatbot_answers_should_fail_for_wrong_file_type(self):
        url = reverse('generate_chatbot_response')
        response = self.client.post(
            url,
            {
                "data_feeder": SimpleUploadedFile("questions.txt",
                                                  b'{"questions": [{"question": "What is your name?"}]}'),
                "questions_set": self.data_feeder_file,
            },
        )
        response_data = json.loads(response.content.decode('utf-8'))
        # Assertions for the response
        self.assertEqual(response_data.get('code'), '0004')
        self.assertEqual(response_data.get('error'), 'INVALID_DATA_FEEDER_FILE_EXTENSION')

    def test_generate_chatbot_answers_should_fail_for_invalid_request_data(self):
        url = reverse('generate_chatbot_response')
        response = self.client.post(
            url,
            {
                "data_feeder_invalid_name": self.questions_file,
                "questions_set": self.data_feeder_file,
            },
        )
        response_data = json.loads(response.content.decode('utf-8'))
        # Assertions for the response
        self.assertEqual(response_data.get('code'), '0001')
        self.assertEqual(response_data.get('error'), 'INVALID_REQUEST_DATA')

    @patch('chatbot.views.Chroma.from_documents')
    @patch('chatbot.factory.embeddings_factory.EmbeddingsFactory.get_embedding')
    def test_create_vector_store_success(self, mock_get_embedding, mock_from_documents):
        mock_get_embedding.return_value = 'mock_embedding_result'
        mock_from_documents.return_value = 'mock_vector_store_result'

        result = create_vector_store(['text1', 'text2'])

        # Assert the expected behavior
        mock_get_embedding.assert_called_once_with('open_ai')
        mock_from_documents.assert_called_once_with(documents=['text1', 'text2'], embedding='mock_embedding_result')
        self.assertEqual(result, 'mock_vector_store_result')

    @patch('chatbot.factory.embeddings_factory.EmbeddingsFactory.get_embedding')
    def test_create_vector_store_exception(self, mock_get_embedding):
        mock_get_embedding.side_effect = Exception('Mocked exception')

        with self.assertRaises(ChatbotException) as context:
            create_vector_store(['text1', 'text2'])

        # Assert the expected exception behavior
        mock_get_embedding.assert_called_once_with('open_ai')
        self.assertEqual(context.exception.exception_id, '0009')
        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(str(context.exception.exception), 'Mocked exception')
