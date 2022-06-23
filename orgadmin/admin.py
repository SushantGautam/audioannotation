from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import OrgAdmin, Organization, Aggrement, Contract, ContractSign, VerificationRequest

class OrgAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'created_at', 'is_active')
admin.site.register(Organization, OrgAdminAdmin)

class OrgAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_fullname',  'get_email', 'organization_code')
    list_filter = ('organization_code',)
    search_fields = ('user',)
   
    @admin.display(ordering='user__first_name', description='Full Name')
    def get_fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    @admin.display(ordering='user__email', description='Email')
    def get_email(self, obj):
        return obj.user.email
admin.site.register(OrgAdmin, OrgAdminAdmin)

class AggrementAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ('id', 'title', 'organization_code', 'created_at', 'updated_at')
    list_filter = ('organization_code',)
    search_fields = ('title',)
admin.site.register(Aggrement, AggrementAdmin)

class ContractAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ('id', 'title', 'user_type', 'created_at', 'created_by', 'upload_file')
    list_filter = ('user_type', 'is_active')
admin.site.register(Contract, ContractAdmin)


class ContractSignAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract_code', 'user', 'created_at', 'approved', 'upload_file')
    list_filter = ('contract_code', 'approved')
admin.site.register(ContractSign, ContractSignAdmin)

class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feedback', 'created_at', 'approved')
admin.site.register(VerificationRequest, VerificationRequestAdmin)

