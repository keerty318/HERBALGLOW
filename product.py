from flask import render_template,session,redirect
from db import cursor,conn
# from app import app

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



# add to cart
    @app.route("/add-to-cart/<int:prd_id>")
    def add_to_cart(prd_id):
        usr_id = session["customer_id"]
        sql = "SELECT * FROM cart WHERE user_id = %s AND prod_id = %s"
        cursor.execute(sql, (usr_id,prd_id))

        item = cursor.fetchone()
    # if one product's qty is increased by cus 
        if item is None:
            sql_ins = "INSERT INTO cart (user_Id,prod_id,cart_qty) VALUES (%s, %s, 1)"
            cursor.execute(sql_ins, (usr_id,prd_id))
        else:
            sql_upd = "UPDATE cart SET cart_qty = cart_qty +1 WHERE cart_id = %s"
            cursor.execute(sql_upd, (item["cart_id"],))

        conn.commit()
        return redirect("/cart")


# view cart- ie cart html pg
    @app.route("/cart")
    def cart():
        usr_id = session["customer_id"]
        sql_cart = "SELECT * FROM cart c JOIN products p ON p.prod_id = c.prod_id WHERE c.user_id = %s"
        cursor.execute(sql_cart, (usr_id,))
        cart_items = cursor.fetchall()
        # to calculate the total amount
        sql_tots = "SELECT sum((p.prod_price*c.cart_qty)) as total FROM cart c JOIN products p ON p.prod_id = c.prod_id WHERE c.user_id = %s"
        cursor.execute(sql_tots, (usr_id,))
        cart_tot = cursor.fetchone()
        tot_amt = cart_tot["total"]

        return render_template("cart.html", tot_amt=tot_amt, cart = cart_items)



# place  order(no-chk out)
    @app.route("/place_order")
    def place_order():
        usr_id = session["customer_id"]
        # to calculate the total amount
        sql_tots = "SELECT sum((p.prod_price*c.cart_qty)) as total FROM cart c JOIN products p ON p.prod_id = c.prod_id WHERE c.user_id = %s"
        cursor.execute(sql_tots, (usr_id,))
        cart_tot = cursor.fetchone()
        tot_amt = cart_tot["total"]
        # creating order
        sql_order = "INSERT INTO orders (user_id,total_amount) VALUES (%s,%s) "
        cursor.execute(sql_order, (usr_id,tot_amt))
        order_id = cursor.lastrowid
    
        sql_order_item = "INSERT INTO order_items (order_id,prod_id,cart_qty,prod_price) select %s,c.prod_id,c.cart_qty,p.prod_price from cart c join products  p on p.prod_id = c.prod_id  where c.user_id=%s"
        cursor.execute(sql_order_item, (order_id,usr_id))


    # delete cart   
        sql_cart_del="delete from cart where user_id = %s"
        cursor.execute(sql_cart_del, (usr_id,))
        conn.commit()
    
        return render_template("order_success.html",order_id = order_id)




    

