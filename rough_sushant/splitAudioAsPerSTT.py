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


users = ["ajordan@sa.nsdai.org", "alicegold@sa.nsdai.org", "alinakan@sa.nsdai.org",
         "Amal.Kabbous@ruhr-uni-bochum.de", "chenyin@sa.nsdai.org", "christinapark@sa.nsdai.org",
         "crz970826@gmail.com", "ekaterinabaiun@sa.nsdai.org", "ger_bochum_01@sa.nsdai.org",
         "ger_bochum_06@sa.nsdai.org", "ger_bochum_07@sa.nsdai.org", "ger_bochum_11@sa.nsdai.org",
         "ger_bochum_16@sa.nsdai.org", "ger_bochum_18@sa.nsdai.org", "ger_bochum_26@sa.nsdai.org",
         "ger_bochum_31@sa.nsdai.org", "ger_bochum_32@sa.nsdai.org", "ger_bochum_33@sa.nsdai.org",
         "ger_bochum_35@sa.nsdai.org", "ger_bochum_36@sa.nsdai.org", "ger_bochum_38@sa.nsdai.org",
         "ger_bochum_39@sa.nsdai.org", "ger_bochum_40@sa.nsdai.org", "ger_bochum_41@sa.nsdai.org",
         "ger_bochum_42@sa.nsdai.org", "ger_bochum_47@sa.nsdai.org", "ger_bochum_51@sa.nsdai.org",
         "ger_bochum_52@sa.nsdai.org", "ger_bochum_53@sa.nsdai.org", "ger_bochum_55@sa.nsdai.org",
         "ger_bochum_58@sa.nsdai.org", "ger_bochum_59@sa.nsdai.org", "ger_bochum_61@sa.nsdai.org",
         "ger_bochum_62@sa.nsdai.org", "ger_bochum_66@sa.nsdai.org", "ger_bochum_70@sa.nsdai.org",
         "ger_bochum_74@sa.nsdai.org", "ger_bochum_76@sa.nsdai.org", "ger_bochum_77@sa.nsdai.org",
         "ger_bochum_80@sa.nsdai.org", "hoff-mar@web.de", "Jasmin.Duesterloh@ruhr-uni-bochum.de",
         "jessicanorton@sa.nsdai.org", "Jiajie.chen@ruhr-uni-bochum.de", "jinyeonjin@sa.nsdai.org",
         "Johanna.Spanbroek@rub.de", "kaylamakai@sa.nsdai.org", "kokkeying@sa.nsdai.org",
         "Lorena.Wolf@rub.de", "marytarakey@sa.nsdai.org", "minority25@sa.nsdai.org",
         "nsd_iana@sa.nsdai.org", "nsd_luiza@sa.nsdai.org", "nsd_oona@sa.nsdai.org",
         "ohkusanoriko@sa.nsdai.org", "pia.heyn@rub.de", "sarah.kessener@rub.de",
         "sinekaterina@sa.nsdai.org", "tanweiwen@sa.nsdai.org", "tarantellishaun@sa.nsdai.org",
         "teresachien@sa.nsdai.org", "thilinhnguyen@sa.nsdai.org", "thuongpham@sa.nsdai.org",
         "tianruijia@sa.nsdai.org", "wellingtoncordelia@sa.nsdai.org", "yangcharis@sa.nsdai.org",
         "yanglin@sa.nsdai.org", "yulyanatyo@sa.nsdai.org", "yuriykim@sa.nsdai.org"]

