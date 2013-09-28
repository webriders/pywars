# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Game.time_ended'
        db.delete_column(u'core_game', 'time_ended')

        # Adding field 'Game.time_finished'
        db.add_column(u'core_game', 'time_finished',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Player.health'
        db.delete_column(u'core_player', 'health')

        # Adding field 'Player.state'
        db.add_column(u'core_player', 'state',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Player.is_winner'
        db.add_column(u'core_player', 'is_winner',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Game.time_ended'
        db.add_column(u'core_game', 'time_ended',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Game.time_finished'
        db.delete_column(u'core_game', 'time_finished')

        # Adding field 'Player.health'
        db.add_column(u'core_player', 'health',
                      self.gf('django.db.models.fields.IntegerField')(default=100),
                      keep_default=False)

        # Deleting field 'Player.state'
        db.delete_column(u'core_player', 'state')

        # Deleting field 'Player.is_winner'
        db.delete_column(u'core_player', 'is_winner')


    models = {
        u'core.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_finished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.gameround': {
            'Meta': {'ordering': "('number',)", 'object_name': 'GameRound'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': u"orm['core.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'scene': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.gamesnippet': {
            'Meta': {'unique_together': "(('game_round', 'player'),)", 'object_name': 'GameSnippet'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'game_round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snippets'", 'to': u"orm['core.GameRound']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snippets'", 'to': u"orm['core.Player']"})
        },
        u'core.player': {
            'Meta': {'unique_together': "(('game', 'role'),)", 'object_name': 'Player'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': u"orm['core.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'is_winner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'state': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']