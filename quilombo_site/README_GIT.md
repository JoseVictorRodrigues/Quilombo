# Publicar no GitHub — Quilombo Araucária

Execute os comandos abaixo **dentro da pasta `quilombo_site`** (onde está o `manage.py`).

---

## 1. Inicializar o repositório Git

```powershell
cd C:\Users\monoc\Documents\Projects\Quilombo\quilombo_site
git init
git branch -M main
```

## 2. Confirmar que o .gitignore está correto

```powershell
# Verifica quais arquivos serão enviados (não deve incluir .env, db.sqlite3, media/, staticfiles/)
git status
```

## 3. Adicionar todos os arquivos e criar o commit inicial

```powershell
git add .
git commit -m "feat: versão inicial do site Quilombo Araucária"
```

## 4. Criar o repositório no GitHub

Acesse https://github.com/new e crie um repositório com o nome:

```
quilombo-araucaria-site
```

- Visibilidade: **Privado** (recomendado — o `.env.example` deixa claro o que não deve ser exposto)
- **NÃO** marque "Initialize with README" (já temos o nosso)

## 5. Conectar e enviar

Substitua `SEU_USUARIO` pelo seu nome de usuário no GitHub:

```powershell
git remote add origin https://github.com/SEU_USUARIO/quilombo-araucaria-site.git
git push -u origin main
```

---

## Comandos do dia a dia

```powershell
# Ver o que mudou
git status

# Adicionar mudanças
git add .

# Criar commit
git commit -m "descrição do que foi feito"

# Enviar para o GitHub
git push
```

---

## Antes de cada deploy

1. Copie `.env.example` → `.env` e preencha com valores reais de produção.
2. Execute `python manage.py collectstatic --noinput`
3. Configure `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` com o domínio real.
4. Nunca commite o arquivo `.env` — ele está no `.gitignore`.
