
class ChatbotException(Exception):

    def __init__(self, exception_id, exception, status_code):
        self.exception_id = exception_id
        self.exception = exception
        self.status_code = status_code
        super().__init__(self.exception)
        