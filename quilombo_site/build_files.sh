#!/bin/bash
# Script de build para Vercel
# Instala dependências e coleta arquivos estáticos

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
