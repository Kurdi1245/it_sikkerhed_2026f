from src.test_strategier.login_system import LoginSystem


def test_bruger_livscyklus():
    system = LoginSystem()
    system.create_user("bob", "hemmelig123")

    # Korrekt login
    assert system.login("bob", "hemmelig123") == "ok"

    # 3 forkerte forsøg
    assert system.login("bob", "forkert") == "forkert"
    assert system.login("bob", "forkert") == "forkert"
    assert system.login("bob", "forkert") == "forkert"

    # Nu skal konto være låst
    assert system.login("bob", "hemmelig123") == "låst"