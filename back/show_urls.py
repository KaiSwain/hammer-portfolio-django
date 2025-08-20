#!/usr/bin/env python

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()

from django.urls import get_resolver
from django.conf import settings

def show_urls():
    """Display all URL patterns"""
    print("🔍 Available URL Patterns:")
    print("=" * 50)
    
    resolver = get_resolver()
    
    def print_urls(patterns, prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                # This is an include() pattern
                new_prefix = prefix + str(pattern.pattern)
                print(f"{new_prefix} (include)")
                print_urls(pattern.url_patterns, new_prefix)
            else:
                # This is a regular pattern
                full_pattern = prefix + str(pattern.pattern)
                name = getattr(pattern, 'name', 'no-name')
                print(f"  {full_pattern} [{name}]")
    
    print_urls(resolver.url_patterns)
    
    print("\n" + "=" * 50)
    print("🧪 Test these URLs:")
    print("• http://localhost:8000/api/students/")
    print("• http://localhost:8000/students/")
    print("• http://localhost:8000/api/health/")
    print("• http://localhost:8000/admin/")

if __name__ == "__main__":
    show_urls()
