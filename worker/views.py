import json
import os

from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView


def homepage(request):
    return render(request, 'worker/homepage.html')


def getStaticPrediction():
    return {
        "annotations": "[]",
        "audio_segments": ["media/audio-splits/4/11_UK94EJ2DRW.mp3", "media/audio-splits/4/3_EIUC5O6KXZ.mp3",
                           "media/audio-splits/4/10_6P12XSSXBH.mp3", "media/audio-splits/4/1_YDR24KHHND.mp3",
                           "media/audio-splits/4/2_T0ZYZ216AE.mp3", "media/audio-splits/4/0_0TXXAK0PJS.mp3",
                           "media/audio-splits/4/9_WCQ9Y14F4F.mp3", "media/audio-splits/4/4_0XFF22CNG5.mp3",
                           "media/audio-splits/4/18_IYODIII3L1.mp3", "media/audio-splits/4/8_Z00BQR5SGK.mp3",
                           "media/audio-splits/4/16_49G46PSSTL.mp3", "media/audio-splits/4/17_WQMY5U7CS8.mp3",
                           "media/audio-splits/4/13_0M3FEEEYHC.mp3", "media/audio-splits/4/12_KPABYA4D6H.mp3",
                           "media/audio-splits/4/5_W95TKZYTZR.mp3", "media/audio-splits/4/14_OICOWOOCSW.mp3",
                           "media/audio-splits/4/15_VBWISS4JRC.mp3", "media/audio-splits/4/6_W0IKJCXWUH.mp3",
                           "media/audio-splits/4/7_Q3F5BAN5N9.mp3"],
        "split_data": [{
            "start": 0.723,
            "end": 4.663
        }, {
            "start": 4.58,
            "end": 6.454
        }, {
            "start": 6.745,
            "end": 9.957
        }, {
            "start": 9.885,
            "end": 12.872
        }, {
            "start": 14.835,
            "end": 16.712
        }, {
            "start": 16.699,
            "end": 19.359
        }, {
            "start": 19.594,
            "end": 20.264
        }, {
            "start": 20.672,
            "end": 21.285
        }, {
            "start": 22.151,
            "end": 23.363
        }, {
            "start": 23.481,
            "end": 24.907
        }, {
            "start": 27.125,
            "end": 30.095
        }, {
            "start": 30.4,
            "end": 31.786
        }, {
            "start": 31.976,
            "end": 33.349
        }, {
            "start": 33.731,
            "end": 35.297
        }, {
            "start": 35.299,
            "end": 39.434
        }, {
            "start": 39.463,
            "end": 40.283
        }, {
            "start": 40.536,
            "end": 45.907
        }, {
            "start": 45.871,
            "end": 47.183
        }, {
            "start": 47.355,
            "end": 48.906
        }],
        "stt_predictions_annotations": [{
            "value": {
                "start": 0.08,
                "end": 7.64,
                "labels": ["voice"]
            },
            "id": "splitter_0",
            "from_name": "labels",
            "to_name": "audio",
            "type": "labels"
        }, {
            "value": {
                "start": 0.08,
                "end": 7.64,
                "text": [""]
            },
            "id": "splitter_0",
            "from_name": "transcription",
            "to_name": "audio",
            "type": "textarea"
        }, {
            "value": {
                "start": 7.93,
                "end": 17.69,
                "labels": ["voice"]
            },
            "id": "splitter_1",
            "from_name": "labels",
            "to_name": "audio",
            "type": "labels"
        }, {
            "value": {
                "start": 7.93,
                "end": 17.69,
                "text": ["하나 둘 셋 셋 셋 감사입니다. 구리야"]
            },
            "id": "splitter_1",
            "from_name": "transcription",
            "to_name": "audio",
            "type": "textarea"
        }]
    }

from django.templatetags.static import static
class AnnotationPage(TemplateView):
    template_name = 'worker/annotation-tool.html'

    def get_context_data(self, **kwargs):
        context = super(AnnotationPage, self).get_context_data()
        path = settings.MEDIA_ROOT
        print(path)
        final_path = path + '/naverResponseChanged.json'
        print(final_path)
        stt_data = []
        try:
            with open(final_path, encoding='utf8') as json_file:
                stt_data = json.load(json_file)
        except FileNotFoundError as e:
            print("File does not exist at {}.".format(final_path))

        context['stt_data'] = json.dumps(stt_data)
        context['audio_file'] = os.path.join(path, "Speech.mp3")
        
        return context
