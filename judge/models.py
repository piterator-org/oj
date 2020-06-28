from datetime import timedelta
import json
from threading import Thread

import dockerjudge
import dockerjudge.processor

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


from django.contrib.auth.models import User


class Problem(models.Model):
    title = models.CharField(_('title'), max_length=200)
    time_limit = models.DurationField(_('time limit'),
                                      default=timedelta(seconds=1))
    input_file = models.CharField(_('input file'), max_length=255, blank=True)
    output_file = models.CharField(_('output file'), max_length=255,
                                   blank=True)
    description = models.TextField(_('description'))
    input = models.TextField(_('input'))
    output = models.TextField(_('output'))

    class Meta:
        verbose_name = _('problem')
        verbose_name_plural = _('problems')

    def get_absolute_url(self):
        return reverse('problem', args=(self.pk,))

    def __str__(self):
        return self.title


class Example(models.Model):
    problem = models.ForeignKey(Problem, models.CASCADE,
                                verbose_name=_('problem'))
    input = models.TextField(_('input'), blank=True)
    output = models.TextField(_('output'), blank=True)

    class Meta:
        verbose_name = _('example')
        verbose_name_plural = _('examples')


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, models.CASCADE,
                                verbose_name=_('problem'))
    input = models.TextField(_('input'), blank=True)
    output = models.TextField(_('output'), blank=True)

    class Meta:
        verbose_name = _('test case')
        verbose_name_plural = _('test cases')


class Submission(models.Model):
    user = models.ForeignKey(User, models.CASCADE, verbose_name=_('user'))
    problem = models.ForeignKey(Problem, models.CASCADE,
                                verbose_name=_('problem'))
    time = models.DateTimeField(_('time'), auto_now_add=True)
    processor = models.TextField(_('processor'), default='{}')
    source = models.TextField(_('source'), blank=True)
    error = models.TextField(_('error'), blank=True)
    score = models.FloatField(_('score'))

    class Meta:
        verbose_name = _('submission')
        verbose_name_plural = _('submissions')

    def get_absolute_url(self):
        return reverse('submission', args=(self.pk,))

    def judge(self):

        def compiling_callback(code, error):
            self.error = error.decode()
            if code:
                for test_point in self.testpoint_set.all():
                    test_point.status = 'CE'
                    test_point.save()
                self.score = 0
                self.save()

        def judging_callback(status_pk, status, output, duration):
            testpoint = self.testpoint_set.all()[status_pk]
            testpoint.status = status.name
            testpoint.stdout = (output[0] or b'').decode()
            testpoint.stderr = (output[1] or b'').decode()
            testpoint.duration = timedelta(seconds=duration)
            testpoint.save()

        def threaded_judge(*args):
            res = dockerjudge.judge(*args)
            self.score = [r[0] for r in res[0]].count(
                dockerjudge.status.Status.AC
            ) * 100 / len(res[0])
            self.save()

        processor = json.loads(self.processor)
        Thread(
            target=threaded_judge,
            args=(
                next(
                    cls
                    for cls in dockerjudge.processor.Processor.__subclasses__()
                    if cls.__name__ == processor['processor']
                )(**{
                    k: processor[k]
                    for k in processor
                    if k in ['version', 'language', 'options']
                }),
                self.source.encode(),
                [
                    (case.input.encode(), case.output.encode())
                    for case in self.problem.testcase_set.all()
                ],
                {
                    'limit': {
                        'time': self.problem.time_limit.total_seconds()
                    },
                    'iofilaname': {
                        'in': self.problem.input_file,
                        'out': self.problem.output_file
                    },
                    'callback': {
                        'compile': compiling_callback,
                        'judge': judging_callback
                    }
                }
            )
        ).start()


class TestPoint(models.Model):
    submission = models.ForeignKey(Submission, models.CASCADE,
                                   verbose_name=_('submission'))
    status = models.CharField(
        _('status'),
        max_length=3,
        choices=[
            (i, dockerjudge.status.Status[i].value)
            for i in dockerjudge.status.Status.__members__
        ],
        blank=True
    )
    stdout = models.TextField(_('standard output'), blank=True)
    stderr = models.TextField(_('standard error'), blank=True)
    duration = models.DurationField(_('duration'), default=timedelta())

    class Meta:
        verbose_name = _('test point')
        verbose_name_plural = _('test points')
