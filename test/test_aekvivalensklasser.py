import pytest


def validate_username(username: str) -> bool:
    return 3 <= len(username) <= 20


@pytest.mark.parametrize("username, forventet", [
    ("ab", False),          # for kort
    ("abc", True),          # gyldig minimum
    ("brugernavn123", True), # gyldig
    ("a" * 21, False),      # for langt
    ("", False),            # tom
    ("  abc  ", True),      # mellemrum OK? (måske strip først?)
])
def test_brugernavn_aekvivalensklasser(username, forventet):
    assert validate_username(username) == forventet