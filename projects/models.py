from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class SubmissionProfile(models.Model):
    public_name = models.CharField(max_length=256, unique=True, blank=True, null=True)
    user        = models.OneToOneField(User)
