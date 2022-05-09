from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from professor.models import Question,QuestionSet


def homepage(request):
    return render(request, 'professor/homepage.html')


class QuestionListPage(ListView):
    template_name = 'professor/QuestionListPage.html'
    model = Question


def QuestionSetPage(request):
    return render(request, 'professor/QuestionSetPage.html')