# Yiska Cleaning VOF — website

Premium, meerpagina-website voor **Yiska Cleaning VOF**, een professioneel
schoonmaakbedrijf voor bedrijven. Gebouwd in pure HTML/CSS/JavaScript — geen
build-stap, geen dependencies — zodat de site overal snel te hosten is en
uitstekend scoort bij zoekmachines en AI-engines.

Ontwerprichting: **Apple × Amazon** — premium, minimalistisch en betrouwbaar
(Apple) gecombineerd met duidelijk, gestructureerd en conversiegericht (Amazon).
"De Apple onder de schoonmaakbedrijven."

## Pagina's
| Pagina | Bestand | Doel |
|--------|---------|------|
| Home | `index.html` | 5-secondenpitch, diensten, waarom Yiska, proces, FAQ, CTA |
| Diensten | `diensten.html` | Gedetailleerde dienstbeschrijvingen + Service-schema |
| Over Yiska | `over-yiska.html` | Verhaal, kernwaarden, belofte |
| Voor Bedrijven | `voor-bedrijven.html` | B2B-doelgroepen, voordelen, werkwijze (conversie) |
| Contact | `contact.html` | Offerteformulier + contactgegevens + ContactPage-schema |

## Bestandsstructuur
```
.
├── index.html / diensten.html / over-yiska.html / voor-bedrijven.html / contact.html
├── robots.txt          # AI-bots (GPTBot, PerplexityBot, Google-Extended, Applebot ...) expliciet toegestaan
├── sitemap.xml
└── assets/
    ├── css/styles.css  # volledig design system
    ├── js/main.js      # navigatie, scroll-reveal, formulier, image-fallback
    └── images/         # plaats hier de foto's (zie PLAATS-AFBEELDINGEN-HIER.md)
```

## Foto's toevoegen
Zie **`assets/images/PLAATS-AFBEELDINGEN-HIER.md`** voor de exacte bestandsnamen.
Zolang foto's ontbreken, tonen we automatisch nette placeholders in de
huisstijl — de site oogt dus altijd af.

## Bedrijfsgegevens (ingevuld)
De echte bedrijfsgegevens staan overal verwerkt in de HTML (footer + JSON-LD),
`sitemap.xml` en `robots.txt`:

- **Bedrijfsnaam**: Yiska Cleaning VOF
- **Domein**: `https://yiska.com/`
- **E-mail**: `hello@yiska.org`
- **Telefoon**: `+31614265377` / weergave `06 14 26 53 77`
- **KvK-nummer**: `99892421`
- **Werkgebied**: "Actief in heel Nederland" — vul desgewenst plaats/regio in
  voor sterkere lokale SEO (bv. stad in `address` van het JSON-LD).

### Contactformulier koppelen
Het formulier werkt out-of-the-box via een `mailto:`-fallback (opent de
mailclient). Voor een echte serververwerking koppel je `#contact-form` aan een
endpoint, bijvoorbeeld [Formspree](https://formspree.io):

```html
<form id="contact-form" action="https://formspree.io/f/JOUW_ID" method="POST">
```
en verwijder dan de `e.preventDefault()`-regel in `assets/js/main.js`.

## SEO & AI-engine optimalisatie
- Semantische HTML5, één duidelijke `<h1>` per pagina, logische H2/H3-structuur.
- Unieke `<title>` en meta-description per pagina + canonical + Open Graph.
- **Structured data (JSON-LD)**: `CleaningService` (LocalBusiness), `FAQPage`,
  `Service`/`ItemList`, `AboutPage`, `ContactPage`, `BreadcrumbList`.
- `sitemap.xml` + `robots.txt` die AI-crawlers expliciet toelaten.
- Natuurlijke verwerking van zoektermen: *schoonmaakbedrijf voor bedrijven,
  zakelijke schoonmaak, kantoorschoonmaak, glazenwasser voor bedrijven,
  schoonmaakcontract, professioneel schoonmaakbedrijf, schoonmaak voor kantoren,
  schoonmaak voor bedrijfspanden*.
- Heldere "wie helpen we / wat doen we / waar werken we / waarom Yiska"-blokken.

## Lokaal bekijken
Open `index.html` in de browser, of start een lokale server:
```bash
python3 -m http.server 8000
# → http://localhost:8000
```

## Deployen op Vercel (statische site — GEEN build)
Dit is een statische site zonder build-stap. Er is **geen** `package.json`,
Vite, npm of andere bundler nodig.

De meegeleverde `vercel.json` zet dit expliciet vast, zodat Vercel niets
probeert te builden:
```json
{
  "framework": null,
  "buildCommand": "",
  "installCommand": "",
  "outputDirectory": "."
}
```

**Als de deploy nog steeds `vite build` draait**, staat er nog een override in
het Vercel-dashboard. Zet daar (Project → Settings → Build & Development
Settings):
- **Framework Preset**: `Other`
- **Build Command**: leeg laten (override uitschakelen)
- **Output Directory**: leeg laten / `.` (override uitschakelen)
- **Install Command**: leeg laten

Daarna opnieuw deployen. De site wordt dan rechtstreeks vanuit de repo-root
geserveerd (`index.html` als startpagina).
