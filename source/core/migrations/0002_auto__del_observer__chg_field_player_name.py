# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Observer'
        db.delete_table(u'core_observer')


        # Changing field 'Player.name'
        db.alter_column(u'core_player', 'name', self.gf('django.db.models.fields.CharField')(default='name', max_length=254))

    def backwards(self, orm):
        # Adding model 'Observer'
        db.create_table(u'core_observer', (
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Game'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Observer'])


        # Changing field 'Player.name'
        db.alter_column(u'core_player', 'name', self.gf('django.db.models.fields.CharField')(max_length=254, null=True))

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
        u'core.player': {
            'Meta': {'unique_together': "(('game', 'role'),)", 'object_name': 'Player'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['core.Game']"}),
            'health': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['core']