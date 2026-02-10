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