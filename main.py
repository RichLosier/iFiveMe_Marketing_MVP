#!/usr/bin/env python3
"""
iFiveMe Marketing MVP - Point d'entrée principal
Démonstration et test du système d'automatisation marketing
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.append(str(Path(__file__).parent))

from config.settings import LOGGING_CONFIG
from agents.orchestrator_agent import MarketingOrchestrator
from utils.base_agent import AgentTask

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def demo_campaign_creation():
    """Démo de création d'une campagne complète"""
    print("🚀 iFiveMe Marketing MVP - Démonstration")
    print("=" * 60)

    # Créer l'orchestrateur
    print("\n📋 Initialisation de l'orchestrateur marketing...")
    orchestrator = MarketingOrchestrator()

    # Vérifier la santé du système
    health_check = await orchestrator.health_check()
    if not health_check:
        print("❌ Échec du health check")
        return

    print("✅ Orchestrateur initialisé avec succès")

    # Démonstration 1: Campagne de lancement produit
    print("\n🎯 Démonstration 1: Campagne de lancement produit")
    print("-" * 50)

    campaign_task = orchestrator.create_task(
        task_type="create_campaign",
        priority=9,
        data={
            "type": "product_launch",
            "name": "Lancement iFiveMe 2.0 - Nouvelles fonctionnalités",
            "budget": 5000.0,
            "channels": ["social_media", "email", "content"],
            "target_audience": "entrepreneurs_canada",
            "duration_days": 30,
            "objectives": [
                "Générer 1000 nouveaux utilisateurs",
                "Atteindre un ROI de 4.0",
                "Augmenter la notoriété de marque de 25%"
            ],
            "key_messages": [
                "Nouvelles fonctionnalités analytics avancées",
                "Interface utilisateur améliorée",
                "Intégration CRM renforcée"
            ]
        }
    )

    await orchestrator.add_task(campaign_task)
    await orchestrator.execute_tasks()

    print("✅ Campagne créée et lancée")

    # Démonstration 2: Monitoring en temps réel
    print("\n📊 Démonstration 2: Monitoring des performances")
    print("-" * 50)

    monitoring_task = orchestrator.create_task(
        task_type="monitor_performance",
        priority=7,
        data={
            "campaigns": ["all"],
            "metrics": ["roi", "conversions", "engagement"],
            "alert_thresholds": {
                "roi_minimum": 300,
                "conversion_rate_minimum": 2.0,
                "budget_utilization_maximum": 80
            }
        }
    )

    await orchestrator.add_task(monitoring_task)
    await orchestrator.execute_tasks()

    print("✅ Monitoring configuré et actif")

    # Démonstration 3: Optimisation automatique
    print("\n🎯 Démonstration 3: Optimisation budgétaire automatique")
    print("-" * 50)

    optimization_task = orchestrator.create_task(
        task_type="optimize_budget",
        priority=8,
        data={
            "strategy": "roi_maximization",
            "reallocation_percentage": 20,
            "minimum_performance_threshold": 250  # ROI minimum 250%
        }
    )

    await orchestrator.add_task(optimization_task)
    await orchestrator.execute_tasks()

    print("✅ Optimisation budgétaire effectuée")

    # Démonstration 4: Rapport complet
    print("\n📈 Démonstration 4: Génération de rapport stratégique")
    print("-" * 50)

    report_task = orchestrator.create_task(
        task_type="generate_strategic_report",
        priority=6,
        data={
            "period": "30d",
            "include_forecasts": True,
            "include_recommendations": True,
            "audience": "executive"
        }
    )

    await orchestrator.add_task(report_task)
    await orchestrator.execute_tasks()

    print("✅ Rapport stratégique généré")

    # Afficher le statut final
    print("\n📋 Statut final du système")
    print("-" * 50)

    status = orchestrator.get_status()
    print(f"Agent: {status['name']}")
    print(f"Statut: {'🟢 Actif' if status['is_active'] else '🔴 Inactif'}")
    print(f"Tâches traitées: {status['metrics']['tasks_completed']}")
    print(f"Taux de succès: {status['metrics']['success_rate']:.1f}%")
    print(f"Temps de réponse moyen: {status['metrics']['average_response_time']:.2f}s")

    # Arrêt propre
    await orchestrator.stop()
    print("\n✅ Démonstration terminée avec succès!")

