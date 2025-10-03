# backend/tests/test_auth.py
from backend.auth import get_password_hash, verify_password

def test_password_hashing():
    password = "mysecretpassword"

    # Hash the password
    hashed_password = get_password_hash(password)

    # Ensure the hash is not the same as the original password
    assert hashed_password != password

    # Verify that the correct password passes
    assert verify_password(password, hashed_password) == True

    # Verify that an incorrect password fails
    assert verify_password("wrongpassword", hashed_password) == False