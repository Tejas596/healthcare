from rest_framework import viewsets, permissions
from .models import Department, Patient, Doctor, PatientRecord
from .serializers import DepartmentSerializer, PatientSerializer, DoctorSerializer, PatientRecordSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PatientRecordSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return PatientRecord.objects.filter(patient__user=user)
        elif hasattr(user, 'patient'):
            return PatientRecord.objects.filter(patient__user=user)
        else:
            return PatientRecord.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'doctor'):
            serializer.save(patient__user=user)
        else:
            raise PermissionDenied("You do not have permission to create records.")

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        if record.patient.user != request.user and not hasattr(request.user, 'doctor'):
            raise PermissionDenied("You do not have permission to modify this record.")
        return super().update(request, *args, **kwargs)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return Patient.objects.filter(department__doctor=user)
        return super().get_queryset()
