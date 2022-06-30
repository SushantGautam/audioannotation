# nsd_luiza_sa.nsdai.org
# nsd_luiza_sa.nsdai.org
import datetime
import json
import os

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from professor.models import Question
from speaker.models import SpeakerSubmission


def convertMillis(millis):
    #  return this foemat hh:mm:ss
    m, s = divmod(millis, 1000 * 60)
    h, m = divmod(m, 60)
    s = round(s / 1000, 2)
    # return "%d:%02d:%02d" % (h, m, s)
    return str(datetime.timedelta(milliseconds=millis))


class QuestionSerializer(ModelSerializer):
    category_name = serializers.CharField(source='subcategory_code.name')

    class Meta:
        model = Question
        fields = ["unique_code", "question_title", 'description', 'category_name', 'question_keywords',
                  "evaluation_purpose"
                  ]
        read_only_fields = ["unique_code", 'category_name', "question_title", 'subcategory_code', 'description',
                            'question_keywords',
                            "evaluation_purpose"]


os.system("rm .rough_sushant/splitfinal/*.mp3")
os.system("rm media/kimfinal.zip")

for submission in SpeakerSubmission.objects.filter(speaker__id=17):
    os.system("cp 'media/" + submission.audio_file.name + "' .rough_sushant/originalAudio/")

    file = submission.audio_file.name.split("speaker/audio/nsd_luiza_sa.nsdai.org/")[1]
    if os.path.isfile(".rough_sushant/STToutput/" + file + '.json'):
        # print("STToutput/"+file + '.json'+ '  exists')
        pass
        # continue
    # read json file
    with open(".rough_sushant/STToutput/" + file + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        if data.get('result') == 'NO_SEGMENT':
            print(".rough_sushant/splitfinal/" + str(submission.id) + "_" + str(
                submission.question.unique_code) + 'NO_SEGMENT')
            pass
        elif data.get('result') == 'COMPLETED':
            if data.get('segments'):
                for idx, seg in enumerate(data.get('segments')):
                    print(seg.get('text'), seg.get('start'), seg.get('end'))
                    outpath = ".rough_sushant/splitfinal/" + str(submission.speaker.user.username) + "_" + str(
                        submission.question.unique_code) + "_" + str(idx) + "_" + str(seg.get('text')[:50]) + "_" + file
                    # print(outpath)
                    filepath = "media/speaker/audio/nsd_luiza_sa.nsdai.org/" + file
                    cmd = "ffmpeg -y -i " + filepath + " -ss " + convertMillis(
                        seg.get('start')) + " -t " + convertMillis(
                        (seg.get('end') - seg.get('start'))) + " -c:a libmp3lame '" + outpath + "'"
                    print(cmd)
                    os.system(cmd)  # this will slice the audio

        # write STToutput With Qsn
        data = json.load(f)
        data['QuestionInfo'] = dict(QuestionSerializer(instance=submission.question, ).data)
        # save file
        with open(".rough_sushant/STToutputWithQsn/" + file + '.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
            print('success')

os.system(
    "zip -r media/kimfinal.zip .rough_sushant/splitfinal/ .rough_sushant/STToutputWithQsn/ .rough_sushant/originalAudio/")

# venv/bin/python manage.py  shell
# rm .rough_sushant/splitfinal/*.mp3
# exec(open(".rough_sushant/splitAudioAsPerSTT.py").read())
# zip -r media/kimfinal.zip .rough_sushant/splitfinal/ .rough_sushant/STToutput/ .rough_sushant/originalAudio/
