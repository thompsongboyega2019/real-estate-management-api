from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LandlordProfileView
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
    path('landlord/profile/', LandlordProfileView.as_view(), name='landlord-profile'),
    # path('api/auth/', include('estate.auth_urls')),
]


