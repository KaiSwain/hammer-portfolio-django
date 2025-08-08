from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hammer_backendapi.models import (
    Student,
    Teacher,

)

# -----------------------------
# Student Serializer
# -----------------------------
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

        depth=1

# -----------------------------
# Student ViewSet
# -----------------------------
class StudentView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
            students = Student.objects.filter(teacher=teacher)
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
            data = request.data.copy()
            data['teacher'] = teacher.id
            serializer = StudentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
