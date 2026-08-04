from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = db.cursor()
        db.close()

        query = """
        SELECT * FROM users
        WHERE username = %s AND password = %s
        """

        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        cursor.close()

        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))

        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor()

    # Total number of products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    # Total stock quantity
    cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM products")
    total_stock = cursor.fetchone()[0]

    # Products with stock less than or equal to 5
    cursor.execute(
        "SELECT COUNT(*) FROM products WHERE quantity <= 5"
    )
    low_stock = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_stock=total_stock,
        low_stock=low_stock
    )

@app.route("/products")
def products():

    if "username" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    cursor = db.cursor()

    if search:
        query = """
        SELECT * FROM products
        WHERE name LIKE %s
        OR category LIKE %s
        OR supplier LIKE %s
        ORDER BY id DESC
        """

        search_value = "%" + search + "%"

        cursor.execute(
            query,
            (search_value, search_value, search_value)
        )

    else:
        cursor.execute(
            "SELECT * FROM products ORDER BY id DESC"
        )

    products = cursor.fetchall()

    cursor.close()

    return render_template(
        "products.html",
        products=products,
        search=search
    )

@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if "username" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor()

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        supplier = request.form["supplier"]

        query = """
        UPDATE products
        SET name = %s,
            category = %s,
            price = %s,
            quantity = %s,
            supplier = %s
        WHERE id = %s
        """

        cursor.execute(
            query,
            (name, category, price, quantity, supplier, id)
        )

        db.commit()

        cursor.close()

        return redirect(url_for("products"))

    cursor.execute(
        "SELECT * FROM products WHERE id = %s",
        (id,)
    )

    product = cursor.fetchone()

    cursor.close()

    if product is None:
        return "Product not found", 404

    return render_template(
        "edit_product.html",
        product=product
    )

@app.route("/delete_product/<int:id>")
def delete_product(id):

    if "username" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()

    return redirect(url_for("products"))

@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        supplier = request.form["supplier"]

        cursor = db.cursor()

        query = """
        INSERT INTO products
        (name, category, price, quantity, supplier)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (name, category, price, quantity, supplier)
        )

        db.commit()

        cursor.close()

        return redirect(url_for("products"))

    return render_template("add_product.html")
@app.route("/sales", methods=["GET", "POST"])
def sales():

    if "username" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor()

    if request.method == "POST":

        product_id = request.form["product_id"]
        quantity_sold = int(request.form["quantity"])

        # Get product details
        cursor.execute(
            "SELECT name, price, quantity FROM products WHERE id = %s",
            (product_id,)
        )

        product = cursor.fetchone()

        if product is None:
            cursor.close()

            return render_template(
                "sales.html",
                products=[],
                sales=[],
                error="Product not found"
            )

        product_name = product[0]
        price = float(product[1])
        available_quantity = product[2]

        # Check stock
        if quantity_sold > available_quantity:

            cursor.execute("""
                SELECT id, name, category, price, quantity, supplier
                FROM products
                ORDER BY id DESC
            """)

            products = cursor.fetchall()

            cursor.execute("""
                SELECT
                    sales.id,
                    products.name,
                    sales.quantity_sold,
                    sales.total_amount,
                    sales.sale_date
                FROM sales
                JOIN products
                ON sales.product_id = products.id
                ORDER BY sales.id DESC
            """)

            sales_data = cursor.fetchall()

            cursor.close()

            return render_template(
                "sales.html",
                products=products,
                sales=sales_data,
                error=f"Only {available_quantity} units of {product_name} are available."
            )

        # Calculate total
        total_amount = price * quantity_sold

        # Record sale
        cursor.execute("""
            INSERT INTO sales
            (product_id, quantity_sold, total_amount)
            VALUES (%s, %s, %s)
        """, (
            product_id,
            quantity_sold,
            total_amount
        ))

        # Update stock
        cursor.execute("""
            UPDATE products
            SET quantity = quantity - %s
            WHERE id = %s
        """, (
            quantity_sold,
            product_id
        ))

        db.commit()

    # Get products
    cursor.execute("""
        SELECT id, name, category, price, quantity, supplier
        FROM products
        ORDER BY name
    """)

    products = cursor.fetchall()

    # Get recent sales
    cursor.execute("""
        SELECT
            sales.id,
            products.name,
            sales.quantity_sold,
            sales.total_amount,
            sales.sale_date
        FROM sales
        JOIN products
        ON sales.product_id = products.id
        ORDER BY sales.id DESC
    """)

    sales_data = cursor.fetchall()

    cursor.close()

    return render_template(
        "sales.html",
        products=products,
        sales=sales_data,
        message="Sale recorded successfully"
        if request.method == "POST"
        else None,
        error=None
    )
@app.route("/low_stock")
def low_stock():

    if "username" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, category, price, quantity, supplier
        FROM products
        WHERE quantity <= 5
        ORDER BY quantity ASC
    """)

    products = cursor.fetchall()

    cursor.close()

    return render_template(
        "low_stock.html",
        products=products
    )
@app.route("/reports")
def reports():

    if "username" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor()

    # Total products
    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    total_products = cursor.fetchone()[0]


    # Total stock
    cursor.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM products"
    )

    total_stock = cursor.fetchone()[0]


    # Number of sales
    cursor.execute(
        "SELECT COUNT(*) FROM sales"
    )

    total_sales = cursor.fetchone()[0]


    # Total sales amount
    cursor.execute(
        "SELECT COALESCE(SUM(total_amount), 0) FROM sales"
    )

    total_sales_amount = cursor.fetchone()[0]


    # Inventory data
    cursor.execute("""
        SELECT
            id,
            name,
            category,
            price,
            quantity,
            supplier
        FROM products
        ORDER BY id DESC
    """)

    products = cursor.fetchall()


    # Sales data
    cursor.execute("""
        SELECT
            sales.id,
            products.name,
            sales.quantity_sold,
            sales.total_amount,
            sales.sale_date
        FROM sales
        JOIN products
        ON sales.product_id = products.id
        ORDER BY sales.id DESC
    """)

    sales_data = cursor.fetchall()


    cursor.close()


    return render_template(
        "reports.html",
        total_products=total_products,
        total_stock=total_stock,
        total_sales=total_sales,
        total_sales_amount=total_sales_amount,
        products=products,
        sales=sales_data
    )

@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
