from flask import Flask, render_template, request, redirect,session
from db import cursor,conn
import product


app = Flask(__name__, template_folder="HTML", static_folder=".", static_url_path="")
# requires to mantain session for individual user
app.secret_key = "first_glow"

# REGISTER PRODUCT ROUTES HERE
product.register_product_routes(app)


@app.route("/")
def home():
    return redirect("/products/face")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message="")

    uname = request.form["uname"]
    pwd   = request.form["pwd"]

    cursor.execute(
        "SELECT password,user_Id FROM User_Details WHERE user_Name=%s",
        (uname,)
    )
    res = cursor.fetchone()

    if res and res["password"] == pwd:
        session["customer_id"] = res["user_Id"]
        return redirect("/products/face")

    return render_template("login.html", message="Invalid login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")

    uname = request.form["uname"]
    phone = request.form["phone"]
    mail  = request.form["mail"]
    pwd   = request.form["pwd"]

    cursor.execute(
        "SELECT * FROM User_Details WHERE user_Name=%s",
        (uname,)
    )
    if cursor.fetchone():
        return render_template("register.html", message="Username already exists")

    cursor.execute(
        "INSERT INTO User_Details (user_Name, phoneNum, email, password) VALUES (%s,%s,%s,%s)",
        (uname, phone, mail, pwd)
    )
    conn.commit()
    return redirect("/login")



if __name__ == "__main__":
    app.run(debug=True)
