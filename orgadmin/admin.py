from django.contrib import admin
from .models import OrgAdmin, Organization, Contract, ContractSign, VerificationRequest

admin.site.register(OrgAdmin)
admin.site.register(Organization)
admin.site.register(Contract)
admin.site.register(ContractSign)
admin.site.register(VerificationRequest)

