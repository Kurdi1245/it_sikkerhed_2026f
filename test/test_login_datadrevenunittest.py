import pytest
from src.test_strategier.login_system import LoginSystem


@pytest.mark.parametrize(
    "forsøg_password, antal_fejl_forinden, forventet_resultat",
    [
        ("12345678", 0, "ok"),          # korrekt, ingen fejl før
        ("forkert",   0, "forkert"),     # forkert første gang
        ("forkert",   2, "forkert"),     # forkert tredje gang
        ("12345678",  3, "låst"),        # korrekt efter lås
        ("forkert",   3, "låst"),        # forkert efter lås
    ]
)
def test_login_datadreven(forsøg_password, antal_fejl_forinden, forventet_resultat):
    system = LoginSystem()
    system.create_user("test", "12345678")

    # Simuler tidligere fejl
    system.failed_attempts["test"] = antal_fejl_forinden
    if antal_fejl_forinden >= 3:
        system.locked_users.add("test")

    assert system.login("test", forsøg_password) == forventet_resultat