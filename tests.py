from unittest import TestCase
import flask
import server
import os
import app
import seed_data
import crud
import re
import io


class FlaskTests(TestCase):
    # Test Routes
    def test_home_page(self):
        response = self.client.get("/")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Learn how to create different makeup looks", content)
        self.assertIn("1_p.jpg", content)

    def test_user_profile(self):
        response = self.client.get("/user/1")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Amanda Cerney", content)

    def test_all_posts_page(self):
        response = self.client.get("/posts")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Makeup Looks", content)
        self.assertIn("1_p.jpg", content)

    def test_posts_page(self):
        response = self.client.get("/posts/1")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("NATIVE", content)
        self.assertIn("1_0.jpg", content)
        self.assertIn("1_1.jpg", content)
        self.assertIn("1_2.jpg", content)

    def test_login_page(self):
        response = self.client.get("/login")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Email address", content)

    def test_signup_page(self):
        response = self.client.get("/signup")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sign Up", content)

    def test_search_notfound_page(self):
        response = self.client.get("/search?search_text=wedding")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Results for "wedding"', content)
        self.assertNotIn("1_p.jpg", content)

    def test_search_found_page(self):
        response = self.client.get("/search?search_text=dramatic")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Results for "dramatic"', content)
        self.assertIn("1_p.jpg", content)

    def test_product_search_notfound(self):
        response = self.client.get("/products/search.json?q=abc")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual("[]\n", content)

    def test_product_search_found(self):
        response = self.client.get("/products/search.json?q=Face")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("1.webp", content)

    def test_favorites_page(self):
        response = self.client.get("/user/1/favorites")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Favorites", content)
        self.assertNotIn("1_p.jpg", content)

    def test_user_personal_profile_page(self):
        with server.flask_app.test_client() as c:
            with c.session_transaction() as session:
                session["user_id"] = "1"

            response = c.get("/profile")
            content = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Your Profile", content)
            self.assertIn("Amanda Cerney", content)

    def test_user_personal_edit_page(self):
        with server.flask_app.test_client() as c:
            with c.session_transaction() as session:
                session["user_id"] = "1"

            response = c.get("/profile/edit")
            content = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("First name:", content)
            self.assertIn("Last name:", content)

    def test_favorites_with_images_page(self):
        with server.flask_app.test_client() as c:
            with c.session_transaction() as session:
                session["user_id"] = "1"

            # Add to favorites
            response = c.get("/favorites/user/add/1")

            # Check image is in favorites
            response = c.get("/user/1/favorites")
            content = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Favorites", content)
            self.assertIn("1_p.jpg", content)

            # Remove from favorites
            response = c.get("/favorites/user/remove/1")

            # Check image is not in favorites
            response = c.get("/user/1/favorites")
            content = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Favorites", content)
            self.assertNotIn("1_p.jpg", content)

    def test_comment(self):
        with server.flask_app.test_client() as c:
            with c.session_transaction() as session:
                session["user_id"] = "1"

            # Write a comment
            response = c.post("/posts/1/comment", data={"comment": "test comment"})
            self.assertEqual(response.status_code, 302)

            # Load page to see comment added
            response = c.get("/posts/1")
            content = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("test comment", content)

            m = re.search('comment_id="([0-9]+)', content)
            comment_id = m.group(1)

            # Delete a comment
            response = c.post(f"/posts/1/comments/{comment_id}/delete")
            self.assertEqual(response.status_code, 302)

            # Load page to see comment removed
            response = c.get("/posts/1")
            content = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn("test comment", content)

    def test_create_post(self):
        with server.flask_app.test_client() as c:
            with c.session_transaction() as session:
                session["user_id"] = "1"

            img = None
            with open("data/sampledata/posts/1_0.jpg", "rb") as f:
                img = io.BytesIO(f.read())

            # Create a new post
            response = c.post(
                "/newlook",
                data={
                    "description": "test description",
                    "title": "test_title",
                    "makeup_type": "runway",
                    "images": (img, "test.jpg"),
                },
                content_type="multipart/form-data",
            )
            self.assertEqual(response.status_code, 302)

    # Test Setup
    def setUp(self):

        # Get test Flask test client
        self.client = server.flask_app.test_client()

        # Connect to test db
        app.connect_to_db(server.flask_app, "postgresql:///testdb")

    def tearDown(self):
        app.db.session.close()

    @classmethod
    def tearDownClass(cls):
        super(FlaskTests, cls).tearDownClass()
        app.db.drop_all()

    @classmethod
    def setUpClass(cls):
        super(FlaskTests, cls).setUpClass()

        app.connect_to_db(server.flask_app, "postgresql:///testdb")

        server.flask_app.config["WTF_CSRF_ENABLED"] = False

        # Create tables
        app.db.create_all()

        # Add sample data
        seed_data.create(
            email="amanda@outlook.com",
            password="123456",
            first_name="Amanda",
            last_name="Cerney",
            insta_handle="@madihagoheerofficial",
            bio="Some test bio",
            posts=[
                {
                    "title": "NATIVE",
                    "description": "test description",
                    "makeup_type": "dramatic",
                    "images": ["1_0.jpg", "1_1.jpg", "1_2.jpg"],
                    "products": [],
                }
            ],
            profile_picture="1.jpg",
        )

        seed_data.create_product(
            "Face Brushes",
            "PRO Concealer Brush #57",
            "https://www.sephora.com/product/pro-airbrush-concealer-brush-57-P313020",
            "1.webp",
        )


if __name__ == "__main__":
    import unittest

    os.system("dropdb testdb")
    os.system("createdb testdb")

    unittest.main(verbosity=2)
