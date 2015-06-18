from import_export import resources
from .models import Ticket


class TicketResource(resources.ModelResource):

    class Meta:
        model = Ticket
        fields = (
            'event__name',
            'base_user__email',
            'base_user__first_name',
            'base_user__last_name'
        )
