import os
from flask import Flask, render_template, request
import anthropic
import markdown
import nh3

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise SystemExit("ANTHROPIC_API_KEY is not set. Run 'export ANTHROPIC_API_KEY=your-key' first.")

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
        except Exception as e:
            print(e)
            review_html = "<p>Something went wrong reaching the API — check your connection or API key.</p>"

        return render_template("result.html", review_html=review_html)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)