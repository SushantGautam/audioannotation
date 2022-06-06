from django.forms import ModelForm, DateTimeField, DateTimeInput

from speaker.models import SpeakerSubmission, Speaker


class SpeakerSubmissionForm(ModelForm):
    class Meta:
        model = SpeakerSubmission
        fields = ["question", "speaker", "audio_file"]


class ProfileEditForm(ModelForm):
    class Meta:
        model = Speaker
        exclude = ('organization_code', 'user', 'verified')

        widgets = {
            'birth_date': DateTimeInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }
