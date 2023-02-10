from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='demo'),
    url(r'^word_cloud/$', views.word_cloud, name='word_cloud'),
    url(r'^map/$', views.heat_map, name='map'),
    url(r'^cure_line/$', views.cure_line, name='cure_line'),
    url(r'^confirm_line/$', views.confirm_line, name='confirm_line'),
]