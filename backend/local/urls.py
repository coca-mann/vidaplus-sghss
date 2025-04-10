from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.local.views import LocalViewSet

router = DefaultRouter()
router.register('local', LocalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]