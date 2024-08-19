# These errors can occur during the pipeline execution and can be handy to raise a specific status code for the API

class PipelineError(Exception):
    """Base class for other exceptions in the pipeline"""
    pass

class NoFileFoundError(PipelineError):
    """Raised when the input file is not found"""
    def __init__(self, message):
        self.message = message
        self.status_code = 404  # HTTP status code for Not Found

class EmptyDataError(PipelineError):
    """Raised when the input file is empty"""
    def __init__(self, message):
        self.message = message
        self.status_code = 400  # HTTP status code for Bad Request

class ParsingError(PipelineError):
    """Raised when the input file cannot be parsed"""
    def __init__(self, message):
        self.message = message
        self.status_code = 400  # HTTP status code for Bad Request

class UnexpectedError(PipelineError):
    """Raised when an unexpected error occurs"""
    def __init__(self, message):
        self.message = message
        self.status_code = 500  # HTTP status code for Internal Server Error
