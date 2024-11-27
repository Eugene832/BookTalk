from flask import Flask, send_file, session
import database

app = Flask("Website")

@app.route("/favicon.ico")
def get_image():
    return send_file("files/favicon.png", mimetype="image/png")

@app.route("/")
def home():
    if "user_id" in session:
        return send_file("files/mainpage.html", mimetype="html")
    return "<a href='/login'>Login</a> or <a href='/register'>Register</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)