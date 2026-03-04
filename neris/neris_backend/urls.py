from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reporting.views import IncidentViewSet, LookupViewSet

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'lookups', LookupViewSet, basename='lookup')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
