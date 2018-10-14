from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from Stadium import views

urlpatterns = [
    url(r'^checkstadium/$', views.checkstadium),
    url(r'^reserve/$', views.reserve),
]

urlpatterns = format_suffix_patterns(urlpatterns)