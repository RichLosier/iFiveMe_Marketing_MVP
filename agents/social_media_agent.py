"""
iFiveMe Marketing MVP - Agent Gestionnaire Réseaux Sociaux
Gestion complète des médias sociaux multi-plateformes
"""

import asyncio
import json
import logging
import requests
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import sys
from pathlib import Path
import hashlib
import random
from urllib.parse import urlencode

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.base_agent import BaseAgent, AgentTask
from config.settings import COMPANY_INFO, API_KEYS, AGENTS_CONFIG

class Platform(Enum):
    """Plateformes de médias sociaux supportées"""
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"

class PostStatus(Enum):
    """Statuts des publications"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

class EngagementType(Enum):
    """Types d'engagement"""
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    MENTION = "mention"
    DM = "direct_message"

@dataclass
class SocialMediaPost:
    """Structure d'une publication sur les réseaux sociaux"""
    id: str
    platform: Platform
    content: str
    media_urls: List[str]
    hashtags: List[str]
    scheduled_time: datetime
    status: PostStatus
    analytics: Dict[str, Any]
    created_at: datetime
    published_at: Optional[datetime] = None
    engagement_metrics: Optional[Dict[str, int]] = None

@dataclass
class EngagementActivity:
    """Structure d'une activité d'engagement"""
    id: str
    platform: Platform
    type: EngagementType
    user_id: str
    user_name: str
    content: str
    post_id: Optional[str]
    timestamp: datetime
    handled: bool = False
    response: Optional[str] = None

@dataclass
class InfluencerProfile:
    """Profil d'influenceur"""
    id: str
    platform: Platform
    username: str
    follower_count: int
    engagement_rate: float
    niche: List[str]
    contact_info: Dict[str, str]
    collaboration_history: List[Dict[str, Any]]
    last_contacted: Optional[datetime] = None

@dataclass
class CrisisAlert:
    """Alerte de crise de réputation"""
    id: str
    severity: str  # low, medium, high, critical
    platform: Platform
    trigger_content: str
    sentiment_score: float
    mentions_count: int
    timestamp: datetime
    action_taken: Optional[str] = None

class OptimalTimingAnalyzer:
    """Analyseur pour déterminer les meilleurs horaires de publication"""

    def __init__(self):
        # Données basées sur les études d'engagement au Québec
        self.optimal_times = {
            Platform.LINKEDIN: {
                "weekdays": [(8, 0), (12, 0), (17, 0)],  # 8h, 12h, 17h
                "weekends": [(10, 0), (14, 0)]            # 10h, 14h
            },
            Platform.TWITTER: {
                "weekdays": [(9, 0), (13, 0), (18, 0)],  # 9h, 13h, 18h
                "weekends": [(11, 0), (15, 0)]            # 11h, 15h
            },
            Platform.FACEBOOK: {
                "weekdays": [(9, 30), (13, 30), (19, 0)], # 9h30, 13h30, 19h
                "weekends": [(10, 30), (14, 30)]           # 10h30, 14h30
            },
            Platform.INSTAGRAM: {
                "weekdays": [(11, 0), (14, 0), (20, 0)],  # 11h, 14h, 20h
                "weekends": [(12, 0), (16, 0)]             # 12h, 16h
            }
        }

    def get_next_optimal_time(self, platform: Platform, from_time: datetime = None) -> datetime:
        """Retourne le prochain horaire optimal pour une plateforme"""
        if from_time is None:
            from_time = datetime.now(timezone.utc)

        # Convertir en heure locale du Québec (EST/EDT)
        quebec_tz = timezone(timedelta(hours=-5))  # Approximation
        local_time = from_time.astimezone(quebec_tz)

        times = self.optimal_times.get(platform, {})
        is_weekend = local_time.weekday() >= 5

        schedule = times.get("weekends" if is_weekend else "weekdays", [(9, 0)])

        # Trouver le prochain créneau disponible
        for hour, minute in schedule:
            next_time = local_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_time > local_time:
                return next_time.astimezone(timezone.utc)

        # Si aucun créneau aujourd'hui, prendre le premier de demain
        next_day = local_time + timedelta(days=1)
        next_schedule = times.get("weekends" if next_day.weekday() >= 5 else "weekdays", [(9, 0)])
        hour, minute = next_schedule[0]
        next_time = next_day.replace(hour=hour, minute=minute, second=0, microsecond=0)

        return next_time.astimezone(timezone.utc)

class HashtagOptimizer:
    """Optimiseur de hashtags pour iFiveMe"""

    def __init__(self):
        self.ifiveme_hashtags = {
            "core": ["#iFiveMe", "#CartesVirtuelles", "#NetworkingDigital", "#Quebec"],
            "business": ["#Entrepreneur", "#BusinessCard", "#Networking", "#DigitalBusiness"],
            "tech": ["#Innovation", "#Technology", "#DigitalTransformation", "#VirtualCard"],
            "local": ["#Quebec", "#Montreal", "#Canada", "#Francophone"],
            "trending": []  # À mettre à jour dynamiquement
        }

        self.platform_limits = {
            Platform.LINKEDIN: 30,
            Platform.TWITTER: 10,
            Platform.FACEBOOK: 30,
            Platform.INSTAGRAM: 30,
            Platform.TIKTOK: 100
        }

    def optimize_hashtags(self, platform: Platform, content: str,
                         category: str = "business") -> List[str]:
        """Optimise les hashtags pour une plateforme et un contenu"""
        limit = self.platform_limits.get(platform, 10)

        # Hashtags de base iFiveMe
        hashtags = self.ifiveme_hashtags["core"].copy()

        # Ajouter hashtags par catégorie
        if category in self.ifiveme_hashtags:
            hashtags.extend(self.ifiveme_hashtags[category])

        # Ajouter hashtags locaux pour le marché québécois
        hashtags.extend(self.ifiveme_hashtags["local"])

        # Limiter selon la plateforme et éliminer les doublons
        unique_hashtags = list(dict.fromkeys(hashtags))
        return unique_hashtags[:limit]

