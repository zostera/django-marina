from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from marina.db.models import ProtectedModelMixin
from marina.test.clients import ClientWithFetch
from marina.test.test_cases import BaseViewsTestCase


class ProtectedModel(ProtectedModelMixin, models.Model):
    name = models.CharField(max_length=10)


class ProtectedModelMixinTestCase(TestCase):

    def test_assertNotFound(self):
        self.assertNotFound(url=self.url_not_found, user=None)
        self.assertNotFound(url=self.url_not_found, user=self.user)
        self.assertNotFound(url=self.url_not_found, user=self.superuser)
