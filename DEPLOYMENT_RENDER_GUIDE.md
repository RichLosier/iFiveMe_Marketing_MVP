# 🚀 Guide de Déploiement iFiveMe sur Render.com

## ✅ Étapes de Déploiement

### 1. Préparation du Dépôt Git
```bash
# Ajouter les nouveaux fichiers de déploiement
git add render.yaml Dockerfile DEPLOYMENT_RENDER_GUIDE.md render_setup_agent.py
git commit -m "🚀 Configuration déploiement Render.com - iFiveMe Marketing MVP prêt pour production"
```

### 2. Création du Service sur Render.com

#### A. Connexion et Nouveau Service
1. **Aller sur render.com** (déjà ouvert dans votre navigateur)
2. **Créer un compte** avec richard@ifiveme.com
3. **Cliquer "New +"** → **"Web Service"**

#### B. Configuration Repository
1. **Connect Repository**: Connecter votre dépôt GitHub iFiveMe_Marketing_MVP
2. **Branch**: `master`
3. **Root Directory**: `.` (racine du projet)

#### C. Paramètres du Service
- **Name**: `ifiveme-control-tower`
- **Region**: `Oregon (US West)` ou le plus proche
- **Branch**: `master`
- **Build Command**:
  ```bash
  pip install -r requirements.txt && npm install && npx playwright install chromium
  ```
- **Start Command**:
  ```bash
  python ifiveme_control_tower.py
  ```

#### D. Variables d'Environnement Render
```bash
# Variables requises à ajouter dans Render:
PORT=5001
HOST=0.0.0.0
FLASK_ENV=production
FLASK_DEBUG=false
PYTHON_VERSION=3.12.1
NODE_VERSION=22.19.0

# Variables secrètes (à ajouter individuellement):
IFIVEME_ADMIN_EMAIL=richard@ifiveme.com
IFIVEME_ADMIN_PASSWORD=bonjour
OPENAI_API_KEY=[Votre clé OpenAI]
ANTHROPIC_API_KEY=[Votre clé Anthropic]

# Variable Google Drive:
GOOGLE_DRIVE_FOLDER_ID=1RE8sOSWPS8YhZsaSHRLIouZV08p1iUk0
```

#### E. Plan de Service
- **Instance Type**: `Starter` ($7/mois)
- **Auto-Deploy**: `Yes` (déploiement automatique sur push Git)

### 3. Configuration Avancée

#### A. Build Settings
- **Build Command**:
  ```bash
  pip install --no-cache-dir -r requirements.txt && npm install && npx playwright install chromium --with-deps
  ```

#### B. Health Check
- **Health Check Path**: `/`
- **Health Check Timeout**: `30s`

#### C. Disk Storage
- **Disk Type**: `SSD`
- **Size**: `1 GB` (pour logs et données temporaires)

### 4. URLs d'Accès Après Déploiement

Une fois déployé, vous aurez accès aux URLs :

```
🏗️ Control Tower Principal:
https://ifiveme-control-tower.onrender.com

🌐 Interface Marketing:
https://ifiveme-control-tower.onrender.com/generate

📊 Status Agents:
https://ifiveme-control-tower.onrender.com/status

🔧 Logs Système:
Accessible via Dashboard Render.com
```

### 5. Services Secondaires (Optionnel)

#### Interface Marketing Séparée
Pour déployer l'interface web d'approbation séparément :

- **Name**: `ifiveme-web-approval`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `cd web_approval && python app.py`
- **PORT**: `8080`

### 6. Post-Déploiement

#### A. Vérification Fonctionnelle
```bash
# Tests à faire après déploiement:
1. ✅ Page d'accueil Control Tower charge
2. ✅ WebSocket connexion fonctionne
3. ✅ 7 agents listés correctement
4. ✅ Interface génération posts accessible
5. ✅ Logs pas d'erreurs critiques
```

#### B. Configuration DNS (Optionnel)
Pour utiliser un domaine personnalisé :
1. **Render Dashboard** → **Settings** → **Custom Domain**
2. Ajouter : `control.ifiveme.com`
3. Configurer CNAME chez votre registraire de domaines

### 7. Monitoring et Maintenance

#### A. Logs en Temps Réel
```bash
# Via Render Dashboard:
- Logs → Live tail
- Events → Deploy history
- Metrics → Performance data
```

#### B. Redémarrage
- **Manuel**: Button "Manual Deploy" dans Dashboard
- **Automatique**: Push vers branch `master`

### 8. Dépannage Commun

#### Playwright Issues
```bash
# Si erreurs Playwright, ajouter à Build Command:
apt-get update && apt-get install -y libnss3-tools
npx playwright install-deps
```

#### Memory Issues
- Upgrade vers `Starter Plus` si nécessaire
- Monitor memory usage dans Metrics

#### WebSocket Issues
- Vérifier CORS settings
- Confirmer Socket.IO version compatibility

## 🎯 Résultat Final

**Votre système iFiveMe sera accessible 24/7 :**
- ✅ **Control Tower** : Interface unifiée tous agents
- ✅ **Marketing Automation** : Posts authentiques iFiveMe
- ✅ **Admin Actions** : Connexion admin.ifiveme.com
- ✅ **Web Navigation** : Capacités illimitées
- ✅ **Observer-Think-Act** : Apprentissage continu
- ✅ **Monitoring** : Logs et métriques temps réel

**🚀 iFiveMe Marketing MVP sera déployé en production sur Render.com ! 🎯**