# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table(u'core_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('time_ended', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Game'])

        # Adding model 'Player'
        db.create_table(u'core_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Game'])),
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('health', self.gf('django.db.models.fields.IntegerField')(default=100)),
        ))
        db.send_create_signal(u'core', ['Player'])

        # Adding unique constraint on 'Player', fields ['game', 'role']
        db.create_unique(u'core_player', ['game_id', 'role'])

        # Adding model 'Observer'
        db.create_table(u'core_observer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Game'])),
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Observer'])

        # Adding model 'GameRound'
        db.create_table(u'core_gameround', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rounds', to=orm['core.Game'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('scene', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['GameRound'])

        # Adding model 'GameSnippet'
        db.create_table(u'core_gamesnippet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_round', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snippets', to=orm['core.GameRound'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snippets', to=orm['core.Player'])),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['GameSnippet'])

        # Adding unique constraint on 'GameSnippet', fields ['game_round', 'player']
        db.create_unique(u'core_gamesnippet', ['game_round_id', 'player_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'GameSnippet', fields ['game_round', 'player']
        db.delete_unique(u'core_gamesnippet', ['game_round_id', 'player_id'])

        # Removing unique constraint on 'Player', fields ['game', 'role']
        db.delete_unique(u'core_player', ['game_id', 'role'])

        # Deleting model 'Game'
        db.delete_table(u'core_game')

        # Deleting model 'Player'
        db.delete_table(u'core_player')

        # Deleting model 'Observer'
        db.delete_table(u'core_observer')

        # Deleting model 'GameRound'
        db.delete_table(u'core_gameround')

        # Deleting model 'GameSnippet'
        db.delete_table(u'core_gamesnippet')


    models = {
        u'core.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
        u'core.observer': {
            'Meta': {'object_name': 'Observer'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['core.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'})
        },
        u'core.player': {
            'Meta': {'unique_together': "(('game', 'role'),)", 'object_name': 'Player'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['core.Game']"}),
            'health': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['core']