#!/bin/bash
# Script de build para Vercel: instala dependencias y recolecta estáticos.
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
