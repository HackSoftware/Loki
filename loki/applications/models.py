from django.db import models

from education.models import Course
from base_app.models import BaseUser

# start and end date for appling to course
class ApplicationInfo(models.Model):
   start_date = models.DateTimeField()
   end_date = models.DateTimeField()
   course = models.OneToOneField(Course)

   def __str__():
       return "from {0} to {1} appling to {2}".format(self.start_date,
                                                      self.end_date,
                                                      self.course)


class ApplicationProblem(models.Model):
   application_info = models.ManyToManyField(ApplicationInfo)
   name = models.CharField(max_length=30)
   description = RichTextField(blank=False)
   description_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Application(models.Model):
    application_info = models.ForeignKey(ApplicationInfo)
    user = models.ForeignKey(BaseUser)

    phone = models.CharField(null=True, blank=True, max_length=20)
    skype = models.CharField(null=True, blank=True, max_length=30)
    works_at = models.CharField(null=True, blank=True, max_length=110)
    studies_at = models.CharField(blank=True, null=True, max_length=110)


class ApplicationProblemSolution(models.Model):
   application = models.ForeignKey(Application)
   problem = models.ForeignKey(ApplicationProblem)
   solution_url = models.URLField(null=True, blank=True)
