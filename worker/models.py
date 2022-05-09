from django.db import models

from orgadmin.models import BaseUserModel

class Worker(BaseUserModel):
    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'
