from django.contrib import admin

from .models import Problem, Example, TestCase, Submission, TestPoint


class ExampleInline(admin.TabularInline):
    model = Example
    extra = 3


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 5


class ProblemAdmin(admin.ModelAdmin):
    inlines = [ExampleInline, TestCaseInline]


class TestPointInline(admin.TabularInline):
    model = TestPoint
    extra = 0


class SubmissionAdmin(admin.ModelAdmin):
    inlines = [TestPointInline]


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submission, SubmissionAdmin)
