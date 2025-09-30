import bcrypt

MAX_PASSWORD_BYTES = 72

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    Ensures it's within bcrypt's 72-byte limit.
    """
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > MAX_PASSWORD_BYTES:
        raise ValueError(
            f"Password is too long for bcrypt: {len(password_bytes)} bytes "
            f"(limit is {MAX_PASSWORD_BYTES})"
        )

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against the stored hash.
    """
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > MAX_PASSWORD_BYTES:
        return False  # bcrypt won't handle this safely

    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
