"""
iFiveMe Marketing MVP - Orchestrator Agent
Agent principal qui coordonne toutes les activités marketing
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import sys
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.base_agent import BaseAgent, AgentTask, AgentMetrics
from config.settings import COMPANY_INFO, API_KEYS

# Import des agents spécialisés
try:
    from agents.content_creator_agent import ContentCreatorAgent
    from agents.social_media_agent import SocialMediaAgent
    from agents.email_marketing_agent import EmailMarketingAgent
    from agents.analytics_agent import AnalyticsAgent
except ImportError:
    # Mode dégradé si les agents ne sont pas disponibles
    ContentCreatorAgent = None
    SocialMediaAgent = None
    EmailMarketingAgent = None
    AnalyticsAgent = None

class CampaignType(Enum):
    """Types de campagnes marketing"""
    PRODUCT_LAUNCH = "product_launch"
    BRAND_AWARENESS = "brand_awareness"
    LEAD_GENERATION = "lead_generation"
    CUSTOMER_RETENTION = "customer_retention"
    SEASONAL_PROMO = "seasonal_promo"
    CRISIS_MANAGEMENT = "crisis_management"
    COMPETITIVE_RESPONSE = "competitive_response"
    CONTENT_SERIES = "content_series"

class CampaignStatus(Enum):
    """Statuts des campagnes"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

@dataclass
class MarketingCampaign:
    """Structure d'une campagne marketing complète"""
    id: str
    name: str
    type: CampaignType
    status: CampaignStatus
    description: str
    target_audience: Dict[str, Any]
    channels: List[str]
    budget: float
    allocated_budget: Dict[str, float]
    start_date: datetime
    end_date: datetime
    objectives: List[str]
    kpis: Dict[str, float]
    content_plan: Dict[str, Any]
    automation_rules: List[Dict[str, Any]]
    created_at: datetime
    created_by: str
    priority: int = 5
    tags: List[str] = None
    ab_tests: List[Dict[str, Any]] = None
    performance_data: Dict[str, Any] = None
    notes: str = ""

@dataclass
class OrchestratorMetrics:
    """Métriques spécifiques à l'orchestrateur"""
    campaigns_managed: int = 0
    active_campaigns: int = 0
    successful_campaigns: int = 0
    failed_campaigns: int = 0
    total_budget_managed: float = 0.0
    roi_average: float = 0.0
    agent_coordination_success_rate: float = 0.0
    crisis_responses: int = 0

