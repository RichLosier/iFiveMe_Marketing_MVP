"""
iFiveMe Marketing MVP - Agent Analytics et Rapports
Collecte, analyse et génère des rapports marketing
"""

import json
import asyncio
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.base_agent import BaseAgent, AgentTask
from config.settings import COMPANY_INFO, MARKETING_KPIS, API_KEYS

@dataclass
class MarketingMetric:
    """Structure pour une métrique marketing"""
    name: str
    value: float
    previous_value: float
    change_percentage: float
    period: str
    source: str
    target: Optional[float] = None
    status: str = "normal"  # normal, warning, critical

@dataclass
class CampaignAnalytics:
    """Analytics d'une campagne"""
    campaign_id: str
    campaign_name: str
    channel: str
    start_date: datetime
    end_date: datetime
    budget: float
    impressions: int
    clicks: int
    conversions: int
    revenue: float
    roi: float
    cpa: float
    ctr: float
    conversion_rate: float

@dataclass
class ChannelPerformance:
    """Performance d'un canal marketing"""
    channel: str
    impressions: int
    clicks: int
    conversions: int
    cost: float
    revenue: float
    roi: float
    attribution_weight: float

class AnalyticsAgent(BaseAgent):
    """Agent spécialisé dans l'analyse des données marketing iFiveMe"""

    def __init__(self):
        super().__init__(
            agent_id="analytics",
            name="Agent Analytics Marketing iFiveMe",
            config={
                "reporting_frequency": "daily",
                "data_retention_days": 365,
                "alert_thresholds": {
                    "roi_minimum": 200,
                    "conversion_rate_minimum": 2.0,
                    "cost_per_acquisition_maximum": 50
                },
                "attribution_model": "last_click"
            }
        )

        # Canaux de marketing iFiveMe
        self.marketing_channels = {
            "paid_social": {
                "name": "Publicités Réseaux Sociaux",
                "platforms": ["Facebook", "LinkedIn", "Instagram", "Twitter"],
                "cost_model": "CPC",
                "attribution_weight": 0.25
            },
            "organic_social": {
                "name": "Réseaux Sociaux Organiques",
                "platforms": ["LinkedIn", "Twitter", "Facebook", "Instagram"],
                "cost_model": "Time",
                "attribution_weight": 0.15
            },
            "email_marketing": {
                "name": "Email Marketing",
                "platforms": ["Mailchimp", "Custom"],
                "cost_model": "Fixed",
                "attribution_weight": 0.20
            },
            "content_marketing": {
                "name": "Marketing de Contenu",
                "platforms": ["Blog", "YouTube", "Webinaires"],
                "cost_model": "Time",
                "attribution_weight": 0.15
            },
            "paid_search": {
                "name": "Recherche Payante",
                "platforms": ["Google Ads", "Bing"],
                "cost_model": "CPC",
                "attribution_weight": 0.20
            },
            "referral": {
                "name": "Parrainage",
                "platforms": ["Programme Partenaires"],
                "cost_model": "Commission",
                "attribution_weight": 0.05
            }
        }

        # KPIs principaux iFiveMe
        self.primary_kpis = {
            "user_acquisition": {
                "new_users": "Nouveaux utilisateurs",
                "user_activation": "Taux d'activation",
                "time_to_first_card": "Temps première carte"
            },
            "engagement": {
                "cards_created": "Cartes créées",
                "cards_shared": "Cartes partagées",
                "profile_views": "Vues de profil"
            },
            "revenue": {
                "mrr": "Revenu récurrent mensuel",
                "ltv": "Valeur à vie client",
                "churn_rate": "Taux de désabonnement"
            },
            "marketing": {
                "cac": "Coût d'acquisition client",
                "roas": "Retour sur investissement publicitaire",
                "organic_traffic": "Trafic organique"
            }
        }

        # Configuration des alertes
        self.alert_rules = {
            "roi_below_target": {
                "metric": "roi",
                "condition": "below",
                "threshold": 200,
                "severity": "high"
            },
            "cac_above_ltv": {
                "metric": "cac_to_ltv_ratio",
                "condition": "above",
                "threshold": 0.3,
                "severity": "critical"
            },
            "conversion_drop": {
                "metric": "conversion_rate",
                "condition": "decrease",
                "threshold": 20,  # 20% drop
                "severity": "medium"
            }
        }

        # Base de données simulée
        self.campaigns_data = []
        self.daily_metrics = []
        self.user_journey_data = []

    def get_capabilities(self) -> List[str]:
        return [
            "Collecte de données multi-canaux",
            "Analyse de performance en temps réel",
            "Attribution marketing avancée",
            "Génération de rapports automatisés",
            "Alertes intelligentes",
            "Analyse de cohortes utilisateurs",
            "Prévisions et recommandations",
            "Dashboard marketing interactif",
            "ROI et ROAS tracking",
            "Analyse des parcours clients"
        ]

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite les tâches d'analytics"""
        task_type = task.type
        data = task.data

        if task_type == "collect_data":
            return await self._collect_marketing_data(data)
        elif task_type == "generate_report":
            return await self._generate_marketing_report(data)
        elif task_type == "analyze_campaign":
            return await self._analyze_campaign_performance(data)
        elif task_type == "track_attribution":
            return await self._track_marketing_attribution(data)
        elif task_type == "monitor_kpis":
            return await self._monitor_kpis(data)
        elif task_type == "cohort_analysis":
            return await self._perform_cohort_analysis(data)
        elif task_type == "forecast":
            return await self._generate_marketing_forecast(data)
        elif task_type == "competitive_analysis":
            return await self._analyze_competitive_landscape(data)
        elif task_type == "dashboard":
            return await self._generate_dashboard_data(data)
        else:
            raise ValueError(f"Type de tâche non supporté: {task_type}")

    async def _collect_marketing_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Collecte les données marketing depuis différentes sources"""
        sources = data.get("sources", list(self.marketing_channels.keys()))
        date_range = data.get("date_range", 30)  # jours

        collected_data = {}

        for source in sources:
            source_data = await self._fetch_source_data(source, date_range)
            collected_data[source] = source_data

        # Agrégation des métriques
        aggregated_metrics = self._aggregate_metrics(collected_data)

        return {
            "collection_timestamp": datetime.now().isoformat(),
            "sources": sources,
            "date_range_days": date_range,
            "raw_data": collected_data,
            "aggregated_metrics": aggregated_metrics,
            "data_quality_score": self._calculate_data_quality_score(collected_data),
            "collection_status": "success"
        }

    async def _generate_marketing_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un rapport marketing complet"""
        report_type = data.get("type", "monthly")  # daily, weekly, monthly, quarterly
        include_channels = data.get("channels", list(self.marketing_channels.keys()))
        include_forecasts = data.get("include_forecasts", True)

        # Période du rapport
        if report_type == "daily":
            period_days = 1
        elif report_type == "weekly":
            period_days = 7
        elif report_type == "monthly":
            period_days = 30
        else:  # quarterly
            period_days = 90

        # Collecter les données
        report_data = await self._collect_marketing_data({
            "sources": include_channels,
            "date_range": period_days
        })

        # Analyser les performances
        performance_analysis = self._analyze_period_performance(report_data, period_days)

        # Insights et recommandations
        insights = self._generate_insights(performance_analysis)
        recommendations = self._generate_recommendations(performance_analysis)

        # Prévisions
        forecasts = {}
        if include_forecasts:
            forecasts = await self._generate_marketing_forecast({
                "horizon_days": period_days,
                "metrics": ["revenue", "users", "cac"]
            })

        return {
            "report_id": f"report_{report_type}_{datetime.now().strftime('%Y%m%d')}",
            "type": report_type,
            "period": {
                "start": (datetime.now() - timedelta(days=period_days)).isoformat(),
                "end": datetime.now().isoformat(),
                "days": period_days
            },
            "summary": {
                "total_spend": performance_analysis["total_spend"],
                "total_revenue": performance_analysis["total_revenue"],
                "total_users": performance_analysis["total_users"],
                "overall_roi": performance_analysis["overall_roi"],
                "best_performing_channel": performance_analysis["best_channel"],
                "worst_performing_channel": performance_analysis["worst_channel"]
            },
            "channel_performance": performance_analysis["channels"],
            "key_insights": insights,
            "recommendations": recommendations,
            "forecasts": forecasts,
            "appendix": {
                "data_sources": include_channels,
                "methodology": "Attribution last-click avec pondération multi-touch",
                "confidence_level": 0.85
            }
        }

    async def _analyze_campaign_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse la performance d'une campagne spécifique"""
        campaign_id = data.get("campaign_id")
        compare_to_benchmark = data.get("compare_to_benchmark", True)

        # Simuler les données de campagne
        campaign_data = self._simulate_campaign_data(campaign_id)

        # Calculs de performance
        metrics = self._calculate_campaign_metrics(campaign_data)

        # Comparaison aux benchmarks
        benchmark_comparison = {}
        if compare_to_benchmark:
            benchmarks = self._get_industry_benchmarks(campaign_data["channel"])
            benchmark_comparison = self._compare_to_benchmarks(metrics, benchmarks)

        # Analyse temporelle
        temporal_analysis = self._analyze_campaign_timeline(campaign_data)

        # Segments de performance
        segment_analysis = self._analyze_campaign_segments(campaign_data)

        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign_data["name"],
            "channel": campaign_data["channel"],
            "status": campaign_data["status"],
            "period": {
                "start": campaign_data["start_date"].isoformat(),
                "end": campaign_data["end_date"].isoformat(),
                "duration_days": (campaign_data["end_date"] - campaign_data["start_date"]).days
            },
            "metrics": metrics,
            "benchmark_comparison": benchmark_comparison,
            "temporal_analysis": temporal_analysis,
            "segment_performance": segment_analysis,
            "optimization_opportunities": self._identify_optimization_opportunities(metrics, benchmarks if compare_to_benchmark else None),
            "next_actions": self._recommend_campaign_actions(metrics, temporal_analysis)
        }

    async def _track_marketing_attribution(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse l'attribution marketing multi-touch"""
        attribution_model = data.get("model", "last_click")  # first_click, last_click, linear, time_decay
        conversion_window = data.get("window_days", 30)
        include_offline = data.get("include_offline", False)

        # Simuler les données de parcours client
        customer_journeys = self._simulate_customer_journeys(1000, conversion_window)

        # Appliquer le modèle d'attribution
        attribution_results = self._apply_attribution_model(customer_journeys, attribution_model)

        # Analyser les parcours
        journey_insights = self._analyze_customer_journeys(customer_journeys)

        # Impact sur les budgets
        budget_recommendations = self._calculate_attribution_impact(attribution_results)

        return {
            "attribution_model": attribution_model,
            "conversion_window_days": conversion_window,
            "total_conversions_analyzed": len(customer_journeys),
            "channel_attribution": {
                channel: {
                    "attributed_conversions": results["conversions"],
                    "attributed_revenue": results["revenue"],
                    "attribution_percentage": results["percentage"],
                    "avg_position_in_journey": results["avg_position"]
                }
                for channel, results in attribution_results.items()
            },
            "journey_insights": journey_insights,
            "budget_optimization": budget_recommendations,
            "model_comparison": self._compare_attribution_models(customer_journeys),
            "recommendations": [
                f"Modèle {attribution_model} suggère une réallocation de {budget_recommendations['reallocation_percentage']}% du budget",
                f"Canal sous-investi: {budget_recommendations['underinvested_channel']}",
                f"Canal sur-investi: {budget_recommendations['overinvested_channel']}"
            ]
        }

    async def _monitor_kpis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Surveille les KPIs et déclenche des alertes"""
        kpi_categories = data.get("categories", list(self.primary_kpis.keys()))
        alert_level = data.get("alert_level", "medium")  # low, medium, high, critical

        current_metrics = {}
        alerts = []
        recommendations = []

        for category in kpi_categories:
            category_kpis = self.primary_kpis[category]

            for kpi_key, kpi_name in category_kpis.items():
                # Simuler les métriques actuelles
                current_value = self._simulate_kpi_value(kpi_key)
                historical_value = self._simulate_kpi_value(kpi_key, historical=True)
                target_value = self._get_kpi_target(kpi_key)

                metric = MarketingMetric(
                    name=kpi_name,
                    value=current_value,
                    previous_value=historical_value,
                    change_percentage=((current_value - historical_value) / historical_value * 100) if historical_value != 0 else 0,
                    period="30d",
                    source=category,
                    target=target_value
                )

                # Déterminer le statut
                metric.status = self._determine_metric_status(metric)

                current_metrics[kpi_key] = asdict(metric)

                # Vérifier les alertes
                alert = self._check_alert_conditions(metric, alert_level)
                if alert:
                    alerts.append(alert)

                # Générer des recommandations
                rec = self._generate_kpi_recommendations(metric)
                if rec:
                    recommendations.extend(rec)

        return {
            "monitoring_timestamp": datetime.now().isoformat(),
            "categories_monitored": kpi_categories,
            "total_kpis": len(current_metrics),
            "current_metrics": current_metrics,
            "alerts": alerts,
            "recommendations": recommendations,
            "dashboard_summary": {
                "healthy_metrics": len([m for m in current_metrics.values() if m["status"] == "normal"]),
                "warning_metrics": len([m for m in current_metrics.values() if m["status"] == "warning"]),
                "critical_metrics": len([m for m in current_metrics.values() if m["status"] == "critical"]),
                "overall_health_score": self._calculate_health_score(current_metrics)
            },
            "trends": self._analyze_kpi_trends(current_metrics),
            "next_monitoring": (datetime.now() + timedelta(hours=24)).isoformat()
        }

    async def _perform_cohort_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Effectue une analyse de cohortes"""
        cohort_type = data.get("type", "monthly")  # daily, weekly, monthly
        metric = data.get("metric", "retention")  # retention, revenue, engagement
        periods = data.get("periods", 12)  # nombre de périodes à analyser

        # Simuler les données de cohorte
        cohort_data = self._simulate_cohort_data(cohort_type, periods)

        # Calculer les métriques de cohorte
        cohort_metrics = self._calculate_cohort_metrics(cohort_data, metric)

        # Analyser les tendances
        trends = self._analyze_cohort_trends(cohort_metrics)

        # Identifier les insights
        insights = self._extract_cohort_insights(cohort_metrics, trends)

        return {
            "analysis_id": f"cohort_{cohort_type}_{metric}_{datetime.now().strftime('%Y%m%d')}",
            "cohort_type": cohort_type,
            "metric_analyzed": metric,
            "periods_analyzed": periods,
            "cohort_table": cohort_metrics,
            "key_insights": insights,
            "trends": trends,
            "benchmarks": {
                "industry_avg_retention_30d": 0.25,
                "industry_avg_retention_90d": 0.12,
                "ifiveme_target_retention_30d": 0.35,
                "ifiveme_target_retention_90d": 0.18
            },
            "recommendations": [
                "Améliorer l'onboarding des cohortes avec rétention < 20%",
                "Analyser les facteurs de succès des cohortes avec rétention > 40%",
                "Implémenter des campagnes de réactivation ciblées"
            ],
            "visualization_config": self._generate_cohort_visualization_config(cohort_metrics)
        }

    async def _generate_marketing_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère des prévisions marketing"""
        horizon_days = data.get("horizon_days", 90)
        metrics = data.get("metrics", ["revenue", "users", "cac"])
        confidence_level = data.get("confidence_level", 0.8)

        forecasts = {}

        for metric in metrics:
            # Simuler les données historiques
            historical_data = self._simulate_historical_data(metric, 180)  # 6 mois d'historique

            # Générer la prévision
            forecast_data = self._generate_metric_forecast(historical_data, horizon_days)

            forecasts[metric] = {
                "forecast_values": forecast_data["values"],
                "confidence_intervals": forecast_data["confidence_intervals"],
                "trend": forecast_data["trend"],
                "seasonality_detected": forecast_data["seasonality"],
                "accuracy_score": forecast_data["accuracy"],
                "key_drivers": self._identify_forecast_drivers(metric)
            }

        # Scénarios
        scenarios = self._generate_forecast_scenarios(forecasts)

        return {
            "forecast_id": f"forecast_{datetime.now().strftime('%Y%m%d_%H%M')}",
            "horizon_days": horizon_days,
            "confidence_level": confidence_level,
            "forecasts": forecasts,
            "scenarios": scenarios,
            "assumptions": [
                "Pas de changement majeur dans la stratégie marketing",
                "Conditions économiques stables",
                "Pas de nouveaux concurrents majeurs",
                "Croissance organique continue"
            ],
            "risk_factors": [
                "Volatilité du marché des cartes d'affaires digitales",
                "Changements dans les algorithmes des plateformes sociales",
                "Fluctuations saisonnières B2B"
            ],
            "recommendations": self._generate_forecast_recommendations(forecasts, scenarios)
        }

    async def _analyze_competitive_landscape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse le paysage concurrentiel"""
        competitors = data.get("competitors", ["HiHello", "CamCard", "Inigo", "Popl"])
        metrics = data.get("metrics", ["traffic", "social_engagement", "ad_spend"])

        competitive_data = {}

        for competitor in competitors:
            competitor_metrics = self._simulate_competitor_data(competitor, metrics)
            competitive_data[competitor] = competitor_metrics

        # Analyser la position iFiveMe
        ifiveme_position = self._analyze_market_position(competitive_data)

        # Identifier les opportunités et menaces
        swot_analysis = self._generate_swot_analysis(competitive_data)

        return {
            "analysis_date": datetime.now().isoformat(),
            "competitors_analyzed": competitors,
            "metrics_analyzed": metrics,
            "competitive_landscape": competitive_data,
            "ifiveme_market_position": ifiveme_position,
            "swot_analysis": swot_analysis,
            "key_insights": [
                f"iFiveMe se positionne #{ifiveme_position['rank']} sur le marché des cartes virtuelles",
                f"Principal avantage concurrentiel: {ifiveme_position['key_advantage']}",
                f"Principale menace: {ifiveme_position['main_threat']}"
            ],
            "strategic_recommendations": [
                "Renforcer la différenciation sur les fonctionnalités analytics",
                "Développer la présence sur LinkedIn vs concurrents",
                "Optimiser le coût d'acquisition client"
            ],
            "monitoring_alerts": self._setup_competitive_alerts(competitors)
        }

    async def _generate_dashboard_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère les données pour le dashboard marketing"""
        dashboard_type = data.get("type", "executive")  # executive, operational, tactical
        time_period = data.get("period", "30d")

        # Métriques principales
        key_metrics = await self._get_dashboard_key_metrics(time_period)

        # Données des graphiques
        chart_data = self._generate_chart_data(time_period)

        # Alertes et notifications
        alerts = self._get_dashboard_alerts()

        # Recommandations actionables
        action_items = self._get_dashboard_actions()

        return {
            "dashboard_type": dashboard_type,
            "last_updated": datetime.now().isoformat(),
            "period": time_period,
            "key_metrics": key_metrics,
            "charts": chart_data,
            "alerts": alerts,
            "action_items": action_items,
            "quick_insights": [
                f"ROI global: {key_metrics['roi']}% (↑ {key_metrics['roi_change']}%)",
                f"Meilleur canal: {key_metrics['best_channel']} ({key_metrics['best_channel_roi']}% ROI)",
                f"CAC moyen: {key_metrics['avg_cac']}$ (objectif: <40$)",
                f"LTV/CAC ratio: {key_metrics['ltv_cac_ratio']}:1"
            ],
            "performance_summary": {
                "status": key_metrics["overall_status"],  # excellent, good, needs_attention, critical
                "score": key_metrics["performance_score"],  # 0-100
                "trend": key_metrics["trend"]  # improving, stable, declining
            }
        }

    # Méthodes utilitaires

    async def _fetch_source_data(self, source: str, days: int) -> Dict[str, Any]:
        """Simule la collecte de données d'une source"""
        await asyncio.sleep(0.1)  # Simuler délai API

        # Données simulées basées sur le canal
        base_metrics = {
            "paid_social": {
                "impressions": 125000,
                "clicks": 3750,
                "conversions": 187,
                "cost": 2800,
                "revenue": 9350
            },
            "organic_social": {
                "impressions": 85000,
                "clicks": 2550,
                "conversions": 89,
                "cost": 0,
                "revenue": 4450
            },
            "email_marketing": {
                "impressions": 45000,
                "clicks": 2250,
                "conversions": 156,
                "cost": 200,
                "revenue": 7800
            },
            "paid_search": {
                "impressions": 95000,
                "clicks": 4750,
                "conversions": 203,
                "cost": 3200,
                "revenue": 10150
            }
        }

        return base_metrics.get(source, {
            "impressions": 50000,
            "clicks": 1500,
            "conversions": 75,
            "cost": 1000,
            "revenue": 3750
        })

    def _simulate_campaign_data(self, campaign_id: str) -> Dict[str, Any]:
        """Simule les données d'une campagne"""
        import random

        channels = list(self.marketing_channels.keys())
        channel = random.choice(channels)

        start_date = datetime.now() - timedelta(days=random.randint(7, 30))
        end_date = start_date + timedelta(days=random.randint(7, 21))

        return {
            "id": campaign_id,
            "name": f"Campagne iFiveMe {campaign_id}",
            "channel": channel,
            "start_date": start_date,
            "end_date": end_date,
            "status": "active",
            "budget": random.randint(1000, 5000),
            "impressions": random.randint(50000, 200000),
            "clicks": random.randint(1500, 8000),
            "conversions": random.randint(75, 400)
        }

    def _calculate_campaign_metrics(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule les métriques d'une campagne"""
        impressions = campaign_data["impressions"]
        clicks = campaign_data["clicks"]
        conversions = campaign_data["conversions"]
        budget = campaign_data["budget"]

        # Simuler le revenu basé sur les conversions
        avg_order_value = 50  # $ par conversion iFiveMe
        revenue = conversions * avg_order_value

        return {
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": revenue,
            "ctr": (clicks / impressions * 100) if impressions > 0 else 0,
            "conversion_rate": (conversions / clicks * 100) if clicks > 0 else 0,
            "cpc": (budget / clicks) if clicks > 0 else 0,
            "cpa": (budget / conversions) if conversions > 0 else 0,
            "roi": ((revenue - budget) / budget * 100) if budget > 0 else 0,
            "roas": (revenue / budget) if budget > 0 else 0
        }

    def _simulate_kpi_value(self, kpi_key: str, historical: bool = False) -> float:
        """Simule une valeur de KPI"""
        import random

        base_values = {
            "new_users": 1250 if not historical else 1180,
            "user_activation": 68.5 if not historical else 65.2,
            "cards_created": 3420 if not historical else 3180,
            "mrr": 45600 if not historical else 42300,
            "ltv": 285 if not historical else 275,
            "churn_rate": 3.2 if not historical else 3.8,
            "cac": 38.50 if not historical else 41.20,
            "roas": 420 if not historical else 385
        }

        base = base_values.get(kpi_key, 100)
        variation = random.uniform(-0.1, 0.1)
        return round(base * (1 + variation), 2)

    def _get_kpi_target(self, kpi_key: str) -> Optional[float]:
        """Retourne la cible pour un KPI"""
        targets = {
            "new_users": 1500,
            "user_activation": 75.0,
            "cards_created": 4000,
            "mrr": 50000,
            "ltv": 300,
            "churn_rate": 2.5,
            "cac": 35.0,
            "roas": 450
        }

        return targets.get(kpi_key)

    def _determine_metric_status(self, metric: MarketingMetric) -> str:
        """Détermine le statut d'une métrique"""
        if metric.target:
            if metric.name in ["churn_rate", "cac"]:  # Plus bas = mieux
                if metric.value <= metric.target * 0.9:
                    return "normal"
                elif metric.value <= metric.target:
                    return "warning"
                else:
                    return "critical"
            else:  # Plus haut = mieux
                if metric.value >= metric.target * 0.9:
                    return "normal"
                elif metric.value >= metric.target * 0.8:
                    return "warning"
                else:
                    return "critical"

        # Basé sur le changement
        if abs(metric.change_percentage) < 5:
            return "normal"
        elif abs(metric.change_percentage) < 15:
            return "warning"
        else:
            return "critical"

    def _calculate_health_score(self, metrics: Dict[str, Dict[str, Any]]) -> int:
        """Calcule un score de santé global"""
        if not metrics:
            return 0

        status_scores = {"normal": 100, "warning": 70, "critical": 30}
        total_score = sum(status_scores.get(m["status"], 50) for m in metrics.values())

        return int(total_score / len(metrics))

    async def _get_dashboard_key_metrics(self, period: str) -> Dict[str, Any]:
        """Récupère les métriques clés pour le dashboard"""
        return {
            "roi": 342,
            "roi_change": 12.5,
            "best_channel": "Email Marketing",
            "best_channel_roi": 485,
            "avg_cac": 38.50,
            "ltv_cac_ratio": 7.4,
            "overall_status": "good",
            "performance_score": 82,
            "trend": "improving"
        }