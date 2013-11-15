# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import MailingList


class MailingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_should_be_agree', 'all_users')
    readonly_fields = ('or_list',)
    search_fields = ('name',)


admin.site.register(MailingList, MailingListAdmin)
