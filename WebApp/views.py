from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class QuestionListView(generic.ListView):
    model = models.Question
    form_class = forms.QuestionForm


class QuestionCreateView(generic.CreateView):
    model = models.Question
    form_class = forms.QuestionForm


class QuestionDetailView(generic.DetailView):
    model = models.Question
    form_class = forms.QuestionForm


class QuestionUpdateView(generic.UpdateView):
    model = models.Question
    form_class = forms.QuestionForm
    pk_url_kwarg = "pk"


class QuestionDeleteView(generic.DeleteView):
    model = models.Question
    success_url = reverse_lazy("Question_list")


class SubmissionsListView(generic.ListView):
    model = models.Submissions
    form_class = forms.SubmissionsForm


class SubmissionsCreateView(generic.CreateView):
    model = models.Submissions
    form_class = forms.SubmissionsForm


class SubmissionsDetailView(generic.DetailView):
    model = models.Submissions
    form_class = forms.SubmissionsForm


class SubmissionsUpdateView(generic.UpdateView):
    model = models.Submissions
    form_class = forms.SubmissionsForm
    pk_url_kwarg = "pk"


class SubmissionsDeleteView(generic.DeleteView):
    model = models.Submissions
    success_url = reverse_lazy("Submissions_list")


class ProjectListView(generic.ListView):
    model = models.Project
    form_class = forms.ProjectForm


class ProjectCreateView(generic.CreateView):
    model = models.Project
    form_class = forms.ProjectForm


class ProjectDetailView(generic.DetailView):
    model = models.Project
    form_class = forms.ProjectForm


class ProjectUpdateView(generic.UpdateView):
    model = models.Project
    form_class = forms.ProjectForm
    pk_url_kwarg = "pk"


class ProjectDeleteView(generic.DeleteView):
    model = models.Project
    success_url = reverse_lazy("Project_list")
