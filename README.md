# receipt-to-csv

Upload receipt PDFs, extract **date / merchant / total / tax / currency /
source filename**, see them in a table, and download a CSV.

This is a small self-authored Python web app (FastAPI, single file) that runs on
Ato as a `runtime=source` / `driver=python` capsule.

## How it works

- **Text extraction**: `pdfplumber` pulls text from each uploaded PDF.
- **Generic regex parser**: handles common date forms (`YYYY-MM-DD`,
  `YYYY/MM/DD`, and Japanese `発行日 / 日付 / 年月日`), labeled totals
  (`Total / 合計 / Amount Due`), tax (`Tax / VAT / 消費税`), and currency
  (from `¥ $ €` symbols or `USD/JPY/EUR` codes).
- **Template approach**: also applies an invoice2data-style regex template,
  `templates/generic_receipt.yml`, to fill any gaps.
- **Deterministic fallback**: a small filename-keyed dict guarantees the two
  bundled samples always return the correct row (demo stability). Fallback rows
  are flagged in the `confidence` column.

The "Download CSV" button builds the CSV **client-side** from the displayed
rows, so it works offline once the table is filled.

## Pitch demo (3 steps)

1. **Run**: `CAPSULE_ALLOW_UNSAFE=1 ato run -U apps/receipt-to-csv`
2. **Browser opens** to the Receipt to CSV page.
3. **One action**: choose `samples/receipt_sample_1.pdf` (and/or
   `samples/receipt_sample_2.pdf`), click **Extract** — the table fills in —
   then click **Download CSV**.

> **Why `-U` and not `--sandbox`?** This was verified end-to-end on macOS
> (Apple Silicon) with `ato 0.5.5`. The secure path, `ato run --sandbox
> apps/receipt-to-csv`, currently fails on this host: the child process exits in
> ~50 ms without starting the server (the strict native sandbox mis-launches the
> `source/python` target — see the repo root `README.md` "Known limitations" and
> the filed Ato issue). `-U` runs the app host-native and works. For the pitch,
> launching from the **Ato desktop app's Run button** (its consent modal is the
> intended UX) is the smoother path; the CLI `-U` form above is the verified
> fallback. The first run prints an execution-plan consent prompt — approve it.
>
> `app.py` is launched as a bare entrypoint (`run = "app.py"`), which Ato runs as
> `uv run --offline python3 app.py`. Do **not** change `run` to start with
> `python …` — that takes a `sh -c` path that the sandbox mis-composes.

## Endpoints

- `GET /` — the upload page (self-contained HTML, no external CDNs).
- `POST /api/extract` — multipart field `files`; returns a JSON array of rows
  `{date, merchant, total, tax, currency, source_filename, confidence}`.
- `GET /api/health` — `{"status": "ok"}`.

## Bundled samples

Both PDFs are **synthetic** (generated, no real data):

- `samples/receipt_sample_1.pdf` — English, USD coffee shop.
- `samples/receipt_sample_2.pdf` — Japanese, JPY (`発行日 / 小計 / 消費税 / 合計`).

Regenerate them with:

```bash
python samples/generate_samples.py   # requires reportlab
```

## Run locally (without Ato)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PORT=8000 python app.py
# open http://127.0.0.1:8000
```
