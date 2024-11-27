from flask import *
import database as db
import hashlib

app = Flask("Website")
app.secret_key = db.getHash("super secret key")

@app.route("/favicon.png")
def get_image():
    return send_file("files/favicon.png", mimetype="image/png")


@app.route("/")
def home():
    if "user_id" in session:
        return render_template("mainpage.html")
    return render_template("login_or_register.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if ("user_id" in session):
        return redirect("/")
    
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        
        hashed_password = db.getPasswordHash(username)
        if (hashed_password):
            return jsonify({"message": "Username already exists!", "category": "error"}), 400
        else:
            db.setPassword(username, password)
            return jsonify({"redirect" : "/login", "message": "Registration successful!", "category": "success"}), 400
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")
    
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        
        hashed_password = db.getPasswordHash(username)
        if not hashed_password:
            return jsonify({"message": "Username does not exist!", "category": "error"}), 400
        
        if (hashed_password != db.getHash(password)):
            return jsonify({"message": "Invalid password!", "category": "error"}), 400
        
        session["user_id"] = username
        return jsonify({"redirect" : "/", "message": "Logged in!", "category": "success"}), 400
    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)