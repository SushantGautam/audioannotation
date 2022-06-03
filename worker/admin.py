from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Worker, EvaluationTitle, WorkerTask, WorkerSubmission

class EvaluationTitleResource(resources.ModelResource):
    class Meta:
        model = EvaluationTitle

class EvaluationTitleAdmin(ImportExportModelAdmin):
    resource_class = EvaluationTitleResource

admin.site.register(Worker)
admin.site.register(EvaluationTitle, EvaluationTitleAdmin)
admin.site.register(WorkerTask)
admin.site.register(WorkerSubmission)
