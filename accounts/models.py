import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.managers import UserManager


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128)
    first_name = models.CharField(_('first name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_superuser = models.BooleanField(_('is superuser'), default=False)
    last_request = models.DateTimeField(_('last request'), blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