for user in users:
    ss = SpeakerSubmission.objects.filter(
        speaker__user__email=user,
        question__subcategory_code__name__in=["Reading Word", 'Reading Sentence',
                                              'Reading Paragraph'])
    # filter latest value of subcategory_code__name for each user
    ss_list = ss.values_list('pk', 'question', 'speaker')
    dict_ss = {}
    for ss_item in ss_list:
        if str(ss_item[1]) + str(ss_item[2]) not in dict_ss:
            dict_ss[str(ss_item[1]) + str(ss_item[2])] = ss_item[0]
        else:
            if dict_ss[str(ss_item[1]) + str(ss_item[2])] < ss_item[0]:  # if the one on list is lesser than we have
                dict_ss[str(ss_item[1]) + str(ss_item[2])] = ss_item[0]
    ss = ss.filter(pk__in=dict_ss.values())
    # end filter latest value of subcategory_code__name for each user

    print("Processing. User" + user)
    totalFiles = len(ss)
    alreadyProcessedFiles = 0
    for idx, obj in enumerate(list(ss)):
        filex = obj.audio_file.path
        file = filex.replace("/home/audio_annotation/media/speaker/audio/", "").split("/")[-1]
        folder = filex.replace("/home/audio_annotation/media/speaker/audio/", "").split("/")[0]
        if os.path.isfile("kim/" + folder + "__" + file + '.json'):
            alreadyProcessedFiles += 1
            continue
    if alreadyProcessedFiles == totalFiles:
        print("All files already processed")

        for idx, obj in enumerate(list(ss)):
            filex = obj.audio_file.path
            file = filex.replace("/home/audio_annotation/media/speaker/audio/", "").split("/")[-1]
            folder = filex.replace("/home/audio_annotation/media/speaker/audio/", "").split("/")[0]
            STTSavePath = "media/kimExport/" + user + "/STT/"
            AudioSavePath = "media/kimExport/" + user + "/Audio/"
            AudioSplitSavePath = "media/kimExport/" + user + "/AudioSplit/"

            os.system("mkdir -p " + STTSavePath)
            os.system("mkdir -p " + AudioSavePath)
            os.system("mkdir -p " + AudioSplitSavePath)

            print(file, "-", folder)
            with open("kim/" + folder + "__" + file + '.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('result') == 'NO_SEGMENT':
                    print("kim/" + str(obj.id) + "_" + str(
                        obj.question.unique_code) + 'NO_SEGMENT')
                    pass
                elif data.get('result') == 'COMPLETED':
                    if data.get('segments'):
                        for idx, seg in enumerate(data.get('segments')):
                            print(seg.get('text'), seg.get('start'), seg.get('end'))
                            outpath = AudioSplitSavePath + str(obj.question.unique_code) + "__" + file + "__" + str(
                                idx) + "__" + str(seg.get('text')[:50]) + "_" + ".mp3"
                            # print(outpath)
                            filepath = filex
                            cmd = "ffmpeg -y -i " + filepath + " -ss " + convertMillis(
                                seg.get('start')) + " -t " + convertMillis(
                                (seg.get('end') - seg.get('start'))) + " -c:a libmp3lame '" + outpath + "'"
                            print(cmd)
                            os.system(cmd)  # this will slice the audio

                # write STToutput With Qsn
                data['QuestionInfo'] = dict(QuestionSerializer(instance=obj.question, ).data)
                # save file
                with open(STTSavePath + str(obj.question.unique_code) + "__" + file + '.json', 'w',
                          encoding='utf-8') as f:
                    f.write(json.dumps(data, ensure_ascii=False, indent=4))
                    print('success')
                os.system("cp 'media/" + obj.audio_file.name + "' " + AudioSavePath + str(
                    obj.question.unique_code) + "__" + file)
    else:
        print("Some files are not processed")
#
# for submission in SpeakerSubmission.objects.filter(speaker__id=17):
#     os.system("cp 'media/" + submission.audio_file.name + "' .rough_sushant/originalAudio/")
#
#     file = submission.audio_file.name.split("speaker/audio/nsd_luiza_sa.nsdai.org/")[1]
#     if os.path.isfile(".rough_sushant/STToutput/" + file + '.json'):
#         # print("STToutput/"+file + '.json'+ '  exists')
#         pass
#         # continue
#     # read json file
#     with open(".rough_sushant/STToutput/" + file + '.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
#         if data.get('result') == 'NO_SEGMENT':
#             print(".rough_sushant/splitfinal/" + str(submission.id) + "_" + str(
#                 submission.question.unique_code) + 'NO_SEGMENT')
#             pass
#         elif data.get('result') == 'COMPLETED':
#             if data.get('segments'):
#                 for idx, seg in enumerate(data.get('segments')):
#                     print(seg.get('text'), seg.get('start'), seg.get('end'))
#                     outpath = ".rough_sushant/splitfinal/" + str(submission.speaker.user.username) + "_" + str(
#                         submission.question.unique_code) + "_" + str(idx) + "_" + str(seg.get('text')[:50]) + "_" + file
#                     # print(outpath)
#                     filepath = "media/speaker/audio/nsd_luiza_sa.nsdai.org/" + file
#                     cmd = "ffmpeg -y -i " + filepath + " -ss " + convertMillis(
#                         seg.get('start')) + " -t " + convertMillis(
#                         (seg.get('end') - seg.get('start'))) + " -c:a libmp3lame '" + outpath + "'"
#                     print(cmd)
#                     os.system(cmd)  # this will slice the audio
#
#         # write STToutput With Qsn
#         data = json.load(f)
#         data['QuestionInfo'] = dict(QuestionSerializer(instance=submission.question, ).data)
#         # save file
#         with open(".rough_sushant/STToutputWithQsn/" + file + '.json', 'w', encoding='utf-8') as f:
#             f.write(json.dumps(data, ensure_ascii=False, indent=4))
#             print('success')
#
# os.system(
#     "zip -r media/kimfinal.zip .rough_sushant/splitfinal/ .rough_sushant/STToutputWithQsn/ .rough_sushant/originalAudio/")

# venv/bin/python manage.py  shell
# exec(open("rough_sushant/splitAudioAsPerSTT.py").read())
# zip -r media/kimfinal.zip ./media/kimExport/