class SocialMediaAPIManager:
    """Gestionnaire des APIs des réseaux sociaux avec mocks pour testing"""

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.mock_responses = {}
        self.rate_limits = {
            Platform.LINKEDIN: {"requests_per_hour": 100, "current": 0, "reset_time": None},
            Platform.TWITTER: {"requests_per_hour": 300, "current": 0, "reset_time": None},
            Platform.FACEBOOK: {"requests_per_hour": 200, "current": 0, "reset_time": None},
            Platform.INSTAGRAM: {"requests_per_hour": 200, "current": 0, "reset_time": None}
        }

    async def publish_post(self, platform: Platform, post: SocialMediaPost) -> Dict[str, Any]:
        """Publie un post sur une plateforme"""
        if self.use_mock:
            return await self._mock_publish(platform, post)

        # Vérifier les limites de taux
        if not self._check_rate_limit(platform):
            raise Exception(f"Rate limit dépassé pour {platform.value}")

        try:
            if platform == Platform.LINKEDIN:
                return await self._publish_linkedin(post)
            elif platform == Platform.TWITTER:
                return await self._publish_twitter(post)
            elif platform == Platform.FACEBOOK:
                return await self._publish_facebook(post)
            elif platform == Platform.INSTAGRAM:
                return await self._publish_instagram(post)
            else:
                raise ValueError(f"Plateforme non supportée: {platform}")

        except Exception as e:
            logging.error(f"Erreur publication {platform.value}: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _mock_publish(self, platform: Platform, post: SocialMediaPost) -> Dict[str, Any]:
        """Mock de publication pour testing sans API"""
        # Simuler un délai de réseau
        await asyncio.sleep(random.uniform(0.5, 2.0))

        # Simuler succès/échec (95% succès)
        if random.random() < 0.95:
            mock_post_id = f"mock_{platform.value}_{int(time.time())}"
            return {
                "success": True,
                "post_id": mock_post_id,
                "url": f"https://{platform.value}.com/post/{mock_post_id}",
                "published_at": datetime.now(timezone.utc).isoformat()
            }
        else:
            return {
                "success": False,
                "error": "Mock API error for testing"
            }

    def _check_rate_limit(self, platform: Platform) -> bool:
        """Vérifie si on peut faire une requête selon les limites"""
        limit_info = self.rate_limits.get(platform)
        if not limit_info:
            return True

        now = datetime.now(timezone.utc)

        # Reset si l'heure est passée
        if limit_info["reset_time"] and now > limit_info["reset_time"]:
            limit_info["current"] = 0
            limit_info["reset_time"] = now + timedelta(hours=1)

        # Vérifier la limite
        return limit_info["current"] < limit_info["requests_per_hour"]

    async def get_post_analytics(self, platform: Platform, post_id: str) -> Dict[str, Any]:
        """Récupère les analytics d'un post"""
        if self.use_mock:
            return await self._mock_analytics(platform, post_id)

        # Implementation réelle des APIs ici
        return {}

    async def _mock_analytics(self, platform: Platform, post_id: str) -> Dict[str, Any]:
        """Mock des analytics pour testing"""
        await asyncio.sleep(random.uniform(0.3, 1.0))

        # Générer des métriques réalistes
        base_reach = random.randint(100, 5000)
        engagement_rate = random.uniform(0.02, 0.08)  # 2-8%

        return {
            "post_id": post_id,
            "platform": platform.value,
            "metrics": {
                "reach": base_reach,
                "impressions": int(base_reach * random.uniform(1.2, 3.0)),
                "likes": int(base_reach * engagement_rate * 0.6),
                "comments": int(base_reach * engagement_rate * 0.15),
                "shares": int(base_reach * engagement_rate * 0.25),
                "clicks": int(base_reach * engagement_rate * 0.3),
                "engagement_rate": round(engagement_rate, 4)
            },
            "demographics": {
                "age_groups": {"25-34": 35, "35-44": 30, "45-54": 20, "18-24": 15},
                "locations": {"Quebec": 60, "Ontario": 25, "Other": 15}
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

class SocialMediaAgent(BaseAgent):
    """Agent gestionnaire complet des réseaux sociaux pour iFiveMe"""

    def __init__(self, use_mock_apis: bool = True):
        super().__init__(
            agent_id="social_media_manager",
            name="Agent Gestionnaire Réseaux Sociaux iFiveMe",
            config={
                "platforms": ["linkedin", "twitter", "facebook", "instagram"],
                "posting_frequency": {"daily": 3, "weekly": 21},
                "engagement_response_time": 3600,  # 1 heure en secondes
                "crisis_monitoring_interval": 300   # 5 minutes
            }
        )

        # Composants spécialisés
        self.timing_analyzer = OptimalTimingAnalyzer()
        self.hashtag_optimizer = HashtagOptimizer()
        self.api_manager = SocialMediaAPIManager(use_mock=use_mock_apis)

        # Stockage des données
        self.scheduled_posts: List[SocialMediaPost] = []
        self.published_posts: List[SocialMediaPost] = []
        self.engagement_queue: List[EngagementActivity] = []
        self.influencer_database: List[InfluencerProfile] = []
        self.crisis_alerts: List[CrisisAlert] = []

        # Cache pour les analytics
        self.analytics_cache = {}
        self.cache_ttl = 1800  # 30 minutes

        # Configuration spécifique iFiveMe
        self.brand_voice = {
            "tone": "professionnel mais accessible",
            "keywords": ["innovation", "networking", "digital", "professionnel"],
            "avoid": ["spam", "pushy", "aggressive"],
            "emojis": ["💼", "🚀", "💡", "🔗", "📱", "✨"]
        }

        self.content_themes = [
            "innovation_produit",
            "success_stories",
            "networking_tips",
            "digital_transformation",
            "testimonials",
            "behind_scenes",
            "industry_insights"
        ]

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent"""
        return [
            "Publication multi-plateforme automatisée",
            "Planification de contenu avec timing optimal",
            "Gestion des réponses et engagement communautaire",
            "Monitoring des mentions et hashtags",
            "Analytics et reporting de performance",
            "Optimisation des hashtags par plateforme",
            "Coordination avec influenceurs",
            "Détection et gestion de crise de réputation",
            "A/B testing des contenus",
            "Veille concurrentielle automatisée"
        ]

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite les différents types de tâches sociales"""
        task_type = task.type
        data = task.data

        try:
            if task_type == "publish_post":
                return await self._handle_publish_post(data)
            elif task_type == "schedule_posts":
                return await self._handle_schedule_posts(data)
            elif task_type == "engage_community":
                return await self._handle_community_engagement(data)
            elif task_type == "analyze_performance":
                return await self._handle_performance_analysis(data)
            elif task_type == "monitor_mentions":
                return await self._handle_mention_monitoring(data)
            elif task_type == "influencer_outreach":
                return await self._handle_influencer_outreach(data)
            elif task_type == "crisis_management":
                return await self._handle_crisis_management(data)
            elif task_type == "competitive_analysis":
                return await self._handle_competitive_analysis(data)
            else:
                raise ValueError(f"Type de tâche non supporté: {task_type}")

        except Exception as e:
            self.logger.error(f"Erreur traitement tâche {task_type}: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _handle_publish_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la publication immédiate d'un post"""
        try:
            platform = Platform(data["platform"])
            content = data["content"]
            media_urls = data.get("media_urls", [])

            # Optimiser les hashtags
            hashtags = self.hashtag_optimizer.optimize_hashtags(
                platform, content, data.get("category", "business")
            )

            # Créer le post
            post = SocialMediaPost(
                id=f"post_{int(time.time())}_{platform.value}",
                platform=platform,
                content=content,
                media_urls=media_urls,
                hashtags=hashtags,
                scheduled_time=datetime.now(timezone.utc),
                status=PostStatus.DRAFT,
                analytics={},
                created_at=datetime.now(timezone.utc)
            )

            # Publier
            result = await self.api_manager.publish_post(platform, post)

            if result["success"]:
                post.status = PostStatus.PUBLISHED
                post.published_at = datetime.now(timezone.utc)
                self.published_posts.append(post)

                self.logger.info(f"Post publié avec succès sur {platform.value}: {result['post_id']}")

                return {
                    "success": True,
                    "post_id": result["post_id"],
                    "platform": platform.value,
                    "url": result.get("url"),
                    "analytics_available": False
                }
            else:
                post.status = PostStatus.FAILED
                return {
                    "success": False,
                    "error": result["error"],
                    "post_id": post.id
                }

        except Exception as e:
            self.logger.error(f"Erreur publication post: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _handle_schedule_posts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la planification de posts sur plusieurs plateformes"""
        try:
            content_batch = data["content_batch"]  # Liste de contenus
            platforms = [Platform(p) for p in data["platforms"]]
            start_date = datetime.fromisoformat(data.get("start_date", datetime.now(timezone.utc).isoformat()))

            scheduled_posts = []

            for i, content_item in enumerate(content_batch):
                for platform in platforms:
                    # Calculer l'horaire optimal
                    base_time = start_date + timedelta(days=i // 3)  # 3 posts par jour
                    optimal_time = self.timing_analyzer.get_next_optimal_time(platform, base_time)

                    # Optimiser hashtags
                    hashtags = self.hashtag_optimizer.optimize_hashtags(
                        platform, content_item["content"], content_item.get("category", "business")
                    )

                    # Créer post planifié
                    post = SocialMediaPost(
                        id=f"scheduled_{int(time.time())}_{i}_{platform.value}",
                        platform=platform,
                        content=content_item["content"],
                        media_urls=content_item.get("media_urls", []),
                        hashtags=hashtags,
                        scheduled_time=optimal_time,
                        status=PostStatus.SCHEDULED,
                        analytics={},
                        created_at=datetime.now(timezone.utc)
                    )

                    self.scheduled_posts.append(post)
                    scheduled_posts.append({
                        "post_id": post.id,
                        "platform": platform.value,
                        "scheduled_time": optimal_time.isoformat(),
                        "content_preview": content_item["content"][:100] + "..."
                    })

            self.logger.info(f"Planification de {len(scheduled_posts)} posts terminée")

            return {
                "success": True,
                "scheduled_posts_count": len(scheduled_posts),
                "posts": scheduled_posts,
                "next_publication": min(p["scheduled_time"] for p in scheduled_posts)
            }

        except Exception as e:
            self.logger.error(f"Erreur planification posts: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _handle_community_engagement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gère l'engagement avec la communauté"""
        try:
            platforms = [Platform(p) for p in data.get("platforms", ["linkedin", "twitter"])]
            response_templates = data.get("response_templates", {})

            engagement_results = []

            for platform in platforms:
                # Simuler la récupération des mentions/interactions
                mock_engagements = await self._get_platform_engagements(platform)

                for engagement in mock_engagements:
                    if not engagement.handled:
                        response = await self._generate_engagement_response(engagement, response_templates)

                        # Mock de la réponse (en réalité on utiliserait l'API)
                        success = await self._send_engagement_response(engagement, response)

                        if success:
                            engagement.handled = True
                            engagement.response = response

                        engagement_results.append({
                            "engagement_id": engagement.id,
                            "platform": platform.value,
                            "type": engagement.type.value,
                            "user": engagement.user_name,
                            "handled": engagement.handled,
                            "response_sent": success
                        })

            handled_count = sum(1 for r in engagement_results if r["handled"])

            return {
                "success": True,
                "total_engagements": len(engagement_results),
                "handled_count": handled_count,
                "response_rate": round(handled_count / len(engagement_results) * 100, 2) if engagement_results else 0,
                "engagements": engagement_results
            }

        except Exception as e:
            self.logger.error(f"Erreur engagement communautaire: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _handle_performance_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse les performances des posts"""
        try:
            period_days = data.get("period_days", 7)
            platforms = [Platform(p) for p in data.get("platforms", ["linkedin", "twitter", "facebook"])]

            start_date = datetime.now(timezone.utc) - timedelta(days=period_days)

            # Filtrer les posts publiés dans la période
            recent_posts = [
                p for p in self.published_posts
                if p.published_at and p.published_at >= start_date and p.platform in platforms
            ]

            analytics_results = {}
            total_metrics = {
                "reach": 0,
                "engagement": 0,
                "clicks": 0,
                "shares": 0
            }

            for platform in platforms:
                platform_posts = [p for p in recent_posts if p.platform == platform]
                platform_metrics = {"posts_count": len(platform_posts), "metrics": {}}

                for post in platform_posts:
                    # Récupérer ou générer les analytics
                    analytics = await self.api_manager.get_post_analytics(platform, post.id)
                    post.analytics = analytics

                    # Agréger les métriques
                    if "metrics" in analytics:
                        for metric, value in analytics["metrics"].items():
                            if metric in platform_metrics["metrics"]:
                                platform_metrics["metrics"][metric] += value
                            else:
                                platform_metrics["metrics"][metric] = value

                            # Métriques totales
                            if metric in total_metrics:
                                total_metrics[metric] += value

                # Calculer les moyennes
                if len(platform_posts) > 0:
                    for metric in platform_metrics["metrics"]:
                        platform_metrics["metrics"][f"avg_{metric}"] = round(
                            platform_metrics["metrics"][metric] / len(platform_posts), 2
                        )

                analytics_results[platform.value] = platform_metrics

            # Identifier les meilleurs posts
            best_posts = sorted(
                recent_posts,
                key=lambda p: p.analytics.get("metrics", {}).get("engagement_rate", 0),
                reverse=True
            )[:5]

            best_posts_data = [{
                "post_id": p.id,
                "platform": p.platform.value,
                "content_preview": p.content[:100] + "...",
                "engagement_rate": p.analytics.get("metrics", {}).get("engagement_rate", 0),
                "reach": p.analytics.get("metrics", {}).get("reach", 0)
            } for p in best_posts]

            return {
                "success": True,
                "period_days": period_days,
                "total_posts": len(recent_posts),
                "platform_analytics": analytics_results,
                "total_metrics": total_metrics,
                "best_performing_posts": best_posts_data,
                "recommendations": await self._generate_performance_recommendations(analytics_results)
            }

        except Exception as e:
            self.logger.error(f"Erreur analyse performance: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _handle_mention_monitoring(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Surveille les mentions de iFiveMe"""
        try:
            keywords = data.get("keywords", ["iFiveMe", "@iFiveMe", "#iFiveMe", "carte affaires virtuelle"])
            platforms = [Platform(p) for p in data.get("platforms", ["twitter", "linkedin", "facebook"])]

            mentions_found = []
            sentiment_summary = {"positive": 0, "neutral": 0, "negative": 0}

            for platform in platforms:
                # Mock de monitoring des mentions
                platform_mentions = await self._monitor_platform_mentions(platform, keywords)
                mentions_found.extend(platform_mentions)

                # Analyser le sentiment
                for mention in platform_mentions:
                    sentiment = await self._analyze_sentiment(mention["content"])
                    mention["sentiment"] = sentiment
                    sentiment_summary[sentiment] += 1

            # Identifier les mentions critiques
            critical_mentions = [
                m for m in mentions_found
                if m.get("sentiment") == "negative" and m.get("follower_count", 0) > 1000
            ]

            # Générer des alertes si nécessaire
            if critical_mentions:
                for mention in critical_mentions:
                    alert = CrisisAlert(
                        id=f"alert_{int(time.time())}",
                        severity="high" if mention.get("follower_count", 0) > 10000 else "medium",
                        platform=Platform(mention["platform"]),
                        trigger_content=mention["content"],
                        sentiment_score=mention.get("sentiment_score", -0.5),
                        mentions_count=1,
                        timestamp=datetime.now(timezone.utc)
                    )
                    self.crisis_alerts.append(alert)

            return {
                "success": True,
                "total_mentions": len(mentions_found),
                "sentiment_breakdown": sentiment_summary,
                "critical_mentions_count": len(critical_mentions),
                "mentions": mentions_found[:20],  # Limiter pour l'affichage
                "alerts_generated": len(critical_mentions)
            }

        except Exception as e:
            self.logger.error(f"Erreur monitoring mentions: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _handle_influencer_outreach(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gère les campagnes d'outreach vers les influenceurs"""
        try:
            campaign_type = data.get("campaign_type", "product_awareness")
            target_follower_range = data.get("follower_range", [1000, 100000])
            niches = data.get("niches", ["business", "networking", "technology"])

            # Rechercher des influenceurs pertinents
            potential_influencers = await self._find_relevant_influencers(
                target_follower_range, niches
            )

            outreach_results = []

            for influencer in potential_influencers[:10]:  # Limiter à 10 pour l'exemple
                # Générer un message personnalisé
                message = await self._generate_influencer_outreach_message(
                    influencer, campaign_type
                )

                # Mock d'envoi du message
                sent_success = await self._send_influencer_message(influencer, message)

                if sent_success:
                    influencer.last_contacted = datetime.now(timezone.utc)

                outreach_results.append({
                    "influencer_id": influencer.id,
                    "username": influencer.username,
                    "platform": influencer.platform.value,
                    "followers": influencer.follower_count,
                    "engagement_rate": influencer.engagement_rate,
                    "message_sent": sent_success,
                    "message_preview": message[:100] + "..."
                })

            successful_outreach = sum(1 for r in outreach_results if r["message_sent"])

            return {
                "success": True,
                "campaign_type": campaign_type,
                "influencers_contacted": len(outreach_results),
                "successful_contacts": successful_outreach,
                "success_rate": round(successful_outreach / len(outreach_results) * 100, 2),
                "outreach_results": outreach_results
            }

        except Exception as e:
            self.logger.error(f"Erreur outreach influenceurs: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _handle_crisis_management(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gère les crises de réputation"""
        try:
            severity_threshold = data.get("severity_threshold", "medium")
            auto_respond = data.get("auto_respond", False)

            # Vérifier les alertes actives
            active_alerts = [
                alert for alert in self.crisis_alerts
                if not alert.action_taken and self._get_severity_level(alert.severity) >= self._get_severity_level(severity_threshold)
            ]

            crisis_actions = []

            for alert in active_alerts:
                action_plan = await self._generate_crisis_action_plan(alert)

                if auto_respond and alert.severity in ["low", "medium"]:
                    # Réponse automatique pour les crises mineures
                    response_sent = await self._execute_crisis_response(alert, action_plan)
                    alert.action_taken = "automated_response" if response_sent else "failed_response"
                else:
                    # Escalade pour les crises importantes
                    alert.action_taken = "escalated_to_human"

                crisis_actions.append({
                    "alert_id": alert.id,
                    "severity": alert.severity,
                    "platform": alert.platform.value,
                    "action_taken": alert.action_taken,
                    "action_plan": action_plan,
                    "timestamp": alert.timestamp.isoformat()
                })

            # Générer un rapport de situation
            situation_report = await self._generate_crisis_report(active_alerts)

            return {
                "success": True,
                "active_crises": len(active_alerts),
                "actions_taken": len(crisis_actions),
                "auto_resolved": sum(1 for a in crisis_actions if "automated" in a["action_taken"]),
                "escalated": sum(1 for a in crisis_actions if "escalated" in a["action_taken"]),
                "crisis_actions": crisis_actions,
                "situation_report": situation_report
            }

        except Exception as e:
            self.logger.error(f"Erreur gestion de crise: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _handle_competitive_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse la concurrence sur les réseaux sociaux"""
        try:
            competitors = data.get("competitors", ["HiHello", "CamCard", "Digitalo"])
            platforms = [Platform(p) for p in data.get("platforms", ["linkedin", "twitter"])]
            analysis_period = data.get("period_days", 30)

            competitive_analysis = {}

            for competitor in competitors:
                competitor_data = {}

                for platform in platforms:
                    # Mock d'analyse concurrentielle
                    platform_analysis = await self._analyze_competitor_platform(
                        competitor, platform, analysis_period
                    )
                    competitor_data[platform.value] = platform_analysis

                competitive_analysis[competitor] = competitor_data

            # Générer des insights et recommandations
            insights = await self._generate_competitive_insights(competitive_analysis)

            # Identifier les opportunités
            opportunities = await self._identify_content_opportunities(competitive_analysis)

            return {
                "success": True,
                "analysis_period_days": analysis_period,
                "competitors_analyzed": len(competitors),
                "competitive_analysis": competitive_analysis,
                "key_insights": insights,
                "content_opportunities": opportunities,
                "recommendations": await self._generate_competitive_recommendations(competitive_analysis)
            }

        except Exception as e:
            self.logger.error(f"Erreur analyse concurrentielle: {str(e)}")
            return {"success": False, "error": str(e)}

    # Méthodes utilitaires et helpers

    async def _get_platform_engagements(self, platform: Platform) -> List[EngagementActivity]:
        """Mock pour récupérer les engagements d'une plateforme"""
        mock_engagements = []

        # Générer des engagements fictifs pour testing
        for i in range(random.randint(3, 8)):
            engagement = EngagementActivity(
                id=f"engagement_{platform.value}_{i}_{int(time.time())}",
                platform=platform,
                type=random.choice(list(EngagementType)),
                user_id=f"user_{random.randint(1000, 9999)}",
                user_name=f"User{random.randint(100, 999)}",
                content=f"Contenu d'engagement simulé {i} pour iFiveMe",
                post_id=f"post_{random.randint(1, 100)}",
                timestamp=datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 24)),
                handled=False
            )
            mock_engagements.append(engagement)

        return mock_engagements

    async def _generate_engagement_response(self, engagement: EngagementActivity, templates: Dict) -> str:
        """Génère une réponse personnalisée pour un engagement"""
        response_templates = {
            EngagementType.COMMENT: [
                "Merci pour votre commentaire! Nous sommes ravis que iFiveMe vous intéresse.",
                "Excellente question! Notre équipe va vous répondre rapidement.",
                "Nous apprécions votre feedback! C'est exactement ce qui nous motive chez iFiveMe."
            ],
            EngagementType.MENTION: [
                "Merci de mentionner iFiveMe! Nous sommes là si vous avez des questions.",
                "Nous sommes honorés d'être mentionnés! Comment pouvons-nous vous aider?",
                "Merci pour le partage! N'hésitez pas à nous contacter pour en savoir plus."
            ],
            EngagementType.DM: [
                "Bonjour! Merci de votre intérêt pour iFiveMe. Comment pouvons-nous vous aider?",
                "Salut! Notre équipe est disponible pour répondre à toutes vos questions sur nos cartes virtuelles."
            ]
        }

        if engagement.type in response_templates:
            return random.choice(response_templates[engagement.type])

        return "Merci pour votre intérêt envers iFiveMe! Notre équipe reviendra vers vous rapidement."

    async def _send_engagement_response(self, engagement: EngagementActivity, response: str) -> bool:
        """Mock d'envoi de réponse d'engagement"""
        # Simuler un délai et un taux de succès
        await asyncio.sleep(random.uniform(0.5, 2.0))
        return random.random() > 0.1  # 90% de succès

    async def _monitor_platform_mentions(self, platform: Platform, keywords: List[str]) -> List[Dict[str, Any]]:
        """Mock de surveillance des mentions"""
        mentions = []

        for _ in range(random.randint(2, 8)):
            mention = {
                "id": f"mention_{platform.value}_{int(time.time())}_{random.randint(1, 1000)}",
                "platform": platform.value,
                "content": f"Mention simulée de {random.choice(keywords)} - super produit!",
                "author": f"user_{random.randint(1000, 9999)}",
                "follower_count": random.randint(100, 50000),
                "timestamp": datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48)),
                "url": f"https://{platform.value}.com/post/{random.randint(100000, 999999)}"
            }
            mentions.append(mention)

        return mentions

    async def _analyze_sentiment(self, content: str) -> str:
        """Analyse de sentiment basique (mock)"""
        # Mots positifs/négatifs simples pour simulation
        positive_words = ["super", "excellent", "génial", "parfait", "recommande", "love", "amazing"]
        negative_words = ["nul", "mauvais", "problème", "bug", "déçu", "horrible", "waste"]

        content_lower = content.lower()
        positive_score = sum(1 for word in positive_words if word in content_lower)
        negative_score = sum(1 for word in negative_words if word in content_lower)

        if positive_score > negative_score:
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        else:
            return "neutral"

    def _get_severity_level(self, severity: str) -> int:
        """Convertit le niveau de sévérité en nombre"""
        levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return levels.get(severity, 1)

    async def _generate_crisis_action_plan(self, alert: CrisisAlert) -> Dict[str, Any]:
        """Génère un plan d'action pour une crise"""
        return {
            "immediate_actions": [
                "Surveiller l'évolution de la situation",
                "Préparer une réponse officielle",
                "Alerter l'équipe de direction"
            ],
            "communication_strategy": "Réponse transparente et professionnelle",
            "timeline": "Réponse dans les 2 heures",
            "escalation_needed": alert.severity in ["high", "critical"]
        }

    async def _execute_crisis_response(self, alert: CrisisAlert, action_plan: Dict) -> bool:
        """Exécute la réponse à une crise"""
        # Mock d'exécution
        await asyncio.sleep(random.uniform(1.0, 3.0))
        return random.random() > 0.2  # 80% de succès

    async def _generate_crisis_report(self, alerts: List[CrisisAlert]) -> Dict[str, Any]:
        """Génère un rapport de situation de crise"""
        return {
            "total_alerts": len(alerts),
            "severity_breakdown": {
                severity: len([a for a in alerts if a.severity == severity])
                for severity in ["low", "medium", "high", "critical"]
            },
            "platforms_affected": list(set(a.platform.value for a in alerts)),
            "recommended_actions": [
                "Maintenir la surveillance active",
                "Préparer des réponses proactives",
                "Réviser la stratégie de communication"
            ]
        }

    async def _find_relevant_influencers(self, follower_range: List[int], niches: List[str]) -> List[InfluencerProfile]:
        """Mock de recherche d'influenceurs"""
        mock_influencers = []

        for i in range(random.randint(5, 15)):
            influencer = InfluencerProfile(
                id=f"influencer_{i}_{int(time.time())}",
                platform=random.choice(list(Platform)),
                username=f"@influencer{i}",
                follower_count=random.randint(follower_range[0], follower_range[1]),
                engagement_rate=random.uniform(0.02, 0.15),
                niche=random.sample(niches, random.randint(1, len(niches))),
                contact_info={"email": f"influencer{i}@email.com"},
                collaboration_history=[]
            )
            mock_influencers.append(influencer)

        return mock_influencers

    async def _generate_influencer_outreach_message(self, influencer: InfluencerProfile, campaign_type: str) -> str:
        """Génère un message d'approche personnalisé"""
        templates = {
            "product_awareness": f"""
Bonjour {influencer.username},

Nous avons découvert votre contenu sur {influencer.platform.value} et sommes impressionnés par votre expertise dans le domaine du networking professionnel.

Chez iFiveMe, nous révolutionnons les cartes d'affaires avec notre solution virtuelle. Nous pensons que cela pourrait intéresser votre audience de {influencer.follower_count} abonnés.

Seriez-vous intéressé(e) par une collaboration? Nous proposons un accès gratuit à notre plateforme premium et sommes ouverts à discuter d'un partenariat.

Cordialement,
L'équipe iFiveMe
            """,
            "content_collaboration": f"""
Bonjour {influencer.username},

Votre contenu sur {influencer.platform.value} résonne parfaitement avec notre mission chez iFiveMe.

Nous cherchons des créateurs authentiques pour partager leurs expériences avec nos cartes d'affaires virtuelles. Votre engagement de {influencer.engagement_rate:.1%} montre la qualité de votre communauté.

Intéressé(e) par une collaboration de contenu?

Bien à vous,
iFiveMe
            """
        }

        return templates.get(campaign_type, templates["product_awareness"]).strip()

    async def _send_influencer_message(self, influencer: InfluencerProfile, message: str) -> bool:
        """Mock d'envoi de message à un influenceur"""
        await asyncio.sleep(random.uniform(0.5, 2.0))
        return random.random() > 0.3  # 70% de succès d'envoi

    async def _analyze_competitor_platform(self, competitor: str, platform: Platform, days: int) -> Dict[str, Any]:
        """Mock d'analyse concurrentielle"""
        return {
            "posts_count": random.randint(5, 30),
            "avg_engagement_rate": round(random.uniform(0.01, 0.08), 4),
            "follower_growth": random.randint(-100, 500),
            "top_performing_content_types": random.sample(
                ["product_demo", "tips", "testimonials", "behind_scenes"], 2
            ),
            "posting_frequency": round(random.uniform(0.5, 2.0), 1),
            "peak_activity_hours": random.sample(list(range(8, 20)), 3)
        }

    async def _generate_competitive_insights(self, analysis: Dict) -> List[str]:
        """Génère des insights concurrentiels"""
        return [
            "Les concurrents publient principalement en matinée (8h-11h)",
            "Le contenu éducatif génère 40% plus d'engagement",
            "LinkedIn reste la plateforme principale pour le B2B",
            "Les démonstrations produit performent mieux que les annonces",
            "La fréquence optimale semble être 1-2 posts par jour"
        ]

    async def _identify_content_opportunities(self, analysis: Dict) -> List[str]:
        """Identifie les opportunités de contenu"""
        return [
            "Gap sur le contenu 'behind the scenes' - opportunité à saisir",
            "Peu de contenu vidéo chez les concurrents sur Instagram",
            "Testimonials clients sous-exploités",
            "Créneaux horaires 13h-15h peu utilisés",
            "Hashtags de niche peu exploités"
        ]

    async def _generate_competitive_recommendations(self, analysis: Dict) -> List[str]:
        """Génère des recommandations basées sur l'analyse"""
        return [
            "Augmenter la fréquence de publication sur LinkedIn",
            "Développer plus de contenu vidéo court (Reels/Stories)",
            "Créer une série de témoignages clients",
            "Explorer les créneaux horaires moins saturés",
            "Optimiser l'usage des hashtags de niche"
        ]

    async def _generate_performance_recommendations(self, analytics: Dict) -> List[str]:
        """Génère des recommandations d'amélioration des performances"""
        recommendations = []

        # Analyse basique des performances
        total_posts = sum(platform_data.get("posts_count", 0) for platform_data in analytics.values())

        if total_posts < 10:
            recommendations.append("Augmenter la fréquence de publication pour améliorer la visibilité")

        # Recommandations par plateforme
        for platform, data in analytics.items():
            avg_engagement = data.get("metrics", {}).get("avg_engagement_rate", 0)
            if avg_engagement < 0.02:  # Moins de 2%
                recommendations.append(f"Améliorer l'engagement sur {platform} avec du contenu plus interactif")

        recommendations.extend([
            "Publier du contenu vidéo pour augmenter l'engagement",
            "Utiliser plus de questions pour encourager les commentaires",
            "Optimiser les horaires de publication selon l'audience",
            "Tester différents formats de contenu (carrousels, stories, etc.)"
        ])

        return recommendations

    async def execute_scheduled_posts(self):
        """Exécute les posts programmés qui sont dus"""
        now = datetime.now(timezone.utc)
        due_posts = [
            post for post in self.scheduled_posts
            if post.scheduled_time <= now and post.status == PostStatus.SCHEDULED
        ]

        for post in due_posts:
            try:
                result = await self.api_manager.publish_post(post.platform, post)

                if result["success"]:
                    post.status = PostStatus.PUBLISHED
                    post.published_at = now
                    self.published_posts.append(post)
                    self.logger.info(f"Post programmé publié: {post.id}")
                else:
                    post.status = PostStatus.FAILED
                    self.logger.error(f"Échec publication post programmé: {post.id}")

                # Retirer de la liste des posts programmés
                self.scheduled_posts.remove(post)

            except Exception as e:
                self.logger.error(f"Erreur publication post programmé {post.id}: {str(e)}")
                post.status = PostStatus.FAILED

    async def generate_content_calendar(self, days: int = 30) -> Dict[str, Any]:
        """Génère un calendrier de contenu pour les prochains jours"""
        calendar = {}
        start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        for day in range(days):
            current_date = start_date + timedelta(days=day)
            date_key = current_date.strftime("%Y-%m-%d")

            # 3 posts par jour avec themes rotatifs
            daily_posts = []
            themes = self.content_themes

            for slot in range(3):  # 3 créneaux par jour
                theme = themes[(day * 3 + slot) % len(themes)]
                platforms = [Platform.LINKEDIN, Platform.TWITTER, Platform.FACEBOOK]

                for platform in platforms:
                    optimal_time = self.timing_analyzer.get_next_optimal_time(
                        platform, current_date + timedelta(hours=8 + slot * 4)
                    )

                    post_suggestion = {
                        "time": optimal_time.strftime("%H:%M"),
                        "platform": platform.value,
                        "theme": theme,
                        "suggested_hashtags": self.hashtag_optimizer.optimize_hashtags(
                            platform, "", theme
                        )[:5],
                        "content_type": random.choice([
                            "educational", "promotional", "behind_scenes", "user_generated"
                        ])
                    }
                    daily_posts.append(post_suggestion)

            calendar[date_key] = {
                "date": current_date.strftime("%A, %B %d, %Y"),
                "posts": daily_posts[:6],  # Limiter à 6 posts par jour
                "weekly_theme": themes[(day // 7) % len(themes)]
            }

        return {
            "calendar": calendar,
            "total_days": days,
            "posts_per_day": 6,
            "total_planned_posts": days * 6
        }

    async def get_social_media_dashboard(self) -> Dict[str, Any]:
        """Génère un tableau de bord des médias sociaux"""
        now = datetime.now(timezone.utc)
        last_7_days = now - timedelta(days=7)

        # Métriques récentes
        recent_posts = [
            p for p in self.published_posts
            if p.published_at and p.published_at >= last_7_days
        ]

        # Calculs des métriques
        total_reach = sum(
            p.analytics.get("metrics", {}).get("reach", 0)
            for p in recent_posts
        )

        total_engagement = sum(
            p.analytics.get("metrics", {}).get("likes", 0) +
            p.analytics.get("metrics", {}).get("comments", 0) +
            p.analytics.get("metrics", {}).get("shares", 0)
            for p in recent_posts
        )

        avg_engagement_rate = (
            sum(p.analytics.get("metrics", {}).get("engagement_rate", 0) for p in recent_posts) /
            len(recent_posts) if recent_posts else 0
        )

        # Répartition par plateforme
        platform_breakdown = {}
        for platform in Platform:
            platform_posts = [p for p in recent_posts if p.platform == platform]
            platform_breakdown[platform.value] = {
                "posts": len(platform_posts),
                "reach": sum(p.analytics.get("metrics", {}).get("reach", 0) for p in platform_posts),
                "engagement": sum(
                    p.analytics.get("metrics", {}).get("likes", 0) +
                    p.analytics.get("metrics", {}).get("comments", 0) +
                    p.analytics.get("metrics", {}).get("shares", 0)
                    for p in platform_posts
                )
            }

        # Posts en attente
        pending_posts = len([p for p in self.scheduled_posts if p.status == PostStatus.SCHEDULED])

        # Engagement à traiter
        pending_engagements = len([e for e in self.engagement_queue if not e.handled])

        # Alertes actives
        active_alerts = len([a for a in self.crisis_alerts if not a.action_taken])

        return {
            "period": "Last 7 days",
            "summary": {
                "total_posts": len(recent_posts),
                "total_reach": total_reach,
                "total_engagement": total_engagement,
                "avg_engagement_rate": round(avg_engagement_rate, 4),
                "pending_posts": pending_posts,
                "pending_engagements": pending_engagements,
                "active_alerts": active_alerts
            },
            "platform_breakdown": platform_breakdown,
            "top_performing_posts": [
                {
                    "id": p.id,
                    "platform": p.platform.value,
                    "content_preview": p.content[:100] + "...",
                    "engagement_rate": p.analytics.get("metrics", {}).get("engagement_rate", 0),
                    "reach": p.analytics.get("metrics", {}).get("reach", 0)
                }
                for p in sorted(
                    recent_posts,
                    key=lambda x: x.analytics.get("metrics", {}).get("engagement_rate", 0),
                    reverse=True
                )[:5]
            ],
            "recommendations": [
                "Maintenir la fréquence de publication actuelle",
                "Développer plus de contenu interactif",
                "Optimiser les horaires de publication",
                "Augmenter la présence sur Instagram"
            ]
        }

# Fonctions utilitaires pour l'agent

async def create_ifiveme_social_media_agent(use_mock_apis: bool = True) -> SocialMediaAgent:
    """Factory function pour créer l'agent social media iFiveMe"""
    agent = SocialMediaAgent(use_mock_apis=use_mock_apis)

    # Health check initial
    if await agent.health_check():
        logging.info("Agent Social Media iFiveMe initialisé avec succès")
    else:
        logging.error("Problème lors de l'initialisation de l'agent")

    return agent

# Example d'utilisation
if __name__ == "__main__":
    async def main():
        # Créer l'agent
        agent = await create_ifiveme_social_media_agent(use_mock_apis=True)

        # Test de publication
        publish_task = agent.create_task(
            task_type="publish_post",
            priority=5,
            data={
                "platform": "linkedin",
                "content": "iFiveMe révolutionne le networking avec nos cartes d'affaires virtuelles! 🚀 Découvrez comment simplifier vos échanges professionnels.",
                "category": "innovation_produit"
            }
        )

        await agent.add_task(publish_task)
        await agent.execute_tasks()

        # Afficher le dashboard
        dashboard = await agent.get_social_media_dashboard()
        print(json.dumps(dashboard, indent=2, default=str))

    # Exécuter l'exemple
    asyncio.run(main())