# -*- coding: utf-8 -*-
from model_utils import Choices

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as

from post_office.models import EmailTemplate, Email, STATUS
from post_office.mail import from_template

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class SubscriptionSettings(models.Model):
    user = models.OneToOneField(USER_MODEL)
    subscribed = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s - %s' % (self.user.username, str(self.subscribed))

    class Meta:
        verbose_name_plural = "Subscription Settings"


class MailingList(models.Model):
    name = models.CharField(verbose_name='List name', max_length=255)
    user_should_be_agree = models.BooleanField(
        verbose_name=_('User should be agreed to receive mails'), default=True)
    all_users = models.BooleanField(
        verbose_name=_('All users'), default=False)
    or_list = models.TextField(verbose_name='json OR-list', default='')
    additional_users = models.ManyToManyField(
        USER_MODEL, verbose_name=_('Additional users'), null=True)

    def __unicode__(self):
        return self.name

    def clean(self):
        if self.or_list:
            try:
                simplejson.loads(self.or_list)
            except ValueError:
                raise ValidationError('OR-list json is not valid.')
        if self.all_users and not self.user_should_be_agree:
            self.user_should_be_agree = True
        if self.all_users and (self.or_list or (self.id and self.additional_users.count())):
            self.or_list = ''
            if self.id:
                for au in self.additional_users.all():
                    self.additional_users.remove(au)

    def get_users_queryset(self):
        if self.all_users:
            user_qs = get_user_model().objects.all()
        else:
            q = Q()
            if self.additional_users.exists():
                q |= Q(id__in=self.additional_users.values_list('id', flat=True))
            if self.or_list:
                for i in simplejson.loads(self.or_list):
                    q |= Q(**i)
            user_qs = get_user_model().objects.filter(q)
        if self.user_should_be_agree:
            user_qs = user_qs.filter(subscriptionsettings__subscribed=True)
        return (
            user_qs
            .filter(is_active=True, email__isnull=False)
            .exclude(email='').distinct()
        )

    def get_emails_generator(self):
        for user in self.get_users_queryset():
            yield user.email


class MassEmail(models.Model):
    PRIORITY_CHOICES = Choices(
        (0, 'low', _('low')),
        (1, 'medium', _('medium')),
        (2, 'high', _('high')),
        (3, 'now', _('now'))
        )

    mailing_list = models.ForeignKey(MailingList, verbose_name='Mailing List')
    template = models.ForeignKey(
        EmailTemplate,
        help_text='Template with access to `{{ user }}` variable',
        verbose_name='Template')
    emails = models.ManyToManyField(
        Email, verbose_name='Emails',
        null=True, blank=True)
    scheduled_time = models.DateTimeField(blank=True, null=True, db_index=True)
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES,
        blank=True, null=True, db_index=True)

    def __unicode__(self):
        return u'Mails for {self.mailing_list} with template {self.template}'.format(self=self)

    def save(self, *args, **kwargs):
        super(MassEmail, self).save(*args, **kwargs)
        for user in self.mailing_list.get_users_queryset():
            email = from_template(
                settings.DEFAULT_FROM_EMAIL,
                recipient=user.email,
                template=self.template,
                context={'user': user},
                scheduled_time=self.scheduled_time,
                priority=self.priority)
            email.save()
            self.emails.add(email)

    @property
    def status(self):
        result = {}
        for status in STATUS._fields:
            result[status] = self.emails.filter(status=getattr(STATUS, status)).count()

        return result
