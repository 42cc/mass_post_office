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


class StatusField(widgets.Widget):
    def render(self, name, value, attrs=None):
        import ipdb; ipdb.set_trace()
        if value is None:
            value = { 'sent': 0, 'failed': 0, 'queued': 0}
        output = u"sent: %s, failed: %s, queued: %s" % (
            value['sent'], value['failed'], value['queued'])
        return output


class MassEmailAdminForm(forms.ModelForm):
    status = forms.CharField(widget=StatusField, required=False)
    class Meta:
        exclude = ['emails']


class MassEmailAdmin(admin.ModelAdmin):
    list_display = ('mailing_list', 'template', 'scheduled_time')
    form = MassEmailAdminForm


admin.site.register(MailingList, MailingListAdmin)
admin.site.register(SubscriptionSettings)
admin.site.register(MassEmail, MassEmailAdmin)
