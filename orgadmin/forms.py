from django.contrib.auth.models import User
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

from orgadmin.models import Contract


class UserChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ('title', 'user_type', 'description', 'upload_file')
        widgets = {
            'description': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        existing_choices = Contract.objects.all().values_list('user_type', flat=True)
        choices = list(Contract.USER_TYPE_CHOICES)
        new_choices = []

        for value, display in choices:
            if value not in existing_choices:
                new_choices.append((value, display))
            if self.instance.pk and self.instance.user_type == value:
                new_choices.append((value, display))
        self.fields['user_type'].choices = tuple(new_choices)
