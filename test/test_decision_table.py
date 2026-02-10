import pytest
from src.test_strategier.login_system import LoginSystem


@pytest.mark.parametrize("korrekt_kode, konto_laast, forventet", [
    (True,  False, "ok"),     # korrekt + ikke låst
    (False, False, "forkert"), # forkert + ikke låst
    (False, True,  "låst"),    # forkert + låst
    (True,  True,  "låst"),    # korrekt + låst → stadig låst
])
def test_login_decision_table(korrekt_kode, konto_laast, forventet):
    system = LoginSystem()
    system.create_user("test", "kode1234")

    if konto_laast:
        system.locked_users.add("test")

    password = "kode1234" if korrekt_kode else "forkert"
    assert system.login("test", password) == forventet