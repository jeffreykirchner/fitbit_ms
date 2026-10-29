from django.test import TestCase
from django.urls import reverse


class TermsOfServicePageTests(TestCase):
    def test_terms_of_service_page_renders_policy_content(self):
        response = self.client.get(reverse("terms_of_service"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Terms of Service - ESI Exercise Study</title>", html=True)
        self.assertContains(response, "HUMAN SUBJECTS PROTECTION PROGRAM POLICY")
        self.assertContains(response, "Michael Briggs, Director of Research Integrity")
