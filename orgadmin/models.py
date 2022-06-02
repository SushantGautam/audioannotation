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
    permanent_address = models.CharField(max_length=256, null=True, blank=True)
    current_address = models.CharField(max_length=256, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=256, null=True, blank=True)
    verified = models.BooleanField(default=False)
    organization_code = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    class Meta:
        abstract = True

class OrgAdmin(BaseUserModel):
    class Meta:
        verbose_name = 'Organization Admin'
        verbose_name_plural = 'Organization Admins'

def contract_file_name(instance, filename):
    return 'contract/{0}_contract/{1}'.format(instance.created_by.organization_code, filename)

class Contract(models.Model):
    USER_TYPE_CHOICES = (
        ('PRF', 'Professor'),
        ('WOR', 'Worker'),
        ('STU', 'Student'),
    )
    title = models.CharField(max_length=256)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=3)
    description = models.TextField(null=True, blank=True)
    upload_file = models.FileField(upload_to=contract_file_name, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(OrgAdmin, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

def contract_sign_file_name(instance, filename):
    return 'contract/contract_sign/{0}/{1}'.format(instance.user, filename)

class ContractSign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_file = models.FileField(upload_to=contract_sign_file_name, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    contract_code = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return self.contract_code.title
