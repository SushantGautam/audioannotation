import json

from celery import shared_task

from speaker.clovastt import ClovaSpeechClient
from speaker.models import ExamSetSubmission, SpeakerSubmission


@shared_task
def run_STTClova(exam_set_id):
    print('STTClova task started')
    failed = False

    ess = ExamSetSubmission.objects.get(pk=exam_set_id)
    ess.set_tts_status('STC')  #
    speakerSub = SpeakerSubmission.objects.filter(speaker_id=ess.speaker.id, exam_set_id=ess.exam_set_id)
    last = speakerSub.last()
    for sub in speakerSub:
        print('here')
        if sub.status in ['SS', 'SP', 'SC']:    # Skip item if already completed or processing
            continue

        sID = sub.id
        pathToSave = 'media/audio-splits/' + str(sID) + "/"
        # sub = Submissions.objects.get(id=sID)
        sub.set_tts_status('SP')  # Processing by STT Queue
        if ess.status == 'INS':
            ess.set_tts_status('STI')  # Stt Initiate for exam set

        stt_predictions_annotations = []


        # sub.set_tts_status(3)  # Calling STT API

        res = ClovaSpeechClient().req_upload(file=sub.audio_file.path, completion='sync')
        sub.set_tts_status('SS')    # STT submission for speakerSubmissionAudio
        if res.status_code == 200:
            sub.set_tts_status('SP')    # STT Processing for speakerSubmissionAudio
            if res.json().get('segments'):
                print(res.json().get('segments'))
                for idx, eachDuration in enumerate(res.json()['segments']):
                    stt_predictions_annotations.append({
                        "start": eachDuration['start'] / 1000,
                        "end": eachDuration['end'] / 1000,
                        "id": "splitter_" + str(idx),
                        "data": {
                            "text": [
                                eachDuration['text']
                            ],
                            "labels": [
                                "voice"
                            ]
                        },
                    })
            sub.stt_data = {"stt_predictions_annotations": stt_predictions_annotations}  # set stt data in database
            sub.set_tts_status('SC')    # STT completed for speakerSubmissionAudio
        else:
            sub.set_tts_status('SF')    # if issue, set STT failed
            failed = True
        # sub.set_tts_status(4)  # STT Output Received & Processing
        sub.save()

        # if there are no saved annotations just set predicted annotations as annotations

        # If all speaker submission successfully submitted, change status in exam status
        if sub.pk == last.pk and not failed:
          ess.set_tts_status('STC')  #
    return "TaskID:" + str('sID') + " is splitted by NAVER SPEECH API to " + \
           str(len('stt_predictions_annotations')) + " parts."