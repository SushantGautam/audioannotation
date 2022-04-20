from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer


class SoundAnnotation_WebSocketConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            print(f"Received text={text_data}")
            self.send(text_data="Hello from SoundAnnotation WebSocketConsumer!")
        if bytes_data:
            print(f"Received bytes={bytes_data}")
            self.send(bytes_data=b"Hello from SoundAnnotation WebSocketConsumer!")

    def disconnect(self, message):
        # Called when disconnected
        pass