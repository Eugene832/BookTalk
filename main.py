from flask import *
import database as db
import hashlib

app = Flask("Website")
app.secret_key = db.sekretKey

@app.route("/sorian")
def sorian():
    return render_template("sorian.html")

@app.route("/girl.png")
def girl():
    return send_file("files/girl.png", mimetype="image/png")

@app.route("/background.png")
def background():
    return send_file("files/background.png", mimetype="image/png")

@app.route("/favicon.ico")
def favicon():
    return send_file("files/favicon.png", mimetype="image/png")

@app.route("/books", methods=["GET"])
def books():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))
    books = db.getBooksBatch(offset, limit)
    return jsonify(books)

@app.route("/")
def home():
    #if "username" in session:
    #    return render_template("mainpage.html")
    return render_template("mainpage.html")

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

@app.route("/add_book", methods=["POST"])
def add_book():
    if "username" not in session: return None, 400
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"message": "Title and content are required."}), 200

    db.addBook(session["username"], title, content)

    return jsonify({"redirect": "/"}), 200

@app.route("/publication")
def publication():
    if "username" not in session:
        return redirect("/")
    return render_template("publication.html")

@app.route("/review")
def review():
    if "username" not in session:
        return redirect("/")
    return render_template("review.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
