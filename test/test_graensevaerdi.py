import pytest


def validate_password(password: str) -> bool:
    """Validerer password – minimum 8 tegn."""
    return len(password) >= 8


def test_password_graensevaerdi():
    # Grænseværdi-analyse: 7, 8, 9 tegn
    assert validate_password("1234567") is False   # lige under grænse
    assert validate_password("12345678") is True   # præcis på grænsen
    assert validate_password("123456789") is True  # over grænsen
    
    # Ekstra: tom streng og meget kort
    assert validate_password("") is False
    assert validate_password("a") is False