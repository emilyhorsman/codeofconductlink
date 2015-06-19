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
    user          = models.ForeignKey(User, related_name='submitted_by')
    project       = models.ForeignKey(Project, related_name='submissions')
    created_date  = models.DateTimeField(default=timezone.now)
    verified_date = models.DateTimeField(blank=True, null=True)
    verified_by   = models.ForeignKey(User, blank=True, null=True, related_name='verified_by')
    name          = models.CharField(max_length=256, null=True, blank=True)
    homepage      = models.CharField(max_length=256, null=True, blank=True)
    tags          = models.CharField(max_length=256, null=True, blank=True)

    def is_verified(self):
        return bool(self.verified_date)

    def verify(self, verifying_user):
        self.verified_date = timezone.now()
        self.verified_by   = verifying_user
        self.save()

    def __str__(self):
        return 'Name: {} Homepage: {} Tags: {}'.format(self.name, self.homepage, self.tags)
