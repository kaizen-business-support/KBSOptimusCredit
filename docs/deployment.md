# Guide de Déploiement - Outil d'Analyse Financière BCEAO v2.0

## 🎯 Vue d'Ensemble du Déploiement

Ce guide détaille la procédure complète de déploiement de l'outil d'analyse financière BCEAO, de l'installation locale jusqu'à la mise en production sur Streamlit Cloud ou serveurs dédiés.

### 🏗️ Architecture de Déploiement

```
Production Environment
├── Streamlit Cloud (Recommandé)
│   ├── Auto-deployment depuis GitHub
│   ├── Scaling automatique
│   └── HTTPS inclus
├── Serveur Dédié (Alternative)
│   ├── Docker containerization
│   ├── Nginx reverse proxy
│   └── SSL/TLS configuration
└── Développement Local
    ├── Python virtual environment
    ├── Streamlit development server
    └── Tests et debugging
```

## 📋 Prérequis Système

### Environnement Minimum

- **Python** : 3.8 ou supérieur
- **RAM** : 2 GB minimum, 4 GB recommandé
- **Stockage** : 500 MB d'espace libre
- **OS** : Windows 10+, macOS 10.14+, Ubuntu 18.04+ ou CentOS 7+

### Dépendances Logicielles

```bash
# Vérifier la version Python
python --version  # Doit être >= 3.8

# Installer pip si nécessaire
python -m ensurepip --upgrade

# Vérifier Git
git --version
```

### Comptes et Accès Requis

- **GitHub** : Pour le code source et déploiement automatique
- **Streamlit Cloud** : Pour l'hébergement (gratuit)
- **Email BCEAO** : Pour la configuration des alertes

## 🚀 Installation Locale

### Étape 1 : Récupération du Code Source

```bash
# Cloner le repository
git clone https://github.com/bceao/financial-analyzer.git
cd financial-analyzer

# Vérifier la structure
ls -la
```

### Étape 2 : Configuration de l'Environnement

```bash
# Créer un environnement virtuel
python -m venv venv

# Activation de l'environnement
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate

# Vérifier l'activation
which python  # Doit pointer vers venv/
```

### Étape 3 : Installation des Dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Vérifier les installations
pip list | grep streamlit
pip list | grep pandas
```

### Étape 4 : Configuration Initiale

```bash
# Créer la structure des dossiers
mkdir -p data assets docs tests
mkdir -p modules/{core,components,pages,utils}

# Créer les fichiers __init__.py
touch modules/__init__.py
touch modules/core/__init__.py
touch modules/components/__init__.py
touch modules/pages/__init__.py
touch modules/utils/__init__.py

# Copier les fichiers de données
cp data/bceao_norms.json.example data/bceao_norms.json
cp data/sectoral_norms.json.example data/sectoral_norms.json
```

### Étape 5 : Test de l'Installation

```bash
# Lancer l'application
streamlit run main.py

# Vérifier l'accès
# Ouvrir http://localhost:8501 dans le navigateur
```

## 🐳 Déploiement avec Docker

### Création du Dockerfile

```dockerfile
FROM python:3.9-slim

# Métadonnées
LABEL maintainer="BCEAO IT Team <support@bceao.int>"
LABEL version="2.0"
LABEL description="Outil d'Analyse Financière BCEAO"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Port exposé
EXPOSE 8501

# Commande de démarrage
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Construction et Test du Container

```bash
# Construction de l'image
docker build -t bceao-financial-analyzer:2.0 .

# Test local du container
docker run -p 8501:8501 bceao-financial-analyzer:2.0

# Vérifier l'accès
curl http://localhost:8501
```

### Docker Compose (Optionnel)

```yaml
# docker-compose.yml
version: '3.8'

services:
  financial-analyzer:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
    volumes:
      - ./data:/app/data:ro
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - financial-analyzer
    restart: unless-stopped
```

## ☁️ Déploiement Streamlit Cloud

