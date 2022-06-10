from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from orgadmin.models import OrgAdmin, Organization
from professor.models import Professor
from speaker.models import Speaker
from worker.models import Worker


@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    if sociallogin.account.provider == 'whalespace':
        user_data = user.socialaccount_set.filter(provider='whalespace')[0].extra_data
        user_organization = ''
        user_type = user_data['userType']
        if user_data['space']:
            user_organization = user_data['space']['code']
        if user_organization and Organization.objects.filter(name=user_organization).exists():
            org = Organization.objects.get(name=user_organization)
            if user_type == 'spe':
                Speaker.objects.create(user=user, organization_code=org)
            elif user_type == 'prf':
                Professor.objects.create(user=user, organization_code=org)
            elif user_type == 'wor':
                Worker.objects.create(user=user, organization_code=org)
            elif user_type == 'org':
                OrgAdmin.objects.create(user=user, organization_code=org)