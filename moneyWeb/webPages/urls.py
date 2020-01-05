from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainPage_view, name='view-home'),
]
