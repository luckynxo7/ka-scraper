import os
import re
import io
import zipfile
import streamlit as st
from typing import List, Dict

from scraper.client import KleinanzeigenClient, ScraperConfig
from scraper.parse import enrich_with_domain_fields
from scraper.export import write_csv

st.set_page_config(page_title="Kleinanzeigen Felgen/Reifen Scraper", layout="wide")
st.title("🔧 Kleinanzeigen Scraper – Felgen / Reifen / Kompletträder")

st.markdown(
    "Gib unten **ein oder mehrere Händler-Links** (jeweils eine Zeile) ein. "
    "Das Tool blättert automatisch durch alle Seiten, lädt **alle Bilder** und exportiert eine **CSV** für den Bulk-Upload."
)

vendor_input = st.text_area("Händler-Links (je Zeile ein Link)",
                            placeholder="https://www.kleinanzeigen.de/pro/reifenfelgenkeller")
col1, col2 = st.columns(2)
with col1:
    out_dir = st.text_input("Ausgabeordner", value="output")
with col2:
    csv_name = st.text_input("CSV-Dateiname", value="export.csv")

start = st.button("🚀 Start")
progress = st.empty()
log = st.empty()

if start:
    vendors = [l.strip() for l in vendor_input.splitlines() if l.strip()]
    if not vendors:
        st.error("Bitte mindestens einen Händler-Link angeben.")
        st.stop()

    cfg = ScraperConfig()
    client = KleinanzeigenClient(cfg)
    all_rows: List[Dict] = []

    for v_idx, vurl in enumerate(vendors, start=1):
        st.write(f"### Händler {v_idx}: {vurl}")
        v_slug = re.sub(r"[^a-z0-9]+", "-", vurl.lower())
        vendor_dir = os.path.join(out_dir, v_slug)
        os.makedirs(vendor_dir, exist_ok=True)

        page_no = 0
        for html in client.iter_vendor_pages(vurl):
            page_no += 1
            links = client.extract_listing_links(html, vurl)
            st.write(f"Seite {page_no}: {len(links)} Inserate gefunden")

            for i, link in enumerate(links, start=1):
                progress.progress(((v_idx-1) + i/ max(1,len(links))) / max(1,len(vendors)))
                item = client.parse_listing(link)
                item['source_url'] = vurl

                # Bilder speichern
                img_dir = os.path.join(vendor_dir, re.sub(r"[^a-z0-9]+", "-", link.lower())[-30:])
                image_paths = client.download_images(item.get('image_urls', []), img_dir)
                item['image_paths'] = image_paths

                # Domainfelder anreichern
                item = enrich_with_domain_fields(item)
                all_rows.append(item)

    csv_path = os.path.join(out_dir, csv_name)
    write_csv(all_rows, csv_path)

    st.success(f"Fertig! CSV exportiert: {csv_path}")
    st.dataframe(all_rows)

    # Downloads
    with open(csv_path, "rb") as f:
        st.download_button("📄 CSV herunterladen", f, file_name=csv_name, mime="text/csv")

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_path, arcname=csv_name)
        for row in all_rows:
            for p in (row.get("image_paths") or []):
                try:
                    zf.write(p, arcname=p.replace(out_dir + os.sep, ""))
                except Exception:
                    pass
    zip_buf.seek(0)
    st.download_button("📦 Alles als ZIP herunterladen", zip_buf, file_name="export_bundle.zip", mime="application/zip")
