from django.db import models
from django.contrib.auth.models import User


# Organization Model
class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # raw initially, then hashed
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# ===========================
# NEW Lookup Models
# ===========================

class GenderIdentity(models.Model):
    gender = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.gender


class DiscAssessment(models.Model):
    type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type_name


class SixteenTypeAssessment(models.Model):
    type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type_name


class EnneagramResult(models.Model):
    result_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.result_name
    
class OshaType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FundingSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, help_text="Optional description of the funding source")

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True, help_text="Two-letter state abbreviation")

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ===========================
# Student Model
# ===========================

class Student(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    nccer_number = models.CharField(max_length=50, blank=True, null=True, help_text="NCCER credential number")

    # Use Foreign Keys instead of plain text
    gender_identity = models.ForeignKey(GenderIdentity, on_delete=models.SET_NULL, null=True, blank=True)
    disc_assessment_type = models.ForeignKey(DiscAssessment, on_delete=models.SET_NULL, null=True, blank=True)
    sixteen_types_assessment = models.ForeignKey(SixteenTypeAssessment, on_delete=models.SET_NULL, null=True, blank=True)
    enneagram_result = models.ForeignKey(EnneagramResult, on_delete=models.SET_NULL, null=True, blank=True)
    funding_source = models.ForeignKey(FundingSource, on_delete=models.SET_NULL, null=True, blank=True)

    # Training Dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Training & Exams
    complete_50_hour_training = models.BooleanField(default=False)
    passed_osha_10_exam = models.BooleanField(default=False)
    osha_completion_date = models.DateField(null=True, blank=True)
    osha_type = models.ForeignKey(OshaType, on_delete=models.SET_NULL, null=True, blank=True)

    # Skills
    hammer_math = models.BooleanField(default=False)
    employability_skills = models.BooleanField(default=False)
    job_interview_skills = models.BooleanField(default=False)

    # Assessments
    passed_ruler_assessment = models.BooleanField(default=False)
    pretest_score = models.IntegerField(null=True, blank=True)
    posttest_score = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


import os
import uuid

def student_file_path(instance, filename):
    """Generate file path: students/{student_name}/{student_name}_{filename}"""
    import re
    
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    # Get student name and clean it for filesystem safety
    student_name = instance.student.full_name
    # Replace spaces with underscores and remove special characters
    safe_student_name = re.sub(r'[^\w\s-]', '', student_name)
    safe_student_name = re.sub(r'[-\s]+', '_', safe_student_name)
    
    # Clean the original filename
    safe_base = re.sub(r'[^\w\s-]', '', base)
    safe_base = re.sub(r'[-\s]+', '_', safe_base)
    
    # Create descriptive filename: StudentName_OriginalFilename.ext
    safe_filename = f"{safe_student_name}_{safe_base}{ext}"
    
    # Create path for student files
    path = f"students/{safe_student_name}/{safe_filename}"
    return path

class StudentFile(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=student_file_path)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100, default='application/octet-stream')
    size_bytes = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Student File'
        verbose_name_plural = 'Student Files'
    
    def __str__(self):
        return f"{self.student.full_name} - {self.original_name}"
    
    @property
    def file_size_mb(self):
        return round(self.size_bytes / (1024 * 1024), 2)

