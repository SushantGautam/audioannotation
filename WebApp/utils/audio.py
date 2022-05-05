import json
import tempfile

from celery import shared_task
from django.core.files.temp import NamedTemporaryFile
from pydub import AudioSegment

from clovaStt import ClovaSpeechClient


@shared_task
def segmentaudio(sID):
    # song = AudioSegment.from_file(audiofile)
    # sil = silence.split_on_silence(song,
    #                                min_silence_len=constance.config.min_silence_len,
    #                                silence_thresh=constance.config.silence_thresh,
    #                                keep_silence=constance.config.keep_silence,
    #                                seek_step=constance.config.seek_step)
    pathToSave = 'media/audio-splits/' + str(sID) + "/"
    # pathlib.Path(pathToSave).mkdir(parents=True, exist_ok=True)
    # for i in os.listdir(pathToSave): os.remove(pathToSave + i)
    #
    # for idx, val in enumerate(sil):
    #     val.export(pathToSave + str(idx) + "_" +
    #                ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)  # random
    #                        )
    #                + ".mp3", format="mp3")
    # # update audio_segments extras
    from WebApp.models import Submissions
    # paths = [pathToSave + i for i in os.listdir(pathToSave)]
    sub = Submissions.objects.get(id=sID)
    sub.set_tts_status(2)  # Processing by STT Queue

    # sub.extras['audio_segments'] = paths
    #
    # # get start and end of the audio segment
    # split_data = []
    # nonsilent_ms = silence.detect_nonsilent(song,
    #                                         min_silence_len=constance.config.min_silence_len,
    #                                         silence_thresh=constance.config.silence_thresh,
    #                                         seek_step=constance.config.seek_step)
    # for idx, eachDuration in enumerate(nonsilent_ms):
    #     split_data.append({"start": (eachDuration[0] - constance.config.keep_silence) / 1000,
    #                        "end": (eachDuration[1] + constance.config.keep_silence) / 1000})
    # sub.extras['split_data'] = split_data
    #
    stt_predictions_annotations = []
    # for idx, eachDuration in enumerate(split_data):
    #     stt_predictions_annotations.append({
    #         "value": {
    #             "start": eachDuration['start'],
    #             "end": eachDuration['end'],
    #             "labels": [
    #                 "voice"
    #             ]
    #         },
    #         "id": "splitter_" + str(idx),
    #         "from_name": "labels",
    #         "to_name": "audio",
    #         "type": "labels"
    #     })
    #     stt_predictions_annotations.append({
    #         "value": {
    #             "start": eachDuration['start'],
    #             "end": eachDuration['end'],
    #             "text": [
    #                 str(idx) + " To be Annotated by STT. This is from splitter. By Sushant."
    #             ]
    #         },
    #         "id": "splitter_" + str(idx),
    #         "from_name": "transcription",
    #         "to_name": "audio",
    #         "type": "textarea"
    #     })

    sub.set_tts_status(3)  # Calling STT API

    # TODO: https://pythonbasics.org/convert-mp3-to-wav/
    res= None
    with tempfile.TemporaryFile(delete=False) as fp:
        sound = AudioSegment.from_wav(sub.sound_file.path)
        sound.export(fp, format="mp3")
        res = ClovaSpeechClient().req_upload(file=fp.name, completion='sync')

    if res and res.status_code == 200:
        if res.json().get('segments'):
            for idx, eachDuration in enumerate(res.json()['segments']):
                stt_predictions_annotations.append({
                    "value": {
                        "start": eachDuration['start'] / 1000,
                        "end": eachDuration['end'] / 1000,
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
                        "start": eachDuration['start'] / 1000,
                        "end": eachDuration['end'] / 1000,
                        "text": [
                            eachDuration['text']
                        ]
                    },
                    "id": "splitter_" + str(idx),
                    "from_name": "transcription",
                    "to_name": "audio",
                    "type": "textarea"
                })
    sub.set_tts_status(4)  # STT Output Received & Processing
    sub.no_post_save = True
    sub.save()
    # if there are no saved annotations just set predicted annotations as annotations
    if not sub.extras.get('annotations'):
        sub.extras['annotations'] = json.dumps(stt_predictions_annotations)
    sub.extras['stt_predictions_annotations'] = stt_predictions_annotations
    sub.save()
    sub.set_tts_status(5)  # STT TaskCompleted | AnnotationSaved
    return "TaskID:" + str(sID) + " is splitted by NAVER SPEECH API to " + \
           str(len(stt_predictions_annotations)) + " parts."
    # return len(stt_predictions_annotations

# segmentaudio(sID=1, audiofile="./../../media/question_audio/Recording.m4a")
