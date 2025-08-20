# GenAI Sports Tournament Calendar (Assignment Solution)


## ✅ What this delivers
- A pipeline to **collect** (stubbed), **process**, **store**, and **serve** upcoming sports tournaments.
- Output in **CSV/JSON** and a **SQLite** DB.
- A **Flask API** (`GET /tournaments`) + a minimal **UI** (HTML + JS) to browse data.
- **Sample data** included; replace with real scraping/API in `src/collect.py`.

## 📦 Project Structure
```
genai_tournaments/
├── data/                     # sample data + SQLite DB
├── db/                       # schema
├── src/                      # code
├── templates/                # UI template
├── static/                   # (reserved)
└── requirements.txt
```

## 🛠 Tech Stack
- Python 3.9+
- Libraries: Flask, pandas, requests, beautifulsoup4, python-dotenv (optional)
- DB: SQLite (in-memory or file)

## 🧭 How to Run (Local)
```bash
pip install -r requirements.txt

# (1) Initialize DB with sample data
python -m src.load_db

# (2) Start API + UI (served from the same Flask app)
python -m src.api
# visit http://localhost:8000
```

### API Examples
- `GET /tournaments`
- `GET /tournaments?sport=Cricket&level=National`
- `GET /tournaments?from=2025-09-01&to=2025-12-31&limit=50`

## 🧩 Data Model
Fields:
- `sport`, `tournament_name`, `level`, `start_date`, `end_date`,
- `official_url`, `streaming`, `image`, `summary`

Indexes on dates, sport, level for faster filtering.

## 🧱 Sample DB Schema
See `db/schema.sql`.

## 🔄 Pipeline
1. **Collect**: `src/collect.py`
   - `collect_all(mode="sample")` loads sample JSON.
   - Replace with site-specific scrapers or official APIs (BCCI, AIFF, BWF, etc.).
2. **Process**: `src/process.py` → normalize dates, ensure columns, sort.
3. **Export**: `src/export.py` → CSV/JSON.
4. **Load DB**: `src/load_db.py` → SQLite.
5. **Serve**: `src/api.py` → `/tournaments`; `templates/index.html` is the UI.

## 🧪 Generate Artifacts
```bash
python - <<'PY'
from src.collect import collect_all
from src.process import to_dataframe
from src.export import export_csv, export_json

items = collect_all(mode="sample")
df = to_dataframe(items)
export_csv(df, "data/tournaments.csv")
export_json(df, "data/tournaments.json")
print("Exported data/tournaments.csv and data/tournaments.json")
PY
```

## 🧠 Ensuring Accuracy & Freshness (Design Notes)
- **Sources**: Prefer official federation websites and event pages.
- **Verification**: Cross-check at least two sources; store `last_checked_at`.
- **Freshness**: Schedule daily update; compare against prior hash to detect changes.
- **Normalization**: Pydantic (optional) for schema validation.
- **Errors**: Retry with exponential backoff; capture 4xx/5xx separately.

## ⚖️ Scalability
- Swap SQLite with MySQL/PostgreSQL.
- Add Celery/cron for periodic refresh.
- Cache frequent queries with Redis.
- Add pagination (`limit`, `offset`) already supported.

## 🚧 Limitations & Next Steps
- Scraping varies by site → need per-site adapters.
- Some events lack structured dates → require robust parsing.
- Add tests (pytest) and logging.
- Optional: integrate LLM summarization for 50-word summary (OpenAI/Groq) with guardrails.

## 🧰 Suggested Tools & APIs
- Search: Google Custom Search API / SerpAPI
- Sports: Official federation pages (BCCI, AIFF, BWF, BFI, TTFI, AICF, CFI, PKL)
- Parsing: BeautifulSoup, lxml
- Scheduling: cron / APScheduler
- Validation: Pydantic

