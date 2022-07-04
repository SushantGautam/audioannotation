import json

import requests
from joblib import Memory

memory = Memory(".cache_cloavaStt_req_upload")


class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/2554/6c446f5fbf6ae9dbef029931c42107bb6e894edfddfcd650e470cd374e50bd5f'
    # Clova Speech secret key
    secret = 'be51a2c3bf6949de8796b0dea451cc11'

    def req_url(self, url, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                wordAlignment=True, fullText=True, diarization=None):
        request_body = {
            'url': url,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/url',
                             data=json.dumps(request_body).encode('UTF-8'))

    def req_object_storage(self, data_key, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                           wordAlignment=True, fullText=True, diarization=None):
        request_body = {
            'dataKey': data_key,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/object-storage',
                             data=json.dumps(request_body).encode('UTF-8'))

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None):
        @memory.cache
        def _req_upload(file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                        wordAlignment=True, fullText=True, diarization=None):
            request_body = {
                'language': 'ko-KR',
                'completion': completion,
                'callback': callback,
                'userdata': userdata,
                'wordAlignment': wordAlignment,
                'fullText': fullText,
                'forbiddens': forbiddens,
                'boostings': boostings,
                'diarization': diarization,
            }
            headers = {
                'Accept': 'application/json;UTF-8',
                'X-CLOVASPEECH-API-KEY': self.secret
            }
            print(json.dumps(request_body, ensure_ascii=False).encode('UTF-8'))
            files = {
                'media': open(file, 'rb'),
                'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
            }
            response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
            return response

        return _req_upload(file, completion, callback, userdata, forbiddens, boostings, wordAlignment, fullText,
                           diarization)


if __name__ == '__main__':
    # res = ClovaSpeechClient().req_url(url='http://example.com/media.mp3', completion='sync')
    # res = ClovaSpeechClient().req_object_storage(data_key='data/media.mp3', completion='sync')
    res = ClovaSpeechClient().req_upload(file='/data/media.mp3', completion='sync')
    print(res.text)
