from django.contrib.auth.models import User
from django.forms import ModelForm


class UserChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
