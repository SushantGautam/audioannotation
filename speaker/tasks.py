from celery import shared_task


@shared_task(bind=True)
def run_STTClova(self, exam_set):
    print('STTClova task started')
    # pathToSave = 'media/audio-splits/' + str(sID) + "/"
    # from WebApp.models import Submissions

    # sub = Submissions.objects.get(id=sID)
    # sub.set_tts_status(2)  # Processing by STT Queue

    # stt_predictions_annotations = []
    

    # sub.set_tts_status(3)  # Calling STT API

    # res = ClovaSpeechClient().req_upload(file=sub.sound_file.path, completion='sync')
    # if res.status_code == 200:
    #     if res.json().get('segments'):
    #         for idx, eachDuration in enumerate(res.json()['segments']):
    #             stt_predictions_annotations.append({
    #                 "value": {
    #                     "start": eachDuration['start'] / 1000,
    #                     "end": eachDuration['end'] / 1000,
    #                     "labels": [
    #                         "voice"
    #                     ]
    #                 },
    #                 "id": "splitter_" + str(idx),
    #                 "from_name": "labels",
    #                 "to_name": "audio",
    #                 "type": "labels"
    #             })
    #             stt_predictions_annotations.append({
    #                 "value": {
    #                     "start": eachDuration['start'] / 1000,
    #                     "end": eachDuration['end'] / 1000,
    #                     "text": [
    #                         eachDuration['text']
    #                     ]
    #                 },
    #                 "id": "splitter_" + str(idx),
    #                 "from_name": "transcription",
    #                 "to_name": "audio",
    #                 "type": "textarea"
    #             })
    # sub.set_tts_status(4)  # STT Output Received & Processing
    # sub.no_post_save = True
    # sub.save()
    # # if there are no saved annotations just set predicted annotations as annotations
    # if not sub.extras.get('annotations'):
    #     sub.extras['annotations'] = json.dumps(stt_predictions_annotations)
    # sub.extras['stt_predictions_annotations'] = stt_predictions_annotations
    # sub.save()
    # sub.set_tts_status(5)  # STT TaskCompleted | AnnotationSaved
    # return "TaskID:" + str(sID) + " is splitted by NAVER SPEECH API to " + \
    #        str(len(stt_predictions_annotations)) + " parts."