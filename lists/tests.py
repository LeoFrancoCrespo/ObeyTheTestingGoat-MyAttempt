from django.test import TestCase

# Create your tests here.
class SmokeTest(TestCase):
    def test_badat_maths(self):
        self.assertEqual(1 + 1, 3)