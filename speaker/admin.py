from django.contrib import admin
from .models import Speaker, SpeakerSubmission, ExamSetSubmission

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_fullname', 'level', 'get_email', 'topik_score', 'organization_code')
    list_filter = ('level', 'organization_code', 'is_verified')
    
    @admin.display(ordering='user__first_name', description='Full Name')
    def get_fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    
    @admin.display(ordering='user__email', description='Email')
    def get_email(self, obj):
        return obj.user.email
admin.site.register(Speaker, SpeakerAdmin)

class SpeakerSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'speaker', 'question', 'exam_set', 'created_at' ,'status')
    list_filter = ('speaker', 'exam_set', 'status')

admin.site.register(SpeakerSubmission, SpeakerSubmissionAdmin)

class ExamSetSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'speaker', 'exam_set', 'created_at' ,'status')
    list_filter = ('speaker', 'exam_set', 'status')
admin.site.register(ExamSetSubmission, ExamSetSubmissionAdmin)
