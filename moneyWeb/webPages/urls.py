from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainPage_view, name='view-home'),
    path('settings/', views.settings_view, name='view-settings'),
    path('stock/', views.stock_view, name='view-stock'),
]
