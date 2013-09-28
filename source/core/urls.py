from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    'core.views',

    url(r'^$', 'start_game_page', name='core-start-game-page'),
    url(r'^game/(?P<pk>\d+)/$', 'game_page', name='core-game-page'),
    url(r'^game/(?P<pk>\d+)/join/$', 'join_game_feeder', name='core-join-game-feeder'),
    url(r'^game/(?P<game_pk>\d+)/round/(?P<last_round_number>\d+)/$', 'new_rounds_feed', name='core-new-rounds-feed'),

    url(r'^test-game/$', TemplateView.as_view(template_name='core/test_game.html')),
)