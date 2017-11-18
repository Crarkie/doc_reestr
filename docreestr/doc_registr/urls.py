from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user(?P<user_id>[0-9]+)/$', views.list_doc, name='list_doc'),
    url(r'^user(?P<user_id>[0-9]+)/doc(?P<doc_id>[0-9]+)/$', views.preview, name='preview'),
    url(r'^login/$', views.login, name='login'),
    url(r'^registry/$', views.registry, name='registry'),
    url(r'^load_doc/$', views.load_doc, name='load_doc'),
    url(r'^doc/$', views.my_doc, name='my_doc'),
    url(r'^doc(?P<doc_id>[0-9]+)/cancel/$', views.cancel, name='cancel'),
    url(r'^setting/$', views.setting, name='setting')
]