from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.auditoria.views import LogEntryViewSet


router = DefaultRouter()
router.register(r'logs', LogEntryViewSet, basename='logentry')

urlpatterns = [
    path('', include(router.urls)),
]
