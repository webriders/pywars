from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    'core.views',

    url(r'^$', TemplateView.as_view(template_name='core/game_creator.html')),
)