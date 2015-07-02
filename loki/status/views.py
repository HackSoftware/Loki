from datetime import datetime

from django.http import HttpResponse

from education.models import Lecture, CheckIn


def get_group_times(lectures):
    courses = [lecture.course for lecture in lectures]
    courses = set(courses)
    cas = [course.courseassignment_set.all() for course in courses]
    group_times = []
    for cas_set in cas:
        for ca in cas_set:
            group_times.append(ca.group_time)
    group_times = list(set(group_times))
    return group_times

def check_ins_sanity_check(request):
    time = str(datetime.now().time())
    date = str(datetime.now().date())
    first_period = "13:30:00" <= time <= "14:30:00"
    second_period = "19:30:00" <= time <= "21:30:00"

    if first_period and second_period:
        today_lectures = Lecture.objects.filter(date=date)
        if today_lectures.count():
            group_times = get_group_times(today_lectures)
            if 1 in group_times and 2 in group_times:
                if first_period and CheckIn.objects.filter(date=date).count() < 10:
                    return HttpResponse(status=400)
                elif second_period and CheckIn.objects.filter(date=date).count() < 20:
                    return HttpResponse(status=400)
                else:
                    return HttpResponse(status=200)
            elif 1 in group_times and not (2 in group_times):
                if first_period and CheckIn.objects.filter(date=date).count() < 10:
                    return HttpResponse(status=400)
                else:
                    return HttpResponse(status=200)
            elif not (1 in group_times) and 2 in group_times:
                if second_period and CheckIn.objects.filter(date=date).count() < 10:
                    return HttpResponse(status=400)
                else:
                    return HttpResponse(status=200)
            else:
                return HttpResponse(status=200)
        else:
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=200)
