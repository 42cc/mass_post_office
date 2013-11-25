# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.conf import settings

from post_office import mail
from post_office.models import EmailTemplate

from .utils import decode_data
from .models import SubscriptionSettings


def unsubscribe(request, hashed, data):
    try:
        username, email = decode_data(hashed, data)
    except Exception:
        raise Http404
    try:
        subscription = SubscriptionSettings.objects.get(
            user__username=username,
            user__email=email)
    except SubscriptionSettings.DoesNotExist as e:
        raise Http404
    if not request.POST:
        context = {
            'user': subscription.user,
            'cancel_url': '/'
        }
        return render(request, 'mass_post_office/unsubscribe.html', context)
    if not 'is_unsubscribed' in request.POST:
        return redirect('/')
    subscription.subscribed = False
    subscription.save()
    try:
        mail.from_template(
            settings.DEFAULT_FROM_EMAIL,
            subscription.user.email,
            template=u'post_office/canceled_subscription',
            context={
                'user': subscription.user
            })
    except EmailTemplate.DoesNotExist as e:
        # we should process undefined EmailTemplate here
        # try to check 'post_migrate'
        pass
    return redirect(reverse('mass_post_office:unsubscribed'))


def unsubscribed(request):
    context = {}
    return render(request, 'mass_post_office/complete.html', context)
