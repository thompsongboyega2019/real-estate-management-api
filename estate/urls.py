from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import views_auth


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'houses', views.HouseViewSet)
router.register(r'occupants', views.OccupantViewSet)
router.register(r'chief-tenant-assignments', views.ChiefTenantAssignmentViewSet)

app_name = 'real_estate_app'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('estate.auth_urls')),
]

# Restore to the standard DRF login/logout inclusion
urlpatterns += [
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
]
