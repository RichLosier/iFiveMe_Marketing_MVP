"""
iFiveMe Marketing MVP - Agent Approbation Amélioré
Version intégrée avec interface web au lieu d'email
"""

import json
import asyncio
import requests
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.base_agent import BaseAgent, AgentTask
from config.settings import COMPANY_INFO
from config.deployment_config import get_web_app_url

@dataclass
class WebApprovalPost:
    """Structure pour un post à approuver via interface web"""
    id: str
    title: str
    content: str
    platform: str
    created_by: str
    created_at: datetime
    scheduled_time: Optional[datetime]
    status: str = "pending"
    approval_token: str = ""
    web_url: str = ""

class EnhancedApprovalAgent(BaseAgent):
    """Agent d'approbation avec interface web intégrée"""

    def __init__(self, web_app_url: str = None):
        # Utiliser l'URL de production ou celle fournie
        if web_app_url is None:
            web_app_url = get_web_app_url()

        super().__init__(
            agent_id="enhanced_approval",
            name="Agent Approbation Web iFiveMe",
            config={
                "web_app_url": web_app_url,  # URL de votre interface web
                "approval_timeout_hours": 24,
                "notification_enabled": True
            }
        )

        self.web_app_url = web_app_url
        self.pending_approvals: Dict[str, WebApprovalPost] = {}

        self.logger.info(f"Enhanced Approval Agent initialisé avec interface web: {web_app_url}")

    def get_capabilities(self) -> List[str]:
        return [
            "🌐 Interface web d'approbation 24/7",
            "📱 Responsive mobile pour approuver partout",
            "🔄 Dashboard temps réel avec auto-refresh",
            "✅ Approbation en un clic",
            "❌ Rejet avec commentaires détaillés",
            "👀 Prévisualisation complète des posts",
            "📊 Statistiques et historique",
            "⏰ Expiration automatique après 24h",
            "🔔 Notifications système intégrées",
            "🎯 API REST pour intégrations"
        ]

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite les tâches d'approbation web"""
        task_type = task.type
        data = task.data

        if task_type == "submit_for_web_approval":
            return await self._submit_for_web_approval(data)
        elif task_type == "check_approval_status":
            return await self._check_approval_status(data)
        elif task_type == "get_pending_approvals":
            return await self._get_pending_approvals(data)
        elif task_type == "process_web_response":
            return await self._process_web_response(data)
        else:
            raise ValueError(f"Type de tâche non supporté: {task_type}")

    async def _submit_for_web_approval(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Soumet un post pour approbation via interface web"""

        post_id = str(uuid.uuid4())
        approval_token = str(uuid.uuid4())

        # Créer le post d'approbation
        approval_post = WebApprovalPost(
            id=post_id,
            title=data.get("title", "Post iFiveMe"),
            content=data.get("content", ""),
            platform=data.get("platform", "LinkedIn"),
            created_by=data.get("created_by", "Équipe Marketing"),
            created_at=datetime.now(),
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]) if data.get("scheduled_time") else None,
            approval_token=approval_token
        )

        # URLs de l'interface web
        approval_post.web_url = f"{self.web_app_url}/preview/{post_id}/{approval_token}"

        # Sauvegarder localement
        self.pending_approvals[post_id] = approval_post

        # Envoyer à l'interface web
        success = await self._send_to_web_interface(approval_post)

        if success:
            self.logger.info(f"✅ Post {post_id} soumis à l'interface web avec succès")

            return {
                "success": True,
                "post_id": post_id,
                "approval_token": approval_token,
                "web_dashboard_url": f"{self.web_app_url}/",
                "direct_approval_url": f"{self.web_app_url}/approve/{post_id}/{approval_token}",
                "direct_rejection_url": f"{self.web_app_url}/reject/{post_id}/{approval_token}",
                "preview_url": f"{self.web_app_url}/preview/{post_id}/{approval_token}",
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
                "status": "pending_web_approval"
            }
        else:
            return {
                "success": False,
                "error": "Échec de soumission à l'interface web",
                "fallback": "Approbation manuelle requise"
            }

    async def _send_to_web_interface(self, post: WebApprovalPost) -> bool:
        """Envoie le post à l'interface web via API"""

        try:
            api_url = f"{self.web_app_url}/api/submit_post"

            payload = {
                "post_id": post.id,
                "title": post.title,
                "content": post.content,
                "platform": post.platform,
                "created_by": post.created_by,
                "scheduled_time": post.scheduled_time.isoformat() if post.scheduled_time else None,
                "approval_token": post.approval_token
            }

            # En mode développement, simuler l'envoi
            if "localhost" in self.web_app_url:
                self.logger.info("🌐 Mode développement - Simulation envoi interface web")

                print(f"\n🌐 POST SOUMIS À L'INTERFACE WEB")
                print(f"🔗 Dashboard: {self.web_app_url}/")
                print(f"👀 Prévisualisation: {post.web_url}")
                print(f"✅ Approuver: {self.web_app_url}/approve/{post.id}/{post.approval_token}")
                print(f"❌ Rejeter: {self.web_app_url}/reject/{post.id}/{post.approval_token}")
                print(f"📱 Interface disponible 24/7 sur mobile et desktop")

                # Sauvegarder pour démo
                await self._save_for_web_demo(post)
                return True

            # En production, envoyer vraiment
            response = requests.post(api_url, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return True
                else:
                    self.logger.error(f"Erreur API web: {result.get('error')}")
                    return False
            else:
                self.logger.error(f"Erreur HTTP: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erreur connexion interface web: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Erreur inattendue: {str(e)}")
            return False

    async def _save_for_web_demo(self, post: WebApprovalPost):
        """Sauvegarde pour démonstration web"""
        try:
            demo_file = self.data_dir / f"web_approval_{post.id}.json"
            with open(demo_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "post": asdict(post),
                    "urls": {
                        "dashboard": f"{self.web_app_url}/",
                        "preview": post.web_url,
                        "approve": f"{self.web_app_url}/approve/{post.id}/{post.approval_token}",
                        "reject": f"{self.web_app_url}/reject/{post.id}/{post.approval_token}"
                    },
                    "instructions": [
                        "1. Ouvrez le dashboard dans votre navigateur",
                        "2. Cliquez sur Prévisualiser pour voir le post complet",
                        "3. Cliquez sur Approuver ou Rejeter",
                        "4. L'équipe sera automatiquement notifiée"
                    ]
                }, f, indent=2, default=str, ensure_ascii=False)

        except Exception as e:
            self.logger.error(f"Erreur sauvegarde démo: {str(e)}")

    async def _check_approval_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Vérifie le statut d'approbation d'un post"""

        post_id = data.get("post_id")

        if not post_id:
            return {"error": "post_id requis"}

        # Vérifier localement
        if post_id in self.pending_approvals:
            post = self.pending_approvals[post_id]

            # Vérifier sur l'interface web si disponible
            web_status = await self._get_web_status(post_id)

            return {
                "post_id": post_id,
                "status": post.status,
                "web_status": web_status,
                "created_at": post.created_at.isoformat(),
                "expires_at": (post.created_at + timedelta(hours=24)).isoformat(),
                "urls": {
                    "dashboard": f"{self.web_app_url}/",
                    "preview": post.web_url
                }
            }
        else:
            return {"error": "Post non trouvé", "post_id": post_id}

    async def _get_web_status(self, post_id: str) -> Dict[str, Any]:
        """Récupère le statut depuis l'interface web"""
        try:
            if "localhost" in self.web_app_url:
                return {"status": "interface_web_locale", "disponible": True}

            # En production, appeler l'API
            response = requests.get(f"{self.web_app_url}/api/status/{post_id}", timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Interface web non accessible"}

        except Exception as e:
            return {"error": f"Erreur vérification web: {str(e)}"}

    async def _get_pending_approvals(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retourne tous les posts en attente d'approbation"""

        pending = []

        for post_id, post in self.pending_approvals.items():
            # Vérifier si pas expiré
            if datetime.now() < post.created_at + timedelta(hours=24):
                pending.append({
                    "id": post.id,
                    "title": post.title,
                    "platform": post.platform,
                    "created_by": post.created_by,
                    "created_at": post.created_at.isoformat(),
                    "web_url": post.web_url,
                    "expires_in_hours": int((post.created_at + timedelta(hours=24) - datetime.now()).total_seconds() / 3600)
                })

        return {
            "pending_count": len(pending),
            "pending_posts": pending,
            "web_dashboard": f"{self.web_app_url}/",
            "last_updated": datetime.now().isoformat()
        }

    async def _process_web_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Traite une réponse d'approbation depuis l'interface web"""

        post_id = data.get("post_id")
        decision = data.get("decision")  # approved, rejected
        reason = data.get("reason", "")

        if post_id not in self.pending_approvals:
            return {"error": "Post non trouvé"}

        post = self.pending_approvals[post_id]

        # Mettre à jour le statut
        post.status = decision

        # Notifier l'équipe
        notification = await self._notify_team_decision(post, decision, reason)

        # Si approuvé, déclencher la publication
        if decision == "approved":
            publication_result = await self._trigger_publication(post)

            return {
                "post_id": post_id,
                "decision": decision,
                "status": "approved_and_scheduled",
                "notification_sent": notification,
                "publication": publication_result,
                "processed_at": datetime.now().isoformat()
            }
        else:
            return {
                "post_id": post_id,
                "decision": decision,
                "reason": reason,
                "status": "rejected",
                "notification_sent": notification,
                "processed_at": datetime.now().isoformat()
            }

    async def _notify_team_decision(self, post: WebApprovalPost, decision: str, reason: str = "") -> bool:
        """Notifie l'équipe de la décision d'approbation"""

        try:
            print(f"\n📧 NOTIFICATION ÉQUIPE")
            print(f"📝 Post: {post.title}")
            print(f"👤 Créateur: {post.created_by}")
            print(f"✅ Décision: {decision.upper()}")

            if reason:
                print(f"💬 Raison: {reason}")

            print(f"📅 Traité le: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

            # En production, envoyer un vrai email/notification
            return True

        except Exception as e:
            self.logger.error(f"Erreur notification équipe: {str(e)}")
            return False

    async def _trigger_publication(self, post: WebApprovalPost) -> Dict[str, Any]:
        """Déclenche la publication du post approuvé"""

        try:
            print(f"\n🚀 PUBLICATION AUTOMATIQUE")
            print(f"📱 Plateforme: {post.platform}")
            print(f"📝 Contenu: {post.title}")
            print(f"⏰ Programmé: {post.scheduled_time or 'Immédiat'}")

            # En production, intégrer avec les APIs des plateformes sociales
            # Facebook API, LinkedIn API, Twitter API, etc.

            return {
                "status": "publication_scheduled",
                "platform": post.platform,
                "scheduled_time": post.scheduled_time.isoformat() if post.scheduled_time else None,
                "estimated_reach": self._estimate_reach(post),
                "success": True
            }

        except Exception as e:
            self.logger.error(f"Erreur publication: {str(e)}")
            return {
                "status": "publication_failed",
                "error": str(e),
                "success": False
            }

    def _estimate_reach(self, post: WebApprovalPost) -> int:
        """Estime la portée du post selon la plateforme"""

        base_reach = {
            "Facebook": 1200,
            "LinkedIn": 800,
            "Twitter": 500,
            "Instagram": 900
        }

        return base_reach.get(post.platform, 600)

# Fonction utilitaire pour intégration facile
async def submit_for_web_approval(
    title: str,
    content: str,
    platform: str,
    created_by: str,
    scheduled_time: Optional[str] = None,
    web_app_url: str = None
) -> Dict[str, Any]:
    """Fonction simple pour soumettre un post à l'approbation web"""

    approval_agent = EnhancedApprovalAgent(web_app_url)

    task = approval_agent.create_task(
        task_type="submit_for_web_approval",
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