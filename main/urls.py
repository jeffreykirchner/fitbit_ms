'''
URL Patterns
'''
from rest_framework.urlpatterns import format_suffix_patterns

from django.views.generic.base import RedirectView

from django.urls import path,include
from main import views

urlpatterns = [

    path('', views.root_path),

    #txt
    path('robots.txt', views.RobotsTxt, name='robotsTxt'),
    path('ads.txt', views.AdsTxt, name='adsTxt'),
    path('.well-known/security.txt', views.SecurityTxt, name='securityTxt'),
    path('humans.txt', views.HumansTxt, name='humansTxt'),

    #icons
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
    path('apple-touch-icon-precomposed.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),
    path('apple-touch-icon.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),
    path('apple-touch-icon-120x120-precomposed.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
