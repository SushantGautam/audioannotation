import json
import os

from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

from speaker.models import SpeakerSubmission


def homepage(request):
    return render(request, 'worker/homepage.html')


class AnnotationPage(TemplateView):
    template_name = 'worker/annotation-tool.html'

    def get_context_data(self, **kwargs):
        context = super(AnnotationPage, self).get_context_data()

        context['audio_obj'] = SpeakerSubmission.objects.first()
        context['stt_data'] = json.dumps(context['audio_obj'].stt_data)

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
