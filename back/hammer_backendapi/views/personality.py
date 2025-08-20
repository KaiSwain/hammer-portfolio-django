from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from hammer_backendapi.models import Student, Teacher
from hammer_backendapi.serializers import StudentSerializer


class PersonalityViewSet(ModelViewSet):
    
    
