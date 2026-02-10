---

# 📘 Skoleprojekt – IT-Sikkerhed (2. semester)
Ali001

Dette repository indeholder et **skoleprojekt udarbejdet på Zealand – Sjællands Erhvervsakademi, Næstved**, som en del af **IT-Sikkerhed-uddannelsen på 2. semester**.

Projektet er udviklet med fokus på **programkvalitet, software-sikkerhed og secure design principles**, i overensstemmelse med **læringsmålene i studieordningen**.

---

## 🎓 Læringsmål fra studieordningen

### 🧠 Viden

Den studerende har viden om:

**Programkvalitet og IT-sikkerhed**

* 🛡️ Trusler mod software
* ✅ Kriterier for programkvalitet
* ⚠️ Fejlhåndtering i programmer

**Security Design Principles**

* 🏗️ Security by design
* 🕵️ Privacy by design

---

### 🛠️ Færdigheder

Den studerende kan tage højde for sikkerhedsaspekter ved at:

* ⌨️ Programmere håndtering af forventede og uventede fejl
* 🚫 Definere lovlige og ikke-lovlige inputdata (bl.a. til testformål)
* 🔌 Bruge API’er og standardbiblioteker
* 🔍 Opdage og forhindre sårbarheder i programkode
* 🏰 Sikkerhedsvurdere en given softwarearkitektur

---

### 🏆 Kompetencer

Den studerende kan:

* ⚖️ Håndtere risikovurdering af programkode for sårbarheder
* 🔐 Håndtere udvalgte krypteringstiltag

---

## ⚠️ Ansvarsfraskrivelse

Dette projekt er udelukkende udviklet til **undervisnings- og læringsformål** som en del af IT-Sikkerhed-uddannelsen.
Koden og løsningerne er **ikke beregnet til produktionsbrug** uden yderligere test, hærdning og sikkerhedsvurdering.

---

## 🏫 Uddannelsesinstitution

**Zealand – Sjællands Erhvervsakademi**
📍 Næstved
📚 IT-Sikkerhed – 2. semester

---

![alt text](<Skærmbillede 2026-02-03 kl. 11.03.21.png>)

FLERE UNITTEST
![alt text](<Skærmbillede 2026-02-03 kl. 11.25.30.png>)

EGET REPO
![alt text](<Skærmbillede 2026-02-03 kl. 11.25.30-1.png>)

AUTOMATISK TEST VED PUSH - IGANG
![alt text](<Skærmbillede 2026-02-03 kl. 11.42.26.png>)

AUTOMATISK TEST VED PUSH - AFSLUTTET
![alt text](<Skærmbillede 2026-02-03 kl. 11.44.19.png>)

DETALJERET BESKRIVELSE AF TEST
![alt text](<Skærmbillede 2026-02-03 kl. 11.44.08.png>)

NY BRANCH FOR AT TESTE - ALT RETTET
![alt text](<Skærmbillede 2026-02-03 kl. 12.36.38.png>)

**05/02-25 MFA (Multi‑Factor Authentication)** 


***

# ✅ **Testteknikker – MFA (Multi‑Factor Authentication)**

*Alle eksempler er bygget ud fra et klassisk MFA‑flow: login → password → MFA kode → adgang.*

***

# 1) **Ækvivalensklasser**

**Formål:** Dele input i grupper, hvor alle værdier i gruppen forventes at give samme resultat.

### Eksempel – MFA-kode (6‑cifret TOTP)

| Klasse         | Eksempel | Beskrivelse                   | Forventning |
| -------------- | -------- | ----------------------------- | ----------- |
| Gyldig kode    | 123456   | 6 tal                         | Accepteres  |
| Ugyldig længde | 12345    | < 6 tegn                      | Afvises     |
| Ugyldig længde | 1234567  | > 6 tegn                      | Afvises     |
| Ugyldige tegn  | "12A45!" | Ikke kun tal                  | Afvises     |
| Kode udløbet   | 123456   | Korrekt format men for gammel | Afvises     |

***

# 2) **Grænseværdianalyse**

### Eksempel – MFA kode udløbstid (30 sek. TOTP)

Test værdier omkring grænsen:

| Test       | Tid    | Forventning                |
| ---------- | ------ | -------------------------- |
| Lige under | 29 sek | ✔️ Gyldig                  |
| Lige på    | 30 sek | ✔️ Gyldig (nogle systemer) |
| Lige over  | 31 sek | ❌ Afvist                   |

### Eksempel – Antal mislykkede MFA-forsøg (max 5)

| Forsøg | Forventning               |
| ------ | ------------------------- |
| 4      | ✔️ Tilladt                |
| 5      | ✔️ Sidste tilladte forsøg |
| 6      | ❌ Konto låses             |

