from autherrors import *



from sheepdog.globals import (
    SUPPORTED_FORMATS,
)


class UnsupportedError(BaseUnsupportedError):

    def __init__(self, file_format, code=400, json=None):
        self.supported_formats = SUPPORTED_FORMATS
        super(UnsupportedError, self).__init__(message, code, json)

