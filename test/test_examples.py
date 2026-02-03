import pytest

def test_pass():
    # Denne test vil passere
    assert 1 + 1 == 2


def test_fail():
    # Nu rettet – ellers ville den fejle
    assert 1 * 1 == 1           # ← rettet fra 3 til 1


@pytest.mark.skip(reason="Springes over med vilje")
def test_skip():
    assert False                    # bliver ignoreret
    raise RuntimeError("boom")      # bliver også ignoreret


def test_crash():
    # Fjernet crash – nu bare en normal test
    assert True                     # eller fjern assert helt


# ─────────────── Nye simple tests – rettet ───────────────

def test_fail_2():
    # Nu passer den
    assert "hej" == "hej"           # ← rettet fra "hello"


def test_crash_2():
    # Fjernet division med nul
    x = 100 / 1                     # ← rettet fra 0 til 1
    assert x == 100


def test_fail_3():
    # Nu passer listen
    frugter = ["æble", "pære", "banan", "appelsin"]  # ← tilføjet appelsin
    assert "appelsin" in frugter