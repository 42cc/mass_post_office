# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)
user_ptr_name = '%s_ptr' % User._meta.module_name
user_id_name = '%s_id' % User._meta.module_name

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailingList'
        db.create_table(u'mass_post_office_mailinglist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_should_be_agree', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('all_users', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('or_list', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'mass_post_office', ['MailingList'])

        # Adding M2M table for field additional_users on 'MailingList'
        db.create_table(u'mass_post_office_mailinglist_additional_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailinglist', models.ForeignKey(orm[u'mass_post_office.mailinglist'], null=False)),
            (User._meta.module_name, models.ForeignKey(orm[user_model_label], null=False))
        ))
        db.create_unique(u'mass_post_office_mailinglist_additional_users', ['mailinglist_id', user_id_name])


    def backwards(self, orm):
        # Deleting model 'MailingList'
        db.delete_table(u'mass_post_office_mailinglist')

        # Removing M2M table for field additional_users on 'MailingList'
        db.delete_table('mass_post_office_mailinglist_additional_users')


    models = {
        user_model_label: {
        },
        u'mass_post_office.mailinglist': {
            'Meta': {'object_name': 'MailingList'},
            'additional_users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['%s']" % user_orm_label, 'null': 'True', 'symmetrical': 'False'}),
            'all_users': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'or_list': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'user_should_be_agree': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'mass_post_office.subscriptionsettings': {
            'Meta': {'object_name': 'SubscriptionSettings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            User._meta.object_name: ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label})
        }
    }

    complete_apps = ['mass_post_office']