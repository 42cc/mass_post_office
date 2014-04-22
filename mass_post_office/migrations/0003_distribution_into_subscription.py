# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)
user_ptr_name = '%s_ptr' % User._meta.object_name.lower()

class Migration(DataMigration):

    depends_on = (
        ("externalsite", "0020_auto__add_field_proposalsearchconstructor_priority"),
    )

    needed_by = (
        ("externalsite", "0021_auto__del_field_userprofile_distribution"),
    )

    def forwards(self, orm):
        for userprofile in orm['externalsite.UserProfile'].objects.all():
            orm.SubscriptionSettings.objects.create(
                    user=userprofile.user,
                    subscribed=userprofile.distribution)

    def backwards(self, orm):
        for subscription_setting in orm.SubscriptionSettings.objects.all():
            try:
                profile = orm['externalsite.UserProfile'].objects.get(
                        user=subscription_setting.user)
            except orm['externalsite.UserProfile'].DoesNotExist:
                continue
            profile.distribution = subscription_setting.subscribed
            profile.save()

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        user_model_label: {
            'Meta': {'object_name': User.__name__, 'db_table': "'%s'" % User._meta.db_table},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'externalsite.ban': {
            'Meta': {'ordering': "['-end_date']", 'object_name': 'Ban'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label})
        },
        'externalsite.institutionrepresentativeuser': {
            'Meta': {'unique_together': "(('user', 'institution'),)", 'object_name': 'InstitutionRepresentativeUser'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'representatives'", 'to': u"orm['studentoffice.Institution']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'institutions_representative'", 'to': "orm['%s']" % user_orm_label})
        },
        'externalsite.landingpage': {
            'Meta': {'object_name': 'LandingPage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '500'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'externalsite.loadedfile': {
            'Meta': {'object_name': 'LoadedFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filetype': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        'externalsite.loadedimage': {
            'Meta': {'object_name': 'LoadedImage'},
            'alt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'externalsite.news': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'News'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('vsekursi.libs.thumbs.ImageWithThumbsField', [], {'max_length': '100', 'name': "'main_image'"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'externalsite.proposalsearchconstructor': {
            'Meta': {'object_name': 'ProposalSearchConstructor'},
            'certificate_or_qualification': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Country']", 'null': 'True', 'blank': 'True'}),
            'education_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.EducationType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active_certificate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active_city': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active_country': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active_proposal_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active_region': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active_training_form': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'knowledge_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.KnowledgeArea']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5', 'db_index': 'True'}),
            'proposal_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Region']", 'null': 'True', 'blank': 'True'}),
            'training_form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.TrainingForm']", 'null': 'True', 'blank': 'True'})
        },
        'externalsite.regularuser': {
            'Meta': {'object_name': 'RegularUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'regular'", 'unique': 'True', 'to': "orm['%s']" % user_orm_label})
        },
        'externalsite.teacheruser': {
            'Meta': {'object_name': 'TeacherUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'teacher'", 'unique': 'True', 'to': "orm['%s']" % user_orm_label})
        },
        'externalsite.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'default': "'!'", 'max_length': '40'}),
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.City']", 'null': 'True', 'blank': 'True'}),
            'distribution': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'force_logout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 16, 0, 0)'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label, 'unique': 'True'})
        },
        u'mass_post_office.subscriptionsettings': {
            'Meta': {'object_name': 'SubscriptionSettings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label})
        },
        u'studentoffice.city': {
            'Meta': {'ordering': "['priority', 'name']", 'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_index': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Region']", 'null': 'True'})
        },
        u'studentoffice.country': {
            'Meta': {'ordering': "['priority', 'name']", 'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_index': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5', 'db_index': 'True'})
        },
        u'studentoffice.educationtype': {
            'Meta': {'ordering': "('position',)", 'object_name': 'EducationType'},
            'clickable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.EducationType']", 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'should_update_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '500'})
        },
        u'studentoffice.institution': {
            'Meta': {'object_name': 'Institution'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'aloka_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aloka_oid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'average_rate': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'branches': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['studentoffice.InstitutionBranch']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Country']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.InstitutionType']", 'null': 'True', 'blank': 'True'}),
            'is_imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_special': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'lastmod': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'location': ('vsekursi.libs.widgets.LocationField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('vsekursi.libs.thumbs.ImageWithThumbsField', [], {'name': "'logo'", 'sizes': '((135, 72), (280, 159))', 'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'must_request_info': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_index': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Region']", 'null': 'True', 'blank': 'True'}),
            'should_update_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '1023', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '500'})
        },
        u'studentoffice.institutionbranch': {
            'Meta': {'object_name': 'InstitutionBranch'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Country']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('vsekursi.libs.widgets.LocationField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Region']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '1023', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '500', 'blank': 'True'})
        },
        u'studentoffice.institutiontype': {
            'Meta': {'object_name': 'InstitutionType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '500'})
        },
        u'studentoffice.knowledgearea': {
            'Meta': {'ordering': "('position', 'name')", 'object_name': 'KnowledgeArea'},
            'educationtypes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'knowledgeareas'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['studentoffice.EducationType']"}),
            'icon': ('vsekursi.libs.thumbs.ImageWithThumbsField', [], {'max_length': '100', 'null': 'True', 'name': "'icon'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.KnowledgeArea']", 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '500'})
        },
        u'studentoffice.region': {
            'Meta': {'ordering': "['priority', 'name']", 'object_name': 'Region'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_index': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5', 'db_index': 'True'})
        },
        u'studentoffice.trainingform': {
            'Meta': {'object_name': 'TrainingForm'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '500'})
        }
    }

    complete_apps = ['externalsite', 'mass_post_office']
    symmetrical = True
