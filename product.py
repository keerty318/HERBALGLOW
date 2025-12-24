from flask import render_template
from db import cursor

def register_product_routes(app):

    @app.route("/products/face")
    def face_products():
        cursor.execute("SELECT * FROM products WHERE prod_cat='face'")
        prod_list = cursor.fetchall()
        return render_template("products.html", prod=prod_list)
    
    @app.route("/products/hair")
    def hair_products():
        cursor.execute("SELECT * FROM products WHERE prod_cat='hair'")
        prod_list =cursor.fetchall()
        return render_template("hair.html", prod=prod_list)
    
    @app.route("/products/body")
    def body_products():
        cursor.execute("SELECT * FROM products WHERE prod_cat='body'")
        prod_list =cursor.fetchall()
        return render_template("bodycare.html", prod=prod_list)
