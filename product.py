from flask import render_template,session,redirect, request
from db import cursor,conn
import razorpay
import os


# PAYMENTINTGRATION
client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)


def register_product_routes(app):

    @app.route("/products/face")
    def face_products():
        if "customer_id" not in session:
            return redirect("/login")

        cursor.execute("SELECT * FROM products WHERE prod_cat='face'")
        prod_list = cursor.fetchall()
        return render_template("products.html", prod=prod_list)
    
    @app.route("/products/hair")
    def hair_products():
        if "customer_id" not in session:
            return redirect("/login")

        cursor.execute("SELECT * FROM products WHERE prod_cat='hair'")
        prod_list =cursor.fetchall()
        return render_template("hair.html", prod=prod_list)
    
    @app.route("/products/body")
    def body_products():
        if "customer_id" not in session:
            return redirect("/login")

        cursor.execute("SELECT * FROM products WHERE prod_cat='body'")
        prod_list =cursor.fetchall()
        return render_template("bodycare.html", prod=prod_list)



# add to cart
    @app.route("/add-to-cart/<int:prd_id>")
    def add_to_cart(prd_id):
        if "customer_id" not in session:
            return redirect("/login")
        usr_id = session["customer_id"]
        sql = "SELECT * FROM cart WHERE user_Id = %s AND prod_id = %s"
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
    

    # increase  decrease qty of product in cart
        # Increase quantity
    @app.route("/increase_qty/<int:cart_id>")
    def increase_qty(cart_id):

        cursor.execute(
            "UPDATE cart SET cart_qty = cart_qty + 1 WHERE cart_id = %s",
            (cart_id,)
        )
        conn.commit()

        return redirect("/cart")


    # Decrease quantity
    @app.route("/decrease_qty/<int:cart_id>")
    def decrease_qty(cart_id):

        cursor.execute(
            "SELECT cart_qty FROM cart WHERE cart_id = %s",
            (cart_id,)
        )
        item = cursor.fetchone()

        if item["cart_qty"] > 1:

            cursor.execute(
                "UPDATE cart SET cart_qty = cart_qty - 1 WHERE cart_id = %s",
                (cart_id,)
            )

        else:

            cursor.execute(
                "DELETE FROM cart WHERE cart_id = %s",
                (cart_id,)
            )

        conn.commit()

        return redirect("/cart")


# view cart- ie cart html pg
    @app.route("/cart")
    def cart():
        if "customer_id" not in session:
            return redirect("/login")

        usr_id = session["customer_id"]
        sql_cart = "SELECT * FROM cart c JOIN products p ON p.prod_id = c.prod_id WHERE c.user_Id = %s"
        cursor.execute(sql_cart, (usr_id,))
        cart_items = cursor.fetchall()
        # to calculate the total amount
        sql_tots = "SELECT sum(p.prod_price*c.cart_qty) as total FROM cart c JOIN products p ON p.prod_id = c.prod_id WHERE c.user_Id = %s"
        cursor.execute(sql_tots, (usr_id,))
        cart_tot = cursor.fetchone()
        tot_amt = cart_tot["total"] or 0
        if tot_amt < 1:
            return redirect("/products/face")
        razorpay_order = client.order.create({"amount": int(tot_amt * 100), "currency": "INR"})

        return render_template("cart.html", tot_amt=tot_amt, cart = cart_items, razorpay_key=os.getenv("RAZORPAY_KEY_ID"), razorpay_order_id=razorpay_order["id"])
        



# place  order(no-chk out)
    @app.route("/place_order")
    def place_order():
        if "customer_id" not in session:
            return redirect("/login")
        usr_id = session["customer_id"]
        payment_id = request.args.get("payment_id")
        # to calculate the total amount
        sql_tots = "SELECT sum(p.prod_price*c.cart_qty) as total FROM cart c JOIN products p ON p.prod_id = c.prod_id WHERE c.user_Id = %s"
        cursor.execute(sql_tots, (usr_id,))
        cart_tot = cursor.fetchone()
        tot_amt = cart_tot["total"] or 0

        # creating order
        # sql_order = "INSERT INTO orders (user_Id,total_amount) VALUES (%s,%s) "
        # cursor.execute(sql_order, (usr_id,tot_amt))
        sql_order = """INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s)"""

        cursor.execute(sql_order, (usr_id, tot_amt, "PLACED"))
        order_id = cursor.lastrowid

        # paymentdb
        sql_payment = """INSERT INTO payments(order_id, razorpay_payment_id, amount, payment_status, user_id) VALUES (%s, %s, %s, %s, %s)"""

        cursor.execute(sql_payment, (order_id,payment_id,tot_amt,"SUCCESS",usr_id))
    
        sql_order_item = "INSERT INTO order_items (order_id,prod_id,cart_qty,prod_price) select %s,c.prod_id,c.cart_qty,p.prod_price from cart c join products  p on p.prod_id = c.prod_id  where c.user_Id=%s"
        cursor.execute(sql_order_item, (order_id,usr_id))


    # delete cart   
        sql_cart_del="delete from cart where user_Id = %s"
        cursor.execute(sql_cart_del, (usr_id,))
        conn.commit()
    
        return render_template("order_success.html",order_id = order_id,tot_amt=tot_amt)
    
    # history of orders
    @app.route("/my_orders")
    def my_orders():

        if "customer_id" not in session:
            return redirect("/login")

        usr_id = session["customer_id"]

        sql = """
        SELECT *
        FROM orders
        WHERE user_id = %s
        ORDER BY order_date DESC
        """

        cursor.execute(sql, (usr_id,))
        orders = cursor.fetchall()

        return render_template("my_orders.html", orders=orders)
    
    # view order details
    @app.route("/order_details/<int:order_id>")
    def order_details(order_id):

        if "customer_id" not in session:
            return redirect("/login")

        sql = """
        SELECT
            p.prod_name,
            oi.cart_qty,
            oi.prod_price
        FROM order_items oi
        JOIN products p
            ON oi.prod_id = p.prod_id
        WHERE oi.order_id = %s
        """

        cursor.execute(sql, (order_id,))
        products = cursor.fetchall()

        sql = """
        SELECT *
        FROM orders
        WHERE order_id = %s
        """

        cursor.execute(sql, (order_id,))
        order = cursor.fetchone()

        return render_template(
            "order_details.html",
            order=order,
            products=products
        )



    

