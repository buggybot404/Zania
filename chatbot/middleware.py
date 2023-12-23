from django.http import JsonResponse

from .exception.chatbot_exception import ChatbotException
from .exception.exception_constants import EXCEPTION_DETAILS


class ChatbotErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ChatbotException):
            # Customized error response for the custom exception
            error_response = {
                'error': EXCEPTION_DETAILS.get(exception.exception_id),
                'code': exception.exception_id,
            }
            # Log actual exception, if required
            return JsonResponse(error_response, status=exception.status_code)
