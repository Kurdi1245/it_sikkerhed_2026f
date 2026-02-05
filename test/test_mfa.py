import pytest

# ─────────────── Simple MFA tests ───────────────

def test_mfa_valid_code():
    # Gyldig 6-cifret MFA-kode – skal passere
    mfa_code = "123456"
    assert len(mfa_code) == 6
    assert mfa_code.isdigit()


def test_mfa_invalid_code_short():
    # For kort MFA-kode – skal fejle
    mfa_code = "12345"
    assert len(mfa_code) == 6


def test_mfa_invalid_code_long():
    # For lang MFA-kode – skal fejle
    mfa_code = "1234567"
    assert len(mfa_code) == 6


def test_mfa_invalid_characters():
    # Indeholder ikke-talfaste tegn – skal fejle
    mfa_code = "12A45!"
    assert mfa_code.isdigit()


@pytest.mark.skip(reason="Denne test springes over med vilje")
def test_mfa_skipped():
    # Bliver ignoreret helt
    assert False
    raise RuntimeError("Burde aldrig blive kørt")


def test_mfa_crash():
    # Simuleret crash (fx kunne være service timeout)
    raise RuntimeError("MFA systemet crashede med vilje")


def test_mfa_fail_wrong_value():
    # Fejler på forventet MFA-type (bare et eksempel)
    mfa_method = "SMS"
    assert mfa_method == "TOTP"   # fejler


def test_mfa_fail_missing_code():
    # Bruger har ikke indtastet kode → None
    mfa_code = None
    assert mfa_code is not None


def test_mfa_crash_zero_division():
    # Simuleret fejl i TOTP algoritme – division med nul
    result = 10 / 0    # crasher
    assert result == 1  # når aldrig hertil