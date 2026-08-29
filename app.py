import os
from flask import Flask, render_template, request
import anthropic
import markdown
import nh3
import sqlite3
import datetime

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise SystemExit("ANTHROPIC_API_KEY is not set. Run 'export ANTHROPIC_API_KEY=your-key' first.")

DB_FILE = "reviews.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_text TEXT,
            review_text TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)
client = anthropic.Anthropic()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        code_text = request.form.get("code_text", "").strip()
        if not code_text:
            return "<p>No code was submitted.</p><a href='/'>Back</a>"

        try:
            message = client.messages.create(
                model="claude-opus-5",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": f"Review this Python code and list concrete issues:\n\n{code_text}"
                }]
            )
            review_text = ""
            for block in message.content:
                if block.type == "text":
                    review_text += block.text
            review_html = nh3.clean(markdown.markdown(review_text, extensions=["fenced_code"]))

            conn = sqlite3.connect(DB_FILE)
            conn.execute(
                "INSERT INTO reviews (code_text, review_text, created_at) VALUES (?, ?, ?)",
                (code_text, review_text, datetime.datetime.now().isoformat())
            )
            conn.commit()
            conn.close()

        except Exception as e:
            print(e)
            review_html = "<p>Something went wrong reaching the API — check your connection or API key.</p>"

        return render_template("result.html", review_html=review_html)

    return render_template("index.html")

@app.route("/history")
def history():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()
    conn.close()

    history_items = []
    for row in rows:
        history_items.append({
            "code_text": row["code_text"],
            "review_html": nh3.clean(markdown.markdown(row["review_text"], extensions=["fenced_code"])),
            "created_at": row["created_at"]
        })

    return render_template("history.html", history_items=history_items)


if __name__ == "__main__":
    app.run(debug=True)