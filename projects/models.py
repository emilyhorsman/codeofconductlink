from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class SubmissionProfile(models.Model):
    public_name = models.CharField(max_length=256, unique=True, blank=True, null=True)
    user        = models.OneToOneField(User)

    def __str__(self):
        if self.public_name:
            return self.public_name
        return "Anonymous"

class Project(models.Model):
    # A project should be created with an initial ProjectSubmission.
    user         = models.ForeignKey(User)
    created_date = models.DateTimeField(default=timezone.now)

    @property
    def verified_submissions(self):
        return self.submissions.exclude(verified_date__isnull=True).order_by('-verified_date')

    @property
    def name(self):
        return self.verified_submissions.exclude(name__isnull=True).first()

    @property
    def homepage(self):
        return self.verified_submissions.exclude(homepage__isnull=True).first()

    @property
    def tags(self):
        return self.verified_submissions.exclude(tags__isnull=True).first()

    def __str__(self):
        name_submission = self.name
        if name_submission:
            return name_submission.name
        return 'No name given.'

class ProjectSubmission(models.Model):
    user          = models.ForeignKey(User, related_name='project_submissions')
    project       = models.ForeignKey(Project, related_name='submissions')
    created_date  = models.DateTimeField(default=timezone.now)
    verified_date = models.DateTimeField(blank=True, null=True)
    verified_by   = models.ForeignKey(User, blank=True, null=True, related_name='project_verifications')
    name          = models.CharField(max_length=256, null=True, blank=True)
    homepage      = models.CharField(max_length=256, null=True, blank=True)
    tags          = models.CharField(max_length=256, null=True, blank=True)

    def verify(self, verifying_user):
        self.verified_date = timezone.now()
        self.verified_by   = verifying_user
        self.save()

    def __str__(self):
        return 'Name: {} Homepage: {} Tags: {}'.format(self.name, self.homepage, self.tags)

class LinkSubmission(models.Model):
    TAGS = (
        ('COC', 'Code of Conduct'),
        ('DIV', 'Diversity Statement'),
        ('PRC', 'Problematic Conduct'),
    )
    user            = models.ForeignKey(User, related_name='link_submissions')
    project         = models.ForeignKey(Project, related_name='link_submissions')
    tag             = models.CharField(max_length=3, choices=TAGS)
    created_date    = models.DateTimeField(default=timezone.now)
    verified_date   = models.DateTimeField(blank=True, null=True)
    verified_by     = models.ForeignKey(User, blank=True, null=True, related_name='link_verifications')
    url             = models.CharField(max_length=256, blank=True, null=True)
    # A LinkSubmission could be made with no URL and project_has_tag set to
    # False. e.g. Project does not have a Code of Conduct, verified on...by...
    project_has_tag = models.BooleanField(default=False)

class RepresentationSubmission(models.Model):
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
    user            = models.ForeignKey(User, related_name='representation_submissions')
    created_date    = models.DateTimeField(default=timezone.now)
    verified_date   = models.DateTimeField(blank=True, null=True)
    verified_by     = models.ForeignKey(User, blank=True, null=True, related_name='representation_verifications')
