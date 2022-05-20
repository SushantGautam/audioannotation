from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, FormView

from speaker.forms import AudioFileForm, SpeakerSubmissionForm
from speaker.models import Speaker

from professor.models import Question, QuestionSet, ExamSet


@csrf_protect
def homepage(request):
    # return render(request, 'speaker/homepage.html')
    return render(request, 'speaker/homepage.html')


def save_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("File saved")
            obj = form.save(commit=False)
            obj.speaker = Speaker.objects.first()
            obj.save()
        else:
            print("form invalid: ", form.errors)
    return redirect('homepage')


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
        context['qn_set'] = qn_set
        context['qn'] = questions[qn_num]
        context['qn_num'] = qn_num
        context['qn_num1'] = qn_num + 1
        context['prev_qn'] = None if qn_num == 0 else qn_num - 1
        context['next_qn'] = None if questions.count() == (qn_num + 1) else qn_num + 1
        return context

