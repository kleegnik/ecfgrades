from django.conf.urls import include
from django.urls import path
from django.contrib import admin

from ecfgrades.grades import views


urlpatterns = [
    path('grades/', include('ecfgrades.grades.urls')),
    path('statistics/', include('ecfgrades.statistics.urls')),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
]
