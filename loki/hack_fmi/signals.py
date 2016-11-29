from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TeamMembership


@receiver(post_save, sender=TeamMembership)
def set_looking_for_team_to_false(sender, instance, **kwargs):
    sci_object = instance.competitor.seasoncompetitorinfo_set.first()
    sci_object.looking_for_team = False
    sci_object.save()
    import ipdb; ipdb.set_trace()
