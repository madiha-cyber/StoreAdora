from unittest import TestCase
import server
import os
import app
import seed_data
import re
import io
import crud


class FlaskTests(TestCase):
    # Test Routes
    def test_home_page(self):
        # Load the page
        response = self.client.get("/")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Learn how to create different makeup looks", content)
        self.assertIn("1_p.jpg", content)

    def test_user_profile(self):
        # Load the page
        response = self.client.get("/user/1")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Amanda Cerney", content)

    def test_all_posts_page(self):
        # Load the page
        response = self.client.get("/posts")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Makeup Looks", content)
        self.assertIn("1_p.jpg", content)

    def test_posts_page(self):
        # Load the page
        response = self.client.get("/posts/1")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("NATIVE", content)
        self.assertIn("1_0.jpg", content)
        self.assertIn("1_1.jpg", content)
        self.assertIn("1_2.jpg", content)

    def test_login_page(self):
        # Load the page
        response = self.client.get("/login")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Email address", content)

    def test_signup_page(self):
        # Load the page
        response = self.client.get("/signup")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sign Up", content)

    def test_search_notfound_page(self):
        # Load the page
        response = self.client.get("/search?search_text=wedding")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn('Results for "wedding"', content)
        self.assertNotIn("1_p.jpg", content)

    def test_search_found_page(self):
        # Load the page
        response = self.client.get("/search?search_text=dramatic")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn('Results for "dramatic"', content)
        self.assertIn("1_p.jpg", content)

    def test_product_search_notfound(self):
        # Load the page
        response = self.client.get("/products/search.json?q=abc")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertEqual("[]\n", content)

    def test_product_search_found(self):
        # Load the page
        response = self.client.get("/products/search.json?q=Face")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("1.webp", content)

    def test_favorites_page(self):
        # Load the page
        response = self.client.get("/user/1/favorites")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Favorites", content)
        self.assertNotIn("1_p.jpg", content)

    def test_user_personal_profile_page(self):
        # Store user_id in session for logged in user testing
        with self.client.session_transaction() as session:
            session["user_id"] = "1"

        # Load the page
        response = self.client.get("/profile")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Your Profile", content)
        self.assertIn("Amanda Cerney", content)

    def test_user_personal_edit_page(self):
        # Store user_id in session for logged in user testing
        with self.client.session_transaction() as session:
            session["user_id"] = "1"

        # Load the page
        response = self.client.get("/profile/edit")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("First name:", content)
        self.assertIn("Last name:", content)

    def test_favorites_with_images_page(self):
        # Store user_id in session for logged in user testing
        with self.client.session_transaction() as session:
            session["user_id"] = "1"

        # Load the page to Add to favorites
        response = self.client.get("/favorites/user/add/1")

        # Load the page. Check image is in favorites
        response = self.client.get("/user/1/favorites")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Favorites", content)
        self.assertIn("1_p.jpg", content)

        # Remove from favorites
        response = self.client.get("/favorites/user/remove/1")

        # Check image is not in favorites
        response = self.client.get("/user/1/favorites")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Favorites", content)
        self.assertNotIn("1_p.jpg", content)

    def test_comment(self):
        # Store user_id in session for logged in user testing
        with self.client.session_transaction() as session:
            session["user_id"] = "1"

        # Post to a page to Write a comment
        response = self.client.post("/posts/1/comment", data={"comment": "test comment"})
        self.assertEqual(response.status_code, 302)

        # Load page to see comment added
        response = self.client.get("/posts/1")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("test comment", content)

        m = re.search('comment_id="([0-9]+)', content)
        comment_id = m.group(1)

        # Post to a page to Delete a comment
        response = self.client.post(f"/posts/1/comments/{comment_id}/delete")
        self.assertEqual(response.status_code, 302)

        # Load page to see comment removed
        response = self.client.get("/posts/1")
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("test comment", content)

    def test_create_post(self):
        # Store user_id in session for logged in user testing
        with self.client.session_transaction() as session:
            session["user_id"] = "1"

        with open("data/sampledata/posts/1_0.jpg", "rb") as sample_image_file:
            img = io.BytesIO(sample_image_file.read())

        # Post to a page to Create a new post
        response = self.client.post(
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
        # Get the new post URL from the response
        m = re.search("(/posts/[0-9]+)", response.get_data(as_text=True))
        new_post_url = m.group(1)

        # Load page to see new post created
        response = self.client.get(new_post_url)
        content = response.get_data(as_text=True)

        # Validate result
        self.assertEqual(response.status_code, 200)
        self.assertIn("2_0.jpg", content)
        self.assertIn("test_title", content)


    # setUp is called before calling every test method in this class
    def setUp(self):

        # Get test Flask test client
        self.client = server.flask_app.test_client()

        # Connect to test db
        app.connect_to_db(server.flask_app, "postgresql:///testdb")

    # tearDown is called after calling every test method in this class
    def tearDown(self):
        app.db.session.close()

    # setUpClass is called once before any tests is run in this class
    @classmethod
    def setUpClass(cls):
        super(FlaskTests, cls).setUpClass()

        server.flask_app.config["WTF_CSRF_ENABLED"] = False

        app.connect_to_db(server.flask_app, "postgresql:///testdb")

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

        crud.create_product(
            "Face Brushes",
            "PRO Concealer Brush #57",
            "https://www.sephora.com/product/pro-airbrush-concealer-brush-57-P313020",
            "1.webp",
        )

    # tearDownClass is called after all tests have been run in this class.
    @classmethod
    def tearDownClass(cls):
        super(FlaskTests, cls).tearDownClass()
        app.db.drop_all()

if __name__ == "__main__":
    import unittest

    os.system("dropdb testdb")
    os.system("createdb testdb")

    unittest.main(verbosity=2)
