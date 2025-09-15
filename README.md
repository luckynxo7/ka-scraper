# Kleinanzeigen Felgen/Reifen Scraper (Streamlit)

Ein Streamlit‑Tool, das vollständige Händlerseiten von **Kleinanzeigen** (z. B. `https://www.kleinanzeigen.de/pro/reifenfelgenkeller`) crawlt, alle Inserate durchblättert, Titel/Beschreibung **parst**, **Bilder herunterlädt** und alles als **CSV** exportiert – optimiert auf Felgen/Reifen/Kompletträder‑Shops.

> ⚖️ Hinweis: Du gibst an, dass du das Einverständnis von Kleinanzeigen **und** der Händler hast. Verwende das Tool nur mit entsprechender Erlaubnis. Das Script respektiert `robots.txt` optional (konfigurierbar), verwendet Wartezeiten und User‑Agent.

## Features
- Mehrere Händler‑Links auf einmal
- Automatisches Paging (25 Inserate pro Seite → alle Seiten)
- Extrahiert: Felgenhersteller, Reifenhersteller, Felgenfarbe, Zollgröße, Lochkreis, ET VA/HA, Reifengröße VA/HA, Reifenbreite VA/HA, Nabendurchmesser, Reifensaison, Profiltiefe VA/HA, DOT VA/HA
- Speichert **alle Bilder** jedes Inserats (lokal) und referenziert sie in der CSV
- Sauberer **CSV‑Export** für WordPress Bulk‑Upload (inkl. Bildspalten)
- Throttling, Retry, Rotating User‑Agent

## Schnellstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Konfiguration (lokal via .env oder in Streamlit Cloud via Secrets)
```env
SCRAPER_BASE_DELAY=1.5
SCRAPER_JITTER=1.0
SCRAPER_CONCURRENCY=2
SCRAPER_SEPARATE_VENDOR_DIRS=true
SCRAPER_RESPECT_ROBOTS=true
# Optional bei Captcha/403:
KLEINANZEIGEN_SESSION=ka_session=...
```

## CSV-Format
- `source_url`, `listing_url`, `title`, `description`, `price`, `location`, `vendor_name`, `image_paths` (Semikolon‑getrennt), `timestamp`
- Domainfelder: `Felgenhersteller, Reifenhersteller, Felgenfarbe, Zollgröße, Lochkreis, ET_VA, ET_HA, Reifengröße_VA, Reifengröße_HA, Reifenbreite_VA, Reifenbreite_HA, Nabendurchmesser, Reifensaison, Profiltiefe_VA, Profiltiefe_HA, DOT_VA, DOT_HA`

## Hinweise
- Strukturänderungen möglich → Selektoren in `scraper/client.py` anpassen.
- Manche WP‑Importer wollen Bild‑**URLs** statt Pfade → `export.py`/Uploader anpassen.
- In Streamlit Cloud: Ergebnisse über die Download‑Buttons (CSV/ZIP) ziehen.