***

# 3) **CRUD(L)** for MFA

### **Create**

– Opret MFA‑enhed (TOTP, SMS, email, hardware key)

### **Read**

– Se registrerede MFA‑metoder  
– Læse backup‑koder

### **Update**

– Skifte primær MFA  
– Roteringsproces for keys

### **Delete**

– Fjerne MFA‑enheder  
– Deaktivere TOTP‑binding

### **List**

– Liste alle aktive MFA‑metoder for brugeren

***

# 4) **Cycle Process Test**

Test at MFA virker gentagne gange uden fejl:

**Scenarier:**

*   Brugeren logger ind 100 gange → genererer 100 MFA‑koder
*   Ingen hukommelseslæk
*   Ingen stigende svartider
*   Lockout resetter korrekt hver gang
*   Rate limiting holder sig stabil

**Formål:**  
At sikre at MFA‑flowet ikke bliver langsommere, ustabilt eller ikke nulstiller data korrekt over tid.

***

# 5) **Test Pyramiden**

### **Unit Tests (flest)**

*   Validering af MFA-kode længde
*   Tjek af TOTP‑algoritme
*   Lockout‑counter

### **Integration Tests**

*   Kommunikation med SMS‑gateway
*   TOTP sync med tid
*   API‑kald til identity provider

### **System / E2E Tests**

*   Hele login → password → MFA → adgang
*   Bruger med flere MFA‑metoder
*   Timeout flow og fallback

***

# 6) **Decision Table Test**

### **Regler for MFA login**

| Regel | Password OK? | MFA aktiv? | MFA korrekt? | Resultat             |
| ----- | ------------ | ---------- | ------------ | -------------------- |
| R1    | Ja           | Nej        | –            | Login OK (ingen MFA) |
| R2    | Ja           | Ja         | Ja           | Login OK             |
| R3    | Ja           | Ja         | Nej          | Afvist               |
| R4    | Nej          | –          | –            | Afvist               |
| R5    | Ja           | Ja         | –            | Prompt for MFA       |

***

# 7) **Security Gates – Hvor hører dine tests hjemme?**

### **Code/Dev Gate**

*   Unit tests for TOTP validering
*   Input validering for MFA‑kode
*   Ingen hardcodede secrets
*   SAST: ingen kritiske findings

### **Integration Security Gate**

*   Test af korrekt TLS mod SMS/TOTP service
*   Least privilege access
*   Ingen test‑credentials i produktion

### **System Security Gate**

*   DAST scanning: brute‑force MFA beskytte
*   Session‑timeout
*   Token‑genbrug forhindres

### **Release Candidate Gate**

*   Pentest af login/MFA flow
*   Secrets rotation fungerer
*   MFA failover korrekt testet

### **Go/No‑Go Gate**

*   Monitoring aktiv for MFA‑misbrug
*   Lockout alerts fungerer
*   Incident response klar

UNITTEST AF MFA
![alt text](<Skærmbillede 2026-02-05 kl. 10.27.16.png>)


# Flat File JSON Brugerdatabase 10 Feb 2026

Dette projekt implementerer en simpel brugerdatabase, der gemmer alle data i én JSON-fil uden brug af en traditionel relationsdatabase.

## Hvorfor er det smart at bruge en flat-file database (JSON-fil)?

- **Ingen installation eller opsætning** – ingen database-server, ingen Docker-container, ingen cloud-tjeneste
- **Kun Python standardbibliotek** – kræver ingen eksterne pakker (udover dataclasses som er indbygget)
- **Meget nem at forstå og debugge** – åbn filen `db_flat_file.json` i enhver teksteditor og se alle data med det samme
- **Perfekt til små projekter, prototyper, undervisning og PoC** – typisk < 1.000 brugere og lav skrivefrekvens
- **100 % portabel** – kopier bare JSON-filen til en anden maskine → databasen følger med
- **Ingen runtime-afhængigheder** – ingen process kører i baggrunden, ingen port-konflikter
- **Menneskelæselig backup og versionering** – nem at tage backup af, nem at se ændringer i git

**Begrænsninger** (når man skal overveje noget andet):  
- Ikke egnet til mange samtidige skrivninger  
- Ingen transaktioner / ACID-garanti  
- Ingen indeksering → langsom ved meget store datasæt  
- Ingen rettighedsstyring / brugeradgangskontrol  

→ Derfor: **Flat-file JSON er smart til læringsformål, små applikationer og hurtige prototyper** – men ikke til produktion med høj belastning.

## Unit tests – bevis for at databasen virker

Nedenfor er et screenshot af kørte unit tests (pytest -v -s).  
Alle vigtige tests er grønne – de få røde er **bevidst fejlede eksempler** brugt til undervisning i test-resultat-typer (assert-fejl, exceptions, skip osv.).

