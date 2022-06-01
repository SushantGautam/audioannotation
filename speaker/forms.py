from django.forms import ModelForm

from professor.models import Question
from speaker.models import SpeakerSubmission


class SpeakerSubmissionForm(ModelForm):
    class Meta:
        model = SpeakerSubmission
        fields = ["question", "speaker", "audio_file"]



