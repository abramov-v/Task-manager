from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/auth/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/', include('tasks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)
