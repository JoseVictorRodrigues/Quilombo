# Deploy Rápido - PythonAnywhere

## Passo a passo (5 minutos):

### 1. Criar conta
- Vá em https://www.pythonanywhere.com
- Clique "Create a Beginner account" (gratuito)
- Faça cadastro

### 2. Setup no console  
- Dashboard → Tasks → "$ Bash console"
- Cole e execute:
```bash
wget https://raw.githubusercontent.com/JoseVictorRodrigues/Quilombo/main/quilombo_site/setup_pythonanywhere.sh
bash setup_pythonanywhere.sh
```

### 3. Configurar Web App
- Dashboard → Web 
- "Add a new web app" → "Manual configuration" → Python 3.10
- Source code: `/home/SEUUSERNAME/Quilombo/quilombo_site`
- Virtualenv: `/home/SEUUSERNAME/Quilombo/quilombo_site/venv`

### 4. WSGI file
- Clique "WSGI configuration file" 
- Apague tudo e cole o conteúdo de `wsgi_pythonanywhere.py`
- Mude `yourusername` pelo seu username real

### 5. Static files
- Na seção "Static files" adicione:
  - URL: `/static/` Directory: `/home/SEUUSERNAME/Quilombo/quilombo_site/staticfiles/`
  - URL: `/media/` Directory: `/home/SEUUSERNAME/Quilombo/quilombo_site/media/`

### 6. Reload
- Clique botão "Reload" (verde)
- Acesse: `https://SEUUSERNAME.pythonanywhere.com`

**Total: ~5 minutos. Site online.**