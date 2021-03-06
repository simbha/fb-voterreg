# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InvitedToBlock'
        db.create_table('main_invitedtoblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('voting_block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.VotingBlock'])),
        ))
        db.send_create_signal('main', ['InvitedToBlock'])


    def backwards(self, orm):
        # Deleting model 'InvitedToBlock'
        db.delete_table('main_invitedtoblock')


    models = {
        'main.friendship': {
            'Meta': {'unique_together': "(('user', 'fb_uid'),)", 'object_name': 'Friendship'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.FriendshipBatch']", 'null': 'True'}),
            'batch_type': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_pledged': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_voted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'display_ordering': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'far_from_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fb_uid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_individually': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invited_pledge_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'invited_with_batch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_random': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_voted': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.User']"}),
            'user_fb_uid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'voting_frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'votizen_id': ('django.db.models.fields.CharField', [], {'max_length': '132', 'blank': 'True'}),
            'wont_vote_reason': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'})
        },
        'main.friendshipbatch': {
            'Meta': {'object_name': 'FriendshipBatch'},
            'completely_fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'regular_batch_no': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.User']"})
        },
        'main.invitedtoblock': {
            'Meta': {'object_name': 'InvitedToBlock'},
            'fb_uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voting_block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.VotingBlock']"})
        },
        'main.lastappnotification': {
            'Meta': {'object_name': 'LastAppNotification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'notification_scheduled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pledged_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.User']", 'unique': 'True'}),
            'voted_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.mission': {
            'Meta': {'unique_together': "(('user', 'type'),)", 'object_name': 'Mission'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pledged_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.User']"})
        },
        'main.user': {
            'Meta': {'object_name': 'User'},
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'data_fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_invited_friends': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_pledged': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_voted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'explicit_share': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'explicit_share_vote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'far_from_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fb_uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'friends_fetch_last_activity': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'friends_fetched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_pledge_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'last_voted': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'location_city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'location_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'num_friends': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'seen_initial_prompt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unsubscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'used_registration_widget': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'voting_frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'votizen_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '132', 'blank': 'True'}),
            'wont_vote_reason': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '18', 'blank': 'True'})
        },
        'main.votingblock': {
            'Meta': {'object_name': 'VotingBlock'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'organization_privacy_policy': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'organization_website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'main.votingblockfriendship': {
            'Meta': {'unique_together': "(('voting_block', 'friendship'),)", 'object_name': 'VotingBlockFriendship'},
            'friendship': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Friendship']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_individually': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invited_with_batch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'voting_block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.VotingBlock']"})
        },
        'main.votingblockmember': {
            'Meta': {'unique_together': "(('voting_block', 'member'),)", 'object_name': 'VotingBlockMember'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_friendship_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.User']"}),
            'voting_block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.VotingBlock']"})
        },
        'main.wonbadge': {
            'Meta': {'unique_together': "(('user', 'badge_type'),)", 'object_name': 'WonBadge'},
            'badge_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_shown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.User']"})
        }
    }

    complete_apps = ['main']