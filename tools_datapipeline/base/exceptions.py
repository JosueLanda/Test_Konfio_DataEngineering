class ExtractorException(Exception):
    pass


# ======================Exceptions Connectivity======================START


class ExtractorErrorType(ExtractorException):
    pass


class ExtractorErrorAuthentication(ExtractorException):
    pass


class ExtractorErrorConnection(ExtractorException):
    pass


# ======================Exceptions Connectivity======================END

# ======================Exceptions Data======================START


class DataEmptyErrorType(ExtractorException):
    pass


class DataEmptyCollectionErrorType(ExtractorException):
    pass


# ======================Exceptions Data======================END
