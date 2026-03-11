#!/bin/bash
# Script para configurar Quilombo no PythonAnywhere
# Execute este script no console Bash do PythonAnywhere

echo "=== SETUP QUILOMBO ARAUCÁRIA NO PYTHONANYWHERE ==="

# 1. Clonar repositório
git clone https://github.com/JoseVictorRodrigues/Quilombo.git
cd Quilombo/quilombo_site

# 2. Criar ambiente virtual
python3.10 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configurar settings para produção
cat > .env << EOF
SECRET_KEY=addb5e2f61accc316ea44e049989d6ff397c3d9cbc38365f6608f4cd2a9b8f36a158e5eb0ac7439bf4f5ed1cf41b50284d00
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
EOF

# 5. Executar migrações e coletar arquivos estáticos
python manage.py migrate
python manage.py collectstatic --noinput

# 6. Criar superusuário (interativo)
echo "Criando superusuário..."
python manage.py createsuperuser

echo ""
echo "=== SETUP COMPLETO! ==="
echo ""
echo "PRÓXIMOS PASSOS:"
echo "1. Vá para Web tab no dashboard"  
echo "2. Add a new web app >> Manual configuration >> Python 3.10"
echo "3. Em Source code: /home/yourusername/Quilombo/quilombo_site"
echo "4. Em Virtualenv: /home/yourusername/Quilombo/quilombo_site/venv"
echo "5. Edite WSGI file e cole o código que está em wsgi_pythonanywhere.py"
echo "6. Em Static files adicione:"
echo "   URL: /static/   Directory: /home/yourusername/Quilombo/quilombo_site/staticfiles/"
echo "   URL: /media/    Directory: /home/yourusername/Quilombo/quilombo_site/media/"
echo "7. Reload the web app"
echo ""
echo "Seu site estará em: https://yourusername.pythonanywhere.com"