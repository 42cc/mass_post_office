# coding: utf-8
import factory

from django.contrib.auth.models import User


class UserFactory(factory.Factory):

    FACTORY_FOR = User
    password = 'pbkdf2_sha256$10000$YMFSJlSlzmQT$MVdNVG3SxXrytTDwJ8TuDYl1KmnqCKlFXyP6sEMgV8c='
    username = factory.Sequence(lambda n: 'kanata%s' % n)
    email = 'brandon.walsh@mail.com'
    first_name = 'Brandon'
    last_name = 'Walsh'

