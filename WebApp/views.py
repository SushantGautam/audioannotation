import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from . import forms
from . import models
from .models import Submissions


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


from .utils.audio import segmentaudio


def splitAudio(request, qid):
    instance = Submissions.objects.get(id=qid)
    if instance.sound_file:  # first time is sound is added
        instance.set_tts_status(1)
        segmentaudio.delay(sID=instance.id)
        print("new file and audio file changed")
        return HttpResponse(
            'Done! Submitted to speech API. <script>setTimeout(function(){window.opener.location.reload(); window.close()}, 1000) </script>')

    return HttpResponse(
        'No sound File! <script>setTimeout(function(){window.opener.location.reload(); window.close()}, 1000) </script>')


@csrf_exempt
# @login_required
# @api_view(["POST"])
def Record(request, qid):
    if request.method == 'POST':
        audio_file = request.FILES.get('recorded_audio')
        myObj = Submissions.objects.get(id=qid)  # Put aurguments to properly according to your model
        myObj.sound_file = audio_file
        myObj.save()
        return JsonResponse({
            'success': True,
        })

    return render(request, "record.html", {"qid": qid})


@login_required
@ensure_csrf_cookie
def Annotate(request, qid):
    myObj = Submissions.objects.get(id=qid)
    if request.method == 'POST':
        annotation = request.POST.get('annotations')
        myObj.extras['annotations'] = annotation
        myObj.save()
        return JsonResponse({
            'success': True,
        })

    if Submissions.objects.get(id=qid).sound_file:
        if myObj.extras.get('annotations'):
            annotations = json.loads(myObj.extras.get('annotations'))
        else:
            annotations = []
        if myObj.extras.get('stt_predictions_annotations'):
            predictions = myObj.extras.get('stt_predictions_annotations')
        else:
            predictions = []

        return render(request, "annotation-tool.html", {
            "user_pk": request.user.pk,
            "user_firstName": request.user.first_name,
            "user_lastName": request.user.last_name,
            "qid": myObj,
            "audioFile": myObj.sound_file.url,
            "annotations": [{"result": annotations}],
            "predictions": [{
                "model_version": "TTS Model",
                "result": predictions
            }, ]
        }, )
    else:
        return HttpResponse(
            "No Audio file..... . </script>")
