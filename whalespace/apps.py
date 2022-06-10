from django.apps import AppConfig

class WhaleSpaceConfig(AppConfig):
    name = 'whalespace'

    def ready(self):
        import whalespace.signals