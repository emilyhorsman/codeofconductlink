from django.test import TestCase
from .test_helpers import ProfileFactory

class TestProfilePublicName(TestCase):
    def test_anonymous_name(self):
        p = ProfileFactory()
        self.assertEqual(p.name, 'Anonymous', 'Public name should be Anonymous if not set.')

    def test_displayed_public_name(self):
        p = ProfileFactory(public_name='foo')
        self.assertEqual(p.name, 'foo')
