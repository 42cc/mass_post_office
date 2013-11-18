# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.forms import widgets
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

from .models import MailingList, SubscriptionSettings, MassEmail


class MailingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_should_be_agree', 'all_users')
    readonly_fields = ('or_list',)
    search_fields = ('name',)


def status_str(obj):
    return u"sent: {sent}, failed: {failed}, queued: {queued}".format(**obj.status)
status_str.short_description = 'Email queue status'


class MassEmailAdmin(admin.ModelAdmin):
    list_display = ('mailing_list', 'template', 'scheduled_time')
    readonly_fields = (status_str, )
    exclude = ('emails', )


admin.site.register(MailingList, MailingListAdmin)
admin.site.register(SubscriptionSettings)
admin.site.register(MassEmail, MassEmailAdmin)
