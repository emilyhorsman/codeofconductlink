from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db import models
from .managers import ProfileManager

class Profile(AbstractBaseUser, PermissionsMixin):
    public_name = models.CharField(max_length=80, blank=True, null=True)
    profile_slug = models.SlugField(unique=True, default=None, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_moderator(self):
        return self.is_staff

    @property
    def name(self):
        if bool(self.public_name):
            return self.public_name
        return 'Anonymous'

    def get_full_name(self):
        return '{} ({})'.format(self.public_name, self.email).strip()

    def get_short_name(self):
        return self.email

    def get_absolute_url(self):
        return reverse('profiles:detail')

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.email

    def natural_key(self):
        return (self.email,)
