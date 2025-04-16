from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('api/v1/', include('backend.atendimento.urls')),
    path('api/v1/', include('backend.backoffice.urls')),
    path('api/v1/', include('backend.local.urls')),
    path('api/v1/', include('backend.pessoa.urls')),
    path('api/v1/', include('backend.auditoria.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
