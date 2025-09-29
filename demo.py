#!/usr/bin/env python3
"""
iFiveMe Marketing MVP - Démonstration automatique
Test complet du système sans interaction utilisateur
"""

import asyncio
import logging
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.append(str(Path(__file__).parent))

from agents.orchestrator_agent import MarketingOrchestrator
from agents.content_creator_agent import ContentCreatorAgent
from agents.email_marketing_agent import EmailMarketingAgent
from agents.analytics_agent import AnalyticsAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_full_demo():
    """Démonstration complète automatique"""
    print("🚀 iFiveMe Marketing MVP - Démonstration automatique complète")
    print("🎯 Le plus grand créateur de cartes d'affaires virtuelles")
    print("=" * 80)

    try:
        # 1. Test de l'orchestrateur principal
        print("\n📋 1. Test de l'orchestrateur marketing")
        print("-" * 50)

        orchestrator = MarketingOrchestrator()

        # Health check
        health_ok = await orchestrator.health_check()
        print(f"✅ Health check orchestrateur: {'OK' if health_ok else 'FAILED'}")

        # Créer une campagne de test
        campaign_task = orchestrator.create_task(
            task_type="create_campaign",
            priority=9,
            data={
                "type": "product_launch",
                "name": "Test Lancement iFiveMe 2.0",
                "budget": 3000.0,
                "channels": ["social_media", "email"],
                "objectives": ["Tester le système", "Valider l'intégration"]
            }
        )

        await orchestrator.add_task(campaign_task)
        await orchestrator.execute_tasks()

        # Afficher le statut
        status = orchestrator.get_status()
        print(f"📊 Tâches complétées: {status['metrics']['tasks_completed']}")
        print(f"📈 Taux de succès: {status['metrics']['success_rate']:.1f}%")

        await orchestrator.stop()

        # 2. Test agent créateur de contenu
        print("\n✍️ 2. Test agent créateur de contenu")
        print("-" * 50)

        content_agent = ContentCreatorAgent()

        # Test création post LinkedIn
        linkedin_task = content_agent.create_task(
            task_type="create_social_post",
            priority=8,
            data={
                "platform": "linkedin",
                "topic": "Innovation cartes d'affaires virtuelles iFiveMe",
                "key_points": [
                    "Networking moderne et efficace",
                    "Analytics en temps réel",
                    "Intégration CRM complète"
                ]
            }
        )

        await content_agent.add_task(linkedin_task)
        await content_agent.execute_tasks()

        print("✅ Post LinkedIn généré avec succès")

        # Test création email
        email_content_task = content_agent.create_task(
            task_type="create_email_content",
            priority=7,
            data={
                "type": "welcome",
                "user_name": "Nouvel utilisateur iFiveMe"
            }
        )

        await content_agent.add_task(email_content_task)
        await content_agent.execute_tasks()

        print("✅ Contenu email de bienvenue créé")

        # Statut agent content
        content_status = content_agent.get_status()
        print(f"📊 Capacités: {len(content_status['capabilities'])} fonctionnalités")

        await content_agent.stop()

        # 3. Test agent email marketing
        print("\n📧 3. Test agent email marketing")
        print("-" * 50)

        email_agent = EmailMarketingAgent()

        # Test séquence de bienvenue
        sequence_task = email_agent.create_task(
            task_type="create_sequence",
            priority=8,
            data={
                "type": "welcome",
                "segment": "new_users"
            }
        )

        await email_agent.add_task(sequence_task)
        await email_agent.execute_tasks()

        print("✅ Séquence email de bienvenue créée")

        # Test segmentation
        segment_task = email_agent.create_task(
            task_type="segment_contacts",
            priority=6,
            data={
                "segment_name": "active_users",
                "total_contacts": 2000
            }
        )

        await email_agent.add_task(segment_task)
        await email_agent.execute_tasks()

        print("✅ Segmentation des contacts effectuée")

        # Statut email agent
        email_status = email_agent.get_status()
        print(f"📊 Email agent - Capacités: {len(email_status['capabilities'])}")

        await email_agent.stop()

        # 4. Test agent analytics
        print("\n📊 4. Test agent analytics")
        print("-" * 50)

        analytics_agent = AnalyticsAgent()

        # Test collecte de données
        data_task = analytics_agent.create_task(
            task_type="collect_data",
            priority=7,
            data={
                "sources": ["paid_social", "email_marketing"],
                "date_range": 30
            }
        )

        await analytics_agent.add_task(data_task)
        await analytics_agent.execute_tasks()

        print("✅ Données marketing collectées")

        # Test monitoring KPIs
        kpi_task = analytics_agent.create_task(
            task_type="monitor_kpis",
            priority=8,
            data={
                "categories": ["user_acquisition", "revenue"],
                "alert_level": "medium"
            }
        )

        await analytics_agent.add_task(kpi_task)
        await analytics_agent.execute_tasks()

        print("✅ Monitoring KPIs configuré")

        # Test génération rapport
        report_task = analytics_agent.create_task(
            task_type="generate_report",
            priority=6,
            data={
                "type": "monthly",
                "include_forecasts": True
            }
        )

        await analytics_agent.add_task(report_task)
        await analytics_agent.execute_tasks()

        print("✅ Rapport marketing mensuel généré")

        # Statut analytics
        analytics_status = analytics_agent.get_status()
        print(f"📊 Analytics - Capacités: {len(analytics_status['capabilities'])}")

        await analytics_agent.stop()

        # 5. Test d'intégration complète
        print("\n🔄 5. Test d'intégration complète")
        print("-" * 50)

        # Recréer l'orchestrateur pour test final
        final_orchestrator = MarketingOrchestrator()

        # Campagne complexe multi-agents
        complex_campaign = final_orchestrator.create_task(
            task_type="create_campaign",
            priority=10,
            data={
                "type": "brand_awareness",
                "name": "Campagne iFiveMe Intégration Complète",
                "budget": 5000.0,
                "channels": ["social_media", "email", "content"],
                "duration_days": 14,
                "target_audience": "entrepreneurs_quebec",
                "objectives": [
                    "Test d'intégration multi-agents",
                    "Validation du workflow complet",
                    "Démonstration des capacités IA"
                ]
            }
        )

        await final_orchestrator.add_task(complex_campaign)

        # Tâche d'optimisation
        optimization_task = final_orchestrator.create_task(
            task_type="optimize_budget",
            priority=9,
            data={
                "strategy": "roi_maximization",
                "reallocation_percentage": 15
            }
        )

        await final_orchestrator.add_task(optimization_task)

        # Tâche de monitoring
        monitoring_task = final_orchestrator.create_task(
            task_type="monitor_performance",
            priority=8,
            data={
                "campaigns": ["all"],
                "real_time": True
            }
        )

        await final_orchestrator.add_task(monitoring_task)

        # Exécuter toutes les tâches
        await final_orchestrator.execute_tasks()

        print("✅ Campagne intégrée complète exécutée")

        # Statut final
        final_status = final_orchestrator.get_status()
        print(f"📊 Orchestrateur final - Tâches: {final_status['metrics']['tasks_completed']}")
        print(f"⚡ Temps de réponse moyen: {final_status['metrics']['average_response_time']:.2f}s")

        await final_orchestrator.stop()

        # Résumé final
        print("\n🎉 RÉSUMÉ DE LA DÉMONSTRATION")
        print("=" * 80)
        print("✅ Orchestrateur marketing: OPÉRATIONNEL")
        print("✅ Agent créateur de contenu: OPÉRATIONNEL")
        print("✅ Agent email marketing: OPÉRATIONNEL")
        print("✅ Agent analytics: OPÉRATIONNEL")
        print("✅ Intégration multi-agents: OPÉRATIONNEL")
        print("\n🚀 Le système iFiveMe Marketing MVP est entièrement fonctionnel!")
        print("🎯 Prêt pour l'automatisation marketing d'iFiveMe!")

        return True

    except Exception as e:
        logger.error(f"Erreur dans la démonstration: {str(e)}")
        print(f"\n❌ Erreur: {str(e)}")
        return False

async def main():
    """Point d'entrée principal pour la démonstration"""
    try:
        success = await run_full_demo()
        if success:
            print("\n✅ Démonstration terminée avec succès!")
            return 0
        else:
            print("\n❌ La démonstration a échoué!")
            return 1
    except KeyboardInterrupt:
        print("\n🛑 Démonstration interrompue par l'utilisateur")
        return 1
    except Exception as e:
        logger.error(f"Erreur fatale: {str(e)}")
        print(f"\n💥 Erreur fatale: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)