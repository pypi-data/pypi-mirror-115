import qph
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return qph.generate_html("test.html")

if __name__ == "__main__":
    app.run(debug=True)