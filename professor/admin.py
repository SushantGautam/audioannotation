from django.contrib import admin
from .models import *

admin.site.register(Professor)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Question)
admin.site.register(QuestionSet)
