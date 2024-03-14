
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name="adm"),
    path('timetable/', include('timetable.urls')),
    path('',include('main.urls')),
    path('accounts/',include("django.contrib.auth.urls")),
]
