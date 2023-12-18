from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blogs.models import Blog, Category


class DashboardViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser", email="test@example.com")
        cls.category = Category.objects.create(category_name="Test Category")
        cls.blog = Blog.objects.create(
            title="Test Blog",
            slug="test-blog",
            category=cls.category,
            author=cls.user,
            short_description="Test description",
            blog_body="Test blog body content",
            status="Draft",
            is_featured=True,
        )

    def test_dashboard(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dashboard.html")
