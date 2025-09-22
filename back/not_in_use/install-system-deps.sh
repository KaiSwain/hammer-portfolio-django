#!/bin/bash
set -e

echo "Installing system dependencies for WeasyPrint..."

# Try to install required system packages
apt-get update || echo "apt-get update failed, continuing..."

# WeasyPrint system dependencies
apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libharfbuzz0b \
    libfontconfig1 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libgobject-2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libgio-2.0-0 \
    libcairo-gobject2 \
    || echo "System package installation failed, will continue without WeasyPrint"

echo "System dependency installation complete"
