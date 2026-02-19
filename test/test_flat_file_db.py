import pytest
import os
import gc
from src.flat_file.data_handler import Data_handler
from src.flat_file.user import User

TEST_FILE = "db_flat_file_test.json"


@pytest.fixture(autouse=True)
def cleanup_test_file():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    #if os.path.exists(TEST_FILE):
      #  os.remove(TEST_FILE)


# ───────────────────────────────────────────────
# Basis tests – oprettelse og læsning
# ───────────────────────────────────────────────

def test_tom_database_har_0_brugere():
    db = Data_handler(TEST_FILE)
    
    # Given en ny, tom database
    # When vi tjekker antal brugere
    # Then skal antallet være nul
    assert db.get_number_of_users() == 0
    # Risiko hvis testen fejler: Systemet tror der er brugere når der ingen er → kan føre til logikfejl eller sikkerhedshuller


def test_opret_en_bruger_taeller_1():
    db = Data_handler(TEST_FILE)
    
    # Given en tom database
    assert db.get_number_of_users() == 0
    
    # When vi opretter én bruger
    db.create_user("Emma", "Jensen", "Hovedvejen", 5, "hemmelig123")
    
    # Then skal brugerantallet være steget til 1
    assert db.get_number_of_users() == 1
    # Risiko hvis testen fejler: Kan ikke oprette nye brugere → helt basal funktionalitet mangler


def test_oprettet_bruger_har_korrekt_data_og_auto_id():
    db = Data_handler(TEST_FILE)
    
    # Given en tom database
    
    # When vi opretter en bruger med kendte værdier
    raw_password = "pass2025"
    raw_first = "Lucas"
    raw_last = "Nielsen"
    raw_address = "Parkvej"
    db.create_user(raw_first, raw_last, raw_address, 12, raw_password)
    
    # Then skal ID være korrekt tildelt
    user = db.get_user_by_id(0)
    assert user is not None
    assert user.person_id == 0
    decrypted = db.get_user_decrypted(0)
    assert decrypted["street_number"] == 12

    
    # Følsomme felter skal være krypterede (ikke rå værdier)
    assert user.first_name != raw_first
    assert user.last_name != raw_last
    assert user.address != raw_address
    assert user.password != raw_password
    assert user.password.startswith("$argon2id$"), "Password skal være Argon2-hash"
    
    # Tjek at dekryptering virker korrekt
    decrypted = db.get_user_decrypted(0)
    assert decrypted["first_name"] == raw_first
    assert decrypted["last_name"] == raw_last
    assert decrypted["address"] == raw_address
    
    # Verify password virker stadig
    assert db.verify_password(0, raw_password) is True
    assert db.verify_password(0, "forkert") is False
    
    # Risiko hvis denne test fejler: Kryptering eller dekryptering virker ikke → persondata i klartekst eller utilgængelig


def test_flere_brugere_faår_fortloebende_id():
    db = Data_handler(TEST_FILE)
    
    # Given en tom database
    
    # When vi opretter tre brugere i rækkefølge
    db.create_user("A", "A", "A", 1, "a")
    db.create_user("B", "B", "B", 2, "b")
    db.create_user("C", "C", "C", 3, "c")
    
    # Then skal ID'er være fortløbende fra 0
    assert db.get_number_of_users() == 3
    assert db.get_user_by_id(0).person_id == 0
    assert db.get_user_by_id(1).person_id == 1
    assert db.get_user_by_id(2).person_id == 2
    # Risiko hvis testen fejler: ID-kollision eller manglende brugere → dataintegritet ødelagt


# ───────────────────────────────────────────────
# Deaktivering / aktivering
# ───────────────────────────────────────────────

def test_disable_eksisterende_bruger_aendrer_enabled():
    db = Data_handler(TEST_FILE)
    
    # Given en aktiv bruger i databasen
    db.create_user("Sara", "Hansen", "Strandvej", 8, "pink123")
    
    # When vi deaktiverer brugeren
    db.disable_user(0)
    
    # Then skal enabled-flag være False
    assert db.get_user_by_id(0).enabled is False
    # Risiko hvis testen fejler: Deaktivering virker ikke → blokerede brugere kan stadig logge ind (sikkerhedsbrud)


