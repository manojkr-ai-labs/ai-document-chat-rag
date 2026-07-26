class DocumentNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidPDF(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class VectorDatabaseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class LLMError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
class TaskNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)   
        