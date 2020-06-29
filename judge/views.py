import json
from os import path
from ruamel import yaml

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.conf import settings

from .models import Problem, Submission, TestPoint


def load_yaml(filename):
    return yaml.load(
        open(path.join(settings.BASE_DIR, 'judge', filename)),
        Loader=yaml.Loader
    )


def index(request):
    if 'kw' in request.GET and request.GET['kw'].startswith('#'):
        return HttpResponseRedirect(reverse('problem', args=(request.GET['kw'].lstrip('#'),)))
    return render(request, 'pioj/index.html',
                  {'problems': Problem.objects.filter(title__icontains=request.GET['kw']) if 'kw' in request.GET else Problem.objects.all()})


def robots_txt(request):
    return HttpResponse('User-agent: *\nDisallow: /submission/\n',
                        'text/plain')


def problem_detail(request, problem_id):
    return render(request, 'pioj/problem.html',
                  {'problem': get_object_or_404(Problem, pk=problem_id)})


@login_required
def submit(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == 'POST':
        submission = Submission(
            user=request.user, problem=problem, source=request.POST['source'],
            processor=json.dumps({
                k: request.POST[k]
                for k in request.POST
                if k in ['processor', 'version', 'language', 'options']
            }), score=-1
        )
        submission.save()
        TestPoint.objects.bulk_create(
            TestPoint(submission=submission)
            for i in submission.problem.testcase_set.all()
        )
        # for i in submission.problem.testcase_set.all():
        #     TestPoint(submission=submission).save()
        submission.judge()
        return HttpResponseRedirect(reverse('submission',
                                            args=(submission.pk,)))
    return render(
        request,
        'pioj/submit.html',
        {
            'problem': problem,
            'last_submission': (
                get_object_or_404(Submission,
                                  pk=request.GET['last'], user=request.user)
                if 'last' in request.GET
                else Submission.objects.filter(
                    problem=problem, user=request.user
                ).last()),
            'processors': load_yaml('processors.yaml')
        }
    )


def submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    return render(request, 'pioj/submission.html', {'submission': submission})


def submission_json(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    return JsonResponse({
        'score': submission.score,
        'error': submission.error,
        'test_points': [
            {
                'status': test_point.status,
                'duration': test_point.duration.total_seconds(),
                'stdout': test_point.stdout,
                'stderr': test_point.stderr,
            } for test_point in submission.testpoint_set.all()
        ]
    })
