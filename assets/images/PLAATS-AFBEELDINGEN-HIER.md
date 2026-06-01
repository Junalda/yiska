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

## Logo: van JPG naar web-klare PNG + favicons
Het aangeleverde logo is een JPG met witte achtergrond. Zet het eenmalig om naar
een transparante, geoptimaliseerde PNG en genereer de favicons. De website
verwijst al naar `logo.png` (header, footer, `apple-touch-icon`, Open Graph) en
naar `favicon.svg` (browser-tab — al meegeleverd en scherp op elk scherm).

**Snelste route (online, geen installatie):**
1. Achtergrond verwijderen → https://www.remove.bg of https://www.photoroom.com
2. Optimaliseren → https://squoosh.app (exporteer als PNG, ~1000 px breed) → opslaan als `logo.png`
3. Favicons genereren → https://realfavicongenerator.net of https://favicon.io
   en de uitvoer (o.a. `apple-touch-icon.png`, `favicon-32x32.png`) in deze map zetten.

**Of via de command line (ImageMagick):**
```bash
# witte achtergrond transparant maken + bijsnijden
magick logo.jpg -fuzz 8% -transparent white -trim +repage logo-trim.png
# optimaliseren naar webformaat (max 1000 px breed)
magick logo-trim.png -resize 1000x logo.png
# favicons
magick logo.png -resize 180x180 apple-touch-icon.png
magick logo.png -resize 512x512 logo-512.png
```
De meegeleverde `favicon.svg` (vector, transparant, retina-scherp) hoeft niet
vervangen te worden; vervang die alleen als je een exacte 1:1 kopie van het logo
als favicon wilt.

> **Tip (Open Graph):** voor mooie social-previews kun je later een
> `og-image.jpg` van 1200×630 px toevoegen en in de `<meta property="og:image">`
> tags zetten. Nu staat daar `logo.png`, wat ook werkt.

## Aanbevelingen
- **Logo**: lever bij voorkeur een transparante PNG (of SVG) aan.
- **Foto's**: liefst minimaal 1600 px breed, bijgesneden op een liggende
  verhouding (ca. 3:2 of 4:3) voor de scherpste weergave.
- Optimaliseer de bestandsgrootte (bijv. via TinyPNG/Squoosh) voor snelle laadtijd en betere SEO.
