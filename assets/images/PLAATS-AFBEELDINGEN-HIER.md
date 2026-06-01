# Afbeeldingen toevoegen

De website verwijst naar onderstaande bestandsnamen. Zolang een bestand
ontbreekt, toont de site automatisch een nette, gemerkte placeholder (in de
huisstijlkleuren) — er verschijnt dus nooit een "gebroken afbeelding".

Plaats de door jou aangeleverde foto's met **exact deze bestandsnamen** in deze
map (`assets/images/`). Daarna werkt alles automatisch, zonder dat er HTML
aangepast hoeft te worden.

| Bestandsnaam                  | Welke aangeleverde foto                                              | Waar gebruikt |
|-------------------------------|---------------------------------------------------------------------|---------------|
| `logo.png`                    | Het Yiska Cleaning VOF logo (druppel + sprayfles)                  | Header + footer (alle pagina's) |
| `hero-glasbewassing.jpg`      | Medewerker (van achteren) die de winkelpui/ramen wast met wasser   | Hero homepage, Diensten (glasbewassing) |
| `glasbewassing-2.jpg`         | Medewerker (van voren) die geconcentreerd de ruit wast             | Voor Bedrijven (waarom-sectie) |
| `vloeronderhoud-rood.jpg`     | De glanzende **rode** sport-/gymvloer                              | Homepage, Diensten (bedrijfsschoonmaak/contract), Over Yiska |
| `vloeronderhoud-blauw.jpg`    | De **blauwe** vloer in de schoolgang                               | Diensten (kantoorschoonmaak + vloeronderhoud) |
| `team-yiska.jpg`              | De foto van het koppel (oprichters)                                | Over Yiska |

## Belangrijk
Door de webomgeving komen geüploade foto's wél in de chat te staan, maar **niet
als bestand in de repository**. De bestanden hierboven moeten daarom éénmalig
handmatig in deze map worden gezet (via een commit/upload naar de repo). Omdat
de bestandsnamen al overal in de HTML staan, hoeft er verder niets aangepast te
worden — de placeholders verdwijnen automatisch zodra de bestanden aanwezig zijn.

## Logo: van JPG naar web-klare PNG + favicons (geautomatiseerd)
Het aangeleverde logo is een JPG met witte achtergrond. In de repo zit een kant-
en-klaar script dat hiervan alle benodigde, transparante, geoptimaliseerde
assets maakt — met **randbehoud van witte details binnen het logo** (wolkjes,
sparkles en de witte "Yiska"-letters blijven staan; alleen de buitenste witte
achtergrond wordt transparant).

**Aanpak:**
```bash
# eenmalig de beeldbibliotheken installeren
pip install Pillow numpy scipy

# logo-assets genereren uit jouw JPG
python3 tools/build_logo.py pad/naar/jouw-logo.jpg
```

Het script schrijft naar `assets/images/`:

| Bestand                 | Formaat            | Gebruik |
|-------------------------|--------------------|---------|
| `logo.png`              | transparant, ≤1024 px breed | header + footer (alle pagina's) |
| `logo-512.png`          | 512×512, transparant | algemeen / social / app |
| `logo-1024.png`         | 1024×1024, transparant | hoge resolutie / retina |
| `apple-touch-icon.png`  | 180×180, navy (dekkend) | iOS-snelkoppeling |
| `favicon.ico`           | 16/32/48, transparant | browser-tab (oudere browsers) |

De website verwijst al naar deze bestanden:
- `<link rel="icon" href="favicon.svg">` (vector, primair — al meegeleverd)
- `<link rel="icon" href="favicon.ico">` (fallback)
- `<link rel="apple-touch-icon" href="apple-touch-icon.png">`
- header/footer/Open Graph → `logo.png`

Zodra je het script draait verschijnen de bestanden en is alles meteen actief —
geen HTML-aanpassingen nodig.

> **Tip (Open Graph):** voor nóg mooiere social-previews kun je later een
> `og-image.jpg` van 1200×630 px toevoegen in de `<meta property="og:image">`
> tags. Nu staat daar `logo.png`, wat ook prima werkt.

## Aanbevelingen
- **Logo**: lever bij voorkeur een transparante PNG (of SVG) aan.
- **Foto's**: liefst minimaal 1600 px breed, bijgesneden op een liggende
  verhouding (ca. 3:2 of 4:3) voor de scherpste weergave.
- Optimaliseer de bestandsgrootte (bijv. via TinyPNG/Squoosh) voor snelle laadtijd en betere SEO.
