from flask import Flask, send_file

app = Flask(__name__)

@app.route("/favicon.png")
def get_image():
    return send_file("files/favicon.png", mimetype="image/png")

@app.route("/")
def home():
    return send_file("files/mainpage.html", mimetype="html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)