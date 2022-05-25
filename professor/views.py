from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from orgadmin.models import Organization
from professor.forms import QuestionForm, QuestionSetForm
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
        context['organization_codes'] = Organization.objects.all()
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.organization_code = self.request.user.professor.organization_code
            self.object.save()
        return redirect('professor:question_list_page')

    def form_invalid(self, form):
        print('forn_error', form.errors)

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs =  super().get_form_kwargs(*args, **kwargs)
    #     kwargs['request'] = self.request
    #     return kwargs


class QuestionsUpdateView(AjaxableResponseMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'professor/question/ajax/QuestionsCreateAjax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subcat'] = SubCategory.objects.all()
        context['organization_codes'] = Organization.objects.all()
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
        return redirect('professor:question_list_page')


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'professor/question/QuestionsDetailPage.html'


def MultipleQuestionDeleteView(request):
    if request.method == 'POST':
        try:
            Obj = Question.objects.filter(pk__in=request.POST.getlist('question_ids[]'))
            Obj.delete()
            return redirect('professor:question_list_page')

        except:
            messages.error(request,
                           "Cannot delete Questions")
            return JsonResponse({}, status=500)


def QuestionDeleteView(request, pk):
    if request.method == "POST":
        Question.objects.filter(pk=pk).delete()
        return redirect("professor:question_list_page")


class QuestionSetListView(ListView):
    model = QuestionSet
    template_name = 'professor/QuestionSetPage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionSetListView, self).get_context_data(*args, **kwargs)
        return context


class QuestionSetCreateView(AjaxableResponseMixin, CreateView):
    model = QuestionSet
    form_class = QuestionSetForm
    template_name = 'professor/question/ajax/QuestionSetCreateAjax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subcat'] = SubCategory.objects.all()
        context['qn_list'] = Question.objects.filter(organization_code=self.request.user.professor.organization_code)
        # context['sel_qn_list'] = [int(x) for x in self.request.GET['qn_list'].split(",") if x]
        # context['qn_list'] = context['qn_list'].exclude(pk__in=context['sel_qn_list'])
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            try:
                selected_questions = self.request.POST.get("selected_questions").split(',')
                print('type sel', type(selected_questions))
                print('selected_questions', selected_questions)

                self.object.organization_code = self.request.user.professor.organization_code
                self.object.save()
                for q in selected_questions:
                    self.object.questions.add(Question.objects.get(pk=int(q)))
                return redirect('professor:question_set_page')
            except:
                print('except')
                self.object.delete()
                return redirect('professor:question_set_page')

    def form_invalid(self, form):
        print('forn_error', form.errors)
        # selected_questions = self.request.POST.getlist("selected_questions")
        # print('selected_questions', selected_questions)

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs =  super().get_form_kwargs(*args, **kwargs)
    #     kwargs['request'] = self.request
    #     return kwargs


def MultipleQuestionSetDeleteView(request):
    if request.method == 'POST':
        try:
            Obj = QuestionSet.objects.filter(pk__in=request.POST.getlist('questionset_ids[]'))
            Obj.delete()
            return redirect('professor:question_set_page')

        except:
            messages.error(request,
                           "Cannot delete QuestionSet")
            return JsonResponse({}, status=500)


def QuestionSetDeleteView(request, pk):
    if request.method == "POST":
        QuestionSet.objects.filter(pk=pk).delete()
        return redirect("professor:question_set_page")


class ProfileView(TemplateView):
    template_name = "professor/profile.html"
