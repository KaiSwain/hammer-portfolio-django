from django.db import models
from django.contrib.auth.models import User


# Organization Model (optional if needed for grouping)
class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # store raw temporarily, will use for user creation
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.full_name)
    


# Student Model
class Student(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students')
    full_name = models.CharField(max_length=255)
    gender_identity = models.CharField(max_length=50, default="They")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Training & Exams
    complete_50_hour_training = models.BooleanField(default=False)
    passed_osha_10_exam = models.BooleanField(default=False)
    osha_completion_date = models.DateField(null=True, blank=True)
    osha_type = models.CharField(max_length=100, null=True, blank=True)

    # Skills
    hammer_math = models.BooleanField(default=False)
    employability_skills = models.BooleanField(default=False)

    # Assessments
    passed_ruler_assessment = models.BooleanField(default=False)
    pretest_score = models.IntegerField(null=True, blank=True)
    posttest_score = models.IntegerField(null=True, blank=True)

    disk_assessment_type = models.CharField(max_length=100, null=True, blank=True)
    sixteen_types_assessment_type = models.CharField(max_length=100, null=True, blank=True)
    enneagram_results = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.full_name)
    