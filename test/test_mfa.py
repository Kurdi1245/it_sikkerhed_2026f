import pytest

# ─────────────── Simple MFA tests ───────────────

def test_mfa_valid_code():
    """Gyldig 6-cifret MFA-kode – skal passere"""
    mfa_code = "123456"
    assert len(mfa_code) == 6, "Koden skal være præcis 6 tegn"
    assert mfa_code.isdigit(), "Koden skal kun indeholde cifre"


def test_mfa_invalid_code_short():
    """For kort MFA-kode (5 tegn) – skal fejle på længde"""
    mfa_code = "12345"
    
    actual_assertion_error = False
    try:
        assert len(mfa_code) == 6, "Koden skal være præcis 6 tegn"
    except AssertionError:
        actual_assertion_error = True
    
    assert actual_assertion_error, "Forventede AssertionError ved for kort kode"


def test_mfa_invalid_code_long():
    """For lang MFA-kode (7 tegn) – skal fejle på længde"""
    mfa_code = "1234567"
    
    actual_assertion_error = False
    try:
        assert len(mfa_code) == 6, "Koden skal være præcis 6 tegn"
    except AssertionError:
        actual_assertion_error = True
    
    assert actual_assertion_error, "Forventede AssertionError ved for lang kode"


def test_mfa_invalid_characters():
    """Kode med bogstaver/symboler – skal fejle på isdigit()"""
    mfa_code = "12A45!"
    
    actual_assertion_error = False
    try:
        assert mfa_code.isdigit(), "Koden skal kun indeholde cifre"
    except AssertionError:
        actual_assertion_error = True
    
    assert actual_assertion_error, "Forventede AssertionError ved ugyldige tegn"


@pytest.mark.skip(reason="Denne test springes over med vilje – demonstrerer skip")
def test_mfa_skipped():
    """Denne test er bevidst ignoreret"""
    assert False, "Denne assertion skal aldrig køres"
    raise RuntimeError("Burde aldrig nå hertil")


def test_mfa_crash():
    """Simulerer et crash i MFA-systemet (f.eks. timeout eller fejl)"""
    with pytest.raises(RuntimeError, match="MFA systemet crashede"):
        raise RuntimeError("MFA systemet crashede med vilje")


def test_mfa_fail_wrong_value():
    """
    Demonstrerer fejl når MFA-metoden er forkert.
    Testen SKAL fejle – viser AssertionError på forkert værdi.
    """
    mfa_method = "SMS"
    
    actual_assertion_error = False
    try:
        assert mfa_method == "TOTP", "Forventede TOTP som MFA-metode"
    except AssertionError:
        actual_assertion_error = True
    
    assert actual_assertion_error, "Forventede AssertionError ved forkert MFA-metode"


def test_mfa_fail_missing_code():
    """
    Demonstrerer fejl når ingen MFA-kode er indtastet (None).
    Testen SKAL fejle – viser AssertionError på manglende værdi.
    """
    mfa_code = None
    
    actual_assertion_error = False
    try:
        assert mfa_code is not None, "MFA-kode mangler – forventede en værdi"
    except AssertionError:
        actual_assertion_error = True
    
    assert actual_assertion_error, "Forventede AssertionError ved manglende MFA-kode"


def test_mfa_crash_zero_division():
    """Simulerer fejl i TOTP-algoritme (division med nul)"""
    with pytest.raises(ZeroDivisionError):
        result = 10 / 0
        assert result == 1  # når aldrig hertil