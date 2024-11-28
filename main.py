from flask import *
import database as db
import hashlib

app = Flask("Website")
app.secret_key = db.sekretKey

@app.route("/favicon.ico")
def get_image():
    return send_file("files/favicon.png", mimetype="image/png")

@app.route("/")
def home():
    if "username" in session:
        return render_template("mainpage.html")
    return render_template("login_or_register.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if ("username" in session):
        return redirect("/")
    
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        
        hashed_password = db.getPasswordHash(username)
        if (hashed_password):
            return jsonify({"message": "Username already exists!", "category": "error"}), 200
        else:
            db.setPassword(username, password)
            session["username"] = username
            return jsonify({"redirect" : "/", "message": "Registration successful!", "category": "success"}), 200
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/")
    
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        
        hashed_password = db.getPasswordHash(username)
        if not hashed_password:
            return jsonify({"message": "Username does not exist!", "category": "error"}), 200
        
        if (hashed_password != db.getHash(password)):
            return jsonify({"message": "Invalid password!", "category": "error"}), 200
        
        session["username"] = username
        return jsonify({"redirect" : "/", "message": "Logged in!", "category": "success"}), 200
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route("/publication")
def publication():
    if "username" not in session:
        return redirect("/")
    return render_template("publication.html")

@app.route("/books", methods=["GET"])
def books():
    if "username" not in session: return redirect("/")
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))
    books = db.getBooksBatch(offset, limit)
    return jsonify(books)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    