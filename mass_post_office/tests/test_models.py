import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase

from ..models import MailingList, SubscriptionSettings, MassEmail

from vsekursi.studentoffice.tests.factories import UserFactory

from post_office.models import EmailTemplate, Email

class TestModels(TestCase):

    def test_mailing_list(self):
        ml = MailingList(
            name='Some name',
            user_should_be_agree=True,
            all_users=True,
            or_list='')
        ml.save()
        self.assertEqual(str(ml), ml.name)
        # all users withoul user_should_be_agree -> Failure
        ml = MailingList(
            name='Some name',
            user_should_be_agree=False,
            all_users=True,
            or_list='')
        ml.clean()
        ml.save()
        self.assertTrue(ml.user_should_be_agree)
        # all users and or_list
        ml = MailingList(
            name='Some name',
            user_should_be_agree=True,
            all_users=True,
            or_list='{"some list": "123"}')
        ml.clean()
        ml.save()
        self.assertFalse(ml.or_list)
        # all users and additional users
        user = UserFactory()
        ml = MailingList(
            name='Some name',
            user_should_be_agree=True,
            all_users=True,
            or_list='')
        ml.save()
        ml.additional_users.add(user)
        ml.clean()
        ml.save()
        self.assertEqual(ml.additional_users.count(), 0)
        # test not valid json
        ml = MailingList(
            name='Some name',
            user_should_be_agree=True,
            all_users=True,
            or_list='{bad json}')
        is_exception = False
        try:
            ml.clean()
        except ValidationError:
            is_exception = True
        self.assertTrue(is_exception)

    def test_get_users_queryset(self):
        user1 = UserFactory(is_active=True)
        user2 = UserFactory(is_active=True)
        user3 = UserFactory(is_active=True)
        without_email = UserFactory(is_active=True)
        without_email.email = ''
        without_email.save()
        inactive_user = UserFactory(is_active=False)
        # all
        ml = MailingList(
            name='Some name',
            user_should_be_agree=False,
            all_users=True)
        ml.save()
        self.assertEqual(ml.get_users_queryset().count(), 3)
        # or list
        ml = MailingList(
            name='Some name',
            user_should_be_agree=False,
            all_users=False,
            or_list='[{"id": %d}]' % user2.id)
        ml.save()
        self.assertEqual(ml.get_users_queryset().count(), 1)
        self.assertEqual(ml.get_users_queryset()[0].id, user2.id)
        # additional users
        ml.additional_users.add(user1)
        self.assertEqual(ml.get_users_queryset().count(), 2)

    def test_get_emails_generator(self):
        user1 = UserFactory(is_active=True)
        user2 = UserFactory(is_active=True)
        ml = MailingList(
            name='Some name',
            user_should_be_agree=True,
            all_users=True)
        ml.save()
        generator = ml.get_emails_generator()
        emails = [e for e in generator]
        self.assertEqual(len(emails), 0)

        SubscriptionSettings.objects.create(user=user1, subscribed=True)
        SubscriptionSettings.objects.create(user=user2, subscribed=True)

        generator = ml.get_emails_generator()
        emails = [e for e in generator]
        self.assertEqual(len(emails), 2)
        self.assertIn(user1.email, emails)

    def test_mass_emails(self):
        priority=2
        user1 = UserFactory(is_active=True)
        self.assertTrue(len(user1.first_name))
        self.assertTrue(len(user1.last_name))
        ml = MailingList(
            name='Some name',
            user_should_be_agree=False,
            all_users=True)
        ml.save()
        email_template = EmailTemplate.objects.create(name='welcome',
            subject='Welcome!', content='Hi {{ user.first_name }} {{ user.last_name }}!')
        today = datetime.datetime.today()
        from django.db.models import Q
        mass_emails_qs = Q(scheduled_time=today, priority=priority, 
            mailing_list=ml, template=email_template)
        mass_emails = MassEmail.objects.filter(mass_emails_qs)
        self.assertEqual(len(mass_emails), 0)
        me = MassEmail(
            scheduled_time=today,
            priority=priority,
            mailing_list=ml,
            template=email_template
            )
        me.save()
        mass_emails = MassEmail.objects.filter(mass_emails_qs)
        self.assertEqual(len(mass_emails), 1)
        emails = me.emails.all()
        self.assertEqual(len(emails), 1)
        email = emails[0]
        self.assertEqual(user1.email, email.to)
        self.assertIn(user1.first_name, email.message)
        self.assertIn(user1.last_name, email.message)
        self.assertEqual(today, email.scheduled_time)
        self.assertEqual(priority, email.priority)
