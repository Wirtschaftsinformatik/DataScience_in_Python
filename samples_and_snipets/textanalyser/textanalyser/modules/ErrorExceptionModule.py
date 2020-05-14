class Error(Exception):
    pass


class NoTextFoundError(Error):
    """Exception raised if no text found after reading pdf"""

    def __init__(self, file, message):
        if message is None:
            message = 'No text found in given file'
        super(NoTextFoundError, self).__init__(message)
        self.file = file
