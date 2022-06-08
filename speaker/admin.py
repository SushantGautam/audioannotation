from django.contrib import admin
from .models import Speaker, SpeakerSubmission, ExamSetSubmission

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_fullname', 'get_email', 'organization_code')
    list_filter = ('level', 'organization_code', 'is_active', 'is_verified')
    search_fields = ('user',)
    
    @admin.display(ordering='user__first_name', description='Full Name')
    def get_fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    
    @admin.display(ordering='user__email', description='Email')
    def get_email(self, obj):
        return obj.user.email
admin.site.register(Speaker)
admin.site.register(SpeakerSubmission)
admin.site.register(ExamSetSubmission)