### Étape 1 : Préparation du Repository GitHub

```bash
# Pousser le code vers GitHub
git add .
git commit -m "Initial commit for deployment"
git push origin main

# Vérifier que tous les fichiers sont présents
# - main.py
# - requirements.txt
# - modules/
# - data/
# - .streamlit/config.toml
```

### Étape 2 : Configuration Streamlit Cloud

1. **Connexion à Streamlit Cloud**
   - Aller sur https://share.streamlit.io
   - Se connecter avec GitHub
   - Autoriser l'accès aux repositories

2. **Création de l'Application**
   - Cliquer sur "New app"
   - Sélectionner le repository `bceao/financial-analyzer`
   - Branch : `main`
   - Main file path : `main.py`
   - App URL : `bceao-financial-analyzer` (personnalisable)

3. **Configuration des Secrets**
   ```toml
   # Dans Advanced settings > Secrets
   [general]
   support_email = "support@bceao.int"
   admin_password = "votre_mot_de_passe_admin"
   
   [database]
   connection_string = "postgresql://user:pass@host:port/db"
   ```

### Étape 3 : Déploiement et Vérification

```bash
# Le déploiement est automatique après push
git push origin main

# URL de l'application : 
# https://bceao-financial-analyzer.streamlit.app
```

### Étape 4 : Configuration du Domaine Personnalisé (Optionnel)

1. **Configuration DNS**
   ```
   Type: CNAME
   Name: outils-analyse (ou sous-domaine souhaité)
   Value: bceao-financial-analyzer.streamlit.app
   TTL: 300
   ```

2. **Certificat SSL**
   - Automatiquement géré par Streamlit Cloud
   - Renouvellement automatique

## 🖥️ Déploiement Serveur Dédié

### Configuration du Serveur

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git

# CentOS/RHEL
sudo yum update
sudo yum install -y python3 python3-pip nginx git
```

### Installation de l'Application

```bash
# Créer un utilisateur dédié
sudo useradd -m -s /bin/bash streamlit
sudo su - streamlit

# Cloner et installer
git clone https://github.com/bceao/financial-analyzer.git
cd financial-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration Systemd

```ini
# /etc/systemd/system/financial-analyzer.service
[Unit]
Description=BCEAO Financial Analyzer
After=network.target

[Service]
Type=simple
User=streamlit
WorkingDirectory=/home/streamlit/financial-analyzer
Environment=PATH=/home/streamlit/financial-analyzer/venv/bin
ExecStart=/home/streamlit/financial-analyzer/venv/bin/streamlit run main.py --server.port=8501
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Activer le service
sudo systemctl daemon-reload
sudo systemctl enable financial-analyzer
sudo systemctl start financial-analyzer
sudo systemctl status financial-analyzer
```

### Configuration Nginx

```nginx
# /etc/nginx/sites-available/financial-analyzer
server {
    listen 80;
    server_name outils-analyse.bceao.int;
    
    # Redirection HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name outils-analyse.bceao.int;
    
    # Certificats SSL
    ssl_certificate /etc/ssl/certs/bceao.crt;
    ssl_certificate_key /etc/ssl/private/bceao.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    # Proxy vers Streamlit
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_read_timeout 86400;
    }
    
    # Fichiers statiques
    location /static {
        alias /home/streamlit/financial-analyzer/assets;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Activer la configuration
sudo ln -s /etc/nginx/sites-available/financial-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔧 Configuration Avancée

### Variables d'Environnement

```bash
# .env (pour développement local)
STREAMLIT_THEME_PRIMARY_COLOR="#1e3a8a"
STREAMLIT_THEME_BACKGROUND_COLOR="#ffffff"
STREAMLIT_SERVER_PORT=8501
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

BCEAO_SUPPORT_EMAIL="support@bceao.int"
BCEAO_API_BASE_URL="https://api.bceao.int"
LOG_LEVEL="INFO"
```

### Configuration Streamlit Avancée

```toml
# .streamlit/config.toml
[global]
developmentMode = false
logLevel = "info"

