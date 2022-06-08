from django import forms

from speaker.models import SpeakerSubmission, Speaker


class SpeakerSubmissionForm(forms.ModelForm):
    class Meta:
        model = SpeakerSubmission
        fields = ["question", "speaker", "audio_file"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Speaker
        exclude = ('organization_code', 'user', 'verified')

        widgets = {
            'birth_date': forms.DateTimeInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'gender': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        # Focus on form field whenever error occurred
        errorList = list(self.errors)
        for item in errorList:
            self.fields[item].widget.attrs.update({'autofocus': ''})
            break
