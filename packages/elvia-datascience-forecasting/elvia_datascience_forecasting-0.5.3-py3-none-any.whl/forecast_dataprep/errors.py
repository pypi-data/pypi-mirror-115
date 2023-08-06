class NotEnoughDataError(Exception):
    """Exception class to be raised when """
    pass


class UnspecifiedTimeSpanError(Exception):
    pass

class DataNotFound(Exception):
    """Exception class to be raised when the data coming from the Azure Dataset is not present"""
    pass