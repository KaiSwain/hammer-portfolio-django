from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from .models import (
    Teacher,
    Student,
    Organization,
    GenderIdentity,
    DiscAssessment,
    SixteenTypeAssessment,
    EnneagramResult,
    OshaType,
    FundingSource,
    State,
    Region
)

# Customize Admin Site Headers
admin.site.site_header = "If I Had A Hammer - Admin Portal"
admin.site.site_title = "Hammer Admin"
admin.site.index_title = "Welcome to If I Had A Hammer Administration"

# -------------------------
# Teacher Admin
# -------------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'state', 'region', 'organization', 'created_at')
    search_fields = ('full_name', 'email', 'state__name', 'region__name', 'organization__name')
    list_filter = ('state', 'region', 'organization', 'created_at')
    exclude = ('user',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Teacher Information', {
            'fields': ('full_name', 'email', 'state', 'region', 'organization')
        }),
        ('Account Settings', {
            'fields': ('password',),
            'description': 'Leave password blank to auto-generate a secure password.'
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.user:
            raw_password = obj.password if obj.password else get_random_string(12)
            user = User.objects.create_user(
                username=obj.email,
                email=obj.email,
                password=raw_password
            )
            obj.user = user
            token, created = Token.objects.get_or_create(user=user)
            messages.add_message(
                request,
                messages.SUCCESS,
                f"✅ Teacher '{obj.full_name}' created successfully! "
                f"Login credentials - Email: {obj.email} | Password: {raw_password} | API Token: {token.key}"
            )
        super().save_model(request, obj, form, change)


# -------------------------
# Student Admin
# -------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'teacher', 'email', 'nccer_number', 'gender_identity', 
                   'funding_source', 'start_date', 'end_date', 'complete_50_hour_training', 
                   'passed_osha_10_exam', 'osha_completion_date', 'osha_type', 
                   'hammer_math', 'employability_skills', 'job_interview_skills', 'created_at')
    search_fields = ('full_name', 'teacher__full_name', 'teacher__email', 'email', 'nccer_number')
    list_filter = ('teacher', 'gender_identity', 'funding_source', 'osha_type', 'complete_50_hour_training', 
                  'passed_osha_10_exam', 'hammer_math', 'employability_skills', 'job_interview_skills', 
                  'start_date', 'end_date', 'created_at')
    autocomplete_fields = ('teacher', 'gender_identity', 'disc_assessment_type',
                           'sixteen_types_assessment', 'enneagram_result', 'osha_type', 'funding_source')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Student Information', {
            'fields': ('full_name', 'teacher', 'email', 'nccer_number', 'funding_source')
        }),
        ('Training Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Personal Details', {
            'fields': ('gender_identity',),
            'classes': ('wide',)
        }),
        ('Assessment Results', {
            'fields': ('disc_assessment_type', 'sixteen_types_assessment', 'enneagram_result'),
            'classes': ('wide',),
            'description': 'Select the assessment results for this student.'
        }),
        ('Training & OSHA', {
            'fields': ('complete_50_hour_training', 'passed_osha_10_exam', 'osha_completion_date', 'osha_type'),
            'classes': ('wide',),
            'description': 'Training completion and OSHA certification details.'
        }),
        ('Skills Development', {
            'fields': ('hammer_math', 'employability_skills', 'job_interview_skills'),
            'classes': ('wide',),
            'description': 'Skills training completed by the student.'
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'teacher', 'gender_identity', 'disc_assessment_type',
            'sixteen_types_assessment', 'enneagram_result', 'osha_type', 'funding_source'
        )


# -------------------------
# Organization Admin
# -------------------------
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def teacher_count(self, obj):
        return obj.teacher_set.count()
    teacher_count.short_description = "Number of Teachers"


# -------------------------
# Assessment Type Models (Lookup Tables)
# -------------------------
@admin.register(GenderIdentity)
class GenderIdentityAdmin(admin.ModelAdmin):
    list_display = ('gender', 'student_count')
    search_fields = ('gender',)
    ordering = ('gender',)
    
    def student_count(self, obj):
        return obj.student_set.count()
    student_count.short_description = "Students"


@admin.register(DiscAssessment)
class DiscAssessmentAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'student_count')
    search_fields = ('type_name',)
    ordering = ('type_name',)
    
    def student_count(self, obj):
        return obj.student_set.count()
    student_count.short_description = "Students"


@admin.register(SixteenTypeAssessment)
class SixteenTypeAssessmentAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'student_count')
    search_fields = ('type_name',)
    ordering = ('type_name',)
    
    def student_count(self, obj):
        return obj.student_set.count()
    student_count.short_description = "Students"


@admin.register(EnneagramResult)
class EnneagramResultAdmin(admin.ModelAdmin):
    list_display = ('result_name', 'student_count')
    search_fields = ('result_name',)
    ordering = ('result_name',)
    
    def student_count(self, obj):
        return obj.student_set.count()
    student_count.short_description = "Students"


@admin.register(OshaType)
class OshaTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def student_count(self, obj):
        return obj.student_set.count()
    student_count.short_description = "Students"


@admin.register(FundingSource)
class FundingSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'student_count')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    def student_count(self, obj):
        return obj.student_set.count()
    student_count.short_description = "Students"


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'teacher_count')
    search_fields = ('name', 'abbreviation')
    ordering = ('name',)
    
    def teacher_count(self, obj):
        return obj.teacher_set.count()
    teacher_count.short_description = "Teachers"


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def teacher_count(self, obj):
        return obj.teacher_set.count()
    teacher_count.short_description = "Teachers"
    