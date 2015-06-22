from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils import timezone
from django.db import models

class Report(models.Model):
    class Meta:
        ordering = ['resolved', '-created_date']

    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='reports')
    message        = models.TextField(blank=True, null=True)
    created_date   = models.DateTimeField(default=timezone.now)
    resolved       = models.BooleanField(default=False)
