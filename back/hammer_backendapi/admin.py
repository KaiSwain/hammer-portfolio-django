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
    OshaType
)

# -------------------------
# Teacher Admin
# -------------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'organization', 'user_id')  # show IDs
    search_fields = ('id', 'full_name', 'email')
    list_filter = ('organization',)
    exclude = ('user',)
    readonly_fields = ('id',)  # show ID on form as read-only
    ordering = ('id',)

    def user_id(self, obj):
        return obj.user_id
    user_id.short_description = "User ID"

    def save_model(self, request, obj, form, change):
        if not obj.user:
            raw_password = obj.password if obj.password else get_random_string(10)
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
                f"✅ Teacher '{obj.full_name}' created. "
                f"Login: {obj.email} | Password: {raw_password} | Token: {token.key}"
            )
        super().save_model(request, obj, form, change)


# -------------------------
# Student Admin
# -------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # show ID + raw FK IDs alongside human names
    list_display = (
        'id',
        'full_name',
        'teacher', 'teacher_id',
        'gender_identity', 'gender_identity_id',
        'disc_assessment_type', 'disc_assessment_type_id',
        'sixteen_types_assessment', 'sixteen_types_assessment_id',
        'enneagram_result', 'enneagram_result_id',
        'osha_type', 'osha_type_id',
        'start_date', 'end_date',
        'created_at',
    )
    search_fields = (
        'id', 'full_name',
        'teacher__full_name',
        'gender_identity__gender',
        'disc_assessment_type__type_name',
        'sixteen_types_assessment__type_name',
        'enneagram_result__result_name',
        'osha_type__name',
    )
    list_filter = ('teacher', 'gender_identity', 'start_date', 'end_date', 'created_at')
    autocomplete_fields = ('teacher', 'gender_identity', 'disc_assessment_type',
                           'sixteen_types_assessment', 'enneagram_result', 'osha_type')
    readonly_fields = ('id',)
    ordering = ('id',)


# -------------------------
# Organization Admin
# -------------------------
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    readonly_fields = ('id',)
    ordering = ('id',)


# -------------------------
# Lookup Models
# -------------------------
@admin.register(GenderIdentity)
class GenderIdentityAdmin(admin.ModelAdmin):
    list_display = ('id', 'gender')
    search_fields = ('id', 'gender')
    readonly_fields = ('id',)
    ordering = ('id',)


@admin.register(DiscAssessment)
class DiscAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    search_fields = ('id', 'type_name')
    readonly_fields = ('id',)
    ordering = ('id',)


@admin.register(SixteenTypeAssessment)
class SixteenTypeAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    search_fields = ('id', 'type_name')
    readonly_fields = ('id',)
    ordering = ('id',)


@admin.register(EnneagramResult)
class EnneagramResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'result_name')
    search_fields = ('id', 'result_name')
    readonly_fields = ('id',)
    ordering = ('id',)


@admin.register(OshaType)
class OshaTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    readonly_fields = ('id',)
    ordering = ('id',)
    