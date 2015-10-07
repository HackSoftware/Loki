from django.shortcuts import render, get_object_or_404
from .models import SuccessVideo, SuccessStoryPerson, Snippet, CourseDescription

from education.models import WorkingAt, Student
from base_app.models import Partner


def index(request):
    successors = SuccessStoryPerson.objects.order_by('?')[:6]
    partners = Partner.objects.all().order_by('?')
    videos = SuccessVideo.objects.all()[:4]

    success = WorkingAt.objects.filter(came_working=False)
    success_students = map(lambda x: x.student, success)
    success_students_count = len(set(success_students))

    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, "website/index.html", locals())


def about(request):
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}
    return render(request, "website/about.html", locals())


def courses(request):
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}
    return render(request, "website/courses.html", locals())


def partners(request):
    partners = Partner.objects.all().order_by('?')
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, "website/partners.html", locals())

def course_details(request, course_url):
    # cd refers to course_description
    cd = get_object_or_404(CourseDescription, url=course_url)
    
    return render(request, "website/course_details.html", locals())
