import pytest

def test_pass():
    # Denne test vil passere
    assert 1 + 1 == 2


def test_fail():
    # Denne test vil fejle (assertion fejler)
    assert 1 * 1 == 3


@pytest.mark.skip(reason="Springes over med vilje")
def test_skip():
    assert False                    # bliver ignoreret
    raise RuntimeError("boom")      # bliver også ignoreret


def test_crash():
    # Denne test crasher (exception før assert)
    raise RuntimeError("Test crashede med vilje")
    assert False                    # når aldrig hertil


# ─────────────── Nye simple tests ───────────────

def test_fail_2():
    # En anden måde at fejle på – simpel sammenligning
    assert "hej" == "hello"


def test_crash_2():
    # Simpel division med nul → crasher
    x = 100 / 0


def test_fail_3():
    # Fejler på liste-indhold (meget almindeligt)
    frugter = ["æble", "pære", "banan"]
    assert "appelsin" in frugter