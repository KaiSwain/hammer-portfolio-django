from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from rest_framework.authtoken.models import Token
import boto3
from django.conf import settings
from .models import (
    Teacher,
    Student,
    StudentFile,
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
    list_display = ('full_name', 'teacher', 'teacher_organization', 'email', 'nccer_number', 'gender_identity', 
                   'funding_source', 'start_date', 'end_date', 'complete_50_hour_training', 
                   'passed_osha_10_exam', 'osha_completion_date', 'osha_type', 
                   'hammer_math', 'employability_skills', 'job_interview_skills', 'created_at')
    search_fields = ('full_name', 'teacher__full_name', 'teacher__email', 'email', 'nccer_number')
    list_filter = ('teacher__organization', 'teacher__state', 'teacher__region', 'teacher', 'gender_identity', 'funding_source', 'osha_type', 'complete_50_hour_training', 
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
    
    def teacher_organization(self, obj):
        """Display the teacher's organization"""
        if obj.teacher and obj.teacher.organization:
            return obj.teacher.organization.name
        return "No organization"
    teacher_organization.short_description = "Organization"
    teacher_organization.admin_order_field = 'teacher__organization__name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'teacher', 'teacher__organization', 'teacher__state', 'teacher__region', 
            'gender_identity', 'disc_assessment_type', 'sixteen_types_assessment', 
            'enneagram_result', 'osha_type', 'funding_source'
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


# -------------------------
# Student File Admin
# -------------------------
@admin.register(StudentFile)
class StudentFileAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'student_name', 'content_type', 'file_size_display', 'uploaded_at', 'view_file_link', 'download_file_link')
    list_filter = ('content_type', 'uploaded_at', 'student__teacher__organization')
    search_fields = ('original_name', 'student__full_name', 'student__email')
    readonly_fields = ('uploaded_at', 'file_size_display', 'file_extension', 'size_bytes', 'file_preview')
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('File Information', {
            'fields': ('original_name', 'file', 'content_type')
        }),
        ('Student Association', {
            'fields': ('student', 'uploaded_by')
        }),
        ('File Preview', {
            'fields': ('file_preview',),
        }),
        ('File Details', {
            'fields': ('size_bytes', 'file_size_display', 'file_extension', 'uploaded_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_name(self, obj):
        return obj.student.full_name
    student_name.short_description = "Student"
    student_name.admin_order_field = 'student__full_name'
    
    def file_size_display(self, obj):
        """Display file size in human readable format"""
        if obj.size_bytes:
            size = obj.size_bytes
            if size < 1024:
                return f"{size} bytes"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        return "Unknown"
    file_size_display.short_description = "File Size"
    
    def file_extension(self, obj):
        """Get file extension from original_name"""
        if obj.original_name:
            return obj.original_name.split('.')[-1].upper() if '.' in obj.original_name else 'None'
        return 'None'
    file_extension.short_description = "Extension"
    
    def _generate_signed_url(self, obj, as_attachment=False):
        """Generate a signed S3 URL for the file"""
        if not obj.file:
            return None
        
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            params = {
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': obj.file.name
            }
            
            if as_attachment:
                params['ResponseContentDisposition'] = f'attachment; filename="{obj.original_name}"'
            
            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=3600  # 1 hour
            )
            
            return signed_url
            
        except Exception as e:
            return None
    
    def view_file_link(self, obj):
        """Generate a view link for the file"""
        signed_url = self._generate_signed_url(obj, as_attachment=False)
        
        if signed_url:
            return format_html(
                '<a href="{}" target="_blank" class="button" style="background-color: #417690; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">🔍 View</a>',
                signed_url
            )
        else:
            return format_html('<span style="color: #999;">No file</span>')
    
    view_file_link.short_description = "View File"
    
    def download_file_link(self, obj):
        """Generate a download link for the file"""
        signed_url = self._generate_signed_url(obj, as_attachment=True)
        
        if signed_url:
            return format_html(
                '<a href="{}" class="button" style="background-color: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">📥 Download</a>',
                signed_url
            )
        else:
            return format_html('<span style="color: #999;">No file</span>')
    
    download_file_link.short_description = "Download"
    
    def file_preview(self, obj):
        """Show file preview with signed URL"""
        if not obj.file:
            return format_html('<span style="color: #999;">No file uploaded</span>')
        
        signed_url = self._generate_signed_url(obj, as_attachment=False)
        
        if not signed_url:
            return format_html('<span style="color: #d32f2f;">Error generating preview URL</span>')
        
        # File information
        file_info = format_html(
            '''
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; color: #333;">
                <h4 style="margin: 0 0 10px 0; color: #333;">File Information</h4>
                <p style="color: #333;"><strong>Original Name:</strong> {}</p>
                <p style="color: #333;"><strong>S3 Path:</strong> {}</p>
                <p style="color: #333;"><strong>Size:</strong> {}</p>
                <p style="color: #333;"><strong>Type:</strong> {}</p>
                <p style="color: #333;"><strong>Uploaded:</strong> {}</p>
            </div>
            ''',
            obj.original_name,
            obj.file.name,
            self.file_size_display(obj),
            obj.content_type,
            obj.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # PDF preview
        if obj.content_type == 'application/pdf':
            preview = format_html(
                '''
                <div style="margin: 15px 0;">
                    <h4 style="color: #333;">PDF Preview</h4>
                    <iframe src="{}" width="100%" height="400" style="border: 1px solid #ddd; border-radius: 4px;"></iframe>
                </div>
                ''',
                signed_url
            )
        else:
            preview = format_html(
                '''
                <div style="margin: 15px 0;">
                    <p style="color: #666;"><em>Preview not available for this file type</em></p>
                </div>
                '''
            )
        
        # Action buttons
        buttons = format_html(
            '''
            <div style="margin: 15px 0;">
                <a href="{}" target="_blank" class="button" style="background-color: #417690; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; margin-right: 10px;">🔍 Open in New Tab</a>
                <a href="{}" class="button" style="background-color: #28a745; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px;">📥 Download File</a>
            </div>
            ''',
            signed_url,
            self._generate_signed_url(obj, as_attachment=True) or signed_url
        )
        
        return format_html('{}<hr>{}<hr>{}', file_info, preview, buttons)
    
    file_preview.short_description = "File Preview & Actions"
    