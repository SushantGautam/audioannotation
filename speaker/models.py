from django.db import models
from orgadmin.models import BaseUserModel

class Speaker(BaseUserModel):
    class Meta:
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'
