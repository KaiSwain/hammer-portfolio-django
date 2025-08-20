# Django Log Files

# This directory contains Django application logs
# These files are automatically created by the Django logging configuration

# Log files:
# - django.log: General Django application logs
# - error.log: Error-specific logs (if configured)
# - access.log: Request access logs (if configured)

# In production, these logs should be:
# 1. Regularly rotated to prevent disk space issues
# 2. Monitored for errors and performance issues
# 3. Backed up as part of your monitoring strategy

# Log rotation can be set up using logrotate:
# sudo nano /etc/logrotate.d/django-hammer-portfolio

# Example logrotate configuration:
# /path/to/hammer-portfolio-django/back/logs/*.log {
#     daily
#     missingok
#     rotate 52
#     compress
#     delaycompress
#     notifempty
#     create 644 django django
# }
