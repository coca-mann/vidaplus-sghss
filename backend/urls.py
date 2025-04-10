from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/v1/', include('backend.atendimento.urls')),
    path('api/v1/', include('backend.backoffice.urls')),
    path('api/v1/', include('backend.local.urls')),
    path('api/v1/', include('backend.pessoa.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
