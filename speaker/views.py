from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import ListView, FormView, TemplateView

from speaker.forms import SpeakerSubmissionForm
from speaker.models import Speaker, SpeakerSubmission

from professor.models import Question, QuestionSet, ExamSet


def homepage(request):
    return render(request, 'speaker/homepage.html')

class QuestionSetList(ListView):
    template_name = 'speaker/question_set_list.html'
    model = QuestionSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_set = ExamSet.objects.get(pk=self.request.GET['exam_set'])
        context['object_list'] = exam_set.question_sets.all()
        return context

class ExamSetList(ListView):
    template_name = 'speaker/exam_set_list.html'
    model = ExamSet


class ExamPopupView(FormView):
    form_class = SpeakerSubmissionForm
    template_name = 'speaker/test_popup.html'
    qn_num = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        qn_set = self.request.GET['qn_set']
        qn_num = int(self.request.GET.get('qn_num', self.qn_num))
        qn_set = QuestionSet.objects.get(pk=qn_set)
        questions = qn_set.questions.all()
        speaker = Speaker.objects.get(user=self.request.user)

        context['qn'] = questions[qn_num]
        exam_set = context['qn'].questionset_set.first().examset_set.first()
        # que_set = context['qn'].questionset_set.first()
        context['qn'].can_submit = not SpeakerSubmission.objects.filter(question=context['qn'],
                                                                      speaker=speaker,
                                                                      exam_set=exam_set).exists()

        context['speaker'] = speaker
        context['qn_set'] = qn_set
        context['qn_num'] = qn_num
        context['qn_num1'] = qn_num + 1
        context['prev_qn'] = None if qn_num == 0 else qn_num - 1
        context['next_qn'] = None if questions.count() == (qn_num + 1) else qn_num + 1
        return context

    def form_valid(self, form):
        if form.is_valid():
            print("File saved")
            obj = form.save(commit=False)
            obj.exam_set = obj.question.questionset_set.first().examset_set.first()
            obj.save()
        else:
            print("form invalid: ", form.errors)

        res_dict = {
            'success': 'true'
        }

        return JsonResponse(res_dict)

    def form_invalid(self, form):
        print("Error: ", form.errors)
        res_dict = {
            'success': 'false',
            'error': str(form.errors),
        }
        return JsonResponse(res_dict)


class ProfileView(TemplateView):
    template_name = "speaker/profile.html"