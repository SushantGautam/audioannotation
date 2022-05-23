from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class BaseUserModel(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization_code = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    class Meta:
        abstract = True

class OrgAdmin(BaseUserModel):
    class Meta:
        verbose_name = 'Organization Admin'
        verbose_name_plural = 'Organization Admins'
