from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TeamMembership


@receiver(post_save, sender=TeamMembership)
def set_looking_for_team_to_false(sender, instance, created, **kwargs):
    if created:
        """
        We have unique_together = ('competitor', 'season')
        so the query will return one object or None.
        """
        season_competitor_info = instance.competitor.seasoncompetitorinfo_set.first()
        if season_competitor_info:
            season_competitor_info.looking_for_team = False
            season_competitor_info.save()
