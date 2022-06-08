from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_fullname',  'get_email', 'organization_code')
    list_filter = ('organization_code',)
    search_fields = ('user',)
   
    @admin.display(ordering='user__first_name', description='Full Name')
    def get_fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    @admin.display(ordering='user__email', description='Email')
    def get_email(self, obj):
        return obj.user.email

admin.site.register(Professor, ProfessorAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name', 'description')

admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category_code', 'created_at', 'updated_at', 'is_active')
    list_filter = ('category_code', 'is_active')
    search_fields = ('name', 'description')

admin.site.register(SubCategory, SubCategoryAdmin)

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

class QuestionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'question_title', 'unique_code', 'created_at', 'difficulty_level','subcategory_code')
    list_filter = ('subcategory_code', 'difficulty_level', 'organization_code', 'is_active')
    search_fields = ('question_title', 'unique_code', 'question_keywords')
    resource_class = QuestionResource

class QuestionSetResource(resources.ModelResource):
    class Meta:
        model = QuestionSet

class QuestionSetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'unique_code', 'created_at', 'difficulty_level', 'subcategory_code')
    list_filter = ('subcategory_code', 'difficulty_level', 'is_active')
    search_fields = ('unique_code', 'description')
    resource_class = QuestionSetResource

class ExamSetResource(resources.ModelResource):
    class Meta:
        model = ExamSet

class ExamSetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'exam_name', 'start_date', 'end_date', 'difficulty_level')
    list_filter = ('difficulty_level', 'is_active')
    search_fields = ('exam_name', 'description')
    resource_class = ExamSetResource

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(ExamSet, ExamSetAdmin)
