from operator import itemgetter
from fuzzywuzzy import fuzz
from .models import Subject, School, Academy

EXCLUDE_FIELDS = ('pk', 'total_score')


def get_possible_universities():
    subjects = Subject.objects.all()
    possible = [{
        'pk': s.pk,
        'subject': s.name,
        'faculty': s.faculty.name,
        'faculty_abbreviation': s.faculty.abbreviation or "",
        'educationplace': s.faculty.university.name,
        'city': s.faculty.university.city.name,
        'total_score': 0
    } for s in subjects]

    return possible


def get_possible_schools():
    schools = School.objects.all()
    possible = [
        {'pk': s.pk,
         'educationplace': s.name,
         'city': s.city.name,
         'total_score': 0} for s in schools]

    return possible


def get_possible_academies():
    academies = Academy.objects.all()
    possible = [
        {'pk': a.pk,
         'educationplace': a.name,
         'city': a.city.name,
         'total_score': 0} for a in academies]

    return possible


def fuzzy_search_education_place(words):
    universities = get_possible_universities()
    schools = get_possible_schools()
    academies = get_possible_academies()

    everything = universities + schools + academies

    for word in words:
        for obj in everything:
            s = 0
            for field in obj:
                if field in EXCLUDE_FIELDS:
                    continue
                s += fuzz.ratio(word.lower(), obj[field].lower())

            obj['total_score'] += s

    flatten = sorted(everything, key=itemgetter('total_score'), reverse=True)

    return flatten[:5]
