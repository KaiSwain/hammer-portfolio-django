"""
Student Files API Views for Hammer Portfolio Django Backend

Handles file upload, listing, downloading, and deletion for student files.
Follows the existing authentication and API patterns.
"""

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from hammer_backendapi.models import Student, StudentFile
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_student_files(request, student_id):
    """List all files for a student - matches existing API patterns"""
    try:
        student = get_object_or_404(Student, pk=student_id)
        
        # Get all files for this student
        student_files = StudentFile.objects.filter(student=student).order_by('-uploaded_at')
        
        # Return files for this student with metadata
        files = []
        for file_obj in student_files:
            file_data = {
                'id': file_obj.id,
                'original_filename': file_obj.original_name,  # Match frontend expectation
                'content_type': file_obj.content_type,
                'file_size': file_obj.size_bytes,  # Use correct field name
                'uploaded_at': file_obj.uploaded_at.isoformat() if file_obj.uploaded_at else None,
                'uploaded_by_name': file_obj.uploaded_by.username if file_obj.uploaded_by else None,
            }
            files.append(file_data)
        
        # Return just the array of files for frontend compatibility
        return Response(files)
    except Exception as e:
        logger.error(f"Error listing files for student {student_id}: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_student_file(request, student_id):
    """Upload a file for a student - follows token auth pattern"""
    try:
        student = get_object_or_404(Student, pk=student_id)
        
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        
        # Validate file size (100MB limit for all file types)
        max_size = 100 * 1024 * 1024  # 100MB
        if uploaded_file.size > max_size:
            return Response({'error': f'File size exceeds {max_size // (1024*1024)}MB limit'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Security: Block potentially dangerous file types
        dangerous_types = [
            'application/x-executable', 'application/x-msdownload', 'application/x-msdos-program',
            'application/x-sh', 'application/x-shellscript', 'text/x-shellscript'
        ]
        if uploaded_file.content_type in dangerous_types:
            return Response({'error': 'File type not allowed for security reasons'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create StudentFile record
        student_file = StudentFile.objects.create(
            student=student,
            file=uploaded_file,
            original_name=uploaded_file.name,
            content_type=uploaded_file.content_type,
            size_bytes=uploaded_file.size,
            uploaded_by=request.user
        )
        
        logger.info(f"File uploaded successfully: {uploaded_file.name} for student {student_id} by user {request.user}")
        
        return Response({
            'id': student_file.id,
            'message': 'File uploaded successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error uploading file for student {student_id}: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_student_file(request, file_id):
    """Delete a student file"""
    try:
        student_file = get_object_or_404(StudentFile, pk=file_id)
        
        # Log the deletion for audit purposes
        logger.info(f"Deleting file: {student_file.original_name} (ID: {file_id}) for student {student_file.student.id} by user {request.user}")
        
        # Delete the actual file from storage
        student_file.file.delete(save=False)
        student_file.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    except Exception as e:
        logger.error(f"Error deleting file {file_id}: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_student_file(request, file_id):
    """Get download URL for a student file"""
    try:
        student_file = get_object_or_404(StudentFile, pk=file_id)
        
        # Log the download for audit purposes
        logger.info(f"File download requested: {student_file.original_name} (ID: {file_id}) by user {request.user}")
        
        # Return download information (URL will be signed for S3 in production)
        return Response({
            'download_url': student_file.file.url,
            'filename': student_file.original_name,
            'content_type': student_file.content_type,
            'size_bytes': student_file.size_bytes
        })
        
    except Exception as e:
        logger.error(f"Error getting download URL for file {file_id}: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)