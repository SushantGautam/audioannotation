import json
import os

from rough_sushant.clovaStt import ClovaSpeechClient
# loop for all files in directory
from speaker.models import SpeakerSubmission

ss = SpeakerSubmission.objects.filter(speaker__user__email__in=["ajordan@sa.nsdai.org",
                                                                "alicegold@sa.nsdai.org",
                                                                "alinakan@sa.nsdai.org",
                                                                "Amal.Kabbous@ruhr-uni-bochum.de",
                                                                "chenyin@sa.nsdai.org",
                                                                "christinapark@sa.nsdai.org",
                                                                "crz970826@gmail.com",
                                                                "ekaterinabaiun@sa.nsdai.org",
                                                                "ger_bochum_01@sa.nsdai.org",
                                                                "ger_bochum_06@sa.nsdai.org",
                                                                "ger_bochum_07@sa.nsdai.org",
                                                                "ger_bochum_11@sa.nsdai.org",
                                                                "ger_bochum_16@sa.nsdai.org",
                                                                "ger_bochum_18@sa.nsdai.org",
                                                                "ger_bochum_26@sa.nsdai.org",
                                                                "ger_bochum_31@sa.nsdai.org",
                                                                "ger_bochum_32@sa.nsdai.org",
                                                                "ger_bochum_33@sa.nsdai.org",
                                                                "ger_bochum_35@sa.nsdai.org",
                                                                "ger_bochum_36@sa.nsdai.org",
                                                                "ger_bochum_38@sa.nsdai.org",
                                                                "ger_bochum_39@sa.nsdai.org",
                                                                "ger_bochum_40@sa.nsdai.org",
                                                                "ger_bochum_41@sa.nsdai.org",
                                                                "ger_bochum_42@sa.nsdai.org",
                                                                "ger_bochum_47@sa.nsdai.org",
                                                                "ger_bochum_51@sa.nsdai.org",
                                                                "ger_bochum_52@sa.nsdai.org",
                                                                "ger_bochum_53@sa.nsdai.org",
                                                                "ger_bochum_55@sa.nsdai.org",
                                                                "ger_bochum_58@sa.nsdai.org",
                                                                "ger_bochum_59@sa.nsdai.org",
                                                                "ger_bochum_61@sa.nsdai.org",
                                                                "ger_bochum_62@sa.nsdai.org",
                                                                "ger_bochum_66@sa.nsdai.org",
                                                                "ger_bochum_70@sa.nsdai.org",
                                                                "ger_bochum_74@sa.nsdai.org",
                                                                "ger_bochum_76@sa.nsdai.org",
                                                                "ger_bochum_77@sa.nsdai.org",
                                                                "ger_bochum_80@sa.nsdai.org",
                                                                "hoff-mar@web.de",
                                                                "Jasmin.Duesterloh@ruhr-uni-bochum.de",
                                                                "jessicanorton@sa.nsdai.org",
                                                                "Jiajie.chen@ruhr-uni-bochum.de",
                                                                "jinyeonjin@sa.nsdai.org",
                                                                "Johanna.Spanbroek@rub.de",
                                                                "kaylamakai@sa.nsdai.org",
                                                                "kokkeying@sa.nsdai.org",
                                                                "Lorena.Wolf@rub.de",
                                                                "marytarakey@sa.nsdai.org",
                                                                "minority25@sa.nsdai.org",
                                                                "nsd_iana@sa.nsdai.org",
                                                                "nsd_luiza@sa.nsdai.org",
                                                                "nsd_oona@sa.nsdai.org",
                                                                "ohkusanoriko@sa.nsdai.org",
                                                                "pia.heyn@rub.de",
                                                                "sarah.kessener@rub.de",
                                                                "sinekaterina@sa.nsdai.org",
                                                                "tanweiwen@sa.nsdai.org",
                                                                "tarantellishaun@sa.nsdai.org",
                                                                "teresachien@sa.nsdai.org",
                                                                "thilinhnguyen@sa.nsdai.org",
                                                                "thuongpham@sa.nsdai.org",
                                                                "tianruijia@sa.nsdai.org",
                                                                "wellingtoncordelia@sa.nsdai.org",
                                                                "yangcharis@sa.nsdai.org",
                                                                "yanglin@sa.nsdai.org",
                                                                "yulyanatyo@sa.nsdai.org",
                                                                "yuriykim@sa.nsdai.org", ],
                                      question__subcategory_code__name__in=["Reading Word", 'Reading Sentence',
                                                                            'Reading Paragraph'])

print(ss)

for idx, obj in enumerate(list(ss)[::-1]):
    filex = obj.audio_file.path
    print("Processing.. ", idx)
    # if file is a .txt file
    # check if file exists
    filepath = filex.replace("/home/audio_annotation/media/speaker/audio/", "")
    file = filepath.split("/")[-1]
    folderpath = filex.replace("/home/audio_annotation/media/speaker/audio/", "")
    folder = folderpath.split("/")[0]
    print(file, "-", folder)
    # print(idx, folder)

    print("Processing.. ", idx)
    # if file is a .txt file
    # check if file exists
    print("checking-" + "kim/" + folder + "__" + file + '.json')
    if os.path.isfile("kim/" + folder + "__" + file + '.json'):
        print("kim/" + file + '.json' + '  exists')
        continue
    if file.endswith(".mp3"):
        # open file
        fullpath = "media/speaker/audio/" + folder + "/" + file
        print("Reading: " + fullpath)

        res = ClovaSpeechClient().req_upload(file=fullpath, completion='sync', callback=None, userdata=None,
                                             forbiddens=None, boostings=None,
                                             wordAlignment=True, fullText=True, diarization=None)
        if res.status_code == 200:
            if res.json().get('segments'):
                # dump to file
                with open("kim/" + folder + "__" + file + '.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(res.json(), ensure_ascii=False, indent=4))
                    print('success')

                    continue
            else:
                with open("kim/" + folder + "__" + file + '.json', 'w', encoding='utf-8') as f:
                    f.write(
                        '{"result": "NO_SEGMENT", "note": "No segment found, logged by Sushant. I believe the audio is empty."}')
                    print('success')
                print('error')
                continue

# venv/bin/python manage.py  shell
# exec(open("rough_sushant/CallClovaSTTForSingleUser_ForKim.py").read())