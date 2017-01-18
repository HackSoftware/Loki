from django.core.management.base import BaseCommand
from loki.education.models import Solution
from loki.education.tasks import submit_solution


class Command(BaseCommand):
    help = """
        Regrades all pending runs, in case there are stale ones
    """

    def handle(self, *args, **options):
        pendings = Solution.objects.filter(status=Solution.PENDING)

        for solution in pendings:
            solution.status = Solution.SUBMITED
            solution.save()

            solution_id = solution.id

            self.stdout.write('Regrading solution with id: {}'.format(solution_id))

            submit_solution.delay(solution_id)
