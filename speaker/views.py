from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from speaker.forms import AudioFileForm


@csrf_protect
def homepage(request):
    # return render(request, 'speaker/homepage.html')
    return render(request, 'speaker/homepage.html')


def save_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("File saved")
            form.save()
        else:
            print("form invalid: ", form.errors)
    return redirect('homepage')