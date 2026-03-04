from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reporting.views import IncidentViewSet, LookupViewSet, CADFeedViewSet, UnitViewSet, PersonnelViewSet

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'lookups', LookupViewSet, basename='lookup')
router.register(r'cad-feed', CADFeedViewSet, basename='cad-feed')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'personnel', PersonnelViewSet, basename='personnel')

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
