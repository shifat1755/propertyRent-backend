class EmailAlreadyExistsError(Exception):
    """Raised when an email address is already registered in the system."""

    pass


class UsernameAlreadyExistsError(Exception):
    """Raised when a username is already taken by another user."""

    pass
