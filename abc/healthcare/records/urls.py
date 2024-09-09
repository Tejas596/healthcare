from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, PatientRecordViewSet, PatientViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'records', PatientRecordViewSet)
router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]