async def demo_individual_agents():
    """Démo des agents individuels"""
    print("\n🤖 Test des agents individuels")
    print("=" * 60)

    from agents.content_creator_agent import ContentCreatorAgent
    from agents.email_marketing_agent import EmailMarketingAgent

    # Test agent créateur de contenu
    print("\n✍️ Test: Agent Créateur de Contenu")
    print("-" * 40)

    content_agent = ContentCreatorAgent()

    content_task = content_agent.create_task(
        task_type="create_social_post",
        priority=8,
        data={
            "platform": "linkedin",
            "topic": "Innovation en cartes d'affaires virtuelles",
            "key_points": [
                "Networking facilité et moderne",
                "Analytics en temps réel",
                "Intégration CRM complète"
            ]
        }
    )

    await content_agent.add_task(content_task)
    await content_agent.execute_tasks()
    print("✅ Contenu LinkedIn créé")

    # Test agent email marketing
    print("\n📧 Test: Agent Email Marketing")
    print("-" * 40)

    email_agent = EmailMarketingAgent()

    email_task = email_agent.create_task(
        task_type="create_email_sequence",
        priority=7,
        data={
            "type": "welcome",
            "segment": "new_users",
            "user_name": "Nouvel utilisateur iFiveMe"
        }
    )

    await email_agent.add_task(email_task)
    await email_agent.execute_tasks()
    print("✅ Séquence d'emails de bienvenue créée")

    # Arrêt des agents
    await content_agent.stop()
    await email_agent.stop()

async def demo_analytics_dashboard():
    """Démo du dashboard analytics"""
    print("\n📊 Dashboard Analytics iFiveMe")
    print("=" * 60)

    from agents.analytics_agent import AnalyticsAgent

    analytics = AnalyticsAgent()

    # Générer des données de dashboard
    dashboard_task = analytics.create_task(
        task_type="dashboard",
        priority=5,
        data={
            "type": "executive",
            "period": "30d"
        }
    )

    await analytics.add_task(dashboard_task)
    await analytics.execute_tasks()

    print("✅ Dashboard analytics généré")

    # Monitoring des KPIs
    kpi_task = analytics.create_task(
        task_type="monitor_kpis",
        priority=6,
        data={
            "categories": ["user_acquisition", "revenue"],
            "alert_level": "medium"
        }
    )

    await analytics.add_task(kpi_task)
    await analytics.execute_tasks()

    print("✅ Monitoring KPIs configuré")

    await analytics.stop()

async def run_performance_tests():
    """Tests de performance du système"""
    print("\n⚡ Tests de performance")
    print("=" * 60)

    orchestrator = MarketingOrchestrator()

    # Test de charge: créer plusieurs tâches simultanément
    tasks = []

    print("🔄 Création de 5 tâches simultanées...")

    for i in range(5):
        task = orchestrator.create_task(
            task_type="create_campaign",
            priority=5 + i,
            data={
                "type": "brand_awareness",
                "name": f"Test Campaign {i+1}",
                "budget": 1000.0,
                "channels": ["social_media"],
                "quick_test": True
            }
        )
        tasks.append(task)

    # Mesurer le temps d'exécution
    start_time = datetime.now()

    for task in tasks:
        await orchestrator.add_task(task)

    await orchestrator.execute_tasks()

    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    print(f"✅ 5 tâches exécutées en {execution_time:.2f} secondes")
    print(f"📊 Performance moyenne: {execution_time/5:.2f}s par tâche")

    await orchestrator.stop()

async def main():
    """Point d'entrée principal"""
    try:
        print("🚀 iFiveMe Marketing MVP - Système d'automatisation marketing")
        print("🎯 Le plus grand créateur de cartes d'affaires virtuelles")
        print("=" * 80)

        # Menu interactif
        while True:
            print("\n📋 Options disponibles:")
            print("1. 🎯 Démonstration complète (campagne orchestrée)")
            print("2. 🤖 Test des agents individuels")
            print("3. 📊 Dashboard analytics")
            print("4. ⚡ Tests de performance")
            print("5. 🚪 Quitter")

            choice = input("\nVotre choix (1-5): ").strip()

            if choice == "1":
                await demo_campaign_creation()
            elif choice == "2":
                await demo_individual_agents()
            elif choice == "3":
                await demo_analytics_dashboard()
            elif choice == "4":
                await run_performance_tests()
            elif choice == "5":
                print("\n👋 Merci d'avoir utilisé iFiveMe Marketing MVP!")
                break
            else:
                print("\n❌ Choix invalide, veuillez réessayer.")

    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur dans le programme principal: {str(e)}")
        print(f"\n❌ Erreur: {str(e)}")
    finally:
        print("\n🏁 Arrêt du système iFiveMe Marketing MVP")

if __name__ == "__main__":
    asyncio.run(main())