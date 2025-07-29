from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from .models import Teacher, Student, Organization

# -------------------------
# Teacher Admin
# -------------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'organization', 'user')
    search_fields = ('full_name', 'email')
    list_filter = ('organization',)
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        """
        When saving a Teacher:
        - If no linked User exists, create one automatically.
        - Assign an auth token to that user.
        """
        if not obj.user:
            # Generate random password if teacher.password is blank
            raw_password = obj.password if obj.password else get_random_string(10)

            # Create linked Django user
            user = User.objects.create_user(
                username=obj.email,
                email=obj.email,
                password=raw_password
            )
            obj.user = user

            # Create an API Token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Show credentials in Django Admin success message
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
    list_display = ('full_name', 'teacher', 'start_date', 'end_date', 'created_at')
    search_fields = ('full_name',)
    list_filter = ('teacher', 'start_date', 'end_date')


# -------------------------
# Organization Admin
# -------------------------
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    