Unit test resultat – flat file database
![alt text](<Skærmbillede 2026-02-10 kl. 11.01.09.png>)

### Udvalgte tests med risici-kommentarer

Her er nogle af de tests med **Given → When → Then**-struktur og en kort risikovurdering:

![alt text](<Skærmbillede 2026-02-10 kl. 10.39.11.png>)

## Sikkerhed – GDPR og password-beskyttelse

For at opfylde GDPR-krav (især artikel 5 og 32 om dataminimering, integritet og fortrolighed) samt generel god password-sikkerhed, har jeg implementeret både **hashing** og **kryptering** af passwords.

### Valgte algoritmer

**Hashing af passwords**  
- Valgt: **Argon2id**  
- Alternativer: bcrypt, scrypt, PBKDF2-SHA256  
- **Begrundelse**:  
  Argon2id vandt Password Hashing Competition 2015 og er i 2026 stadig OWASP, NIST og ENISA's førstevalg. Den er memory-hard, hvilket gør brute-force og GPU/ASIC-angreb meget dyre. Parametre: time_cost=2, memory_cost=102400, parallelism=8 giver god balance mellem sikkerhed og performance på almindelige computere.

**Kryptering af følsomme data**  
- Valgt: **AES-256-GCM**  
- Alternativer: ChaCha20-Poly1305, AES-256-CBC (med HMAC)  
- **Begrundelse**:  
  AES-256-GCM er NIST-godkendt, understøtter autentificeret kryptering (ingen ændring af ciphertext uden opdagelse), og har hardware-acceleration (AES-NI) på næsten alle moderne processorer. Den er hurtig og giver både fortrolighed og integritet – bedre end CBC-mode (som kræver ekstra MAC).

### Hvornår og hvorfor krypterer jeg data?

- **Ved oprettelse af bruger** (`create_user`) og ved password-opdatering  
- **Hvad krypteres?** Rå-password krypteres med AES-256-GCM (valgfrit ekstra lag) + password hashs med Argon2id før lagring  
- **Hvorfor?**  
  - Hashing gør det umuligt at gendanne original-password ved datalæk (zero-knowledge).  
  - AES-kryptering beskytter JSON-filen mod fysisk tyveri eller uautoriseret læsning (f.eks. på delt server eller stjålen laptop).  
  - Opfylder GDPR artikel 32 krav om "passende tekniske og organisatoriske foranstaltninger".

### Hvornår og hvorfor dekrypterer jeg data?

- **Aldrig** for gemte passwords ved normal brug!  
- Ved login: Jeg dekrypterer **ikke** det gemte password. Jeg hasher det indtastede password og sammenligner med det gemte hash (`verify_password`).  
- **Hvorfor?**  
  Dekryptering af passwords i hukommelse er et stort sikkerhedshul (memory scraping, debugging, cold-boot-angreb). Zero-knowledge-validering eliminerer behovet fuldstændigt.

### Hvornår og hvorfor fjerner jeg dekrypteret data fra hukommelsen?

- **Straks efter brug** – efter `create_user` (når rå-password er hashed/krypteret) og efter `verify_password` (når indtastet password er tjekket)  
- **Hvordan?** `del variabel` + `gc.collect()`  
- **Hvorfor?**  
  GDPR artikel 5(1)e kræver dataminimering – data må kun opbevares så længe det er nødvendigt. Dekrypteret data i RAM er sårbar over for hukommelses-dump-angreb (malware, cold-boot, law-enforcement tools). Ved at fjerne det med det samme minimeres risikoen.

### Andre hensyn jeg har taget

- **Nøglehåndtering**: Master-nøglen til AES er **ikke** hard-coded i kode (demo-brug kun). I produktion skal den hentes fra miljøvariabel (`os.getenv`) eller en secure vault (f.eks. AWS Secrets Manager, HashiCorp Vault).  
- **Key rotation**: Nøglen bør roteres periodisk – ved rotation skal alle passwords gen-krypteres/hashes.  
- **Ingen logging**: Passwords eller rå-data logges aldrig.  
- **Backup-sikkerhed**: JSON-backup skal krypteres eller opbevares sikkert.  
- **Salt**: Håndteres automatisk af Argon2id (ingen manuel salt nødvendig).  
- **Side-channel-beskyttelse**: Argon2id er designet til at modstå timing- og cache-angreb.

![alt text](<Skærmbillede 2026-02-10 kl. 12.30.12.png>)
![alt text](<Skærmbillede 2026-02-10 kl. 12.30.18.png>)
![alt text](<Skærmbillede 2026-02-10 kl. 12.48.51.png>)