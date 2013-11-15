from django.contrib import admin

from .models import MailingList, MassEmail


class MailingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_should_be_agree',)
    readonly_fields = ('or_list',)
    search_fields = ('name',)

class MassEmailAdmin(admin.ModelAdmin):
	list_display = ('mailing_list.name', 'template.name', 'scheduled_time')
	fields = ('mailing_list', 'template', 'scheduled_time', 'priority')

admin.site.register(MailingList, MailingListAdmin)
admin.site.register(MassEmail, MassEmailAdmin)