import unittest
from app import app, db


class InventoryAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "jenkins-test-secret"
        self.client = app.test_client()

        # Login before each test
        self.client.post(
            "/",
            data={
                "username": "jenkins_test",
                "password": "test123"
            }
        )

    def test_login_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        client = app.test_client()

        response = client.post(
            "/",
            data={
                "username": "jenkins_test",
                "password": "test123"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.headers["Location"])

    def test_invalid_login(self):
        client = app.test_client()

        response = client.post(
            "/",
            data={
                "username": "wrong_user",
                "password": "wrong_password"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Invalid username or password",
            response.data
        )

    def test_dashboard(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)

    def test_products_page(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)

    def test_low_stock_page(self):
        response = self.client.get("/low_stock")
        self.assertEqual(response.status_code, 200)

    def test_reports_page(self):
        response = self.client.get("/reports")
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        response = self.client.post(
            "/add_product",
            data={
                "name": "CI Test Product",
                "category": "Testing",
                "price": "250",
                "quantity": "15",
                "supplier": "Jenkins"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)

        cursor = db.cursor()

        cursor.execute(
            "SELECT id FROM products WHERE name = %s",
            ("CI Test Product",)
        )

        product = cursor.fetchone()
        cursor.close()

        self.assertIsNotNone(product)

    def test_search_product(self):
        response = self.client.get(
            "/products?search=Jenkins"
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b"Jenkins",
            response.data
        )

    def test_edit_product(self):
        cursor = db.cursor()

        cursor.execute(
            "SELECT id FROM products WHERE name = %s LIMIT 1",
            ("Jenkins Test Product",)
        )

        product = cursor.fetchone()
        cursor.close()

        self.assertIsNotNone(product)

        product_id = product[0]

        response = self.client.post(
            f"/edit_product/{product_id}",
            data={
                "name": "Jenkins Test Product Updated",
                "category": "Testing",
                "price": "150",
                "quantity": "20",
                "supplier": "Jenkins"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_product(self):
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (name, category, price, quantity, supplier)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                "Delete Test Product",
                "Testing",
                50,
                5,
                "Jenkins"
            )
        )

        db.commit()

        product_id = cursor.lastrowid
        cursor.close()

        response = self.client.get(
            f"/delete_product/{product_id}",
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)

        cursor = db.cursor()

        cursor.execute(
            "SELECT id FROM products WHERE id = %s",
            (product_id,)
        )

        product = cursor.fetchone()
        cursor.close()

        self.assertIsNone(product)

    def test_logout(self):
        response = self.client.get(
            "/logout",
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)

    def test_record_sale(self):
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (name, category, price, quantity, supplier)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                "Sales Test Product",
                "Testing",
                100,
                10,
                "Jenkins"
            )
        )

        db.commit()

        product_id = cursor.lastrowid
        cursor.close()

        response = self.client.post(
            "/sales",
            data={
                "product_id": str(product_id),
                "quantity": "3"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 200)

        cursor = db.cursor()

        cursor.execute(
            "SELECT quantity FROM products WHERE id = %s",
            (product_id,)
        )

        product = cursor.fetchone()

        cursor.execute(
            """
            SELECT quantity_sold, total_amount
            FROM sales
            WHERE product_id = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (product_id,)
        )

        sale = cursor.fetchone()
        cursor.close()

        self.assertEqual(product[0], 7)
        self.assertEqual(sale[0], 3)
        self.assertEqual(float(sale[1]), 300.0)

    def test_prevent_overselling(self):
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (name, category, price, quantity, supplier)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                "Stock Test Product",
                "Testing",
                100,
                5,
                "Jenkins"
            )
        )

        db.commit()

        product_id = cursor.lastrowid
        cursor.close()

        response = self.client.post(
            "/sales",
            data={
                "product_id": str(product_id),
                "quantity": "10"
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b"Only 5 units",
            response.data
        )


if __name__ == "__main__":
    unittest.main()

