from django.conf.urls import url ,include
from django.contrib import admin
from Stadium import urls
from rest_framework import routers


urlpatterns = [
    url(r'^', include(urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]