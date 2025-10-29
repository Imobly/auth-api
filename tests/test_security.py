import os
from importlib import reload


def test_create_and_decode_token(monkeypatch):
    # Ensure settings are created with test secret
    monkeypatch.setenv("SECRET_KEY", "test-secret-for-ci")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "5")

    # Reload config and security modules to pick up env vars
    import app.core.config as config

    reload(config)

    import app.src.auth.security as security

    reload(security)

    token = security.create_access_token({"sub": "123", "username": "tester"})
    payload = security.decode_access_token(token)

    assert payload is not None
    assert payload.get("sub") == "123"
    assert payload.get("username") == "tester"
