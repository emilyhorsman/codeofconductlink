from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

class VerifiedEmailRequiredMixin(object):
    permission_fail_redirect = '/'
    permission_fail_message = 'You are not authorized to view the requested page.'

    # Taken from verified_email_required
    # https://github.com/pennersr/django-allauth/blob/master/allauth/account/decorators.py
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            messages.error(request, 'You must be logged in with a verified email to view the requested page.')
            return redirect(reverse('account_login'))

        if not EmailAddress.objects.filter(user=request.user, verified=True).exists():
            send_email_confirmation(request, request.user)
            messages.error(request, 'You must have a verified email address to view the requested page.')
            return render(request, 'account/verified_email_required.html')

        # The class can define a custom permission test function on top of
        # everything else.
        if getattr(self, 'permission_test', False):
            if not self.permission_test(request, *args, **kwargs):
                messages.error(request, self.permission_fail_message)
                return redirect(self.permission_fail_redirect)

        return super(VerifiedEmailRequiredMixin, self).dispatch(request, *args, **kwargs)
