import os, sqlite3, json, argparse

ROOT = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT, "data", "tournaments.db")
SCHEMA_PATH = os.path.join(ROOT, "db", "schema.sql")
SAMPLE_JSON = os.path.join(ROOT, "data", "sample_tournaments.json")

def init_db():
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(schema)
    conn.commit()
    conn.close()

def load_from_json(json_path=SAMPLE_JSON):
    with open(json_path, "r") as f:
        items = json.load(f)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM tournaments")
    for r in items:
        cur.execute(
            """
            INSERT INTO tournaments (sport, tournament_name, level, start_date, end_date, official_url, streaming, image, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            "",
            (r.get("sport",""), r.get("tournament_name",""), r.get("level",""),
             r.get("start_date",""), r.get("end_date",""), r.get("official_url",""),
             r.get("streaming",""), r.get("image",""), r.get("summary",""))
        )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default=SAMPLE_JSON, help="Path to tournaments JSON.")
    args = parser.parse_args()
    init_db()
    load_from_json(args.json)
    print("Database initialized and loaded from", args.json)
