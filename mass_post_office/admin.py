# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import MailingList, SubscriptionSettings, MassEmail


class MailingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_should_be_agree', 'all_users')
    readonly_fields = ('or_list',)
    search_fields = ('name',)


def status_str(obj):
    return u"sent: {sent}, failed: {failed}, queued: {queued}".format(**obj.status)
status_str.short_description = 'Email queue status'


def template_link(obj):
    if obj.template:
        return (
            u'<a href="%s" target="_blank">EmailTemplate admin</a>. '
            u'Note: Editing template will not change queued emails'
            % reverse('admin:post_office_emailtemplate_change', args=[obj.template.id])
        )
    else:
        return 'N/A'

template_link.allow_tags = True
template_link.short_description = 'View template'


class MassEmailAdmin(admin.ModelAdmin):
    list_display = ('mailing_list', 'template', 'scheduled_time')
    readonly_fields = (status_str, template_link)
    fields = (
        status_str, 'mailing_list', 'template', template_link, 'scheduled_time', 'priority'
    )


admin.site.register(MailingList, MailingListAdmin)
admin.site.register(SubscriptionSettings)
admin.site.register(MassEmail, MassEmailAdmin)
