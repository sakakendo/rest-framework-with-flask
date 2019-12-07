
class APIBaseError(Exception):
    status_code = None
    code = None
    message = ""

    def __init__(self, message):
        self.message = message

    def json(self):
        return {
            "error": {
                "code": self.code,
                "message": self.message
            }
        }

class NotFound(APIBaseError):
    status_code = 404
    code = "NotFound"

class InvalidParamField(APIBaseError):
    status_code = 421
    code = "InvalidParamField"

