#!/bin/bash
# Build estático para Vercel: recolecta los estáticos de Django en staticfiles_build/static
pip install Django whitenoise python-decouple
python3 manage.py collectstatic --noinput --clear