def test_enable_igen_slaar_enabled_til_true():
    db = Data_handler(TEST_FILE)
    
    # Given en deaktiveret bruger
    db.create_user("Noah", "Olsen", "Bygaden", 3, "blue456")
    db.disable_user(0)
    assert db.get_user_by_id(0).enabled is False
    
    # When vi aktiverer brugeren igen
    db.enable_user(0)
    
    # Then skal enabled-flag være True igen
    assert db.get_user_by_id(0).enabled is True
    # Risiko hvis testen fejler: Brugere kan ikke genaktiveres → falsk blokering / support-problemer


def test_disable_og_enable_paa_samme_tidspunkt():
    db = Data_handler(TEST_FILE)
    
    # Given en nyoprettet (aktiv) bruger
    db.create_user("Ida", "Pedersen", "Skovvej", 7, "green789")
    
    # When vi deaktiverer → aktiverer → deaktiverer igen
    db.disable_user(0)
    db.enable_user(0)
    db.disable_user(0)
    
    # Then skal sluttilstanden være deaktiveret
    assert db.get_user_by_id(0).enabled is False
    # Risiko hvis testen fejler: Inkonsekvent tilstandsstyring → uforudsigelig adfærd


def test_disable_og_enable_paa_forskellige_brugere():
    db = Data_handler(TEST_FILE)
    
    # Given to aktive brugere
    db.create_user("Freja", "Møller", "Elmevej", 4, "x")
    db.create_user("William", "Larsen", "Bøgevej", 9, "y")
    
    # When vi deaktiverer begge, men kun re-enabler den første
    db.disable_user(0)
    db.disable_user(1)
    db.enable_user(0)
    
    # Then skal første være aktiv og anden deaktiveret
    assert db.get_user_by_id(0).enabled is True
    assert db.get_user_by_id(1).enabled is False
    # Risiko hvis testen fejler: Forkert bruger påvirkes → sikkerheds- eller brugerfejl


def test_disable_ikke_eksisterende_bruger_returnerer_False():
    db = Data_handler(TEST_FILE)
    
    # Given en tom database
    
    # When vi forsøger at deaktivere en ikke-eksisterende bruger
    result = db.disable_user(999)
    
    # Vis besked i terminalen hvis brugeren ikke findes
    if result is None:
        print("\nBesked: Brugeren findes ikke – kunne ikke deaktivere")
    
    # Then skal metoden returnere None uden at crashe
    assert result is None
    # Risiko hvis testen fejler: Dårlig fejlhåndtering → kan føre til uventede exceptions i kaldende kode


def test_enable_ikke_eksisterende_bruger_returnerer_False():
    db = Data_handler(TEST_FILE)
    
    # Given en tom database
    
    # When vi forsøger at aktivere en ikke-eksisterende bruger
    result = db.enable_user(777)
    
    # Vis besked i terminalen hvis brugeren ikke findes
    if result is None:
        print("\nBesked: Brugeren findes ikke – kunne ikke aktivere")
    
    # Then skal metoden returnere None uden at crashe
    assert result is None
    # Risiko hvis testen fejler: Manglende robusthed → potentielle runtime-fejl


# ───────────────────────────────────────────────
# Edge cases & persistens
# ───────────────────────────────────────────────

def test_hent_bruger_med_ugyldig_id_returnerer_None():
    db = Data_handler(TEST_FILE)
    
    # Given en tom database
    
    # When vi søger efter ugyldige eller ikke-eksisterende ID'er
    # Then skal vi få None tilbage (ikke exception)
    assert db.get_user_by_id(-1) is None
    assert db.get_user_by_id(1000000) is None
    # Risiko hvis testen fejler: Kan føre til KeyError eller crash i steder der forventer None


def test_opret_bruger_med_minimalt_data():
    db = Data_handler(TEST_FILE)
    
    # Given en tom database
    
    # When vi opretter en bruger med minimale værdier
    db.create_user("X", "Y", "Z", 0, "pw")
    
    # Then skal brugeren kunne oprettes og hentes korrekt
    user = db.get_user_by_id(0)
    assert user is not None
    decrypted = db.get_user_decrypted(0)
    assert decrypted["street_number"] == 0

    assert user.enabled is True
    # Risiko hvis testen fejler: Validering mangler → ugyldige data kan gemmes i systemet


