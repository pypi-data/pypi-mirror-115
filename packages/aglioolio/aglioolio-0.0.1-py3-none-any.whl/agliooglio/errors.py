class OctarinError(Exception):
    """Base class for exceptions in this module."""

    pass


class AuthenticationError(OctarinError):
    """Exception raised for authentication errors."""

    def __init__(self, message: str = "Invalid access key"):
        self.message = message


class AlreadyExistsError(OctarinError):
    """Exception raised when uploading an object whose
    name is already registered.
    """

    def __init__(self, message: str = "Object already exists"):
        self.message = message
