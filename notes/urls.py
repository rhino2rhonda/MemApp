from django.conf.urls import url
from notes import views

urlpatterns=[
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^todo/$', views.TodoView.as_view(), name='todo'),
]