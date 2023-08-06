from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


class ActionListFilter(SimpleListFilter):
    title = _('action')
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return (
            (ADDITION, _('addition')),
            (DELETION, _('deletion')),
            (CHANGE, _('change')),
        )

    def queryset(self, request, queryset):
        return queryset.filter(
            action_flag=self.value()) if self.value() else queryset