[server]
runOnSave = false
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 50
maxMessageSize = 50

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[theme]
primaryColor = "#1e3a8a"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
caching = true
displayEnabled = true
```

### Logs et Monitoring

```python
# Configuration des logs
import logging
import sys
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/financial_analyzer_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('financial_analyzer')
```

### Sauvegarde et Restauration

```bash
#!/bin/bash
# backup.sh - Script de sauvegarde

BACKUP_DIR="/backup/financial-analyzer"
DATE=$(date +"%Y%m%d_%H%M%S")

# Créer le répertoire de sauvegarde
mkdir -p $BACKUP_DIR

# Sauvegarder le code source
tar -czf $BACKUP_DIR/source_$DATE.tar.gz /home/streamlit/financial-analyzer

# Sauvegarder les données
cp -r /home/streamlit/financial-analyzer/data $BACKUP_DIR/data_$DATE

# Sauvegarder les logs
cp -r /home/streamlit/financial-analyzer/logs $BACKUP_DIR/logs_$DATE

# Nettoyer les sauvegardes anciennes (garder 30 jours)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Sauvegarde terminée : $DATE"
```

## 📊 Monitoring et Maintenance

### Health Checks

```python
# health_check.py
import requests
import json
import smtplib
from email.mime.text import MIMEText

def check_application_health():
    """Vérifie la santé de l'application"""
    try:
        response = requests.get("http://localhost:8501", timeout=10)
        if response.status_code == 200:
            return True, "Application fonctionnelle"
        else:
            return False, f"Code de statut: {response.status_code}"
    except Exception as e:
        return False, f"Erreur de connexion: {str(e)}"

def send_alert(message):
    """Envoie une alerte par email"""
    msg = MIMEText(message)
    msg['Subject'] = 'Alerte - Outil Analyse Financière BCEAO'
    msg['From'] = 'monitoring@bceao.int'
    msg['To'] = 'admin@bceao.int'
    
    # Configuration SMTP
    server = smtplib.SMTP('smtp.bceao.int', 587)
    server.starttls()
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    is_healthy, message = check_application_health()
    if not is_healthy:
        send_alert(f"Application indisponible: {message}")
```

### Cron Jobs de Maintenance

```bash
# Crontab configuration
# crontab -e

# Health check toutes les 5 minutes
*/5 * * * * /home/streamlit/financial-analyzer/scripts/health_check.py

# Sauvegarde quotidienne à 2h00
0 2 * * * /home/streamlit/financial-analyzer/scripts/backup.sh

# Nettoyage des logs hebdomadaire
0 3 * * 0 find /home/streamlit/financial-analyzer/logs -name "*.log" -mtime +7 -delete

