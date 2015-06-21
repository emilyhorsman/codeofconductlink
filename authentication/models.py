from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core import validators
from django.utils import timezone

class ProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        email = self.normalize_email(email)
        user  = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class Profile(AbstractBaseUser, PermissionsMixin):
    profile_name = models.CharField(max_length=80, unique=True, default=None, blank=True, null=True, validators=[
            validators.RegexValidator(
                r'^\w+$', 'Profile names can only contain letters, numbers, and underscores.'
            ),
        ],
        error_messages={ 'unique': 'Sorry, that profile name is already taken!' },)
    email       = models.EmailField(unique=True)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = ProfileManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    @property
    def can_verify(self):
        return self.is_staff

    def get_public_name(self):
        if bool(self.profile_name):
            return self.profile_name
        return 'Anonymous'

    def get_full_name(self):
        return '{} ({})'.format(self.profile_name, self.email).strip()

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
