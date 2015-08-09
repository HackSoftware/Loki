from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Successor, SuccessViedeo


class SuccessorAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
admin.site.register(Successor, SuccessorAdmin)


class SuccessViedeoAdmin(admin.ModelAdmin):
    pass
admin.site.register(SuccessViedeo, SuccessViedeoAdmin)
