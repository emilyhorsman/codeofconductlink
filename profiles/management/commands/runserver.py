from django.contrib.staticfiles.management.commands import runserver
import os

"""
Add an option to the staticfiles runserver command to disable reCAPTCHA.
"""

class Command(runserver.Command):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--norecaptcha', action='store_false', dest='use_recaptcha', default=True,
                            help='Tells Django to validate all reCAPTCHA fields.')

    def execute(self, *args, **options):
        if options.get('use_recaptcha'):
            os.environ['USE_RECAPTCHA'] = "True"
        super(Command, self).execute(*args, **options)
