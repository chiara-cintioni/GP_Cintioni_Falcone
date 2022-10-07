from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search, name="search"),
    path('download', views.download, name="download"),
    path('contact', views.contact, name="contact"),
    path('help', views.help, name="help"),
    path('sources', views.sources, name="sources"),
    path('info', views.info, name="info"),
]