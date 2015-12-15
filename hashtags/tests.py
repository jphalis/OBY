from django.db import models
from django.test import TestCase

from .models import HashtagMixin


class TestModel(HashtagMixin):
    """
    This model is purely for unit testing
    """
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    hashtag_text_field = 'description'


class HashtagMixinUnitTest(TestCase):
    def test_hashtags_parsed(self):
        c = TestModel(title='foo', description='some #cool #text')
        tags = c._get_hashtags()
        expected_tags = ['cool', 'text']
        self.assertEqual(tags, expected_tags, 'tags did not equal '
            'expected_tags. Instead was: {}'.format(tags))

    def test_hashtags_persisted(self):
        c = TestModel.objects.create(title='foo',
                                     description='some #cool #text')
        self.assertIsNot(c.hashtags.all(), None, 'hashtags were not saved '
            'to the database.')
