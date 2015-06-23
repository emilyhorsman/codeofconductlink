from allauth.account.decorators import verified_email_required

class VerifiedEmailRequiredMixin(object):
    @classmethod
    def as_view(self, **init_kwargs):
        view = super(VerifiedEmailRequiredMixin, self).as_view(**init_kwargs)
        return verified_email_required(view)
