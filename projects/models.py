from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from reports.models import Report

class Vouch(models.Model):
    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='vouches')
    created_date   = models.DateTimeField(default=timezone.now)

class VerifiedModel(models.Model):
    class Meta:
        abstract = True

    verified_date = models.DateTimeField(blank=True, null=True)
    verified_by   = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                      related_name='%(class)s_verifications')

    def verify(self, verifying_user, save=True):
        self.verified_date = timezone.now()
        self.verified_by   = verifying_user
        if save:
            self.save()

class Project(VerifiedModel):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date    = models.DateTimeField(default=timezone.now)
    name            = models.CharField(max_length=256, unique=True)
    homepage        = models.URLField(blank=True, null=True)
    code_of_conduct = models.URLField(blank=True, null=True)
    tags            = TaggableManager(blank=True)
    reports         = GenericRelation(Report)
    vouches         = GenericRelation(Vouch)

    def get_report_url(self):
        return '{}?project={}&target={}'.format(reverse('reports:new'), self.pk, self.name)

    def get_absolute_url(self):
        return reverse('projects:detail', args=(self.pk, slugify(self.name),))

    def get_reports_for_user(self, request_user):
        if request_user.is_moderator:
            return self.reports

        return self.reports.filter(user=request_user)

    def __str__(self):
        return self.name

class Submission(VerifiedModel):
    # A submission is a piece of information about a project. Examples:
    # tags=('queer','contributor') is_contributor=True, url='http://emilyhorsman.com',
    #   public_message='Emily Horsman is a core contributor and identifies as queer.',
    #   private_message='You can contact her @emilymhorsman to verify.'
    # tags=('problematic conduct') url=https://github.com/opal/opal/issues/941#issuecomment-113219234,
    #   public_message='Ignoring transphobia.'
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submissions')
    project         = models.ForeignKey(Project, related_name='submissions')
    tag             = TaggableManager()
    is_contributor  = models.BooleanField(default=False)
    url             = models.URLField()
    public_message  = models.TextField(blank=True, null=True)
    private_message = models.TextField(blank=True, null=True)
    created_date    = models.DateTimeField(default=timezone.now)
    updated_date    = models.DateTimeField(default=timezone.now)
    reports         = GenericRelation(Report)
    vouches         = GenericRelation(Vouch)

    def __str__(self):
        return self.url
