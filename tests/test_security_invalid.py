from app.src.auth.security import decode_access_token, get_password_hash, verify_password


def test_decode_invalid_token_returns_none():
    assert decode_access_token("invalid.token.string") is None


def test_password_hash_and_verify_roundtrip():
    password = "Senha123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpass", hashed) is False
