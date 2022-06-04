from django.forms import ModelForm

from speaker.models import SpeakerSubmission, Speaker


class SpeakerSubmissionForm(ModelForm):
    class Meta:
        model = SpeakerSubmission
        fields = ["question", "speaker", "audio_file"]


class ProfileEditForm(ModelForm):
    class Meta:
        model = Speaker
        exclude = ('organization_code', 'user', 'verified')
