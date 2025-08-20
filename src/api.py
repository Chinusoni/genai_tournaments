from flask import Flask, jsonify, request, send_from_directory
import sqlite3, os

ROOT = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT, "data", "tournaments.db")
TEMPLATES = os.path.join(ROOT, "templates")
STATIC = os.path.join(ROOT, "static")

app = Flask(__name__, template_folder=TEMPLATES, static_folder=STATIC)

def query_db(filters):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql = "SELECT * FROM tournaments WHERE 1=1"
    params = []

    if filters.get("sport"):
        sql += " AND lower(sport)=lower(?)"
        params.append(filters["sport"])
    if filters.get("level"):
        sql += " AND lower(level)=lower(?)"
        params.append(filters["level"])
    if filters.get("from"):
        sql += " AND date(start_date) >= date(?)"
        params.append(filters["from"])
    if filters.get("to"):
        sql += " AND date(end_date) <= date(?)"
        params.append(filters["to"])

    sql += " ORDER BY date(start_date) ASC"
    if filters.get("limit"):
        sql += " LIMIT ?"
        params.append(int(filters["limit"]))
    if filters.get("offset"):
        sql += " OFFSET ?"
        params.append(int(filters["offset"]))

    cur.execute(sql, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/tournaments")
def tournaments():
    filters = {
        "sport": request.args.get("sport"),
        "level": request.args.get("level"),
        "from": request.args.get("from"),
        "to": request.args.get("to"),
        "limit": request.args.get("limit"),
        "offset": request.args.get("offset"),
    }
    return jsonify(query_db(filters))

# Serve UI
@app.get("/")
def home():
    from flask import render_template
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
