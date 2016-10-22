from django.db import models
from .query import InterviewQuerySet


class InterviewerManager(models.Manager):
    def create_from_baseuser(self, baseuser):
        if baseuser.get_interviewer() is not False:
            return None

        interviewer = self.model(baseuser_ptr_id=baseuser.id)

        interviewer.__dict__.update(baseuser.__dict__)
        interviewer.is_staff = True

        interviewer.save()

        return interviewer


class InterviewManager(models.Manager):
    def get_queryset(self):
        return InterviewQuerySet(self.model, using=self._db)

    def get_active(self, user):
        return [interview for interview in self.get_queryset().confirmed_interviews_on(user)
                if interview.active_date()]
