import factory

from faker import Factory
from base_app import models as base_app_models
from hack_fmi import models as hack_fmi_models
from education import models as education_models


faker = Factory.create()


class CompanyFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.Company

    name = factory.Sequence(lambda n: 'company {}'.format(n))
    logo_url = faker.url()
    logo = factory.django.ImageField(color='blue')
    jobs_link = faker.url()


class PartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.Partner

    company = factory.SubFactory(CompanyFactory)
    description = faker.text()
    facebook = faker.url()
    is_active = faker.boolean()
    money_spent = faker.random_int()
    ordering = faker.random_int()
    twitter = faker.url()
    website = faker.url()
    video_presentation = faker.url()


class GeneralPartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.GeneralPartner

    partner = factory.SubFactory(PartnerFactory)


class HostingPartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.HostingPartner

    partner = factory.SubFactory(PartnerFactory)


class CityFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.City

    name = factory.Sequence(lambda n: 'city {}'.format(n))


class EducationPlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.EducationPlace

    name = faker.name()
    city = factory.SubFactory(CityFactory)


class SchoolFactory(EducationPlaceFactory):
    class Meta:
        model = base_app_models.School


class AcademyFactory(EducationPlaceFactory):
    class Meta:
        model = base_app_models.Academy


class UniversityFactory(EducationPlaceFactory):
    class Meta:
        model = base_app_models.University


class FacultyFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.Faculty

    university = factory.SubFactory(UniversityFactory)
    name = faker.name()
    abbreviation = faker.random_letter()


class SubjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.Subject

    faculty = factory.SubFactory(FacultyFactory)
    name = faker.name()


class BaseUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.BaseUser

    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    password = faker.word()
    birth_place = factory.SubFactory(CityFactory)

    github_account = faker.url()
    linkedin_account = faker.url()
    twitter_account = faker.url()
    description = faker.text()

    studies_at = faker.text(max_nb_chars=100)
    works_at = faker.text(max_nb_chars=100)

    avatar = factory.django.ImageField(color='blue')
    full_image = factory.django.ImageField(color='blue')


class EducationInfoFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.EducationInfo

    user = factory.SubFactory(BaseUserFactory)
    place = factory.SubFactory(EducationPlaceFactory)

    start_date = faker.date_time()
    end_date = faker.date_time()
    created_at = faker.date_time()
    updated_at = faker.date_time()

    faculty = factory.SubFactory(FacultyFactory)
    subject = factory.SubFactory(SubjectFactory)


class BaseUserWithEducationInfo(BaseUserFactory):
    class Meta:
        exclude = ("city", "place")
    city = factory.SubFactory(CityFactory)
    place = EducationPlaceFactory(city=city)
    education_info = factory.RelatedFactory(EducationInfoFactory,
                                            'user', place=place)


class BaseUserRegisterTokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.BaseUserRegisterToken

    user = factory.SubFactory(BaseUserFactory)
    token = faker.word()


class BaseUserPasswordResetTokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.BaseUserPasswordResetToken

    user = factory.SubFactory(BaseUserFactory)
    token = faker.word()


class SkillFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Skill

    name = faker.name()


class StudentFactory(BaseUserFactory):
    class Meta:
        model = education_models.Student

    mac = faker.mac_address()
    phone = faker.text(max_nb_chars=20)
    skype = faker.text(max_nb_chars=20)


class CourseFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Course

    description = faker.text()
    git_repository = faker.word()
    image = factory.django.ImageField()
    name = faker.word()
    partner = factory.RelatedFactory(PartnerFactory)
    short_description = faker.word()
    show_on_index = faker.boolean(chance_of_getting_true=0)
    is_free = faker.boolean(chance_of_getting_true=100)

    application_until = faker.date_time()
    applications_url = faker.url()
    ask_for_favorite_partner = faker.boolean(chance_of_getting_true=0)
    ask_for_feedback = faker.boolean(chance_of_getting_true=0)
    end_time = faker.date_time()
    fb_group = faker.url()
    next_season_mail_list = faker.url()
    SEO_description = faker.word()
    SEO_title = faker.word()
    start_time = faker.date_time()
    url = factory.Sequence(lambda n: 'url {}'.format(n))
    video = faker.url()
    generate_certificates_until = faker.date()


class CourseAssignmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.CourseAssignment

    course = factory.SubFactory(CourseFactory)
    user = factory.SubFactory(StudentFactory)
    cv = faker.file_name(category=None, extension=None)
    favourite_partners = factory.RelatedFactory(PartnerFactory)
    group_time = int(faker.random_element(elements=('1', '2')))
    is_attending = faker.boolean()
    student_presence = faker.random_number(digits=1)
    is_online = faker.boolean()


class TeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Teacher

    mac = faker.mac_address()
    phone = faker.text(max_nb_chars=20)
    signature = factory.django.ImageField()
    teached_courses = factory.RelatedFactory(CourseFactory)


class StudentWithAssignmentFactory(StudentFactory):

    courses = factory.RelatedFactory(CourseAssignmentFactory)


class CompetitorFactory(BaseUserFactory):
    class Meta:
        model = hack_fmi_models.Competitor

    is_vegetarian = faker.boolean()
    known_skills = factory.RelatedFactory(SkillFactory)
    faculty_number = faker.random_number()
    shirt_size = faker.random_element(elements=('1', '2', '3', '4'))
    needs_work = faker.boolean()
    social_links = faker.text()
    registered = faker.boolean()


class SeasonFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Season

    name = faker.name()
    topic = faker.word()
    front_page = faker.paragraph()
    min_team_members_count = faker.random_number(digits=1)
    max_team_members_count = faker.random_number(digits=1)
    sign_up_deadline = faker.date()
    make_team_dead_line = faker.date()
    mentor_pick_start_date = faker.date()
    mentor_pick_end_date = faker.date()
    max_mentor_pick = faker.random_number(digits=1)
    is_active = faker.boolean()


class HackFmiPartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Partner

    name = faker.name()
    season = factory.RelatedFactory(SeasonFactory)


class RoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Room

    number = faker.random_number()
    season = factory.SubFactory(SeasonFactory)
    capacity = faker.random_number(digits=1)


class MentorFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Mentor

    name = faker.name()
    description = faker.text()
    picture = factory.django.ImageField()
    seasons = factory.RelatedFactory(SeasonFactory)
    from_company = factory.SubFactory(HackFmiPartnerFactory)
    order = faker.random_number()


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Team

    name = faker.name()
    mentors = factory.RelatedFactory(MentorFactory)
    technologies = factory.RelatedFactory(SkillFactory)
    idea_description = faker.text()
    repository = faker.url()
    season = factory.SubFactory(SeasonFactory)
    need_more_members = faker.boolean()
    room = factory.SubFactory(RoomFactory)
    picture = factory.django.ImageField()


class TeamMembershipFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.TeamMembership

    competitor = factory.SubFactory(CompetitorFactory)
    team = factory.SubFactory(TeamFactory)
    is_leader = faker.boolean()
    place = faker.random_number(digits=1)


class TeamWithCompetitor(TeamFactory):
    class Meta:
        exclude = ('competitor')

    competitor = factory.SubFactory(CompetitorFactory)
    members = factory.RelatedFactory(TeamMembershipFactory,
                                     'team',
                                     competitor=competitor)


class CertificateFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Certificate

    token = faker.word()
    assignment = factory.RelatedFactory(CourseAssignmentFactory)


class CheckInFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.CheckIn

    mac = factory.Sequence(lambda n: 'd0:00:ad:{0}:d8:e9'.format(n))
    student = factory.SubFactory(StudentFactory)
    date = faker.date()


class LectureFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Lecture

    course = factory.SubFactory(CourseFactory)
    date = faker.date_time()


class WorkingAtFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.WorkingAt

    student = factory.SubFactory(StudentFactory)
    company = factory.SubFactory(CompanyFactory)
    location = factory.SubFactory(CityFactory)
    course = factory.SubFactory(CourseFactory)
    came_working = faker.boolean(chance_of_getting_true=0)
    company_name = faker.company()
    start_date = faker.date_time()
    end_date = faker.date_time()
    title = faker.word()
    description = faker.text()


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Task

    course = factory.SubFactory(CourseFactory)
    description = factory.\
        Sequence(lambda n: 'https://github.com/zad{}/solution.py'.format(n))
    is_exam = faker.boolean(chance_of_getting_true=0)
    name = faker.text(max_nb_chars=128)
    week = faker.random_number(digits=1)
    gradable = faker.boolean(chance_of_getting_true=100)


class ProgrammingLanguageFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.ProgrammingLanguage

    name = faker.word()


class TestFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Test

    UNITTEST = 0

    TYPE_CHOICE = (
        (UNITTEST, 'unittest'),
    )

    task = factory.RelatedFactory(TaskFactory)
    language = factory.SubFactory(ProgrammingLanguageFactory)
    test_type = faker.\
        random_element(elements=(str(elem[0]) for elem in TYPE_CHOICE))
    extra_options = faker.file_name(category=None, extension='json')


class SourceCodeTestFactory(TestFactory):
    class Meta:
        model = education_models.SourceCodeTest

    code = faker.text()


class BinaryFileTestFactory(TestFactory):
    class Meta:
        model = education_models.BinaryFileTest

    file = faker.file_name(category=None, extension=None)


class SolutionFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Solution

    PENDING = 0
    RUNNING = 1
    OK = 2
    NOT_OK = 3
    SUBMITED = 4
    MISSING = 5
    SUBMITTED_WITHOUT_GRADING = 6

    STATUS_CHOICE = (
        (PENDING, 'pending'),
        (RUNNING, 'running'),
        (OK, 'ok'),
        (NOT_OK, 'not_ok'),
        (SUBMITED, 'submitted'),
        (MISSING, 'missing'),
        (SUBMITTED_WITHOUT_GRADING, 'submitted_without_grading'),
    )

    task = factory.SubFactory(TaskFactory)
    student = factory.SubFactory(StudentFactory)
    url = faker.url()
    code = faker.text()
    build_id = faker.random_number()
    check_status_location = faker.text(max_nb_chars=128)
    created_at = faker.date_time()
    test_output = faker.text()
    status = faker.\
        random_element(elements=(str(el[0]) for el in STATUS_CHOICE))
    return_code = faker.random_number()
    file = faker.file_name(category=None, extension=None)

