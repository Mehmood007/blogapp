from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Blog, Category, Comment


class BlogModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data
        cls.user = User.objects.create(username="testuser")
        cls.category = Category.objects.create(category_name="Test Category")
        cls.blog = Blog.objects.create(
            title="Test Blog",
            slug="test-blog",
            category=cls.category,
            author=cls.user,
            featured_image="test_image.jpg",
            short_description="Short description for testing",
            blog_body="Body of the test blog",
            status="Draft",
            is_featured=True,
        )
        cls.comment = Comment.objects.create(
            author=cls.user, blog=cls.blog, comment="Test comment"
        )

    def test_category_creation(self):
        category = Category.objects.get(category_name="Test Category")
        self.assertEqual(category.category_name, "Test Category")

    def test_blog_creation(self):
        blog = Blog.objects.get(title="Test Blog")
        self.assertEqual(blog.title, "Test Blog")

    def test_comment_creation(self):
        comment = Comment.objects.get(comment="Test comment")
        self.assertEqual(comment.comment, "Test comment")

    def test_blog_deletion(self):
        blog = Blog.objects.get(slug="test-blog")
        blog_image = blog.featured_image
        blog.delete()

        with self.assertRaises(Blog.DoesNotExist):
            Blog.objects.get(slug="test-blog")

        self.assertFalse(blog_image.storage.exists(blog_image.name))


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.category = Category.objects.create(category_name="Test Category")
        cls.blog = Blog.objects.create(
            title="Test Blog",
            slug="test-blog",
            category=cls.category,
            author=cls.user,
            short_description="Short description for the test blog",
            blog_body="Body content for the test blog",
            status="Published",
            is_featured=True,
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            blog=cls.blog,
            comment="This is a test comment for the test blog",
        )

    def test_posts_by_category_view(self):
        client = Client()
        response = client.get(
            reverse("posts_by_category", kwargs={"category_id": self.category.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts_by_category.html")

    def test_blog_view_post_comment(self):
        client = Client()
        login = client.login(username="testuser", password="12345")
        self.assertTrue(login)
        response = client.post(
            reverse("blog", kwargs={"slug": self.blog.slug}),
            {"comment": "Test Comment"},
        )
        self.assertEqual(response.status_code, 302)

    def test_search_view(self):
        client = Client()
        response = client.get(reverse("search"), {"keyword": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
