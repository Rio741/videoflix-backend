from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.videos.api.urls')),
    path('api/auth/', include('apps.user_auth.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

