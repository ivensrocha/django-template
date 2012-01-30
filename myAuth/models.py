# coding: utf-8
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    confirmation_code_expiration_datetime = models.DateTimeField()

    def create_user_profile(sender, instance, created, **kwargs):
        period = 30  # expiration period in days
        from int.myAuth.utils.expiration_datetime import expiration_datetime
        if created:
            UserProfile.objects.create(user=instance,
                                       confirmation_code_expiration_datetime=expiration_datetime(period))

    post_save.connect(create_user_profile, sender=User)


class UserCustomModelBackend(ModelBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = models.get_model(*settings.AUTH_PROFILE_MODULE.split('.', 2))
            return self._user_class

        if not self._user_class:
            raise ImproperlyConfigured(u'Impossível enxergar o model customizado de User')
