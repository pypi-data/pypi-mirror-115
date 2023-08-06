from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape, format_html
from django.contrib import admin
from django.urls import reverse

from .filters import ActionListFilter


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    actions = None
    list_display_links = ['action_time']

    list_filter = [
        'user',
        'content_type',
        ActionListFilter
    ]

    search_fields = [
        'user__username',
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            try:
                link = format_html('<a href="%s">%s</a>' % (
                    reverse('admin:%s_%s_change' % (ct.app_label, ct.model),
                            args=[obj.object_id]),
                    escape(obj.object_repr)),
                                   )
            except:
                link = ""
        return link

    object_link.admin_order_field = 'object_repr'
    object_link.short_description = _('object')

    def action_description(self, obj):
        action_names = {
            ADDITION: _('addition'),
            DELETION: _('deletion'),
            CHANGE: _('change'),
        }
        return action_names[obj.action_flag]

    action_description.short_description = _('action')
