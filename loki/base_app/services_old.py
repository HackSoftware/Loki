from fuzzywuzzy import fuzz
from .models import Subject


def fuzzy_search_education_place(words):
    subjects = Subject.objects.all()
    possible = [{
        'id': s.pk,
        'subject': s.name.lower(),
        'faculty': s.faculty.name.lower(),
        'faculty_abbreviation': s.faculty.abbreviation.lower() or "",
        'uni': s.faculty.uni.name.lower(),
        'city': s.faculty.uni.city.name.lower()
    } for s in subjects]

    final_result = []

    # scores = [
    #  {'word': word,
    #   'score': [
    #       { 'total_score': 5834,
    #         'pk': 1
    #       }
    #   ]
    # ]

    combined_scores = {}

    for word in words:
        scores = []

        for p in possible:
            score = {
                key: (fuzz.ratio(word, p[key]), p[key]) for key in p if key != 'id'
            }
            score['id'] = p['id']

            scores.append(score)

        total_scores = []

        for score in scores:
            data = {}
            s = 0

            for key in score:
                if key != 'id':
                    s += score[key][0]

            data['total_score'] = s
            data['id'] = score['id']

            total_scores.append(data)

        for total in total_scores:
            if total['id'] not in combined_scores:
                combined_scores[total['id']] = 0

            combined_scores[total['id']] += total['total_score']

        final_result.append({
            'word': word,
            'scores': total_scores
        })

    d = {}

    for pk in combined_scores:
        subject = Subject.objects.get(pk=pk)
        d[subject.represent()] = combined_scores[pk]

    return d
