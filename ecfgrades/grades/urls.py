from django.urls import path

from . import views

app_name = 'grades'
urlpatterns = [
    # e.g. grades/
    path('', views.index, name='index'),
    # e.g. /grades/5/
    path('<str:player_ref>/', views.detail, name='detail'),
]
