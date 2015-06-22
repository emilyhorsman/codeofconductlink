from django.views.generic import UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.http import Http404
from braces.views import FormValidMessageMixin
from projects.models import Project
from common.access_mixins import VerifiedEmailRequiredMixin
from .models import Report
from .forms import CreateReportForm, UpdateReportForm

class CreateReport(FormValidMessageMixin,
                   VerifiedEmailRequiredMixin,
                   CreateView):
    model = Report
    form_class = CreateReportForm
    form_valid_message = 'Report filed.'

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

class UpdateReport(VerifiedEmailRequiredMixin,
                   FormValidMessageMixin,
                   UpdateView):
    model      = Report
    form_class = UpdateReportForm
    form_valid_message = 'Report updated.'

    def permission_test(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return False
        return request.user.is_moderator or Report.objects.filter(pk=kwargs['pk'],
                                                                  user=request.user).exists()

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(UpdateReport, self).get_form_kwargs()
        kwargs.update({ 'request_user': self.request.user })
        return kwargs
