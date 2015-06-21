from django.views.generic import UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.http import Http404
from allauth.account.decorators import verified_email_required
from projects.models import Project
from .models import Report
from .forms import UpdateReportForm

class CreateReport(CreateView):
    model = Report
    fields = ('message',)

    def get_context_data(self, **kwargs):
        context = super(CreateReport, self).get_context_data(**kwargs)
        context['title'] = 'Report on {}'.format(self.request.GET.get('target'))
        return context

    def form_valid(self, form):
        if 'project' in self.request.GET:
            try:
                project = Project.objects.get(pk=self.request.GET['project'])
            except Project.DoesNotExist:
                raise Http404
            form.instance.content_object = project
            self.success_url = project.get_absolute_url()
        form.instance.user = self.request.user
        return super(CreateReport, self).form_valid(form)

    @method_decorator(verified_email_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateReport, self).dispatch(*args, **kwargs)

class UpdateReport(UpdateView):
    model      = Report
    form_class = UpdateReportForm

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(UpdateReport, self).get_form_kwargs()
        kwargs.update({ 'request_user': self.request.user })
        return kwargs