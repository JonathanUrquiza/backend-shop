#!/usr/bin/env bash
# Build script para Render

set -o errexit  # Exit on error

echo "Building Django application..."

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos (omitir si falla)
python manage.py collectstatic --no-input || echo "Warning: collectstatic failed, continuing..."

echo "Build completed successfully!"

