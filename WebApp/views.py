from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from . import forms
from . import models
from .models import Submissions
from .utils.audio import segmentaudio


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


def splitAudio(request, qid):
    instance = Submissions.objects.get(id=qid)
    if instance.sound_file:  # first time is sound is added
        lenSeg = segmentaudio(sID=instance.id, audiofile=instance.sound_file)
        print("new file and audio file changed")
        return HttpResponse(
            'Done! ' + str(
                lenSeg) + ' splits made. <script>setTimeout(function(){window.opener.location.reload(); window.close()}, 1000) </script>')

    return HttpResponse(
        'No sound File! <script>setTimeout(function(){window.opener.location.reload(); window.close()}, 1000) </script>')
