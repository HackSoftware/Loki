from django.core.management import call_command

from test_plus.test import TestCase

from ..helper import get_date_with_timedelta
from ..models import BlackListToken

from faker import Factory

faker = Factory.create()


class TestJWTCleanCommand(TestCase):

    def test_clean_old_jwt_token_commands(self):
        """
        The command deletes all the BlackListTokens that are older than one week.
        get_date_with_timedelta(-7) gives us a date that is older with 7 days from now
        """

        older_than_week_date = get_date_with_timedelta(days=-7)
        BlackListToken.objects.create(token=faker.text(),
                                      created_at=older_than_week_date)
        self.assertTrue(BlackListToken.objects.exists())
        call_command('clean_old_jwt_tokens')
        self.assertFalse(BlackListToken.objects.exists())

    def test_tokens_that_are_not_expired_yet_are_not_deleted(self):
        """
        The command should not delete the BlackListTokens that are not expored yet.
        """

        older_than_week_date = get_date_with_timedelta(days=-7)
        BlackListToken.objects.create(token=faker.text(),
                                      created_at=older_than_week_date)
        within_week_date = get_date_with_timedelta(days=-2)
        BlackListToken.objects.create(token=faker.text(),
                                      created_at=within_week_date)
        self.assertEqual(BlackListToken.objects.count(), 2)
        call_command('clean_old_jwt_tokens')
        self.assertEqual(BlackListToken.objects.count(), 1)
        self.assertEqual(BlackListToken.objects.first().created_at, within_week_date)
