"""
Configuration de déploiement pour iFiveMe
Modifiez PRODUCTION_WEB_URL après déploiement
"""

# URL de production - À MODIFIER après déploiement
PRODUCTION_WEB_URL = "https://9b02f713b297.ngrok-free.app"  # URL publique ngrok

# URL de développement
DEVELOPMENT_WEB_URL = "http://localhost:5000"

# Configuration automatique selon l'environnement
import os

def get_web_app_url():
    """Retourne l'URL appropriée selon l'environnement"""

    # Si une URL de production est définie en variable d'environnement, l'utiliser
    if os.getenv("IFIVEME_WEB_URL"):
        return os.getenv("IFIVEME_WEB_URL")

    # Sinon, utiliser la configuration par défaut
    return PRODUCTION_WEB_URL

# Instructions pour mise à jour post-déploiement
DEPLOYMENT_INSTRUCTIONS = """
🚀 INSTRUCTIONS POST-DÉPLOIEMENT:

1. Déployez votre interface web (Vercel/Railway/Heroku)
2. Récupérez votre URL finale (ex: https://ifiveme-approval-abc123.vercel.app)
3. Modifiez PRODUCTION_WEB_URL dans ce fichier
4. Relancez vos agents avec la nouvelle configuration

EXEMPLE:
PRODUCTION_WEB_URL = "https://votre-url-finale.vercel.app"
"""

print(f"📍 URL Web Interface: {get_web_app_url()}")