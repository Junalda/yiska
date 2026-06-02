# 🖼️ Afbeeldingen-vervangingsgids — Yiska Cleaning VOF

De website gebruikt nu **tijdelijke, premium placeholder-afbeeldingen** zodat de
site er volledig afgewerkt uitziet zolang de definitieve Yiska-foto's er nog niet
zijn. Elke placeholder is in de HTML gemarkeerd met:

```html
<!-- TEMPORARY IMAGE - REPLACE WITH FINAL YISKA PHOTO -->
```

De placeholders zijn gegenereerd met `tools/make_placeholders.py` (huisstijl-
gradient, glas-/architectuurmotieven, zacht licht, vignet en korrel — geen
cartoons, geen stockfoto's, geen lege vlakken).

---

## ✅ Zo vervang je ze — ZONDER de code aan te raken

1. Maak je definitieve Yiska-foto klaar (bijgesneden, liggend, ≥1600 px breed,
   geoptimaliseerd via bijv. [Squoosh](https://squoosh.app)).
2. Sla hem op met **exact dezelfde bestandsnaam** als de placeholder en zet hem
   in `assets/images/` (overschrijf de placeholder).
3. Commit/upload en deploy. Klaar — geen HTML-wijzigingen nodig.

> De `<img src="…">` blijft hetzelfde; alleen de inhoud van het bestand verandert.
> Optioneel mag je daarna de `TEMPORARY`-comment uit de HTML verwijderen.

---

## 📋 Overzicht van alle placeholders

| # | Placeholder-bestand | Waar gebruikt (pagina → sectie) | Vervang door — definitieve Yiska-foto |
|---|---------------------|----------------------------------|----------------------------------------|
| 1 | `hero-placeholder.jpg` | **index.html** → hero (homepage) | Sterkste actiefoto: medewerker die de winkelpui/ramen wast (glasbewassing) |
| 2 | `commercial-cleaning-placeholder.jpg` | **index.html** → "Voor wie wij werken" | Gereinigde bedrijfsruimte / commerciële vloer |
| 3 | `contact-placeholder.jpg` | **contact.html** → "Direct contact" | Uitnodigende team-/locatiefoto of bedrijfspand |

### Eigen foto's met definitieve bestandsnamen (geen "placeholder" in de naam)
Op **over-yiska.html** verwijzen de twee beeldslots naar vaste, semantische
bestandsnamen. Plaats hier je eigen foto's met exact deze namen:

| Bestand | Pagina → sectie | Foto | Aanbevolen formaat |
|---------|------------------|------|--------------------|
| `over-eigenaren.jpg` | **over-yiska.html** → "Ons verhaal" (1e beeld) | De **eigenaren** van Yiska (de foto van het koppel) | ~1600×1200 (4:3), gezichten gecentreerd |
| `over-team.jpg` | **over-yiska.html** → "Onze belofte" (2e beeld) | Het **team** aan het werk (glazenwasser in restaurant) | ~1600×1200 (4:3) |
| `business-clients-yiska.jpg` | **voor-bedrijven.html** → "Waarom bedrijven kiezen voor Yiska" | Zakelijke schoonmaak voor bedrijven (klant-/locatiefoto) | ~1600×1200 (4:3) |
| `office-cleaning-yiska.jpg` | **diensten.html** → Kantoorschoonmaak | ✅ geplaatst (3:2) |
| `glass-cleaning-yiska.jpg` | **diensten.html** → Glasbewassing | ✅ geplaatst (3:2) |
| `commercial-cleaning-yiska.jpg` | **diensten.html** → Bedrijfsschoonmaak | ✅ geplaatst (3:2) |
| `facility-cleaning-yiska.jpg` | **diensten.html** → Vloeronderhoud | ✅ geplaatst (3:2) |
| `team-at-work-yiska.jpg` | **diensten.html** → Schoonmaakcontracten | ✅ geplaatst (3:2) |

> Reeds verwijderd (niet meer in gebruik): `about-placeholder.jpg`,
> `office-cleaning-placeholder.jpg`, `glass-cleaning-placeholder.jpg`,
> `business-placeholder.jpg`. Nog actief als placeholder: `hero-placeholder.jpg`,
> `commercial-cleaning-placeholder.jpg`, `contact-placeholder.jpg`.

---

## 🎨 Specificaties per slot (voor de scherpste weergave)

| Placeholder | Aanbevolen formaat | Verhouding |
|-------------|--------------------|-----------|
| `hero-placeholder.jpg` | 1920×1200 px | ~16:10 (breed, cinematic) |
| overige `*-placeholder.jpg` | 1600×1067 px | 3:2 |
| `contact-placeholder.jpg` | 1600×900 px | 16:9 |

Alle afbeeldingen staan met `object-fit: cover`, dus afwijkende verhoudingen
worden netjes bijgesneden — exact formaat is niet verplicht, maar wel het mooist.

---

## 🔄 Placeholders opnieuw genereren (optioneel)
```bash
pip install Pillow numpy scipy
python3 tools/make_placeholders.py
```

## 🧭 Verschil met de definitieve, semantische bestandsnamen
Wil je liever de oorspronkelijke, semantische bestandsnamen gebruiken
(`hero-glasbewassing.jpg`, `team-yiska.jpg`, …)? Zie dan
`assets/images/PLAATS-AFBEELDINGEN-HIER.md`. Voor de snelste route geldt echter:
**overschrijf simpelweg de `*-placeholder.jpg` bestanden** — dat werkt zonder
enige codewijziging.
