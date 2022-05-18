from django.forms import ModelForm

from professor.models import Question
from speaker.models import AudioFile, SpeakerSubmission


class AudioFileForm(ModelForm):
    class Meta:
        model = AudioFile
        fields = ["audio_file"]


class SpeakerSubmissionForm(ModelForm):
    class Meta:
        model = SpeakerSubmission
        fields = ["question", "speaker", "audio_file"]



