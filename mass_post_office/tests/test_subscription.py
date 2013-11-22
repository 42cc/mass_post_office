# coding: utf-8
from django.core.urlresolvers import reverse
from django import template
from django.test import TestCase
from django.test.client import Client
from south.signals import post_migrate

from post_office import mail
from post_office.models import EmailTemplate, Email, STATUS

from .factories import UserFactory
from ..models import SubscriptionSettings
from ..utils import encode_data


class TagsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_unsubscribe_tag(self):
        from django.template import TemplateSyntaxError
        try:
            tpl = template.Template(
                '{% load subscription %}'
                '{% unsubscribe_link %}'
            )
        except TemplateSyntaxError, e:
            self.assertIn(u'tag requires a single argument', "%s" % e)
        user = UserFactory()
        tpl = template.Template(
            '{% load subscription %}'
            '{% unsubscribe_link user %}'
        )
        context = template.Context({'user': user})
        rendered = tpl.render(context)
        data_tuple = (user.username, user.email)
        hashed, data = encode_data(data_tuple)
        url = reverse('mass_post_office:unsubscribe', 
            kwargs={'hashed': hashed, 'data': data})
        self.assertIn(url, rendered)

    def test_unsubscribe_view(self):
        user = UserFactory(is_active=True)
        subscription = SubscriptionSettings(user=user, subscribed=True)
        subscription.save()
        data_tuple = (user.username, user.email)
        hashed, data = encode_data(data_tuple)
        url = reverse('mass_post_office:unsubscribe', 
            kwargs={'hashed': hashed, 'data': data})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<form method="post" id="unsubscribe-form">', response.content)
        data = {'is_unsubscribed': True}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        subscription = SubscriptionSettings.objects.get(user=user)
        self.assertEqual(subscription.subscribed, False)
        response = self.client.get(reverse('mass_post_office:unsubscribed'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfuly unsubscribed', response.content)

    def test_email_templates(self):
        EmailTemplate.objects.all().delete()
        post_migrate.send(sender=self, app='post_office')

        def __check_email_template(tpl_name, content):
            templates = EmailTemplate.objects.filter(
                name=tpl_name)
            self.assertEqual(templates.count(), 1)
            self.assertIn(content, templates[0].content)

        __check_email_template('post_office/canceled_subscription', 
            u'You successfuly unsubscribed your subscription for')
        __check_email_template('post_office/unsubscribe_page', 
            u'Visit {% unsubscribe_link user %} link to unsubscribe')

    def test_send_email_from_template(self):
        user = UserFactory(is_active=True)

        def __check_send_email(tpl_name, content=None):
            email = mail.from_template(
                "bob@example.com",
                user.email,
                template=tpl_name,
                context=dict(user=user))
            self.assertEqual(Email.objects.get(id=email.id).status, STATUS.queued)
            mail.send_queued()
            self.assertEqual(Email.objects.get(id=email.id).status, STATUS.sent)
            if content:
                for field in content.iterkeys():
                    self.assertIn(content[field], getattr(email, field))

        __check_send_email(u'post_office/canceled_subscription',
            content={'message': "You successfuly unsubscribed your subscription for %s" % user.email})
        data_tuple = (user.username, user.email)
        hashed, data = encode_data(data_tuple)
        url = reverse('mass_post_office:unsubscribe', 
            kwargs={'hashed': hashed, 'data': data})
        __check_send_email('post_office/unsubscribe_page', 
            content={'message': url})
