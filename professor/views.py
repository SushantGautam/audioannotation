from django.shortcuts import render


def homepage(request):
    return render(request, 'professor/homepage.html')


def QuestionListPage(request):
    return render(request, 'professor/QuestionListPage.html')


def QuestionSetPage(request):
    return render(request, 'professor/QuestionSetPage.html')