class MarketingOrchestrator(BaseAgent):
    """Agent Orchestrateur Principal pour le Marketing iFiveMe

    Coordonne tous les agents marketing et gère les campagnes multi-canaux
    """

    def __init__(self):
        super().__init__(
            agent_id="marketing_orchestrator",
            name="Orchestrateur Marketing iFiveMe",
            config={
                "max_concurrent_campaigns": 10,
                "budget_threshold_alert": 0.8,
                "performance_check_interval": 300,  # 5 minutes
                "crisis_detection_threshold": 0.2,
                "auto_optimization": True,
                "real_time_monitoring": True
            }
        )

        # Métriques spécialisées
        self.orchestrator_metrics = OrchestratorMetrics()

        # Storage des campagnes et agents
        self.campaigns: Dict[str, MarketingCampaign] = {}
        self.active_campaigns: Dict[str, MarketingCampaign] = {}
        self.marketing_agents: Dict[str, BaseAgent] = {}

        # Dashboard et monitoring
        self.dashboard_data: Dict[str, Any] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.performance_history: List[Dict[str, Any]] = []

        # Configuration des règles d'automatisation
        self.automation_rules = self._initialize_automation_rules()

        # Templates de campagnes iFiveMe
        self.campaign_templates = self._initialize_campaign_templates()

        # Initialiser les agents
        asyncio.create_task(self._initialize_agents())

    async def _initialize_agents(self):
        """Initialise et configure tous les agents marketing"""
        try:
            # Content Creator Agent
            if ContentCreatorAgent:
                self.marketing_agents["content_creator"] = ContentCreatorAgent()
                self.logger.info("Content Creator Agent initialisé")

            # Social Media Agent
            if SocialMediaAgent:
                self.marketing_agents["social_media"] = SocialMediaAgent()
                self.logger.info("Social Media Agent initialisé")

            # Email Marketing Agent
            if EmailMarketingAgent:
                self.marketing_agents["email_marketing"] = EmailMarketingAgent()
                self.logger.info("Email Marketing Agent initialisé")

            # Analytics Agent
            if AnalyticsAgent:
                self.marketing_agents["analytics"] = AnalyticsAgent()
                self.logger.info("Analytics Agent initialisé")

            # Vérification de santé des agents
            await self._health_check_all_agents()

            self.logger.info(f"Orchestrateur initialisé avec {len(self.marketing_agents)} agents")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation des agents: {str(e)}")

    def _initialize_automation_rules(self) -> List[Dict[str, Any]]:
        """Initialise les règles d'automatisation"""
        return [
            {
                "name": "budget_alert",
                "condition": "budget_spent > budget_threshold",
                "action": "send_alert_and_pause_campaign",
                "parameters": {"threshold": 0.8}
            },
            {
                "name": "poor_performance_optimization",
                "condition": "conversion_rate < minimum_threshold",
                "action": "optimize_campaign_automatically",
                "parameters": {"min_conversion_rate": 0.02}
            },
            {
                "name": "crisis_detection",
                "condition": "negative_sentiment > crisis_threshold",
                "action": "activate_crisis_response",
                "parameters": {"crisis_threshold": 0.3}
            },
            {
                "name": "high_performance_scaling",
                "condition": "roi > scaling_threshold",
                "action": "increase_budget_allocation",
                "parameters": {"scaling_threshold": 3.0, "increase_factor": 1.5}
            }
        ]

    def _initialize_campaign_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialise les templates de campagnes iFiveMe"""
        return {
            "product_launch": {
                "name": "Lancement Produit iFiveMe",
                "description": "Campagne de lancement pour nouvelles fonctionnalités",
                "duration_days": 30,
                "channels": ["social_media", "email", "content_marketing"],
                "budget_allocation": {
                    "social_media": 0.4,
                    "email": 0.3,
                    "content_marketing": 0.3
                },
                "objectives": [
                    "Générer awareness pour la nouvelle fonctionnalité",
                    "Acquérir 500 nouveaux utilisateurs",
                    "Obtenir 50 témoignages clients"
                ]
            },
            "brand_awareness": {
                "name": "Sensibilisation Marque iFiveMe",
                "description": "Campagne de notoriété de marque",
                "duration_days": 60,
                "channels": ["social_media", "content_marketing", "influencer"],
                "budget_allocation": {
                    "social_media": 0.5,
                    "content_marketing": 0.3,
                    "influencer": 0.2
                },
                "objectives": [
                    "Augmenter la reconnaissance de marque de 25%",
                    "Générer 10,000 impressions qualifiées",
                    "Établir iFiveMe comme leader du networking digital"
                ]
            },
            "lead_generation": {
                "name": "Génération de Leads iFiveMe",
                "description": "Campagne d'acquisition de prospects qualifiés",
                "duration_days": 45,
                "channels": ["social_media", "email", "content_marketing"],
                "budget_allocation": {
                    "social_media": 0.4,
                    "email": 0.35,
                    "content_marketing": 0.25
                },
                "objectives": [
                    "Générer 1000 leads qualifiés",
                    "Atteindre un coût par lead de 15$",
                    "Convertir 20% des leads en utilisateurs actifs"
                ]
            }
        }

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite une tâche d'orchestration"""
        task_type = task.type
        task_data = task.data

        try:
            if task_type == "create_campaign":
                return await self._create_campaign(task_data)
            elif task_type == "launch_campaign":
                return await self._launch_campaign(task_data)
            elif task_type == "optimize_campaign":
                return await self._optimize_campaign(task_data)
            elif task_type == "generate_report":
                return await self._generate_comprehensive_report(task_data)
            elif task_type == "crisis_management":
                return await self._handle_crisis(task_data)
            elif task_type == "ab_test_setup":
                return await self._setup_ab_test(task_data)
            elif task_type == "budget_reallocation":
                return await self._reallocate_budget(task_data)
            elif task_type == "performance_monitoring":
                return await self._monitor_performance()
            else:
                raise ValueError(f"Type de tâche non supporté: {task_type}")

        except Exception as e:
            self.logger.error(f"Erreur lors du traitement de la tâche {task.id}: {str(e)}")
            raise

    async def _create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une nouvelle campagne marketing coordonnée"""
        try:
            # Générer ID unique pour la campagne
            campaign_id = f"campaign_{uuid.uuid4().hex[:8]}"

            # Extraire les paramètres de base
            campaign_type = CampaignType(campaign_data.get("type", "brand_awareness"))
            template = self.campaign_templates.get(campaign_type.value, {})

            # Créer l'objet campagne
            campaign = MarketingCampaign(
                id=campaign_id,
                name=campaign_data.get("name", template.get("name", f"Campagne iFiveMe {campaign_id}")),
                type=campaign_type,
                status=CampaignStatus.DRAFT,
                description=campaign_data.get("description", template.get("description", "")),
                target_audience=campaign_data.get("target_audience", self._get_default_audience()),
                channels=campaign_data.get("channels", template.get("channels", ["social_media"])),
                budget=campaign_data.get("budget", 1000.0),
                allocated_budget=self._calculate_budget_allocation(
                    campaign_data.get("budget", 1000.0),
                    campaign_data.get("channels", template.get("channels", ["social_media"])),
                    template.get("budget_allocation", {})
                ),
                start_date=datetime.fromisoformat(campaign_data.get("start_date", datetime.now().isoformat())),
                end_date=datetime.fromisoformat(campaign_data.get(
                    "end_date",
                    (datetime.now() + timedelta(days=template.get("duration_days", 30))).isoformat()
                )),
                objectives=campaign_data.get("objectives", template.get("objectives", [])),
                kpis=campaign_data.get("kpis", self._get_default_kpis()),
                content_plan=await self._create_content_plan(campaign_data, template),
                automation_rules=campaign_data.get("automation_rules", []),
                created_at=datetime.now(),
                created_by="orchestrator",
                priority=campaign_data.get("priority", 5),
                tags=campaign_data.get("tags", []),
                ab_tests=[],
                performance_data={}
            )

            # Stocker la campagne
            self.campaigns[campaign_id] = campaign
            self.orchestrator_metrics.campaigns_managed += 1

            # Créer les tâches pour chaque canal
            channel_tasks = await self._create_channel_tasks(campaign)

            self.logger.info(f"Campagne {campaign_id} créée avec succès")

            return {
                "success": True,
                "campaign_id": campaign_id,
                "campaign": asdict(campaign),
                "channel_tasks": channel_tasks,
                "message": f"Campagne '{campaign.name}' créée avec succès"
            }

        except Exception as e:
            self.logger.error(f"Erreur lors de la création de campagne: {str(e)}")
            raise

    async def _create_content_plan(self, campaign_data: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un plan de contenu coordonné avec l'agent créateur"""
        content_plan = {
            "themes": campaign_data.get("content_themes", [
                "Innovation iFiveMe",
                "Networking Digital",
                "Témoignages Clients",
                "Conseils Business"
            ]),
            "content_calendar": {},
            "asset_requirements": {},
            "approval_workflow": ["content_creator", "orchestrator", "final_approval"]
        }

        # Si l'agent créateur de contenu est disponible, lui demander un plan détaillé
        if "content_creator" in self.marketing_agents:
            try:
                content_task = self.marketing_agents["content_creator"].create_task(
                    task_type="create_content_plan",
                    priority=8,
                    data={
                        "campaign_id": campaign_data.get("campaign_id"),
                        "campaign_type": campaign_data.get("type"),
                        "duration_days": (
                            datetime.fromisoformat(campaign_data.get("end_date", datetime.now().isoformat())) -
                            datetime.fromisoformat(campaign_data.get("start_date", datetime.now().isoformat()))
                        ).days,
                        "channels": campaign_data.get("channels", []),
                        "themes": content_plan["themes"]
                    }
                )

                await self.marketing_agents["content_creator"].add_task(content_task)
                # Note: Dans un vrai système, on attendrait la réponse

            except Exception as e:
                self.logger.warning(f"Impossible de créer le plan de contenu avec l'agent: {str(e)}")

        return content_plan

    async def _create_channel_tasks(self, campaign: MarketingCampaign) -> Dict[str, List[str]]:
        """Crée les tâches spécifiques pour chaque canal de la campagne"""
        channel_tasks = {}

        for channel in campaign.channels:
            tasks = []

            if channel == "social_media" and "social_media" in self.marketing_agents:
                # Tâches réseaux sociaux
                social_task = self.marketing_agents["social_media"].create_task(
                    task_type="campaign_execution",
                    priority=campaign.priority,
                    data={
                        "campaign_id": campaign.id,
                        "campaign_type": campaign.type.value,
                        "budget": campaign.allocated_budget.get("social_media", 0),
                        "target_audience": campaign.target_audience,
                        "content_themes": campaign.content_plan.get("themes", []),
                        "duration": (campaign.end_date - campaign.start_date).days
                    }
                )
                await self.marketing_agents["social_media"].add_task(social_task)
                tasks.append(social_task.id)

            if channel == "email" and "email_marketing" in self.marketing_agents:
                # Tâches email marketing
                email_task = self.marketing_agents["email_marketing"].create_task(
                    task_type="campaign_setup",
                    priority=campaign.priority,
                    data={
                        "campaign_id": campaign.id,
                        "campaign_name": campaign.name,
                        "target_audience": campaign.target_audience,
                        "budget": campaign.allocated_budget.get("email", 0),
                        "objectives": campaign.objectives
                    }
                )
                await self.marketing_agents["email_marketing"].add_task(email_task)
                tasks.append(email_task.id)

            channel_tasks[channel] = tasks

        return channel_tasks

    async def _launch_campaign(self, launch_data: Dict[str, Any]) -> Dict[str, Any]:
        """Lance une campagne et coordonne tous les agents"""
        campaign_id = launch_data.get("campaign_id")

        if campaign_id not in self.campaigns:
            raise ValueError(f"Campagne {campaign_id} introuvable")

        campaign = self.campaigns[campaign_id]

        try:
            # Vérifications pré-lancement
            launch_checks = await self._pre_launch_checks(campaign)

            if not launch_checks["ready"]:
                return {
                    "success": False,
                    "message": "Campagne non prête pour le lancement",
                    "issues": launch_checks["issues"]
                }

            # Changer le statut
            campaign.status = CampaignStatus.RUNNING
            self.active_campaigns[campaign_id] = campaign
            self.orchestrator_metrics.active_campaigns += 1

            # Lancer tous les agents concernés
            launch_results = {}
            for channel in campaign.channels:
                if channel == "social_media" and "social_media" in self.marketing_agents:
                    # Démarrer la campagne social media
                    social_launch_task = self.marketing_agents["social_media"].create_task(
                        task_type="launch_campaign",
                        priority=10,  # Priorité maximale pour le lancement
                        data={"campaign_id": campaign_id}
                    )
                    await self.marketing_agents["social_media"].add_task(social_launch_task)
                    launch_results["social_media"] = "launched"

                if channel == "email" and "email_marketing" in self.marketing_agents:
                    # Démarrer la campagne email
                    email_launch_task = self.marketing_agents["email_marketing"].create_task(
                        task_type="start_campaign",
                        priority=10,
                        data={"campaign_id": campaign_id}
                    )
                    await self.marketing_agents["email_marketing"].add_task(email_launch_task)
                    launch_results["email"] = "launched"

            # Démarrer le monitoring
            await self._start_campaign_monitoring(campaign_id)

            self.logger.info(f"Campagne {campaign_id} lancée avec succès")

            return {
                "success": True,
                "campaign_id": campaign_id,
                "launch_results": launch_results,
                "message": f"Campagne '{campaign.name}' lancée avec succès",
                "monitoring": "enabled"
            }

        except Exception as e:
            campaign.status = CampaignStatus.FAILED
            self.logger.error(f"Erreur lors du lancement de la campagne {campaign_id}: {str(e)}")
            raise

    async def _pre_launch_checks(self, campaign: MarketingCampaign) -> Dict[str, Any]:
        """Effectue des vérifications avant le lancement d'une campagne"""
        issues = []

        # Vérifier le budget
        if campaign.budget <= 0:
            issues.append("Budget invalide ou insuffisant")

        # Vérifier les dates
        if campaign.start_date >= campaign.end_date:
            issues.append("Dates de campagne invalides")

        if campaign.start_date < datetime.now():
            issues.append("Date de début dans le passé")

        # Vérifier les agents nécessaires
        for channel in campaign.channels:
            agent_key = channel.replace("_marketing", "").replace("_media", "_media")
            if agent_key not in self.marketing_agents:
                issues.append(f"Agent pour le canal {channel} non disponible")

        # Vérifier le contenu
        if not campaign.content_plan.get("themes"):
            issues.append("Plan de contenu incomplet")

        # Vérifier l'audience cible
        if not campaign.target_audience:
            issues.append("Audience cible non définie")

        return {
            "ready": len(issues) == 0,
            "issues": issues
        }

    async def _start_campaign_monitoring(self, campaign_id: str):
        """Démarre le monitoring temps réel d'une campagne"""
        if not self.config.get("real_time_monitoring", True):
            return

        # Créer une tâche de monitoring récurrente
        monitoring_task = self.create_task(
            task_type="performance_monitoring",
            priority=3,
            data={
                "campaign_id": campaign_id,
                "interval": self.config.get("performance_check_interval", 300)
            }
        )

        await self.add_task(monitoring_task)

        self.logger.info(f"Monitoring démarré pour la campagne {campaign_id}")

    async def _optimize_campaign(self, optimization_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimise automatiquement une campagne basée sur les performances"""
        campaign_id = optimization_data.get("campaign_id")

        if campaign_id not in self.active_campaigns:
            raise ValueError(f"Campagne active {campaign_id} introuvable")

        campaign = self.active_campaigns[campaign_id]

        try:
            # Collecter les données de performance
            performance_data = await self._collect_performance_data(campaign_id)

            # Analyser les performances
            analysis = await self._analyze_campaign_performance(campaign, performance_data)

            # Générer des recommandations d'optimisation
            optimizations = await self._generate_optimization_recommendations(campaign, analysis)

            # Appliquer les optimisations automatiques si configuré
            applied_optimizations = []
            if self.config.get("auto_optimization", True):
                applied_optimizations = await self._apply_automatic_optimizations(campaign, optimizations)

            # Mettre à jour les données de performance
            campaign.performance_data.update({
                "last_optimization": datetime.now().isoformat(),
                "optimization_analysis": analysis,
                "applied_optimizations": applied_optimizations
            })

            self.logger.info(f"Campagne {campaign_id} optimisée avec {len(applied_optimizations)} modifications")

            return {
                "success": True,
                "campaign_id": campaign_id,
                "performance_analysis": analysis,
                "recommendations": optimizations,
                "applied_optimizations": applied_optimizations,
                "message": f"Campagne optimisée avec {len(applied_optimizations)} améliorations"
            }

        except Exception as e:
            self.logger.error(f"Erreur lors de l'optimisation de la campagne {campaign_id}: {str(e)}")
            raise

    async def _collect_performance_data(self, campaign_id: str) -> Dict[str, Any]:
        """Collecte les données de performance de tous les canaux"""
        performance_data = {
            "campaign_id": campaign_id,
            "timestamp": datetime.now().isoformat(),
            "channels": {}
        }

        # Collecter les données de l'agent analytics si disponible
        if "analytics" in self.marketing_agents:
            analytics_task = self.marketing_agents["analytics"].create_task(
                task_type="collect_campaign_data",
                priority=7,
                data={"campaign_id": campaign_id}
            )
            await self.marketing_agents["analytics"].add_task(analytics_task)
            # Note: Dans un vrai système, on attendrait la réponse

            # Données simulées pour la démonstration
            performance_data["channels"] = {
                "social_media": {
                    "impressions": 15000,
                    "clicks": 750,
                    "conversions": 45,
                    "cost": 300.0,
                    "ctr": 0.05,
                    "conversion_rate": 0.06,
                    "cpc": 0.4,
                    "cpa": 6.67
                },
                "email": {
                    "sent": 2000,
                    "opened": 600,
                    "clicked": 120,
                    "conversions": 24,
                    "cost": 150.0,
                    "open_rate": 0.3,
                    "click_rate": 0.06,
                    "conversion_rate": 0.2
                }
            }

        return performance_data

    async def _analyze_campaign_performance(self, campaign: MarketingCampaign, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse les performances de campagne"""
        analysis = {
            "overall_performance": "satisfactory",
            "roi": 0.0,
            "total_conversions": 0,
            "total_cost": 0.0,
            "channel_performance": {},
            "issues": [],
            "strengths": []
        }

        total_conversions = 0
        total_cost = 0.0
        total_revenue = 0.0

        # Analyser chaque canal
        for channel, data in performance_data.get("channels", {}).items():
            conversions = data.get("conversions", 0)
            cost = data.get("cost", 0)

            total_conversions += conversions
            total_cost += cost
            total_revenue += conversions * 25  # Valeur moyenne par conversion iFiveMe

            # Analyser les performances du canal
            channel_analysis = {
                "performance": "good",
                "efficiency": "normal",
                "recommendations": []
            }

            if channel == "social_media":
                ctr = data.get("ctr", 0)
                if ctr < 0.02:
                    channel_analysis["performance"] = "poor"
                    channel_analysis["recommendations"].append("Améliorer le ciblage et les créatifs")
                elif ctr > 0.08:
                    channel_analysis["performance"] = "excellent"
                    channel_analysis["recommendations"].append("Augmenter le budget pour ce canal")

            elif channel == "email":
                open_rate = data.get("open_rate", 0)
                if open_rate < 0.2:
                    channel_analysis["performance"] = "poor"
                    channel_analysis["recommendations"].append("Optimiser les lignes d'objet")
                elif open_rate > 0.35:
                    channel_analysis["performance"] = "excellent"
                    channel_analysis["recommendations"].append("Maintenir la stratégie actuelle")

            analysis["channel_performance"][channel] = channel_analysis

        # Calculer le ROI global
        if total_cost > 0:
            analysis["roi"] = (total_revenue - total_cost) / total_cost

        analysis["total_conversions"] = total_conversions
        analysis["total_cost"] = total_cost

        # Déterminer la performance globale
        if analysis["roi"] < 1.0:
            analysis["overall_performance"] = "poor"
            analysis["issues"].append("ROI insuffisant")
        elif analysis["roi"] > 3.0:
            analysis["overall_performance"] = "excellent"
            analysis["strengths"].append("Excellent ROI")

        return analysis

    async def _generate_optimization_recommendations(self, campaign: MarketingCampaign, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Génère des recommandations d'optimisation basées sur l'analyse"""
        recommendations = []

        # Recommandations basées sur le ROI global
        if analysis["roi"] < 1.0:
            recommendations.append({
                "type": "budget_reallocation",
                "priority": "high",
                "description": "Réallouer le budget vers les canaux les plus performants",
                "action": "reallocate_budget",
                "parameters": {"threshold": 0.5}
            })

        # Recommandations par canal
        for channel, channel_analysis in analysis["channel_performance"].items():
            if channel_analysis["performance"] == "poor":
                recommendations.append({
                    "type": "channel_optimization",
                    "priority": "high",
                    "description": f"Optimiser les performances du canal {channel}",
                    "action": "optimize_channel",
                    "channel": channel,
                    "parameters": channel_analysis["recommendations"]
                })
            elif channel_analysis["performance"] == "excellent":
                recommendations.append({
                    "type": "budget_increase",
                    "priority": "medium",
                    "description": f"Augmenter le budget pour le canal {channel}",
                    "action": "increase_budget",
                    "channel": channel,
                    "parameters": {"increase_factor": 1.3}
                })

        # Recommandations d'automatisation
        if len(analysis["issues"]) > 2:
            recommendations.append({
                "type": "automation_rule",
                "priority": "medium",
                "description": "Ajouter des règles d'automatisation pour prévenir les problèmes",
                "action": "add_automation_rule",
                "parameters": {"rule_type": "performance_threshold"}
            })

        return recommendations

    async def _apply_automatic_optimizations(self, campaign: MarketingCampaign, optimizations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Applique automatiquement les optimisations approuvées"""
        applied = []

        for optimization in optimizations:
            try:
                if optimization["priority"] == "high" and optimization["type"] == "budget_reallocation":
                    # Réallocation budgétaire automatique
                    result = await self._reallocate_budget({
                        "campaign_id": campaign.id,
                        "optimization_data": optimization
                    })

                    if result["success"]:
                        applied.append({
                            "optimization": optimization,
                            "result": "applied",
                            "timestamp": datetime.now().isoformat()
                        })

                elif optimization["type"] == "channel_optimization":
                    # Optimisation de canal
                    channel = optimization["channel"]
                    if channel in self.marketing_agents:
                        opt_task = self.marketing_agents[channel].create_task(
                            task_type="optimize_performance",
                            priority=9,
                            data={
                                "campaign_id": campaign.id,
                                "recommendations": optimization["parameters"]
                            }
                        )
                        await self.marketing_agents[channel].add_task(opt_task)

                        applied.append({
                            "optimization": optimization,
                            "result": "task_created",
                            "timestamp": datetime.now().isoformat()
                        })

            except Exception as e:
                self.logger.error(f"Erreur lors de l'application de l'optimisation: {str(e)}")
                applied.append({
                    "optimization": optimization,
                    "result": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })

        return applied

    async def _reallocate_budget(self, reallocation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Réalloue le budget entre les canaux d'une campagne"""
        campaign_id = reallocation_data.get("campaign_id")

        if campaign_id not in self.active_campaigns:
            raise ValueError(f"Campagne active {campaign_id} introuvable")

        campaign = self.active_campaigns[campaign_id]

        try:
            # Analyser les performances actuelles pour déterminer la réallocation
            performance_data = await self._collect_performance_data(campaign_id)

            # Calculer les nouveaux allocations basées sur les performances
            new_allocation = {}
            total_budget = campaign.budget

            # Identifier le canal le plus performant (ROI le plus élevé)
            best_channel = None
            best_roi = 0

            for channel, data in performance_data.get("channels", {}).items():
                conversions = data.get("conversions", 0)
                cost = data.get("cost", 1)  # Éviter division par zéro
                roi = (conversions * 25 - cost) / cost if cost > 0 else 0

                if roi > best_roi:
                    best_roi = roi
                    best_channel = channel

            # Réallouer 20% du budget vers le meilleur canal
            if best_channel:
                reallocation_amount = total_budget * 0.2

                for channel in campaign.channels:
                    current_allocation = campaign.allocated_budget.get(channel, 0)

                    if channel == best_channel:
                        new_allocation[channel] = current_allocation + reallocation_amount
                    else:
                        # Réduire proportionnellement les autres canaux
                        reduction = reallocation_amount / (len(campaign.channels) - 1)
                        new_allocation[channel] = max(0, current_allocation - reduction)

                # Mettre à jour la campagne
                campaign.allocated_budget = new_allocation

                self.logger.info(f"Budget réalloué pour la campagne {campaign_id}")

                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "previous_allocation": campaign.allocated_budget,
                    "new_allocation": new_allocation,
                    "best_performing_channel": best_channel,
                    "message": "Budget réalloué avec succès"
                }
            else:
                return {
                    "success": False,
                    "message": "Impossible de déterminer le meilleur canal pour la réallocation"
                }

        except Exception as e:
            self.logger.error(f"Erreur lors de la réallocation budgétaire: {str(e)}")
            raise

    async def _monitor_performance(self) -> Dict[str, Any]:
        """Surveille les performances de toutes les campagnes actives"""
        monitoring_results = {
            "timestamp": datetime.now().isoformat(),
            "campaigns_monitored": 0,
            "alerts_generated": 0,
            "optimizations_triggered": 0,
            "campaign_status": {}
        }

        try:
            for campaign_id, campaign in self.active_campaigns.items():
                # Collecter les données de performance
                performance_data = await self._collect_performance_data(campaign_id)

                # Vérifier les règles d'alerte
                alerts = await self._check_alert_rules(campaign, performance_data)

                # Vérifier les règles d'optimisation automatique
                if self.config.get("auto_optimization", True):
                    optimizations = await self._check_optimization_triggers(campaign, performance_data)

                    if optimizations:
                        await self._optimize_campaign({"campaign_id": campaign_id})
                        monitoring_results["optimizations_triggered"] += 1

                # Stocker les résultats
                monitoring_results["campaign_status"][campaign_id] = {
                    "status": campaign.status.value,
                    "performance": performance_data,
                    "alerts": alerts,
                    "last_monitored": datetime.now().isoformat()
                }

                monitoring_results["campaigns_monitored"] += 1
                monitoring_results["alerts_generated"] += len(alerts)

                # Ajouter aux alertes globales
                self.alerts.extend(alerts)

            # Mettre à jour les données du dashboard
            await self._update_dashboard_data(monitoring_results)

            self.logger.info(f"Monitoring effectué pour {monitoring_results['campaigns_monitored']} campagnes")

            return monitoring_results

        except Exception as e:
            self.logger.error(f"Erreur lors du monitoring des performances: {str(e)}")
            raise

    async def _check_alert_rules(self, campaign: MarketingCampaign, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Vérifie les règles d'alerte pour une campagne"""
        alerts = []

        # Calculer le budget dépensé
        total_cost = sum(
            channel_data.get("cost", 0)
            for channel_data in performance_data.get("channels", {}).values()
        )

        budget_spent_ratio = total_cost / campaign.budget if campaign.budget > 0 else 0

        # Alerte budget
        if budget_spent_ratio > self.config.get("budget_threshold_alert", 0.8):
            alerts.append({
                "type": "budget_alert",
                "severity": "high",
                "message": f"Budget {budget_spent_ratio:.1%} dépensé pour la campagne {campaign.name}",
                "campaign_id": campaign.id,
                "timestamp": datetime.now().isoformat(),
                "data": {"budget_spent": total_cost, "budget_total": campaign.budget}
            })

        # Alerte performance faible
        total_conversions = sum(
            channel_data.get("conversions", 0)
            for channel_data in performance_data.get("channels", {}).values()
        )

        conversion_rate = total_conversions / max(1, sum(
            channel_data.get("clicks", 0)
            for channel_data in performance_data.get("channels", {}).values()
        ))

        if conversion_rate < 0.02:  # Moins de 2% de conversion
            alerts.append({
                "type": "performance_alert",
                "severity": "medium",
                "message": f"Taux de conversion faible ({conversion_rate:.2%}) pour la campagne {campaign.name}",
                "campaign_id": campaign.id,
                "timestamp": datetime.now().isoformat(),
                "data": {"conversion_rate": conversion_rate}
            })

        return alerts

    async def _check_optimization_triggers(self, campaign: MarketingCampaign, performance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Vérifie si des optimisations automatiques doivent être déclenchées"""
        optimizations = []

        # Analyser les performances
        analysis = await self._analyze_campaign_performance(campaign, performance_data)

        # Déclencheur ROI faible
        if analysis["roi"] < 1.0:
            optimizations.append({
                "trigger": "low_roi",
                "action": "budget_reallocation",
                "priority": "high"
            })

        # Déclencheur performance canal
        for channel, channel_analysis in analysis["channel_performance"].items():
            if channel_analysis["performance"] == "poor":
                optimizations.append({
                    "trigger": "poor_channel_performance",
                    "action": "optimize_channel",
                    "channel": channel,
                    "priority": "medium"
                })

        return optimizations

    async def _update_dashboard_data(self, monitoring_data: Dict[str, Any]):
        """Met à jour les données du dashboard temps réel"""
        self.dashboard_data = {
            "last_update": datetime.now().isoformat(),
            "active_campaigns": len(self.active_campaigns),
            "total_campaigns": len(self.campaigns),
            "alerts_count": len(self.alerts),
            "performance_summary": monitoring_data.get("campaign_status", {}),
            "orchestrator_metrics": asdict(self.orchestrator_metrics),
            "agent_status": {
                agent_id: await agent.health_check()
                for agent_id, agent in self.marketing_agents.items()
            }
        }

        # Sauvegarder les données du dashboard
        dashboard_file = self.data_dir / "dashboard_data.json"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            json.dump(self.dashboard_data, f, indent=2, default=str, ensure_ascii=False)

    async def _generate_comprehensive_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un rapport complet sur les campagnes et performances"""
        report_type = report_data.get("type", "campaign_summary")
        period = report_data.get("period", "last_30_days")

        try:
            report = {
                "report_id": f"report_{uuid.uuid4().hex[:8]}",
                "type": report_type,
                "period": period,
                "generated_at": datetime.now().isoformat(),
                "summary": {},
                "campaigns": {},
                "recommendations": [],
                "appendices": {}
            }

            # Résumé exécutif
            report["summary"] = {
                "total_campaigns": len(self.campaigns),
                "active_campaigns": len(self.active_campaigns),
                "completed_campaigns": len([c for c in self.campaigns.values() if c.status == CampaignStatus.COMPLETED]),
                "total_budget_managed": sum(c.budget for c in self.campaigns.values()),
                "average_roi": self.orchestrator_metrics.roi_average,
                "key_achievements": [
                    "Coordination réussie de campagnes multi-canaux",
                    "Optimisation automatique des performances",
                    "Monitoring temps réel des KPIs"
                ]
            }

            # Détails par campagne
            for campaign_id, campaign in self.campaigns.items():
                performance_data = await self._collect_performance_data(campaign_id) if campaign_id in self.active_campaigns else {}

                report["campaigns"][campaign_id] = {
                    "name": campaign.name,
                    "type": campaign.type.value,
                    "status": campaign.status.value,
                    "budget": campaign.budget,
                    "duration": (campaign.end_date - campaign.start_date).days,
                    "channels": campaign.channels,
                    "objectives": campaign.objectives,
                    "performance": performance_data,
                    "roi": performance_data.get("roi", "N/A")
                }

            # Recommandations stratégiques
            report["recommendations"] = await self._generate_strategic_recommendations()

            # Appendices avec données techniques
            report["appendices"] = {
                "agent_performance": {
                    agent_id: asdict(agent.metrics)
                    for agent_id, agent in self.marketing_agents.items()
                },
                "automation_rules": self.automation_rules,
                "alerts_history": self.alerts[-50:]  # 50 dernières alertes
            }

            # Sauvegarder le rapport
            report_file = self.data_dir / f"report_{report['report_id']}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str, ensure_ascii=False)

            self.logger.info(f"Rapport {report['report_id']} généré avec succès")

            return {
                "success": True,
                "report_id": report["report_id"],
                "report": report,
                "file_path": str(report_file),
                "message": "Rapport complet généré avec succès"
            }

        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du rapport: {str(e)}")
            raise

    async def _generate_strategic_recommendations(self) -> List[Dict[str, Any]]:
        """Génère des recommandations stratégiques basées sur l'ensemble des données"""
        recommendations = []

        # Analyse des tendances de performance
        if self.orchestrator_metrics.roi_average < 2.0:
            recommendations.append({
                "category": "performance_optimization",
                "priority": "high",
                "title": "Améliorer le ROI global",
                "description": "Le ROI moyen est en dessous des objectifs. Optimiser le ciblage et les créatifs.",
                "actions": [
                    "Réviser les audiences cibles",
                    "Tester de nouveaux formats créatifs",
                    "Réallouer le budget vers les canaux les plus performants"
                ]
            })

        # Analyse des canaux
        channel_usage = {}
        for campaign in self.campaigns.values():
            for channel in campaign.channels:
                channel_usage[channel] = channel_usage.get(channel, 0) + 1

        if len(channel_usage) < 3:
            recommendations.append({
                "category": "channel_diversification",
                "priority": "medium",
                "title": "Diversifier les canaux marketing",
                "description": "Élargir la présence sur d'autres canaux pour réduire les risques.",
                "actions": [
                    "Explorer le marketing d'influence",
                    "Développer le content marketing",
                    "Tester les publicités display"
                ]
            })

        # Recommandations d'automatisation
        if len(self.automation_rules) < 5:
            recommendations.append({
                "category": "automation",
                "priority": "medium",
                "title": "Renforcer l'automatisation",
                "description": "Ajouter plus de règles d'automatisation pour optimiser les performances.",
                "actions": [
                    "Automatiser la pause des campagnes sous-performantes",
                    "Mettre en place des alertes de budget avancées",
                    "Automatiser l'optimisation des enchères"
                ]
            })

        return recommendations

    async def _handle_crisis(self, crisis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gère les situations de crise marketing"""
        crisis_type = crisis_data.get("type", "general")
        severity = crisis_data.get("severity", "medium")

        try:
            crisis_id = f"crisis_{uuid.uuid4().hex[:8]}"

            crisis_response = {
                "crisis_id": crisis_id,
                "type": crisis_type,
                "severity": severity,
                "detected_at": datetime.now().isoformat(),
                "actions_taken": [],
                "status": "handling"
            }

            # Actions immédiates selon le type de crise
            if crisis_type == "negative_sentiment":
                # Pause des campagnes sensibles
                paused_campaigns = []
                for campaign_id, campaign in self.active_campaigns.items():
                    if campaign.type in [CampaignType.BRAND_AWARENESS, CampaignType.PRODUCT_LAUNCH]:
                        campaign.status = CampaignStatus.PAUSED
                        paused_campaigns.append(campaign_id)

                crisis_response["actions_taken"].append({
                    "action": "pause_sensitive_campaigns",
                    "campaigns_paused": paused_campaigns
                })

            elif crisis_type == "budget_overspend":
                # Pause toutes les campagnes actives
                for campaign_id, campaign in self.active_campaigns.items():
                    campaign.status = CampaignStatus.PAUSED

                crisis_response["actions_taken"].append({
                    "action": "pause_all_campaigns",
                    "reason": "budget_protection"
                })

            elif crisis_type == "performance_drop":
                # Déclencher optimisation d'urgence
                for campaign_id in self.active_campaigns.keys():
                    await self._optimize_campaign({"campaign_id": campaign_id})

                crisis_response["actions_taken"].append({
                    "action": "emergency_optimization",
                    "campaigns_optimized": list(self.active_campaigns.keys())
                })

            # Notification aux parties prenantes
            await self._send_crisis_notifications(crisis_response)

            # Mise à jour des métriques
            self.orchestrator_metrics.crisis_responses += 1

            crisis_response["status"] = "handled"

            self.logger.warning(f"Crise {crisis_id} gérée: {crisis_type}")

            return {
                "success": True,
                "crisis_response": crisis_response,
                "message": f"Crise {crisis_type} gérée avec {len(crisis_response['actions_taken'])} actions"
            }

        except Exception as e:
            self.logger.error(f"Erreur lors de la gestion de crise: {str(e)}")
            raise

    async def _send_crisis_notifications(self, crisis_response: Dict[str, Any]):
        """Envoie des notifications de crise aux parties prenantes"""
        # Dans un vrai système, ceci enverrait des emails/SMS/Slack
        notification = {
            "type": "crisis_alert",
            "crisis_id": crisis_response["crisis_id"],
            "message": f"Crise détectée: {crisis_response['type']} - Actions prises automatiquement",
            "timestamp": datetime.now().isoformat(),
            "severity": crisis_response["severity"]
        }

        self.alerts.append(notification)
        self.logger.warning(f"Notification de crise envoyée: {notification}")

    async def _setup_ab_test(self, ab_test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Configure un test A/B pour une campagne"""
        campaign_id = ab_test_data.get("campaign_id")
        test_variable = ab_test_data.get("variable", "creative")

        if campaign_id not in self.campaigns:
            raise ValueError(f"Campagne {campaign_id} introuvable")

        campaign = self.campaigns[campaign_id]

        try:
            ab_test = {
                "test_id": f"ab_test_{uuid.uuid4().hex[:8]}",
                "campaign_id": campaign_id,
                "variable": test_variable,
                "variants": ab_test_data.get("variants", ["A", "B"]),
                "traffic_split": ab_test_data.get("traffic_split", [50, 50]),
                "duration_days": ab_test_data.get("duration_days", 14),
                "success_metric": ab_test_data.get("success_metric", "conversion_rate"),
                "confidence_level": ab_test_data.get("confidence_level", 0.95),
                "status": "setup",
                "start_date": datetime.now().isoformat(),
                "results": {}
            }

            # Ajouter le test A/B à la campagne
            if not campaign.ab_tests:
                campaign.ab_tests = []
            campaign.ab_tests.append(ab_test)

            # Configurer les variants avec les agents concernés
            for i, variant in enumerate(ab_test["variants"]):
                traffic_percentage = ab_test["traffic_split"][i]

                # Configuration selon la variable testée
                if test_variable == "creative":
                    # Créer différentes versions créatives
                    if "content_creator" in self.marketing_agents:
                        creative_task = self.marketing_agents["content_creator"].create_task(
                            task_type="create_ab_variant",
                            priority=8,
                            data={
                                "campaign_id": campaign_id,
                                "test_id": ab_test["test_id"],
                                "variant": variant,
                                "traffic_percentage": traffic_percentage
                            }
                        )
                        await self.marketing_agents["content_creator"].add_task(creative_task)

                elif test_variable == "audience":
                    # Configurer différents ciblages d'audience
                    if "social_media" in self.marketing_agents:
                        audience_task = self.marketing_agents["social_media"].create_task(
                            task_type="setup_ab_audience",
                            priority=8,
                            data={
                                "campaign_id": campaign_id,
                                "test_id": ab_test["test_id"],
                                "variant": variant,
                                "traffic_percentage": traffic_percentage
                            }
                        )
                        await self.marketing_agents["social_media"].add_task(audience_task)

            ab_test["status"] = "running"

            self.logger.info(f"Test A/B {ab_test['test_id']} configuré pour la campagne {campaign_id}")

            return {
                "success": True,
                "ab_test": ab_test,
                "message": f"Test A/B configuré pour tester {test_variable}"
            }

        except Exception as e:
            self.logger.error(f"Erreur lors de la configuration du test A/B: {str(e)}")
            raise

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'orchestrateur"""
        return [
            "campaign_orchestration",
            "multi_channel_coordination",
            "performance_monitoring",
            "budget_optimization",
            "crisis_management",
            "ab_testing",
            "real_time_analytics",
            "automated_optimization",
            "strategic_reporting",
            "agent_coordination",
            "workflow_automation",
            "roi_maximization"
        ]

    def _get_default_audience(self) -> Dict[str, Any]:
        """Retourne l'audience par défaut pour iFiveMe"""
        return {
            "demographics": {
                "age_range": [25, 55],
                "locations": ["Canada", "USA", "France"],
                "languages": ["fr", "en"]
            },
            "interests": [
                "networking",
                "business_development",
                "digital_tools",
                "entrepreneurship",
                "professional_services"
            ],
            "behaviors": [
                "business_networking",
                "digital_adoption",
                "professional_development"
            ]
        }

    def _get_default_kpis(self) -> Dict[str, float]:
        """Retourne les KPIs par défaut"""
        return {
            "target_roi": 3.0,
            "target_conversion_rate": 0.05,
            "target_cpa": 20.0,
            "target_reach": 10000,
            "target_engagement_rate": 0.08
        }

    def _calculate_budget_allocation(self, total_budget: float, channels: List[str], template_allocation: Dict[str, float] = None) -> Dict[str, float]:
        """Calcule l'allocation budgétaire par canal"""
        if template_allocation:
            return {
                channel: total_budget * template_allocation.get(channel, 1.0 / len(channels))
                for channel in channels
            }
        else:
            # Allocation équitable par défaut
            budget_per_channel = total_budget / len(channels)
            return {channel: budget_per_channel for channel in channels}

    async def _health_check_all_agents(self) -> Dict[str, bool]:
        """Vérifie la santé de tous les agents"""
        health_status = {}

        for agent_id, agent in self.marketing_agents.items():
            try:
                health_status[agent_id] = await agent.health_check()
            except Exception as e:
                health_status[agent_id] = False
                self.logger.error(f"Health check failed for {agent_id}: {str(e)}")

        return health_status

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Retourne les données actuelles du dashboard"""
        return self.dashboard_data

    def get_active_campaigns(self) -> Dict[str, MarketingCampaign]:
        """Retourne toutes les campagnes actives"""
        return self.active_campaigns

    def get_campaign_by_id(self, campaign_id: str) -> Optional[MarketingCampaign]:
        """Retourne une campagne par son ID"""
        return self.campaigns.get(campaign_id)

    async def pause_campaign(self, campaign_id: str) -> bool:
        """Met en pause une campagne"""
        if campaign_id in self.active_campaigns:
            self.active_campaigns[campaign_id].status = CampaignStatus.PAUSED
            self.logger.info(f"Campagne {campaign_id} mise en pause")
            return True
        return False

    async def resume_campaign(self, campaign_id: str) -> bool:
        """Reprend une campagne en pause"""
        if campaign_id in self.campaigns:
            campaign = self.campaigns[campaign_id]
            if campaign.status == CampaignStatus.PAUSED:
                campaign.status = CampaignStatus.RUNNING
                self.active_campaigns[campaign_id] = campaign
                self.logger.info(f"Campagne {campaign_id} reprise")
                return True
        return False

    def get_orchestrator_metrics(self) -> OrchestratorMetrics:
        """Retourne les métriques de l'orchestrateur"""
        return self.orchestrator_metrics

# Fonction utilitaire pour créer et initialiser l'orchestrateur
async def create_marketing_orchestrator() -> MarketingOrchestrator:
    """Crée et initialise l'orchestrateur marketing"""
    orchestrator = MarketingOrchestrator()

    # Attendre l'initialisation des agents
    await asyncio.sleep(1)

    return orchestrator

# Point d'entrée principal
if __name__ == "__main__":
    import asyncio

    async def main():
        # Créer l'orchestrateur
        orchestrator = await create_marketing_orchestrator()

        # Exemple d'utilisation : créer une campagne de lancement produit
        campaign_task = orchestrator.create_task(
            task_type="create_campaign",
            priority=9,
            data={
                "type": "product_launch",
                "name": "Lancement iFiveMe 2.0",
                "budget": 5000.0,
                "channels": ["social_media", "email"],
                "start_date": datetime.now().isoformat(),
                "objectives": [
                    "Générer 1000 nouvelles inscriptions",
                    "Obtenir 50 témoignages clients",
                    "Atteindre un ROI de 4.0"
                ]
            }
        )

        await orchestrator.add_task(campaign_task)
        await orchestrator.execute_tasks()

        # Afficher les résultats
        status = orchestrator.get_status()
        print(f"Orchestrateur initialisé avec {len(orchestrator.marketing_agents)} agents")
        print(f"Campagnes gérées: {orchestrator.orchestrator_metrics.campaigns_managed}")

    asyncio.run(main())