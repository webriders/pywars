from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    'core.views',

    url(r'^$', TemplateView.as_view(template_name='core/game_creator_page.html')),

    url(r'^game/(?P<game_pk>\d+)/round/(?P<last_round_number>\d+)/$', 'new_rounds_feed', name='core-new-rounds-feed')
)