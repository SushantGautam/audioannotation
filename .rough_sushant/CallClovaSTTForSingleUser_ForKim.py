from clovaStt import ClovaSpeechClient
import json

import os
# loop for all files in directory
for idx, file in enumerate(os.listdir("media/speaker/audio/nsd_luiza_sa.nsdai.org/")):
    print("Processing.. ", idx)
    # if file is a .txt file
    # check if file exists
    if os.path.isfile("kim/"+file + '.json'):
        print("kim/"+file + '.json'+ '  exists')
        continue
    if file.endswith(".mp3"):
        # open file
        fullpath = "media/speaker/audio/nsd_luiza_sa.nsdai.org/"+ file
        print("Reading: "+fullpath)

        res = ClovaSpeechClient().req_upload(file=fullpath, completion='sync')
        if res.status_code == 200:
            if res.json().get('segments'):
                # dump to file
                with open("kim/"+file + '.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(res.json(), ensure_ascii=False, indent=4))
                    print('success')

                    continue
            else:
                with open("kim/"+file + '.json', 'w', encoding='utf-8') as f:
                    f.write('{"result": "NO_SEGMENT", "note": "No segment found, logged by Sushant. I believe the audio is empty."}')
                    print('success')
                print('error')
                continue
        