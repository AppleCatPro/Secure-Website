from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('DSWA.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', include('DSWA.urls')),
]
