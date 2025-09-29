"""
Configuration Gmail pour les notifications d'approbation iFiveMe
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class GmailService:
    """Service d'envoi d'emails via Gmail"""

    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "noreply@ifiveme.com"  # À remplacer par votre email iFiveMe

    def send_approval_email(self,
                           to_email: str,
                           subject: str,
                           html_content: str,
                           app_password: str) -> bool:
        """
        Envoie un email d'approbation via Gmail

        Args:
            to_email: Email destinataire (richard@ifiveme.com)
            subject: Sujet de l'email
            html_content: Contenu HTML de l'email
            app_password: Mot de passe d'application Gmail
        """

        try:
            # Créer le message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to_email

            # Ajouter le contenu HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Créer connexion SMTP sécurisée
            context = ssl.create_default_context()

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, app_password)

                # Envoyer l'email
                text = message.as_string()
                server.sendmail(self.sender_email, to_email, text)

            logger.info(f"✅ Email d'approbation envoyé à {to_email}")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur envoi email: {str(e)}")
            return False

# Configuration pour déploiement
GMAIL_SETUP_INSTRUCTIONS = """
🔧 CONFIGURATION GMAIL POUR IFIVEME

1. **Activer l'authentification à 2 facteurs sur votre compte Gmail**
   - Aller sur myaccount.google.com
   - Sécurité → Authentification à 2 facteurs → Activer

2. **Créer un mot de passe d'application**
   - Google Account → Sécurité → Mots de passe des applications
   - Sélectionner "Mail" et votre appareil
   - Générer le mot de passe (16 caractères)

3. **Variables d'environnement à définir:**
   ```bash
   export GMAIL_APP_PASSWORD="votre_mot_de_passe_app_16_caracteres"
   export SENDER_EMAIL="votre-email@ifiveme.com"
   export APPROVAL_EMAIL="richard@ifiveme.com"
   ```

4. **Alternative: Utiliser OAuth2 (plus sécurisé)**
   - Créer un projet Google Cloud Console
   - Activer Gmail API
   - Créer des credentials OAuth2
   - Utiliser refresh token pour authentification
"""