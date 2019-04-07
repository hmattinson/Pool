# pool/urls.py
from django.conf.urls import url
from pool import views

urlpatterns = [
    url(r'^processresult$', views.ProcessResultView.as_view()),
    url(r'^scorejson$', views.JsonServerView.as_view()),
    url(r'^$', views.HomePageView.as_view())
]
