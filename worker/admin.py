from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Worker, EvaluationTitle, WorkerTask, WorkerSubmission


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_fullname', 'get_email', 'organization_code')
    list_filter = ('organization_code',)
    search_fields = ('user',)

    @admin.display(ordering='user__first_name', description='Full Name')
    def get_fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    @admin.display(ordering='user__email', description='Email')
    def get_email(self, obj):
        return obj.user.email
admin.site.register(Worker, WorkerAdmin)
class EvaluationTitleResource(resources.ModelResource):
    class Meta:
        model = EvaluationTitle

class EvaluationTitleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title', 'score', 'evaluation_code', 'evaluation_type', 'subcategory_code')
    list_filter = ('evaluation_type', 'subcategory_code', 'score')  
    search_fields = ('title', 'evaluation_code')
    resource_class = EvaluationTitleResource
admin.site.register(EvaluationTitle, EvaluationTitleAdmin)

class WorkerTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'approved', 'task_type', 'created_at', 'status')
    list_filter = ('task_type', 'approved', 'status')
admin.site.register(WorkerTask, WorkerTaskAdmin)

class WorkerSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'speaker_submission', 'worker_task', 'created_at', 'status')
    list_filter = ('status',)
admin.site.register(WorkerSubmission, WorkerSubmissionAdmin)
