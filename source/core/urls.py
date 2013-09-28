from django.conf.urls import patterns, url

urlpatterns = patterns(
    'core.views',

    url(r'^$', 'start_game_page', name='core-start-game-page'),
    url(r'^game/(?P<pk>\d+)/$', 'game_page', name='core-game-page'),
    url(r'^game/(?P<pk>\d+)/join/$', 'join_game_feeder', name='core-join-game-feeder')
)