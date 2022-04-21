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

    # get start and end of the audio segment
    split_data = []
    nonsilent_ms = silence.detect_nonsilent(song,
                                            min_silence_len=constance.config.min_silence_len,
                                            silence_thresh=constance.config.silence_thresh,
                                            seek_step=constance.config.seek_step)
    for idx, eachDuration in enumerate(nonsilent_ms):
        split_data.append({"start": (eachDuration[0] - constance.config.keep_silence) / 1000,
                           "end": (eachDuration[1] + -constance.config.keep_silence) / 1000})
    sub.extras['split_data'] = split_data

    stt_predictions_annotations = []
    for idx, eachDuration in enumerate(split_data):
        stt_predictions_annotations.append({
            "value": {
                "start": eachDuration['start'],
                "end": eachDuration['end'],
                "labels": [
                    "voice"
                ]
            },
            "id": "splitter_" + str(idx),
            "from_name": "labels",
            "to_name": "audio",
            "type": "labels"
        })
        stt_predictions_annotations.append({
            "value": {
                "start": eachDuration['start'],
                "end": eachDuration['end'],
                "text": [
                    str(idx) + " To be Annotated by STT. This is from splitter. By Sushant."
                ]
            },
            "id": "splitter_" + str(idx),
            "from_name": "transcription",
            "to_name": "audio",
            "type": "textarea"
        })
    sub.extras['stt_predictions_annotations'] = stt_predictions_annotations
    sub.save()

    return len(paths)

# segmentaudio(sID=1, audiofile="./../../media/question_audio/Recording.m4a")
