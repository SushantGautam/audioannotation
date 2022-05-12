from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from speaker.forms import AudioFileForm
from speaker.models import Speaker


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