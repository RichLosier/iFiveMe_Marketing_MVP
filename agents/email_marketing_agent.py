"""
iFiveMe Marketing MVP - Agent Email Marketing
Gère les campagnes d'email marketing automatisées
"""

import json
import asyncio
import smtplib
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
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
class EmailContact:
    """Structure pour un contact email"""
    email: str
    name: str = ""
    segments: List[str] = None
    preferences: Dict[str, Any] = None
    engagement_score: float = 0.0
    last_interaction: Optional[datetime] = None
    status: str = "active"  # active, unsubscribed, bounced

@dataclass
class EmailCampaign:
    """Structure pour une campagne email"""
    id: str
    name: str
    type: str  # welcome, newsletter, promotion, re-engagement
    subject: str
    content: str
    segments: List[str]
    send_time: datetime
    status: str = "draft"
    metrics: Dict[str, Any] = None

@dataclass
class EmailMetrics:
    """Métriques d'une campagne email"""
    sent: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    unsubscribed: int = 0
    bounced: int = 0
    converted: int = 0
    revenue: float = 0.0

class EmailMarketingAgent(BaseAgent):
    """Agent spécialisé dans l'email marketing pour iFiveMe"""

    def __init__(self):
        super().__init__(
            agent_id="email_marketing",
            name="Agent Email Marketing iFiveMe",
            config={
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "max_emails_per_hour": 100,
                "segment_size_limit": 1000,
                "a_b_test_split": 0.1
            }
        )

        # Configuration des segments client iFiveMe
        self.customer_segments = {
            "new_users": {
                "name": "Nouveaux utilisateurs",
                "criteria": "Inscrit dans les 7 derniers jours",
                "welcome_sequence": True
            },
            "active_users": {
                "name": "Utilisateurs actifs",
                "criteria": "Actif dans les 30 derniers jours",
                "engagement_focus": True
            },
            "premium_users": {
                "name": "Utilisateurs premium",
                "criteria": "Abonnement premium actif",
                "retention_focus": True
            },
            "inactive_users": {
                "name": "Utilisateurs inactifs",
                "criteria": "Pas d'activité depuis 60 jours",
                "reengagement_focus": True
            },
            "enterprise_prospects": {
                "name": "Prospects entreprise",
                "criteria": "Lead enterprise qualifié",
                "nurturing_focus": True
            }
        }

        # Templates d'emails iFiveMe
        self.email_templates = {
            "welcome_sequence": {
                "day_1": {
                    "subject": "Bienvenue chez iFiveMe ! Créez votre première carte 🚀",
                    "template": "welcome_day1.html",
                    "focus": "onboarding"
                },
                "day_3": {
                    "subject": "3 astuces pour une carte iFiveMe parfaite 💡",
                    "template": "welcome_day3.html",
                    "focus": "tips"
                },
                "day_7": {
                    "subject": "Vos statistiques iFiveMe cette semaine 📊",
                    "template": "welcome_day7.html",
                    "focus": "analytics"
                }
            },
            "newsletter": {
                "monthly": {
                    "subject": "iFiveMe News - Nouveautés et success stories",
                    "template": "newsletter_monthly.html",
                    "focus": "product_updates"
                }
            },
            "promotional": {
                "premium_upgrade": {
                    "subject": "Débloquez le potentiel complet d'iFiveMe Premium ⭐",
                    "template": "promo_premium.html",
                    "focus": "conversion"
                },
                "referral": {
                    "subject": "Parrainez et gagnez avec iFiveMe ! 🎁",
                    "template": "promo_referral.html",
                    "focus": "growth"
                }
            },
            "reengagement": {
                "win_back": {
                    "subject": "On vous a manqué ! Votre carte iFiveMe vous attend...",
                    "template": "winback.html",
                    "focus": "retention"
                }
            }
        }

        # Configuration A/B testing
        self.ab_test_variants = {
            "subject_lines": {
                "formal": "Mise à jour importante de votre compte iFiveMe",
                "casual": "Du nouveau chez iFiveMe ! 🚀",
                "urgent": "Ne manquez pas ces nouvelles fonctionnalités",
                "personalized": "{name}, vos nouvelles cartes vous attendent"
            },
            "cta_buttons": {
                "action": "Créer ma carte maintenant",
                "benefit": "Découvrir les avantages",
                "curiosity": "Voir les nouveautés",
                "social": "Rejoindre la communauté"
            }
        }

        # Base de données contacts (simulée)
        self.contacts_db = []
        self.campaigns_history = []

    def get_capabilities(self) -> List[str]:
        return [
            "Segmentation avancée des contacts",
            "Séquences d'emails automatisées",
            "A/B testing des campagnes",
            "Personnalisation dynamique",
            "Analyse des performances",
            "Gestion des désabonnements",
            "Optimisation des heures d'envoi",
            "Scoring d'engagement",
            "Intégration CRM",
            "Responsive email design"
        ]

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite les tâches d'email marketing"""
        task_type = task.type
        data = task.data

        if task_type == "send_campaign":
            return await self._send_campaign(data)
        elif task_type == "create_sequence":
            return await self._create_email_sequence(data)
        elif task_type == "segment_contacts":
            return await self._segment_contacts(data)
        elif task_type == "analyze_campaign":
            return await self._analyze_campaign_performance(data)
        elif task_type == "ab_test":
            return await self._run_ab_test(data)
        elif task_type == "manage_contacts":
            return await self._manage_contacts(data)
        elif task_type == "optimize_timing":
            return await self._optimize_send_timing(data)
        elif task_type == "generate_report":
            return await self._generate_email_report(data)
        else:
            raise ValueError(f"Type de tâche non supporté: {task_type}")

    async def _send_campaign(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Envoie une campagne email"""
        campaign_id = data.get("campaign_id")
        segment = data.get("segment", "all")
        immediate = data.get("immediate", False)

        # Récupérer les contacts du segment
        contacts = await self._get_contacts_by_segment(segment)

        # Créer la campagne
        campaign = EmailCampaign(
            id=campaign_id or f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=data.get("name", "Campagne iFiveMe"),
            type=data.get("type", "newsletter"),
            subject=data.get("subject", "Actualités iFiveMe"),
            content=data.get("content", ""),
            segments=[segment],
            send_time=datetime.now() if immediate else datetime.fromisoformat(data.get("send_time", str(datetime.now())))
        )

        if immediate:
            result = await self._execute_campaign_send(campaign, contacts)
        else:
            result = await self._schedule_campaign(campaign, contacts)

        # Sauvegarder la campagne
        self.campaigns_history.append(campaign)
        await self._save_campaign_data(campaign)

        return {
            "campaign_id": campaign.id,
            "status": "sent" if immediate else "scheduled",
            "recipients": len(contacts),
            "segments": campaign.segments,
            "subject": campaign.subject,
            "send_time": campaign.send_time.isoformat(),
            "initial_metrics": result.get("metrics", {}),
            "estimated_performance": self._estimate_campaign_performance(campaign, contacts)
        }

    async def _create_email_sequence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une séquence d'emails automatisée"""
        sequence_type = data.get("type", "welcome")
        trigger = data.get("trigger", "user_signup")
        segment = data.get("segment", "new_users")

        if sequence_type == "welcome":
            emails = self._build_welcome_sequence(data)
        elif sequence_type == "nurturing":
            emails = self._build_nurturing_sequence(data)
        elif sequence_type == "reengagement":
            emails = self._build_reengagement_sequence(data)
        else:
            emails = self._build_custom_sequence(data)

        sequence_id = f"seq_{sequence_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Programmer les emails
        scheduled_campaigns = []
        for i, email_config in enumerate(emails):
            campaign = EmailCampaign(
                id=f"{sequence_id}_email_{i+1}",
                name=f"{sequence_type.title()} Email {i+1}",
                type=sequence_type,
                subject=email_config["subject"],
                content=email_config["content"],
                segments=[segment],
                send_time=datetime.now() + timedelta(days=email_config["delay_days"])
            )
            scheduled_campaigns.append(campaign)

        return {
            "sequence_id": sequence_id,
            "type": sequence_type,
            "trigger": trigger,
            "emails_count": len(emails),
            "scheduled_campaigns": [
                {
                    "id": camp.id,
                    "subject": camp.subject,
                    "send_time": camp.send_time.isoformat()
                } for camp in scheduled_campaigns
            ],
            "estimated_total_engagement": self._estimate_sequence_performance(emails),
            "automation_rules": self._get_automation_rules(sequence_type)
        }

    async def _segment_contacts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Segmente les contacts selon des critères"""
        segment_name = data.get("segment_name", "new_segment")
        criteria = data.get("criteria", {})

        # Simuler la segmentation
        total_contacts = data.get("total_contacts", 5000)

        # Logique de segmentation
        segments = {
            "new_users": int(total_contacts * 0.15),  # 15% nouveaux
            "active_users": int(total_contacts * 0.45),  # 45% actifs
            "premium_users": int(total_contacts * 0.10),  # 10% premium
            "inactive_users": int(total_contacts * 0.25),  # 25% inactifs
            "enterprise_prospects": int(total_contacts * 0.05)  # 5% prospects
        }

        segment_size = segments.get(segment_name, int(total_contacts * 0.1))

        # Créer des contacts simulés pour le segment
        segment_contacts = []
        for i in range(min(segment_size, 50)):  # Limiter pour l'exemple
            contact = EmailContact(
                email=f"user_{i}@example.com",
                name=f"Utilisateur {i}",
                segments=[segment_name],
                engagement_score=self._generate_engagement_score(segment_name),
                last_interaction=datetime.now() - timedelta(days=i)
            )
            segment_contacts.append(contact)

        return {
            "segment_name": segment_name,
            "criteria": criteria,
            "total_contacts": segment_size,
            "sample_contacts": [asdict(c) for c in segment_contacts[:10]],
            "segment_characteristics": {
                "avg_engagement_score": sum(c.engagement_score for c in segment_contacts) / len(segment_contacts),
                "active_percentage": len([c for c in segment_contacts if c.status == "active"]) / len(segment_contacts) * 100,
                "last_interaction_avg_days": sum([(datetime.now() - c.last_interaction).days for c in segment_contacts]) / len(segment_contacts)
            },
            "recommended_campaigns": self._recommend_campaigns_for_segment(segment_name)
        }

    async def _analyze_campaign_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse la performance d'une campagne"""
        campaign_id = data.get("campaign_id")
        timeframe = data.get("timeframe", "7d")

        # Simuler les métriques de campagne
        metrics = self._generate_mock_campaign_metrics(campaign_id)

        # Analyser les tendances
        trends = self._analyze_performance_trends(metrics, timeframe)

        # Générer des recommandations
        recommendations = self._generate_campaign_recommendations(metrics)

        return {
            "campaign_id": campaign_id,
            "timeframe": timeframe,
            "metrics": {
                "sent": metrics.sent,
                "delivered": metrics.delivered,
                "open_rate": (metrics.opened / metrics.delivered * 100) if metrics.delivered > 0 else 0,
                "click_rate": (metrics.clicked / metrics.delivered * 100) if metrics.delivered > 0 else 0,
                "conversion_rate": (metrics.converted / metrics.clicked * 100) if metrics.clicked > 0 else 0,
                "unsubscribe_rate": (metrics.unsubscribed / metrics.delivered * 100) if metrics.delivered > 0 else 0,
                "bounce_rate": (metrics.bounced / metrics.sent * 100) if metrics.sent > 0 else 0,
                "revenue": metrics.revenue
            },
            "benchmarks": self._get_industry_benchmarks(),
            "trends": trends,
            "recommendations": recommendations,
            "top_performing_content": self._identify_top_content(campaign_id),
            "audience_insights": self._generate_audience_insights(campaign_id)
        }

    async def _run_ab_test(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute un test A/B sur une campagne"""
        test_element = data.get("element", "subject_line")  # subject_line, cta, content, send_time
        variant_a = data.get("variant_a")
        variant_b = data.get("variant_b")
        sample_size = data.get("sample_size", 100)
        significance_level = data.get("significance_level", 0.05)

        # Simuler les résultats du test A/B
        results_a = self._simulate_variant_performance(variant_a, test_element)
        results_b = self._simulate_variant_performance(variant_b, test_element)

        # Calculer la signification statistique
        is_significant = self._calculate_statistical_significance(
            results_a, results_b, sample_size, significance_level
        )

        winner = "A" if results_a["performance_score"] > results_b["performance_score"] else "B"
        confidence = abs(results_a["performance_score"] - results_b["performance_score"]) / max(results_a["performance_score"], results_b["performance_score"]) * 100

        return {
            "test_id": f"abtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "element_tested": test_element,
            "sample_size": sample_size,
            "variants": {
                "A": {
                    "config": variant_a,
                    "metrics": results_a
                },
                "B": {
                    "config": variant_b,
                    "metrics": results_b
                }
            },
            "results": {
                "winner": winner,
                "confidence_level": confidence,
                "is_statistically_significant": is_significant,
                "improvement": abs(results_a["performance_score"] - results_b["performance_score"]),
                "recommendation": f"Utiliser la variante {winner}" if is_significant else "Continuer le test"
            },
            "next_actions": self._generate_ab_test_actions(results_a, results_b, is_significant)
        }

    async def _manage_contacts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gère les contacts (ajout, mise à jour, suppression)"""
        action = data.get("action", "add")  # add, update, remove, bulk_import
        contacts_data = data.get("contacts", [])

        results = {
            "action": action,
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "errors": []
        }

        for contact_data in contacts_data:
            try:
                if action == "add":
                    contact = EmailContact(
                        email=contact_data["email"],
                        name=contact_data.get("name", ""),
                        segments=contact_data.get("segments", []),
                        preferences=contact_data.get("preferences", {}),
                        engagement_score=0.0,
                        status="active"
                    )

                    # Vérifier les doublons
                    if not self._contact_exists(contact.email):
                        self.contacts_db.append(contact)
                        results["successful"] += 1
                    else:
                        results["errors"].append(f"Contact {contact.email} existe déjà")
                        results["failed"] += 1

                elif action == "update":
                    updated = self._update_contact(contact_data["email"], contact_data)
                    if updated:
                        results["successful"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append(f"Contact {contact_data['email']} introuvable")

                elif action == "remove":
                    removed = self._remove_contact(contact_data["email"])
                    if removed:
                        results["successful"] += 1
                    else:
                        results["failed"] += 1

                results["processed"] += 1

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Erreur traitement {contact_data.get('email', 'inconnu')}: {str(e)}")

        return {
            **results,
            "total_contacts": len(self.contacts_db),
            "segments_distribution": self._get_segments_distribution(),
            "engagement_stats": self._get_engagement_stats()
        }

    async def _optimize_send_timing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimise les heures d'envoi selon les données d'engagement"""
        segment = data.get("segment", "all")
        timezone = data.get("timezone", "America/Montreal")  # Quebec timezone
        campaign_type = data.get("campaign_type", "newsletter")

        # Analyser les données historiques d'engagement
        engagement_data = self._analyze_historical_engagement(segment, timezone)

        # Recommandations par jour de la semaine
        weekly_recommendations = {
            "monday": {"time": "09:00", "expected_open_rate": 22.5},
            "tuesday": {"time": "10:00", "expected_open_rate": 25.3},
            "wednesday": {"time": "10:00", "expected_open_rate": 24.8},
            "thursday": {"time": "10:30", "expected_open_rate": 23.9},
            "friday": {"time": "11:00", "expected_open_rate": 21.2},
            "saturday": {"time": "14:00", "expected_open_rate": 18.7},
            "sunday": {"time": "15:00", "expected_open_rate": 19.1}
        }

        # Optimisation spécifique au type de campagne
        campaign_adjustments = {
            "welcome": {"time_offset": -60, "open_rate_boost": 15},  # 1h plus tôt, +15% ouverture
            "newsletter": {"time_offset": 0, "open_rate_boost": 0},
            "promotional": {"time_offset": 30, "open_rate_boost": 8},  # 30min plus tard, +8% ouverture
            "reengagement": {"time_offset": -30, "open_rate_boost": 12}
        }

        optimal_schedule = {}
        for day, base_rec in weekly_recommendations.items():
            adjustment = campaign_adjustments.get(campaign_type, {"time_offset": 0, "open_rate_boost": 0})

            # Ajuster l'heure
            base_time = datetime.strptime(base_rec["time"], "%H:%M")
            adjusted_time = base_time + timedelta(minutes=adjustment["time_offset"])

            optimal_schedule[day] = {
                "optimal_time": adjusted_time.strftime("%H:%M"),
                "expected_open_rate": base_rec["expected_open_rate"] + adjustment["open_rate_boost"],
                "timezone": timezone
            }

        return {
            "segment": segment,
            "campaign_type": campaign_type,
            "timezone": timezone,
            "optimal_schedule": optimal_schedule,
            "best_day": max(optimal_schedule.items(), key=lambda x: x[1]["expected_open_rate"])[0],
            "worst_day": min(optimal_schedule.items(), key=lambda x: x[1]["expected_open_rate"])[0],
            "engagement_insights": {
                "peak_hours": ["10:00-11:00", "14:00-15:00"],
                "low_engagement_periods": ["06:00-08:00", "22:00-24:00"],
                "weekend_behavior": "Engagement réduit mais meilleure attention aux contenus premium"
            },
            "recommendations": [
                f"Envoyer les newsletters le {max(optimal_schedule.items(), key=lambda x: x[1]['expected_open_rate'])[0]} à {optimal_schedule[max(optimal_schedule.items(), key=lambda x: x[1]['expected_open_rate'])[0]]['optimal_time']}",
                "Éviter les envois le vendredi après 15h",
                "Tester les envois de fin de semaine pour le contenu premium",
                f"Personnaliser selon le segment {segment}"
            ]
        }

    async def _generate_email_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un rapport complet des performances email"""
        period = data.get("period", "30d")
        include_segments = data.get("include_segments", True)
        include_ab_tests = data.get("include_ab_tests", True)

        # Métriques globales
        global_metrics = self._calculate_global_metrics(period)

        # Performance par segment
        segment_performance = {}
        if include_segments:
            for segment_name in self.customer_segments.keys():
                segment_performance[segment_name] = self._calculate_segment_metrics(segment_name, period)

        # Résultats A/B tests
        ab_test_results = []
        if include_ab_tests:
            ab_test_results = self._get_recent_ab_tests(period)

        # Tendances et insights
        trends = self._analyze_email_trends(period)

        # Recommandations stratégiques
        strategic_recommendations = self._generate_strategic_recommendations(global_metrics, segment_performance)

        return {
            "report_period": period,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_campaigns": global_metrics["campaigns_sent"],
                "total_emails_sent": global_metrics["emails_sent"],
                "avg_open_rate": global_metrics["avg_open_rate"],
                "avg_click_rate": global_metrics["avg_click_rate"],
                "total_revenue": global_metrics["total_revenue"],
                "roi": global_metrics["roi"]
            },
            "segment_performance": segment_performance,
            "top_performing_campaigns": self._get_top_campaigns(period, limit=5),
            "ab_test_insights": {
                "tests_completed": len(ab_test_results),
                "significant_improvements": len([t for t in ab_test_results if t["significant"]]),
                "avg_improvement": sum([t["improvement"] for t in ab_test_results]) / len(ab_test_results) if ab_test_results else 0
            },
            "trends": trends,
            "strategic_recommendations": strategic_recommendations,
            "next_period_forecast": self._forecast_next_period(global_metrics, trends)
        }

    # Méthodes utilitaires

    def _build_welcome_sequence(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Construit la séquence de bienvenue"""
        user_type = data.get("user_type", "individual")

        base_sequence = [
            {
                "delay_days": 0,
                "subject": f"Bienvenue chez iFiveMe, {data.get('user_name', 'cher utilisateur')} ! 🚀",
                "content": self._get_welcome_email_content("day_1", user_type),
                "goal": "onboarding"
            },
            {
                "delay_days": 3,
                "subject": "3 astuces pour maximiser votre networking avec iFiveMe 💡",
                "content": self._get_welcome_email_content("day_3", user_type),
                "goal": "engagement"
            },
            {
                "delay_days": 7,
                "subject": "Vos premiers résultats iFiveMe sont là ! 📊",
                "content": self._get_welcome_email_content("day_7", user_type),
                "goal": "retention"
            }
        ]

        if user_type == "enterprise":
            base_sequence.append({
                "delay_days": 14,
                "subject": "Solutions entreprise iFiveMe : Votre démo personnalisée",
                "content": self._get_welcome_email_content("day_14_enterprise", user_type),
                "goal": "conversion"
            })

        return base_sequence

    def _get_welcome_email_content(self, day: str, user_type: str) -> str:
        """Génère le contenu des emails de bienvenue"""
        templates = {
            "day_1": f"""
Bonjour et bienvenue dans la famille iFiveMe !

Vous venez de faire le premier pas vers une révolution de votre networking professionnel.

🎯 Ce que vous pouvez faire dès maintenant :
• Créer votre première carte d'affaires virtuelle
• Personnaliser votre profil avec vos réseaux sociaux
• Commencer à partager votre carte avec vos contacts

👉 [Créer ma première carte maintenant]

Notre équipe support est là pour vous accompagner : support@ifiveme.com

À bientôt,
L'équipe iFiveMe

P.S. : Suivez-nous sur LinkedIn @iFiveMe pour des conseils networking quotidiens !
""",
            "day_3": """
Bonjour !

Comment se passent vos premiers pas avec iFiveMe ?

Voici 3 astuces de nos experts pour optimiser votre networking :

💡 Astuce #1 : Personnalisez votre carte avec une photo professionnelle
💡 Astuce #2 : Ajoutez vos dernières réalisations et projets
💡 Astuce #3 : Utilisez les analytics pour suivre vos interactions

🚀 Bonus : Saviez-vous que les cartes avec vidéo de présentation ont 300% plus d'engagement ?

[Optimiser ma carte iFiveMe]

Bonne continuation !
L'équipe iFiveMe
""",
            "day_7": """
Une semaine déjà !

Félicitations, voici vos premiers résultats iFiveMe :

📊 Votre carte a été vue X fois
🤝 X nouveaux contacts ajoutés
📈 X% d'engagement sur vos interactions

🎯 Pour aller plus loin :
• Explorez les templates premium
• Configurez votre signature email
• Rejoignez notre communauté d'entrepreneurs

[Voir mon tableau de bord complet]

Continuez sur cette lancée !
L'équipe iFiveMe
"""
        }

        return templates.get(day, "Contenu par défaut iFiveMe")

    async def _get_contacts_by_segment(self, segment: str) -> List[EmailContact]:
        """Récupère les contacts d'un segment"""
        if segment == "all":
            return self.contacts_db

        return [contact for contact in self.contacts_db if segment in contact.segments]

    def _generate_engagement_score(self, segment: str) -> float:
        """Génère un score d'engagement réaliste selon le segment"""
        base_scores = {
            "new_users": 0.7,
            "active_users": 0.85,
            "premium_users": 0.92,
            "inactive_users": 0.25,
            "enterprise_prospects": 0.78
        }

        import random
        base = base_scores.get(segment, 0.5)
        return round(base + random.uniform(-0.15, 0.15), 2)

    def _generate_mock_campaign_metrics(self, campaign_id: str) -> EmailMetrics:
        """Génère des métriques simulées pour une campagne"""
        import random

        sent = random.randint(800, 1500)
        bounce_rate = random.uniform(0.02, 0.05)
        delivered = int(sent * (1 - bounce_rate))
        open_rate = random.uniform(0.18, 0.35)
        opened = int(delivered * open_rate)
        click_rate = random.uniform(0.02, 0.08)
        clicked = int(delivered * click_rate)
        conversion_rate = random.uniform(0.005, 0.025)
        converted = int(clicked * conversion_rate)

        return EmailMetrics(
            sent=sent,
            delivered=delivered,
            opened=opened,
            clicked=clicked,
            unsubscribed=random.randint(1, 10),
            bounced=sent - delivered,
            converted=converted,
            revenue=converted * random.uniform(25, 150)
        )

    def _get_industry_benchmarks(self) -> Dict[str, float]:
        """Retourne les benchmarks de l'industrie"""
        return {
            "open_rate": 21.33,
            "click_rate": 2.62,
            "bounce_rate": 4.31,
            "unsubscribe_rate": 0.26,
            "conversion_rate": 1.87
        }

    def _contact_exists(self, email: str) -> bool:
        """Vérifie si un contact existe déjà"""
        return any(contact.email == email for contact in self.contacts_db)

    def _update_contact(self, email: str, update_data: Dict[str, Any]) -> bool:
        """Met à jour un contact existant"""
        for contact in self.contacts_db:
            if contact.email == email:
                for key, value in update_data.items():
                    if hasattr(contact, key):
                        setattr(contact, key, value)
                return True
        return False

    def _remove_contact(self, email: str) -> bool:
        """Supprime un contact"""
        for i, contact in enumerate(self.contacts_db):
            if contact.email == email:
                del self.contacts_db[i]
                return True
        return False

    def _get_segments_distribution(self) -> Dict[str, int]:
        """Calcule la distribution des segments"""
        distribution = {}
        for contact in self.contacts_db:
            for segment in contact.segments:
                distribution[segment] = distribution.get(segment, 0) + 1
        return distribution

    def _get_engagement_stats(self) -> Dict[str, float]:
        """Calcule les statistiques d'engagement globales"""
        if not self.contacts_db:
            return {"avg_engagement": 0.0, "active_percentage": 0.0}

        total_engagement = sum(contact.engagement_score for contact in self.contacts_db)
        active_contacts = len([c for c in self.contacts_db if c.status == "active"])

        return {
            "avg_engagement": total_engagement / len(self.contacts_db),
            "active_percentage": active_contacts / len(self.contacts_db) * 100
        }

    async def _save_campaign_data(self, campaign: EmailCampaign):
        """Sauvegarde les données de campagne"""
        try:
            campaign_file = self.data_dir / f"campaign_{campaign.id}.json"
            with open(campaign_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(campaign), f, indent=2, default=str, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde campagne: {str(e)}")

    async def _execute_campaign_send(self, campaign: EmailCampaign, contacts: List[EmailContact]) -> Dict[str, Any]:
        """Exécute l'envoi réel d'une campagne (mode simulation)"""
        # Simulation d'envoi
        await asyncio.sleep(1)  # Simuler le temps d'envoi

        metrics = self._generate_mock_campaign_metrics(campaign.id)
        campaign.metrics = asdict(metrics)
        campaign.status = "sent"

        return {"status": "sent", "metrics": asdict(metrics)}

    async def _schedule_campaign(self, campaign: EmailCampaign, contacts: List[EmailContact]) -> Dict[str, Any]:
        """Programme une campagne pour envoi ultérieur"""
        campaign.status = "scheduled"

        return {
            "status": "scheduled",
            "send_time": campaign.send_time.isoformat(),
            "recipients": len(contacts)
        }

    def _estimate_campaign_performance(self, campaign: EmailCampaign, contacts: List[EmailContact]) -> Dict[str, Any]:
        """Estime la performance d'une campagne"""
        avg_engagement = sum(c.engagement_score for c in contacts) / len(contacts) if contacts else 0

        # Estimation basée sur l'engagement du segment
        estimated_open_rate = 15 + (avg_engagement * 25)  # 15-40%
        estimated_click_rate = 2 + (avg_engagement * 6)   # 2-8%

        return {
            "estimated_open_rate": round(estimated_open_rate, 1),
            "estimated_click_rate": round(estimated_click_rate, 1),
            "estimated_revenue": len(contacts) * estimated_click_rate / 100 * 75,  # 75$ par conversion moyenne
            "confidence_level": 0.7 + (avg_engagement * 0.3)
        }

    def _recommend_campaigns_for_segment(self, segment: str) -> List[str]:
        """Recommande des types de campagnes pour un segment"""
        recommendations = {
            "new_users": ["welcome_sequence", "onboarding_tips", "first_success"],
            "active_users": ["newsletter", "feature_announcements", "community_highlights"],
            "premium_users": ["exclusive_content", "advanced_tips", "beta_features"],
            "inactive_users": ["win_back", "special_offers", "what_you_missed"],
            "enterprise_prospects": ["case_studies", "roi_calculator", "demo_invitation"]
        }

        return recommendations.get(segment, ["newsletter", "product_updates"])

    def _calculate_global_metrics(self, period: str) -> Dict[str, Any]:
        """Calcule les métriques globales sur une période"""
        # Simulation de métriques globales
        return {
            "campaigns_sent": 45,
            "emails_sent": 67500,
            "avg_open_rate": 24.7,
            "avg_click_rate": 3.8,
            "total_revenue": 127500.0,
            "roi": 425.0
        }

    def _analyze_performance_trends(self, metrics: EmailMetrics, timeframe: str) -> Dict[str, Any]:
        """Analyse les tendances de performance"""
        return {
            "open_rate_trend": "+2.3% vs période précédente",
            "click_rate_trend": "+0.8% vs période précédente",
            "growth_indicators": ["Amélioration de la personnalisation", "Meilleur timing d'envoi"],
            "areas_for_improvement": ["Taux de désabonnement à surveiller", "Optimiser les CTA"]
        }

    def _generate_campaign_recommendations(self, metrics: EmailMetrics) -> List[str]:
        """Génère des recommandations basées sur les métriques"""
        recommendations = []

        open_rate = (metrics.opened / metrics.delivered * 100) if metrics.delivered > 0 else 0
        click_rate = (metrics.clicked / metrics.delivered * 100) if metrics.delivered > 0 else 0

        if open_rate < 20:
            recommendations.append("Améliorer les objets d'emails avec plus de personnalisation")
        if click_rate < 2:
            recommendations.append("Optimiser les boutons d'appel à l'action")
        if metrics.bounced / metrics.sent > 0.05:
            recommendations.append("Nettoyer la base de données contacts")

        return recommendations