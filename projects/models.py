from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

class Report(models.Model):
    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='reports')
    message        = models.TextField(blank=True, null=True)
    created_date   = models.DateTimeField(default=timezone.now)
    resolved       = models.BooleanField(default=False)

class VerifiedModel(models.Model):
    class Meta:
        abstract = True

    verified_date = models.DateTimeField(blank=True, null=True)
    verified_by   = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                      related_name='%(class)s_verifications'.replace('submission_', '_'))

    def verify(self, verifying_user, save=True):
        self.verified_date = timezone.now()
        self.verified_by   = verifying_user
        if save:
            self.save()

class Project(VerifiedModel):
    # A project should be created with an initial ProjectSubmission.
    user          = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date  = models.DateTimeField(default=timezone.now)
    name          = models.CharField(max_length=256, unique=True)
    homepage      = models.CharField(max_length=256, null=True, blank=True)
    tags          = models.CharField(max_length=256, null=True, blank=True)
    reports       = GenericRelation(Report)

    def get_absolute_url(self):
        return reverse('projects:detail', args=(self.pk, slugify(self.name),))

    def __str__(self):
        return self.name

class LinkSubmission(VerifiedModel):
    TAGS = (
        ('COC', 'Code of Conduct'),
        ('DIV', 'Diversity Statement'),
        ('PRC', 'Problematic Conduct'),
    )
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='link_submissions')
    project         = models.ForeignKey(Project, related_name='link_submissions')
    tag             = models.CharField(max_length=3, choices=TAGS)
    created_date    = models.DateTimeField(default=timezone.now)
    url             = models.CharField(max_length=256, blank=True, null=True)
    # A LinkSubmission could be made with no URL and project_has_tag set to
    # False. e.g. Project does not have a Code of Conduct, verified on...by...
    project_has_tag = models.BooleanField(default=False)
    reports         = GenericRelation(Report)

class RepresentationSubmission(VerifiedModel):
    # The purpose of this field is to describe contributors on the project. For
    # instance, if a project has openly queer contributors it could be tagged
    # queer. We can have icons for particular tags such as queer, trans, woman,
    # fem, PoC, etc
    tag             = models.CharField(max_length=256)
    # A public message will be displayed on the project page history. It can
    # display a link to the team member's work, etc.
    public_message  = models.TextField(blank=True, null=True)
    # A private message will be displayed only to moderators involved with
    # submission verification. This can be a form of proof or a way to contact
    # the representing member. Representation submissions that contain
    # identifying information will only be verified if the member can be
    # contacted.
    private_message = models.TextField(blank=True, null=True)
    project         = models.ForeignKey(Project, related_name='representation_submissions')
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='representation_submissions')
    created_date    = models.DateTimeField(default=timezone.now)
    reports         = GenericRelation(Report)
