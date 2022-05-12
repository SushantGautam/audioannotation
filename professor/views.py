from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from professor.forms import QuestionForm
from professor.models import Question, QuestionSet, SubCategory


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


def homepage(request):
    return render(request, 'professor/homepage.html')


class QuestionListPage(ListView):
    template_name = 'professor/QuestionListPage.html'
    model = Question


class QuestionsCreateView(AjaxableResponseMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'professor/question/ajax/QuestionsCreateAjax.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subcat'] = SubCategory.objects.all()
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
        response = {'url': self.request.build_absolute_uri(reverse('professor:question_list_page')),
                    "status": "success",
                    "msg": "",
                    "qn_code": self.object.subcategory_code.name,
                    "qn_pk": self.object.pk,
                    "qn_title": self.object.title,
                    }
        # return JsonResponse(response)
        return redirect('professor:question_list_page')




class QuestionsUpdateView(AjaxableResponseMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'professor/question/ajax/QuestionsCreateAjax.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subcat'] = SubCategory.objects.all()
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            # file_upload = self.request.FILES['file_upload']
            # self.object.file_upload = file_upload
            self.object.save()
        response = {'url': self.request.build_absolute_uri(reverse('professor:question_list_page')),
                    "status": "success",
                    "msg": "",
                    "qn_code": self.object.subcategory_code.name,
                    "qn_pk": self.object.pk,
                    "qn_title": self.object.title,
                    }
        # return JsonResponse(response)
        return redirect('professor:question_list_page')








def QuestionDeleteView(request, pk):
    if request.method == "POST":
        Question.objects.filter(pk=pk).delete()
        return redirect("professor:question_list_page")



def QuestionSetPage(request):
    return render(request, 'professor/QuestionSetPage.html')
