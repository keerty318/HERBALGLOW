
from flask import Flask, render_template, request, redirect,session
from db import cursor,conn

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os


load_dotenv()
import product
app = Flask(__name__)
# requires to mantain session for individual user
app.secret_key = os.getenv("FLASK_SECRET_KEY")


# REGISTER PRODUCT ROUTES HERE
product.register_product_routes(app)

# ----------------------home-----------------------------------------------------------------------------------------
@app.route("/")
@app.route("/home")
def home():
    # return redirect("/products/face")
    return render_template("home.html")


# --------------------quiz--------------------------------------------------------------------------------
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

# ------------------------login-----------------------------------------------------------------------------------


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
    print("Database:", res["password"] if res else None)
    print("Entered :", pwd)

    if res:
        print("Match:", check_password_hash(res["password"], pwd))

    if res and check_password_hash(res["password"], pwd):
        session["customer_id"] = res["user_Id"]
        return redirect("/products/face")

    return render_template("login.html", message="Invalid login")

# -----------------------register---------------------------------------------------------------------------


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")

    uname = request.form["uname"]
    phone = request.form["phone"]
    mail  = request.form["mail"]
    pwd   = request.form["pwd"]
    address = request.form["address"]
    hashed_pwd = generate_password_hash(pwd)

    cursor.execute(
        "SELECT * FROM User_Details WHERE user_Name=%s",
        (uname,)
    )
    if cursor.fetchone():
        return render_template("register.html", message="Username already exists")

    cursor.execute(
        "INSERT INTO User_Details (user_Name, phoneNum, email, password,ADDRESS) VALUES (%s,%s,%s,%s,%s)",(uname, phone, mail, hashed_pwd,address)
    )
    conn.commit()
    return redirect("/login")


# ---------------connectwithus-----------------------

# connectwithus page connection db
@app.route("/connectwithus", methods=["GET", "POST"] )
def connectwithus():
    if request.method == "GET":
        return render_template("connectwithus.html", )
   
    con_name = request.form["con_name"]
    con_no = request.form["con_no"]
    con_email = request.form["con_email"]
    con_query = request.form["con_query"]
    con_feedback = request.form["con_feedback"]


    
    

    cursor.execute(
    "INSERT INTO contact_us (con_name,con_no ,con_email,con_query,con_feedback)VALUES (%s,%s,%s,%s,%s)",
        (con_name,con_no , con_email, con_query, con_feedback)
    )

    conn.commit()

    return render_template("connectwithus.html", message="Thank you for connecting with HerbalGlow 🌿Your message means a lot to us. We'll get in touch very soon!")

# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