# Mise à jour des normes mensuellement
0 4 1 * * /home/streamlit/financial-analyzer/scripts/update_norms.py
```

### Métriques de Performance

```python
# metrics.py
import psutil
import time
import json
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
    
    def get_system_metrics(self):
        """Collecte les métriques système"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'uptime': time.time() - self.start_time
        }
    
    def log_metrics(self):
        """Enregistre les métriques"""
        metrics = self.get_system_metrics()
        
        with open('logs/metrics.log', 'a') as f:
            f.write(json.dumps(metrics) + '\n')
        
        return metrics

# Utilisation
monitor = PerformanceMonitor()
metrics = monitor.log_metrics()
```

## 🔄 Mise à Jour et Déploiement Continu

### Stratégie de Déploiement

```mermaid
graph LR
    A[Développement] --> B[Tests Locaux]
    B --> C[Push GitHub]
    C --> D[Tests Automatisés]
    D --> E[Déploiement Staging]
    E --> F[Tests d'Intégration]
    F --> G[Déploiement Production]
    G --> H[Monitoring]
```

### Script de Mise à Jour

```bash
#!/bin/bash
# update.sh - Script de mise à jour

set -e  # Arrêt en cas d'erreur

echo "🚀 Début de la mise à jour..."

# Variables
APP_DIR="/home/streamlit/financial-analyzer"
BACKUP_DIR="/backup/pre-update-$(date +%Y%m%d_%H%M%S)"
SERVICE_NAME="financial-analyzer"

# 1. Créer une sauvegarde
echo "📦 Création de la sauvegarde..."
sudo mkdir -p $BACKUP_DIR
sudo cp -r $APP_DIR $BACKUP_DIR/

# 2. Arrêter le service
echo "⏹️ Arrêt du service..."
sudo systemctl stop $SERVICE_NAME

# 3. Mettre à jour le code
echo "📥 Téléchargement des mises à jour..."
cd $APP_DIR
git fetch origin
git checkout main
git pull origin main

# 4. Mettre à jour les dépendances si nécessaire
echo "📚 Vérification des dépendances..."
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 5. Exécuter les migrations/scripts de mise à jour
echo "⚙️ Exécution des scripts de mise à jour..."
if [ -f "scripts/migrate.py" ]; then
    python scripts/migrate.py
fi

# 6. Redémarrer le service
echo "▶️ Redémarrage du service..."
sudo systemctl start $SERVICE_NAME
sudo systemctl status $SERVICE_NAME

# 7. Vérifier la santé de l'application
echo "🏥 Vérification de la santé..."
sleep 10
python scripts/health_check.py

echo "✅ Mise à jour terminée avec succès!"
```

### GitHub Actions (CI/CD)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest coverage
    
    - name: Run tests
      run: |
        coverage run -m pytest tests/
        coverage report --fail-under=80
    
    - name: Lint code
      run: |
        pip install flake8
        flake8 modules/ --count --select=E9,F63,F7,F82 --show-source --statistics
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to Streamlit Cloud
      run: |
        echo "Déploiement automatique sur Streamlit Cloud"
        # Le déploiement se fait automatiquement via GitHub
    
    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#deployments'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 🔒 Sécurité et Conformité

### Configuration SSL/TLS

```bash
# Génération de certificats Let's Encrypt
sudo apt install certbot python3-certbot-nginx

# Obtention du certificat
sudo certbot --nginx -d outils-analyse.bceao.int

# Renouvellement automatique
sudo crontab -e
# Ajouter: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Durcissement de Sécurité

```nginx
# Configuration Nginx sécurisée
server {
    # ... configuration existante ...
    
    # Headers de sécurité
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' wss:;" always;
    
    # Protection contre le clickjacking
    add_header X-Frame-Options "DENY" always;
    
    # Désactiver les signatures de serveur
    server_tokens off;
    
    # Limitation de taille d'upload
    client_max_body_size 10M;
    
    # Timeout de sécurité
    client_body_timeout 12;
    client_header_timeout 12;
    keepalive_timeout 15;
    send_timeout 10;
}
```

### Audit et Logs de Sécurité

```python
# security_audit.py
import logging
import hashlib
import os
from datetime import datetime

class SecurityAuditor:
    def __init__(self):
        self.logger = logging.getLogger('security_audit')
        handler = logging.FileHandler('logs/security.log')
        formatter = logging.Formatter('%(asctime)s - SECURITY - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_file_access(self, user_ip, file_path, action):
        """Log des accès aux fichiers sensibles"""
        self.logger.info(f"FILE_ACCESS: IP={user_ip}, FILE={file_path}, ACTION={action}")
    
    def log_analysis_request(self, user_ip, company_data_hash):
        """Log des demandes d'analyse"""
        data_hash = hashlib.sha256(str(company_data_hash).encode()).hexdigest()[:16]
        self.logger.info(f"ANALYSIS_REQUEST: IP={user_ip}, DATA_HASH={data_hash}")
    
    def check_file_integrity(self):
        """Vérification de l'intégrité des fichiers critiques"""
        critical_files = [
            'data/bceao_norms.json',
            'data/sectoral_norms.json',
            'modules/core/analyzer.py',
            'modules/core/ratios.py'
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    self.logger.info(f"FILE_INTEGRITY: {file_path} = {file_hash}")
```

## 📋 Checklist de Déploiement

### ✅ Pré-déploiement

- [ ] **Code source**
  - [ ] Repository GitHub configuré
  - [ ] Tous les fichiers committé
  - [ ] Tests unitaires passants
  - [ ] Documentation à jour

- [ ] **Configuration**
  - [ ] requirements.txt complet
  - [ ] .streamlit/config.toml configuré
  - [ ] Variables d'environnement définies
  - [ ] Données de référence présentes

- [ ] **Tests**
  - [ ] Tests locaux réussis
  - [ ] Import Excel fonctionnel
  - [ ] Calculs de ratios validés
  - [ ] Interface utilisateur complète

### ✅ Déploiement

- [ ] **Streamlit Cloud**
  - [ ] Application créée sur share.streamlit.io
  - [ ] Repository connecté
  - [ ] Secrets configurés
  - [ ] URL personnalisée définie

- [ ] **Serveur dédié (si applicable)**
  - [ ] Serveur provisionné
  - [ ] Code déployé
  - [ ] Service systemd configuré
  - [ ] Nginx configuré
  - [ ] SSL/TLS activé

### ✅ Post-déploiement

- [ ] **Vérifications**
  - [ ] Application accessible
  - [ ] Toutes les pages fonctionnelles
  - [ ] Import Excel opérationnel
  - [ ] Génération de rapports OK
  - [ ] Performance acceptable

- [ ] **Monitoring**
  - [ ] Health checks configurés
  - [ ] Logs activés
  - [ ] Alertes configurées
  - [ ] Sauvegardes programmées

- [ ] **Documentation**
  - [ ] Guide utilisateur publié
  - [ ] Référence API accessible
  - [ ] Procédures de support documentées
  - [ ] Formation équipe réalisée

## 🆘 Dépannage et Solutions

### Problèmes Courants

#### Erreur de Module Non Trouvé

```bash
# Problème
ModuleNotFoundError: No module named 'streamlit'

# Solution
pip install -r requirements.txt
# ou
pip install streamlit==1.28.0
```

#### Erreur de Port Occupé

```bash
# Problème
OSError: [Errno 98] Address already in use

# Solution
# Trouver le processus utilisant le port
lsof -i :8501

# Tuer le processus
kill -9 <PID>

# Ou utiliser un autre port
streamlit run main.py --server.port 8502
```

#### Problème de Permissions

```bash
# Problème
PermissionError: [Errno 13] Permission denied

# Solution
# Changer les permissions
chmod +x scripts/*.sh
chown -R streamlit:streamlit /home/streamlit/financial-analyzer

# Ou utiliser sudo pour les services système
sudo systemctl restart financial-analyzer
```

#### Erreur de Mémoire

```bash
# Problème
MemoryError: Unable to allocate array

# Solutions
# 1. Augmenter la mémoire du serveur
# 2. Optimiser le code
# 3. Limiter la taille des fichiers uploadés

# Configuration Streamlit
[server]
maxUploadSize = 200
maxMessageSize = 200
```

### Logs de Diagnostic

```python
# diagnostic.py
import streamlit as st
import sys
import platform
import psutil
import pandas as pd

def show_system_info():
    """Affiche les informations système pour diagnostic"""
    
    st.subheader("🔍 Informations Système")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Python**")
        st.code(f"Version: {sys.version}")
        st.code(f"Plateforme: {platform.platform()}")
        
        st.write("**Ressources**")
        st.code(f"CPU: {psutil.cpu_count()} cœurs")
        st.code(f"RAM: {psutil.virtual_memory().total // (1024**3)} GB")
    
    with col2:
        st.write("**Streamlit**")
        st.code(f"Version: {st.__version__}")
        
        st.write("**Modules Importés**")
        modules = ['pandas', 'numpy', 'plotly', 'openpyxl']
        for module in modules:
            try:
                mod = __import__(module)
                st.code(f"{module}: {getattr(mod, '__version__', 'OK')}")
            except ImportError:
                st.error(f"{module}: Non installé")

# Ajout dans le menu de développement
if st.sidebar.button("🔧 Diagnostic Système"):
    show_system_info()
```

## 📞 Support et Contacts

### Équipe Technique BCEAO

- **Chef de Projet** : chef.projet@bceao.int
- **Développeur Senior** : dev.senior@bceao.int
- **Analyste Financier** : analyste.financier@bceao.int
- **Support Utilisateur** : support@bceao.int

### Escalade des Incidents

1. **Niveau 1** : Support utilisateur (support@bceao.int)
2. **Niveau 2** : Équipe technique (dev.senior@bceao.int)
3. **Niveau 3** : Chef de projet (chef.projet@bceao.int)
4. **Niveau 4** : Direction IT BCEAO

### Ressources Utiles

- **Documentation** : https://bceao.int/outils-analyse/docs
- **Repository GitHub** : https://github.com/bceao/financial-analyzer
- **Status Page** : https://status.bceao.int
- **Formation** : formation@bceao.int

## 🔄 Évolutions et Roadmap

### Version 2.1 (Q2 2025)

- [ ] API REST complète
- [ ] Support multi-devises (USD, EUR)
- [ ] Analyses comparatives temporelles
- [ ] Module de prévisions financières
- [ ] Tableaux de bord personnalisables
- [ ] Intégration webhook

### Version 3.0 (Q4 2025)

- [ ] Intelligence artificielle prédictive
- [ ] Détection automatique d'anomalies
- [ ] Benchmarking international
- [ ] Interface mobile native
- [ ] Intégration comptabilité temps réel
- [ ] Blockchain pour audit trail

### Améliorations Techniques

- [ ] Migration vers FastAPI + React
- [ ] Base de données PostgreSQL
- [ ] Cache Redis
- [ ] Microservices architecture
- [ ] Kubernetes deployment
- [ ] GraphQL API

---

**© 2024 BCEAO - Guide de Déploiement v2.0**

*Ce guide est maintenu à jour avec chaque version. Pour les dernières procédures, consultez le repository GitHub officiel.*

---

## 📎 Annexes

### Annexe A : Commandes de Maintenance

```bash
# Redémarrage complet
sudo systemctl restart financial-analyzer nginx

# Vérification des logs
tail -f /home/streamlit/financial-analyzer/logs/app.log
journalctl -u financial-analyzer -f

# Nettoyage du cache
rm -rf /home/streamlit/financial-analyzer/__pycache__
rm -rf /home/streamlit/financial-analyzer/modules/__pycache__

# Vérification de l'espace disque
df -h
du -sh /home/streamlit/financial-analyzer

# Test de connectivité
curl -I https://outils-analyse.bceao.int
wget --spider https://outils-analyse.bceao.int
```

### Annexe B : Configuration Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Iptables (CentOS/RHEL)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables-save > /etc/iptables.rules
```

### Annexe C : Script de Rollback

```bash
#!/bin/bash
# rollback.sh - Script de retour en arrière

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <backup_directory>"
    exit 1
fi

BACKUP_DIR=$1
APP_DIR="/home/streamlit/financial-analyzer"
SERVICE_NAME="financial-analyzer"

echo "🔄 Début du rollback depuis $BACKUP_DIR"

# Arrêter le service
sudo systemctl stop $SERVICE_NAME

# Restaurer depuis la sauvegarde
sudo rm -rf $APP_DIR
sudo cp -r $BACKUP_DIR $APP_DIR
sudo chown -R streamlit:streamlit $APP_DIR

# Redémarrer le service
sudo systemctl start $SERVICE_NAME

echo "✅ Rollback terminé"
```