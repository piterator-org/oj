from django import test

from django.contrib.auth.models import User
from .models import Problem, Submission, TestCase


class ProblemModelTests(test.TestCase):

    def test_problem_str_equals_its_title(self):
        'str(problem) == problem.title'
        problem = Problem()
        self.assertEqual(str(problem), problem.title)


class SubmissionModelTests(test.TestCase):

    def test_source_crlf2lf(self):
        'Replace CRLF with LF'
        user = User()
        user.save()
        problem = Problem()
        problem.save()
        submission = Submission(user=user, problem=problem,
                                source='\r\n', score=0)
        submission.save()
        self.assertEqual(submission.source, '\n')


class TestCaseModelTests(test.TestCase):

    def test_io_crlf2lf(self):
        'Replace CRLF with LF'
        problem = Problem()
        problem.save()
        case = TestCase(problem=problem, input='\r\n', output='\r\n')
        case.save()
        self.assertEqual(case.input, '\n')
        self.assertEqual(case.output, '\n')
