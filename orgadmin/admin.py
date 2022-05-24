from django.contrib import admin
from .models import OrgAdmin, Organization, Contract, ContractSign

admin.site.register(OrgAdmin)
admin.site.register(Organization)
admin.site.register(Contract)
admin.site.register(ContractSign)

