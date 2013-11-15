# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _


class SubscriptionSettings(models.Model):
    user = models.OneToOneField(User)
    subscribed = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s - %s' % (self.user.username, str(self.subscribed))


class MailingList(models.Model):
    name = models.CharField(verbose_name='List name', max_length=255)
    user_should_be_agree = models.BooleanField(
        verbose_name=_('User should be agreed to receive mails'), default=True)
    all_users = models.BooleanField(
        verbose_name=_('All users'), default=False)
    or_list = models.TextField(verbose_name='json OR-list', default='')
    additional_users = models.ManyToManyField(
        User, verbose_name=_('Additional users'), null=True)

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
            user_qs = User.objects.all()
        else:
            q = Q()
            if self.additional_users.exists():
                q |= Q(id__in=self.additional_users.values_list('id', flat=True))
            if self.or_list:
                for i in simplejson.loads(self.or_list):
                    q |= Q(**i)
            user_qs = User.objects.filter(q)
        return (
            user_qs
            .filter(is_active=True, email__isnull=False,
                    subscriptionsettings__subscribed=self.user_should_be_agree)
            .exclude(email='').distinct()
        )

    def get_emails_generator(self):
        for user in self.get_users_queryset():
            yield user.email
