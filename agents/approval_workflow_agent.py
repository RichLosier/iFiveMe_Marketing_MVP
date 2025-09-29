"""
iFiveMe Marketing MVP - Agent Workflow d'Approbation
Gère les approbations de contenu par email avant publication
"""

import json
import asyncio
import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.base_agent import BaseAgent, AgentTask
from config.settings import COMPANY_INFO, API_KEYS

@dataclass
class PendingPost:
    """Structure pour un post en attente d'approbation"""
    id: str
    title: str
    content: str
    platform: str
    created_by: str
    created_at: datetime
    scheduled_time: Optional[datetime]
    status: str = "pending"  # pending, approved, rejected, expired
    approval_token: str = ""
    rejection_reason: Optional[str] = None
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None

class ApprovalWorkflowAgent(BaseAgent):
    """Agent spécialisé dans les workflows d'approbation de contenu"""

    def __init__(self):
        super().__init__(
            agent_id="approval_workflow",
            name="Agent Workflow d'Approbation iFiveMe",
            config={
                "approval_timeout_hours": 24,
                "auto_reminder_hours": 12,
                "notification_email": "richard@ifiveme.com",  # Votre email
                "approval_base_url": "https://approve.ifiveme.com",  # URL pour les actions
                "smtp_settings": {
                    "server": "smtp.gmail.com",
                    "port": 587,
                    "use_tls": True
                }
            }
        )

        # Posts en attente d'approbation
        self.pending_posts: Dict[str, PendingPost] = {}

        # Templates d'emails d'approbation
        self.approval_email_templates = {
            "new_post_approval": {
                "subject": "🚀 iFiveMe - Nouveau post à approuver: {title}",
                "template": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Approbation de contenu iFiveMe</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
        .post-preview {{ background: white; padding: 15px; margin: 15px 0; border-left: 4px solid #667eea; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .actions {{ text-align: center; margin: 20px 0; }}
        .btn {{ display: inline-block; padding: 12px 24px; margin: 10px; text-decoration: none; border-radius: 6px; font-weight: bold; }}
        .btn-approve {{ background: #28a745; color: white; }}
        .btn-reject {{ background: #dc3545; color: white; }}
        .btn-edit {{ background: #ffc107; color: #212529; }}
        .meta {{ background: #e9ecef; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 10px 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 iFiveMe - Approbation de Contenu</h1>
            <p>Nouveau post en attente de votre validation</p>
        </div>

        <div class="content">
            <div class="meta">
                <strong>📋 Détails du post:</strong><br>
                <strong>Titre:</strong> {title}<br>
                <strong>Plateforme:</strong> {platform}<br>
                <strong>Créé par:</strong> {created_by}<br>
                <strong>Date création:</strong> {created_at}<br>
                <strong>Publication prévue:</strong> {scheduled_time}
            </div>

            <div class="post-preview">
                <h3>📝 Aperçu du contenu:</h3>
                <div style="border: 1px solid #ddd; padding: 15px; background: white; white-space: pre-wrap;">{content}</div>
            </div>

            <div class="actions">
                <h3>🎯 Actions disponibles:</h3>
                <a href="{approval_url}" class="btn btn-approve">✅ APPROUVER</a>
                <a href="{rejection_url}" class="btn btn-reject">❌ REJETER</a>
                <a href="{edit_url}" class="btn btn-edit">✏️ DEMANDER MODIFICATIONS</a>
            </div>

            <div class="meta">
                <strong>⏰ Important:</strong><br>
                • Ce post sera automatiquement rejeté après 24h sans réponse<br>
                • Un rappel sera envoyé dans 12h si pas d'action<br>
                • Vous pouvez répondre directement à cet email pour des commentaires
            </div>
        </div>

        <div class="footer">
            <p>iFiveMe Marketing System | Le plus grand créateur de cartes d'affaires virtuelles</p>
            <p>Post ID: {post_id} | Token: {approval_token}</p>
        </div>
    </div>
</body>
</html>
                """
            },
            "approval_reminder": {
                "subject": "⏰ Rappel - Post iFiveMe en attente: {title}",
                "template": """
Bonjour Richard,

🔔 RAPPEL: Un post iFiveMe est toujours en attente de votre approbation.

📋 Détails:
• Titre: {title}
• Plateforme: {platform}
• Temps restant: {hours_remaining}h avant expiration

🎯 Actions rapides:
✅ Approuver: {approval_url}
❌ Rejeter: {rejection_url}

Le post sera automatiquement rejeté si aucune action n'est prise.

Cordialement,
Système d'approbation iFiveMe
                """
            },
            "post_approved": {
                "subject": "✅ Post iFiveMe approuvé: {title}",
                "template": """
Bonjour {created_by},

Excellente nouvelle! Votre post iFiveMe a été approuvé par Richard.

📋 Détails du post:
• Titre: {title}
• Plateforme: {platform}
• Statut: ✅ APPROUVÉ
• Approuvé le: {approved_at}

🚀 Prochaines étapes:
Le post sera publié automatiquement selon le planning prévu.

Merci pour votre contribution au marketing iFiveMe!

L'équipe Marketing iFiveMe
                """
            },
            "post_rejected": {
                "subject": "❌ Post iFiveMe rejeté: {title}",
                "template": """
Bonjour {created_by},

Votre post iFiveMe a été examiné mais nécessite des ajustements.

📋 Détails du post:
• Titre: {title}
• Plateforme: {platform}
• Statut: ❌ REJETÉ

💬 Commentaires de Richard:
{rejection_reason}

🔄 Prochaines étapes:
Veuillez apporter les modifications demandées et soumettre une nouvelle version.

L'équipe Marketing iFiveMe
                """
            }
        }

    def get_capabilities(self) -> List[str]:
        return [
            "Workflow d'approbation par email",
            "Interface web d'approbation rapide",
            "Rappels automatiques",
            "Tracking des approbations",
            "Notifications multi-parties",
            "Gestion des délais d'expiration",
            "Historique des décisions",
            "Integration avec les agents de publication"
        ]

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite les tâches du workflow d'approbation"""
        task_type = task.type
        data = task.data

        if task_type == "submit_for_approval":
            return await self._submit_post_for_approval(data)
        elif task_type == "process_approval_response":
            return await self._process_approval_response(data)
        elif task_type == "send_reminders":
            return await self._send_approval_reminders(data)
        elif task_type == "cleanup_expired":
            return await self._cleanup_expired_posts(data)
        elif task_type == "get_pending_posts":
            return await self._get_pending_posts_status(data)
        elif task_type == "manual_approve":
            return await self._manual_approve_post(data)
        elif task_type == "manual_reject":
            return await self._manual_reject_post(data)
        else:
            raise ValueError(f"Type de tâche non supporté: {task_type}")

    async def _submit_post_for_approval(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Soumet un post pour approbation"""
        post_id = str(uuid.uuid4())
        approval_token = str(uuid.uuid4())

        # Créer le post en attente
        pending_post = PendingPost(
            id=post_id,
            title=data.get("title", "Post iFiveMe"),
            content=data.get("content", ""),
            platform=data.get("platform", "LinkedIn"),
            created_by=data.get("created_by", "Équipe Marketing"),
            created_at=datetime.now(),
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]) if data.get("scheduled_time") else None,
            approval_token=approval_token
        )

        # Sauvegarder le post
        self.pending_posts[post_id] = pending_post

        # Envoyer l'email d'approbation
        approval_sent = await self._send_approval_email(pending_post)

        # Programmer les rappels
        await self._schedule_reminders(pending_post)

        return {
            "post_id": post_id,
            "approval_token": approval_token,
            "status": "submitted_for_approval",
            "approval_email_sent": approval_sent,
            "expires_at": (datetime.now() + timedelta(hours=self.config["approval_timeout_hours"])).isoformat(),
            "approval_urls": {
                "approve": f"{self.config['approval_base_url']}/approve/{post_id}/{approval_token}",
                "reject": f"{self.config['approval_base_url']}/reject/{post_id}/{approval_token}",
                "edit": f"{self.config['approval_base_url']}/edit/{post_id}/{approval_token}"
            },
            "notification_sent_to": self.config["notification_email"]
        }

    async def _send_approval_email(self, post: PendingPost) -> bool:
        """Envoie l'email d'approbation"""
        try:
            template = self.approval_email_templates["new_post_approval"]

            # URLs d'action
            base_url = self.config["approval_base_url"]
            approval_url = f"{base_url}/approve/{post.id}/{post.approval_token}"
            rejection_url = f"{base_url}/reject/{post.id}/{post.approval_token}"
            edit_url = f"{base_url}/edit/{post.id}/{post.approval_token}"

            # Formater le contenu
            subject = template["subject"].format(title=post.title)

            html_content = template["template"].format(
                title=post.title,
                platform=post.platform,
                created_by=post.created_by,
                created_at=post.created_at.strftime("%Y-%m-%d %H:%M"),
                scheduled_time=post.scheduled_time.strftime("%Y-%m-%d %H:%M") if post.scheduled_time else "Non programmé",
                content=post.content,
                approval_url=approval_url,
                rejection_url=rejection_url,
                edit_url=edit_url,
                post_id=post.id,
                approval_token=post.approval_token
            )

            # Simuler l'envoi d'email (en production, utiliser SMTP réel)
            email_result = await self._send_email_notification(
                to_email=self.config["notification_email"],
                subject=subject,
                html_content=html_content
            )

            self.logger.info(f"Email d'approbation envoyé pour post {post.id}")
            return True

        except Exception as e:
            self.logger.error(f"Erreur envoi email d'approbation: {str(e)}")
            return False

    async def _send_email_notification(self, to_email: str, subject: str, html_content: str) -> bool:
        """Envoie réellement l'email (simulation en mode demo)"""
        # En mode démo, on simule l'envoi
        if not API_KEYS.get("smtp_password"):
            # Mode simulation
            print(f"\n📧 EMAIL D'APPROBATION ENVOYÉ À: {to_email}")
            print(f"📋 SUJET: {subject}")
            print("📝 CONTENU: Email HTML avec boutons d'approbation")

            # Sauvegarder l'email pour consultation
            email_file = self.data_dir / f"approval_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(email_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"💾 Email sauvé: {email_file}")
            return True

        # En production, utiliser SMTP réel
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = "noreply@ifiveme.com"
            msg['To'] = to_email

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Configurer SMTP (exemple Gmail)
            smtp_settings = self.config["smtp_settings"]
            server = smtplib.SMTP(smtp_settings["server"], smtp_settings["port"])

            if smtp_settings["use_tls"]:
                server.starttls()

            # Login avec les credentials
            server.login("your_email@gmail.com", API_KEYS.get("smtp_password", ""))

            text = msg.as_string()
            server.sendmail(msg['From'], [to_email], text)
            server.quit()

            return True

        except Exception as e:
            self.logger.error(f"Erreur SMTP: {str(e)}")
            return False

    async def _process_approval_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Traite une réponse d'approbation"""
        post_id = data.get("post_id")
        action = data.get("action")  # approve, reject, edit
        token = data.get("token")
        reason = data.get("reason", "")

        if post_id not in self.pending_posts:
            return {"error": "Post non trouvé", "status": "not_found"}

        post = self.pending_posts[post_id]

        # Vérifier le token
        if post.approval_token != token:
            return {"error": "Token invalide", "status": "invalid_token"}

        # Vérifier si pas expiré
        expires_at = post.created_at + timedelta(hours=self.config["approval_timeout_hours"])
        if datetime.now() > expires_at:
            return {"error": "Demande d'approbation expirée", "status": "expired"}

        # Traiter l'action
        if action == "approve":
            post.status = "approved"
            post.approved_at = datetime.now()
            post.approved_by = "Richard Losier"

            # Notifier l'équipe
            await self._notify_approval_result(post, "approved")

            # Déclencher la publication (intégration avec autres agents)
            await self._trigger_publication(post)

        elif action == "reject":
            post.status = "rejected"
            post.rejection_reason = reason

            # Notifier l'équipe
            await self._notify_approval_result(post, "rejected", reason)

        elif action == "edit":
            # Demander des modifications
            post.status = "needs_revision"
            post.rejection_reason = reason

            await self._notify_approval_result(post, "needs_revision", reason)

        # Sauvegarder les changements
        await self._save_approval_decision(post)

        return {
            "post_id": post_id,
            "action": action,
            "status": post.status,
            "processed_at": datetime.now().isoformat(),
            "notification_sent": True
        }

    async def _notify_approval_result(self, post: PendingPost, result: str, reason: str = ""):
        """Notifie l'équipe du résultat de l'approbation"""
        try:
            if result == "approved":
                template = self.approval_email_templates["post_approved"]
                content = template["template"].format(
                    created_by=post.created_by,
                    title=post.title,
                    platform=post.platform,
                    approved_at=post.approved_at.strftime("%Y-%m-%d %H:%M")
                )
            else:
                template = self.approval_email_templates["post_rejected"]
                content = template["template"].format(
                    created_by=post.created_by,
                    title=post.title,
                    platform=post.platform,
                    rejection_reason=reason or "Aucune raison spécifiée"
                )

            # Simuler l'envoi à l'équipe
            print(f"\n📧 NOTIFICATION ÉQUIPE: {result.upper()}")
            print(f"📋 Post: {post.title}")
            print(f"👤 Destinataire: {post.created_by}")

        except Exception as e:
            self.logger.error(f"Erreur notification équipe: {str(e)}")

    async def _trigger_publication(self, post: PendingPost):
        """Déclenche la publication du post approuvé"""
        # Integration avec les autres agents pour publier
        publication_data = {
            "post_id": post.id,
            "platform": post.platform,
            "content": post.content,
            "scheduled_time": post.scheduled_time,
            "approved_by": post.approved_by,
            "approved_at": post.approved_at
        }

        # En mode démo
        print(f"\n🚀 PUBLICATION DÉCLENCHÉE")
        print(f"📱 Plateforme: {post.platform}")
        print(f"📅 Publication: {post.scheduled_time or 'Immédiate'}")

        # Ici on appellerait l'agent approprié (social media, email, etc.)
        # await self.social_media_agent.publish_post(publication_data)

    async def _schedule_reminders(self, post: PendingPost):
        """Programme les rappels d'approbation"""
        reminder_time = post.created_at + timedelta(hours=self.config["auto_reminder_hours"])

        # En production, utiliser un scheduler comme Celery
        # Pour la démo, on simule
        self.logger.info(f"Rappel programmé pour {reminder_time} pour post {post.id}")

    async def _send_approval_reminders(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Envoie les rappels pour posts en attente"""
        reminders_sent = 0

        for post_id, post in self.pending_posts.items():
            if post.status != "pending":
                continue

            # Vérifier si rappel nécessaire
            reminder_time = post.created_at + timedelta(hours=self.config["auto_reminder_hours"])
            expires_at = post.created_at + timedelta(hours=self.config["approval_timeout_hours"])

            if datetime.now() >= reminder_time and datetime.now() < expires_at:
                await self._send_reminder_email(post)
                reminders_sent += 1

        return {
            "reminders_sent": reminders_sent,
            "timestamp": datetime.now().isoformat()
        }

    async def _send_reminder_email(self, post: PendingPost):
        """Envoie un email de rappel"""
        template = self.approval_email_templates["approval_reminder"]

        expires_at = post.created_at + timedelta(hours=self.config["approval_timeout_hours"])
        hours_remaining = int((expires_at - datetime.now()).total_seconds() / 3600)

        subject = template["subject"].format(title=post.title)
        content = template["template"].format(
            title=post.title,
            platform=post.platform,
            hours_remaining=hours_remaining,
            approval_url=f"{self.config['approval_base_url']}/approve/{post.id}/{post.approval_token}",
            rejection_url=f"{self.config['approval_base_url']}/reject/{post.id}/{post.approval_token}"
        )

        # Simuler l'envoi
        print(f"\n⏰ RAPPEL D'APPROBATION ENVOYÉ")
        print(f"📋 Post: {post.title}")
        print(f"⏳ Expire dans: {hours_remaining}h")

    async def _cleanup_expired_posts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Nettoie les posts expirés"""
        expired_count = 0
        timeout_hours = self.config["approval_timeout_hours"]

        for post_id, post in list(self.pending_posts.items()):
            if post.status == "pending":
                expires_at = post.created_at + timedelta(hours=timeout_hours)

                if datetime.now() > expires_at:
                    post.status = "expired"
                    expired_count += 1

                    # Notifier l'expiration
                    await self._notify_post_expired(post)

        return {
            "expired_posts": expired_count,
            "cleanup_timestamp": datetime.now().isoformat()
        }

    async def _notify_post_expired(self, post: PendingPost):
        """Notifie l'expiration d'un post"""
        print(f"\n⏰ POST EXPIRÉ: {post.title}")
        print(f"👤 Créateur: {post.created_by}")
        print(f"📅 Expiré le: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    async def _get_pending_posts_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retourne le statut des posts en attente"""
        pending = []
        approved = []
        rejected = []
        expired = []

        for post in self.pending_posts.values():
            post_info = {
                "id": post.id,
                "title": post.title,
                "platform": post.platform,
                "created_by": post.created_by,
                "created_at": post.created_at.isoformat(),
                "status": post.status
            }

            if post.status == "pending":
                pending.append(post_info)
            elif post.status == "approved":
                approved.append(post_info)
            elif post.status == "rejected":
                rejected.append(post_info)
            elif post.status == "expired":
                expired.append(post_info)

        return {
            "summary": {
                "total": len(self.pending_posts),
                "pending": len(pending),
                "approved": len(approved),
                "rejected": len(rejected),
                "expired": len(expired)
            },
            "posts": {
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
                "expired": expired
            },
            "generated_at": datetime.now().isoformat()
        }

    async def _manual_approve_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Approuve manuellement un post (pour interface admin)"""
        return await self._process_approval_response({
            "post_id": data.get("post_id"),
            "action": "approve",
            "token": data.get("token"),
            "reason": "Approbation manuelle"
        })

    async def _manual_reject_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Rejette manuellement un post"""
        return await self._process_approval_response({
            "post_id": data.get("post_id"),
            "action": "reject",
            "token": data.get("token"),
            "reason": data.get("reason", "Rejet manuel")
        })

    async def _save_approval_decision(self, post: PendingPost):
        """Sauvegarde la décision d'approbation"""
        try:
            decision_file = self.data_dir / f"approval_decision_{post.id}.json"
            with open(decision_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(post), f, indent=2, default=str, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde décision: {str(e)}")

# Fonction utilitaire pour intégration facile
async def submit_post_for_approval(
    title: str,
    content: str,
    platform: str,
    created_by: str,
    scheduled_time: Optional[str] = None
) -> Dict[str, Any]:
    """Fonction simple pour soumettre un post à l'approbation"""

    approval_agent = ApprovalWorkflowAgent()

    task = approval_agent.create_task(
        task_type="submit_for_approval",
        priority=8,
        data={
            "title": title,
            "content": content,
            "platform": platform,
            "created_by": created_by,
            "scheduled_time": scheduled_time
        }
    )

    await approval_agent.add_task(task)
    await approval_agent.execute_tasks()

    # Récupérer le résultat
    results = []
    for file_path in approval_agent.data_dir.glob("task_*_result.json"):
        with open(file_path, 'r') as f:
            result = json.load(f)
            if result.get("result"):
                results.append(result["result"])

    await approval_agent.stop()

    return results[-1] if results else {"error": "Échec de soumission"}