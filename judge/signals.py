from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Submission, TestCase


@receiver(post_save, sender=Submission)
def source_crlf_to_lf(**kwargs):
    submission = kwargs["instance"]
    source = submission.source.replace('\r\n', '\n')
    if submission.source != source:
        submission.source = source
        submission.save()


@receiver(post_save, sender=TestCase)
def io_crlf_to_lf(**kwargs):
    case = kwargs["instance"]
    if '\r\n' in case.input or '\r\n' in case.output:
        case.input = case.input.replace('\r\n', '\n')
        case.output = case.output.replace('\r\n', '\n')
        case.save()
