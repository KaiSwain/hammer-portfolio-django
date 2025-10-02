from django.core.management.base import BaseCommand
from hammer_backendapi.models import StudentFile
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Clean up student file records that no longer exist in S3'

    def handle(self, *args, **options):
        orphaned_files = []
        total_files = StudentFile.objects.count()
        
        self.stdout.write(f'Checking {total_files} student file records...')
        
        for student_file in StudentFile.objects.all():
            # Check if file exists in storage (S3)
            if not default_storage.exists(student_file.file.name):
                orphaned_files.append(student_file)
                self.stdout.write(f'Orphaned: {student_file.original_name} (ID: {student_file.id})')
        
        if orphaned_files:
            self.stdout.write(f'\nFound {len(orphaned_files)} orphaned records.')
            confirm = input('Delete these orphaned records? (yes/no): ')
            
            if confirm.lower() == 'yes':
                deleted_count = 0
                for student_file in orphaned_files:
                    student_file.delete()
                    deleted_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully deleted {deleted_count} orphaned file records.')
                )
            else:
                self.stdout.write('Operation cancelled.')
        else:
            self.stdout.write(self.style.SUCCESS('No orphaned records found.'))