import re
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from github import Github

from education.models import Course, Task


class Command(BaseCommand):
    args = '<course_id>'
    help = '''
        Generates tasks from <course_id>'s github repository.
    '''

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        courses = Course.objects.filter(start_time__lt=now, end_time__gt=now)
        for course in courses:
            course_github_url = course.git_repository

            github_parameters = get_user_and_repo_names(course_github_url)
            api_repo = get_api_repo(github_parameters)
            api_repo_tree = api_repo.get_git_tree(sha='master', recursive=True)

            # filters tree elements by depth of 2, when base is considered 0
            blob_tree_elements = filter(
                lambda x:
                    'README.md' in x.path
                    and x.path.count('/') > 1 and x.type == 'blob', api_repo_tree.tree
            )

            for element in blob_tree_elements:
                create_db_task(course, element)


def get_api_repo(github_parameters):
    github_client = Github(settings.GITHUB_OATH_TOKEN)
    return github_client.get_user(github_parameters['user']).get_repo(github_parameters['repo_name'])


def get_user_and_repo_names(github_url):
    # Ex: https://github.com/syndbg/HackBulgaria/tree/master/Core-Java-1
    # Becomes  [u'https:', u'', u'github.com', u'syndbg', u'HackBulgaria', u'tree', u'master', u'Core-Java-1']
    # Only 4th and 5th elements are relevant
    github_url_split = github_url.split('/')[3:]

    result = {
        'user': github_url_split[0],
        'repo_name': github_url_split[1]
    } if len(github_url_split) >= 2 else {'user': github_url_split[0]}

    return result


def get_dir_and_task_names(path):
    regex = re.compile(r'(week[0-9]+|exam[1-9][0-9]*)(/.+?/)')
    result = regex.search(path).groups()
    return {'dir': result[0], 'raw_task': result[1]}


def get_formatted_task_url(raw_task_url, dir_task_names):
    raw_task_url = raw_task_url if raw_task_url[-1] != '/' else raw_task_url[:-1]
    dir_name = dir_task_names['dir']
    return '{}/tree/master/{}{}'.format(raw_task_url, dir_name, dir_task_names['raw_task'])


def get_formatted_task_name(raw_task_name):
    raw_task_name = raw_task_name[1:-1].replace('-', ' ').split(' ')
    output = '<{}>'.format(raw_task_name[0])
    for i in range(1, len(raw_task_name)):
        output += ' {}'.format(raw_task_name[i])
    return output


def get_formatted_dir_name(dir_name):
    # Splits dir name by digit and capitalizes dir name
    # Ex week6 = Week 6, exam3 = Exam 3
    regex_output = re.findall(r'(\w+?)(\d+)', dir_name)[0]
    return regex_output[1]


def create_db_task(course, tree_element):
    try:
        dir_task_names = get_dir_and_task_names(tree_element.path)
    except Exception as e:
        print(e)
        return

    task_github_url = get_formatted_task_url(course.git_repository, dir_task_names)
    task_name = get_formatted_task_name(dir_task_names['raw_task'])
    week = get_formatted_dir_name(dir_task_names['dir'])

    obj, created = Task.objects.get_or_create(
        name=task_name,
        description=task_github_url,
        course=course,
        week=week,
    )
    if created:
        print('Created task {} - {}'.format(task_name, task_github_url))
