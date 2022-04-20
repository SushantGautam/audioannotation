import os
import pathlib
import random
import string

import constance
from pydub import AudioSegment, silence


def segmentaudio(sID, audiofile):
    song = AudioSegment.from_file(audiofile)
    sil = silence.split_on_silence(song,
                                   min_silence_len=constance.config.min_silence_len,
                                   silence_thresh=constance.config.silence_thresh,
                                   keep_silence=constance.config.keep_silence,
                                   seek_step=constance.config.seek_step)
    pathToSave = 'media/audio-splits/' + str(sID) + "/"
    pathlib.Path(pathToSave).mkdir(parents=True, exist_ok=True)
    for i in os.listdir(pathToSave): os.remove(pathToSave + i)

    for idx, val in enumerate(sil):
        val.export(pathToSave + str(idx) + "_" +
                   ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)  # random
                           )
                   + ".mp3", format="mp3")
    # update audio_segments extras
    from WebApp.models import Submissions
    paths = [pathToSave + i for i in os.listdir(pathToSave)]
    sub = Submissions.objects.get(id=sID)
    sub.extras['audio_segments'] = paths
    sub.save()
    return len(paths)

# segmentaudio(sID=1, audiofile="./../../media/question_audio/Recording.m4a")
