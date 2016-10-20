from django.db import models


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
    def active(self):
        return [interview for interview in self.all() if interview.active_date()]
