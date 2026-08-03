import unittest
from app import app


class InventoryAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "jenkins-test-secret"
        self.client = app.test_client()

    def login(self):
        return self.client.post(
            "/",
            data={
                "username": "jenkins_test",
                "password": "test123"
            },
            follow_redirects=False
        )

    def test_login_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        response = self.login()

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.headers["Location"])

    def test_invalid_login(self):
        response = self.client.post(
            "/",
            data={
                "username": "wrong_user",
                "password": "wrong_password"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password", response.data)

    def test_dashboard_after_login(self):
        self.login()

        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 200)

    def test_products_after_login(self):
        self.login()

        response = self.client.get("/products")

        self.assertEqual(response.status_code, 200)

    def test_low_stock_after_login(self):
        self.login()

        response = self.client.get("/low_stock")

        self.assertEqual(response.status_code, 200)

    def test_reports_after_login(self):
        self.login()

        response = self.client.get("/reports")

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.login()

        response = self.client.get(
            "/logout",
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 302)

    def test_products_requires_login(self):
        response = self.client.get("/products")

        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
