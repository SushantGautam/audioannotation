from django.db import models
from django.contrib.auth.models import User

class BaseUserModel(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    class Meta:
        abstract = True

class OrgAdmin(BaseUserModel):
    class Meta:
        verbose_name = 'Organization Admin'
        verbose_name_plural = 'Organization Admins'
