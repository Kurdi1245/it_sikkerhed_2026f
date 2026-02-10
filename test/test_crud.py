from src.test_strategier.login_system import LoginSystem


def test_crud_bruger():
    system = LoginSystem()

    # Create
    system.create_user("alice", "password123")
    assert "alice" in system.users
    assert system.users["alice"] == "password123"

    # Read (via direct access)
    assert system.users.get("alice") == "password123"

    # Update
    system.users["alice"] = "nytpassword"
    assert system.users["alice"] == "nytpassword"

    # Delete
    del system.users["alice"]
    assert "alice" not in system.users