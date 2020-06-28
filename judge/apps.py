from django.apps import AppConfig


class JudgeConfig(AppConfig):
    name = 'judge'

    def ready(self):
        from .signals import source_crlf_to_lf, io_crlf_to_lf
