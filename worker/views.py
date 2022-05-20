import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from speaker.models import SpeakerSubmission
from worker.models import WorkerSubmission


def homepage(request):
    context = {
        'speaker_submission': SpeakerSubmission.objects.all()
    }
    return render(request, 'worker/homepage.html', context)


class AnnotationPage(TemplateView):
    template_name = 'worker/annotationTool.html'

    def get_context_data(self, **kwargs):
        context = super(AnnotationPage, self).get_context_data()

        context['audio_obj'] = get_object_or_404(SpeakerSubmission, pk=kwargs.get('id'))
        context['stt_data'] = json.dumps(context['audio_obj'].stt_data)
        annotated_data = ""
        if WorkerSubmission.objects.filter(speaker_submission__pk=kwargs.get('id'), worker=self.request.user.worker).exists():
            annotated_data = WorkerSubmission.objects.get(speaker_submission__pk=kwargs.get('id'), worker=self.request.user.worker).split_data
        context['annotated_data'] = annotated_data


        # path = settings.MEDIA_ROOT
        # print(path)
        # final_path = path + '/naverResponseChanged.json'
        # print(final_path)
        # stt_data = []
        # try:
        #     with open(final_path, encoding='utf8') as json_file:
        #         stt_data = json.load(json_file)
        # except FileNotFoundError as e:
        #     print("File does not exist at {}.".format(final_path))
        #
        # context['stt_data'] = json.dumps(stt_data)
        # context['audio_file'] = os.path.join(path, "Speech.mp3")

        return context


class SaveAnnotation(View):
    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            if SpeakerSubmission.objects.filter(pk=kwargs.get('id')).exists():
                print(self.request.user.worker)
                if WorkerSubmission.objects.filter(speaker_submission__pk=kwargs.get('id'), worker=self.request.user.worker).exists():
                    obj = WorkerSubmission.objects.get(speaker_submission__pk=kwargs.get('id'),
                                                    worker=self.request.user.worker)
                    obj.split_data = self.request.POST.get('annotated_data')
                    obj.save()
                else:
                    WorkerSubmission.objects.create(
                        worker=self.request.user.worker,
                        speaker_submission_id=int(kwargs.get('id')),
                        split_data=json.loads(self.request.POST.get('annotated_data'))
                    )
                return render(self.request, 'worker/alerts/annotationSaveSuccess.html')
        return JsonResponse({"error": ""}, status=400)

class ProfileView(TemplateView):
    template_name = "speaker/profile.html"