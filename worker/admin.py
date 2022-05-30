from django.contrib import admin
from .models import Worker, EvaluationTitle, WorkerTask, WorkerSubmission

admin.site.register(Worker)
admin.site.register(EvaluationTitle)
admin.site.register(WorkerTask)
admin.site.register(WorkerSubmission)
