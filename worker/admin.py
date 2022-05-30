from django.contrib import admin
from .models import *

admin.site.register(Worker)
admin.site.register(WorkerTask)
admin.site.register(WorkerSubmission)