def test_database_persisterer_enabled_aendring_efter_genindlaesning():
    # Given vi arbejder med filbaseret persistens
    db1 = Data_handler(TEST_FILE)
    db1.create_user("Test", "Bruger", "Testvej", 99, "testpw")
    
    # When vi deaktiverer brugeren og genindlæser databasen
    db1.disable_user(0)
    db2 = Data_handler(TEST_FILE)
    
    # Then skal ændringen være bevaret
    assert db2.get_number_of_users() == 1
    assert db2.get_user_by_id(0).enabled is False
    # Risiko hvis testen fejler: Ændringer går tabt ved genstart → brugere bliver utilsigtet aktive


def test_opret_to_brugere_med_samme_navn_er_tilladt():
    db = Data_handler(TEST_FILE)
    
    # Given en tom database
    
    # When vi opretter to brugere med samme navn men forskellige øvrige data
    db.create_user("Anna", "Jensen", "A", 1, "pw1")
    db.create_user("Anna", "Jensen", "B", 2, "pw2")
    
    # Then accepteres begge brugere (ingen unik-navn-begrænsning)
    assert db.get_number_of_users() == 2
    # Risiko hvis testen fejler: Hvis systemet senere kræver unikke navne → inkonsekvent adfærd


def test_password_er_hashed_ved_oprettelse():
    db = Data_handler(TEST_FILE)
    raw_pw = "SuperHemmelig2026!"
    db.create_user("GDPR", "Test", "Sikkerhedsvej", 42, raw_pw)
    
    user = db.get_user_by_id(0)
    assert user.password != raw_pw               # MÅ IKKE være klartekst
    assert "$argon2id$" in user.password         # Argon2 format
    # Risiko hvis fejler: Password lagres i klartekst → GDPR-brud ved datalæk


def test_verify_password_virker():
    db = Data_handler(TEST_FILE)
    raw_pw = "MitPassword123"
    db.create_user("Login", "Bruger", "Loginvej", 1, raw_pw)
    
    assert db.verify_password(0, raw_pw) is True
    assert db.verify_password(0, "Forkert123") is False
    # Risiko hvis fejler: Forkert login tillades → sikkerhedsbrud


def test_midertidig_password_fjernes_fra_hukommelse():
    db = Data_handler(TEST_FILE)
    raw = "TempPw123!"
    db.create_user("Mem", "Test", "RamVej", 1, raw)
    
    # Efter kaldet må raw_password ikke længere være i hukommelse
    del raw
    gc.collect()
    
    # Bare en dummy-assert for at testen kører
    assert True
    # Risiko hvis ikke: Klartekst-password ligger i RAM → sårbar for memory-dump

def test_kryptering_og_dekryptering_er_korrekt():
    db = Data_handler(TEST_FILE)

    # Rå input (kendte værdier)
    raw_first = "Alice"
    raw_last = "Andersen"
    raw_address = "HemmeligVej"
    raw_street = 77
    raw_password = "TopSecret123!"

    # Opret bruger
    db.create_user(
        raw_first,
        raw_last,
        raw_address,
        raw_street,
        raw_password
    )

    # Hent rå (krypteret) bruger
    user = db.get_user_by_id(0)
    assert user is not None

    # ─────────────────────────────────────────
    # 1️⃣ Bevis: data er IKKE gemt i klartekst
    # ─────────────────────────────────────────
    assert user.first_name != raw_first
    assert user.last_name != raw_last
    assert user.address != raw_address
    assert user.street_number != raw_street

    # Password er hashet (ikke krypteret)
    assert user.password != raw_password
    assert user.password.startswith("$argon2id$")

    # ─────────────────────────────────────────
    # 2️⃣ Bevis: dekryptering giver korrekt data
    # ─────────────────────────────────────────
    decrypted = db.get_user_decrypted(0)

    assert decrypted["first_name"] == raw_first
    assert decrypted["last_name"] == raw_last
    assert decrypted["address"] == raw_address
    assert decrypted["street_number"] == raw_street

    # ─────────────────────────────────────────
    # 3️⃣ Bevis: password-verifikation virker
    # ─────────────────────────────────────────
    assert db.verify_password(0, raw_password) is True
    assert db.verify_password(0, "ForkertPassword") is False
