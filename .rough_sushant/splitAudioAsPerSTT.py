from speaker.models import SpeakerSubmission
import os, json
#nsd_luiza_sa.nsdai.org
import datetime

def convertMillis(millis):
    #  return this foemat hh:mm:ss
    m, s = divmod(millis, 1000* 60)
    h, m = divmod(m, 60)
    s= round(s/1000,2)
    # return "%d:%02d:%02d" % (h, m, s)
    return str(datetime.timedelta(milliseconds=millis))

os.system("rm .rough_sushant/splitfinal/*.mp3")
os.system("rm media/kimfinal.zip")

for submission in SpeakerSubmission.objects.filter(speaker__id=17):
    os.system("cp 'media/"+ submission.audio_file.name +"' .rough_sushant/originalAudio/")

    file = submission.audio_file.name.split("speaker/audio/nsd_luiza_sa.nsdai.org/")[1]
    if os.path.isfile(".rough_sushant/STToutput/"+file + '.json'):
        # print("STToutput/"+file + '.json'+ '  exists')
        pass
        # continue
    # read json file
    with open(".rough_sushant/STToutput/"+file + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        if data.get('result') == 'NO_SEGMENT':
            print( ".rough_sushant/splitfinal/"+str(submission.id)+"_"+ str(submission.question.unique_code) +'NO_SEGMENT')
            pass
        elif data.get('result') == 'COMPLETED':
            if data.get('segments'):
                for idx, seg in enumerate(data.get('segments')):
                    print(seg.get('text'), seg.get('start'), seg.get('end'))
                    outpath = ".rough_sushant/splitfinal/"+str(submission.speaker.user.username)+"_"+ str(submission.question.unique_code)+"_"+str(idx)+"_"+ str(seg.get('text')[:50])+"_"+ file
                    # print(outpath)
                    filepath = "media/speaker/audio/nsd_luiza_sa.nsdai.org/" + file
                    cmd = "ffmpeg -y -i "+filepath +" -ss "+ convertMillis(seg.get('start')) +" -t "+ convertMillis((seg.get('end') - seg.get('start')))+" -c:a libmp3lame '"+outpath+"'"
                    print(cmd)
                    os.system(cmd)

os.system("zip -r media/kimfinal.zip .rough_sushant/splitfinal/ .rough_sushant/STToutput/ .rough_sushant/originalAudio/")

# venv/bin/python manage.py  shell
# rm .rough_sushant/splitfinal/*.mp3
# exec(open(".rough_sushant/splitAudioAsPerSTT.py").read())
# zip -r media/kimfinal.zip .rough_sushant/splitfinal/ .rough_sushant/STToutput/ .rough_sushant/originalAudio/
