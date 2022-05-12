from django.forms import ModelForm

from speaker.models import AudioFile


class AudioFileForm(ModelForm):
    class Meta:
        model = AudioFile
        fields = ["audio_file"]

