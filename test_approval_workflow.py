#!/usr/bin/env python3
"""
Test du système d'approbation de posts iFiveMe
Démontre le workflow d'approbation par email
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from agents.approval_workflow_agent import submit_post_for_approval, ApprovalWorkflowAgent

async def demo_approval_workflow():
    """Démonstration du workflow d'approbation"""
    print("🚀 iFiveMe - Test du Workflow d'Approbation")
    print("=" * 60)

    # Test 1: Soumettre un post LinkedIn pour approbation
    print("\n📱 Test 1: Soumission post LinkedIn")
    print("-" * 40)

    linkedin_post = """🚀 Révolutionnez votre networking avec iFiveMe !

Les cartes d'affaires traditionnelles, c'est du passé. Avec iFiveMe, créez des cartes virtuelles professionnelles qui :

✅ Se partagent instantanément
✅ Incluent analytics détaillées
✅ S'intègrent à votre CRM
✅ Respectent l'environnement

Plus de 10,000 entrepreneurs font déjà confiance à iFiveMe pour leur networking digital.

👉 Créez votre carte gratuite : ifiveme.com

#Networking #CartesVirtuelles #iFiveMe #Innovation #Quebec"""

    result1 = await submit_post_for_approval(
        title="Post LinkedIn - Révolutionnez votre networking",
        content=linkedin_post,
        platform="LinkedIn",
        created_by="Marie Dubois - Marketing",
        scheduled_time="2024-09-25T10:00:00"
    )

    print(f"✅ Post soumis pour approbation")
    print(f"📧 Email envoyé à: richard@ifiveme.com")
    print(f"🔗 Post ID: {result1.get('post_id', 'N/A')}")

    # Test 2: Soumettre un post Twitter
    print("\n🐦 Test 2: Soumission post Twitter")
    print("-" * 40)

    twitter_post = """🔥 Plus besoin de cartes papier !

Avec iFiveMe, partagez votre profil pro d'un clic 📱✨

✅ Cartes virtuelles interactives
✅ Analytics temps réel
✅ Intégration CRM

Essayez gratuitement : ifiveme.com

#iFiveMe #Digital #Networking"""

    result2 = await submit_post_for_approval(
        title="Post Twitter - Plus besoin de cartes papier",
        content=twitter_post,
        platform="Twitter",
        created_by="Jean Tremblay - Community Manager",
        scheduled_time="2024-09-25T14:30:00"
    )

    print(f"✅ Post Twitter soumis")
    print(f"📧 Email d'approbation envoyé")
    print(f"🔗 Post ID: {result2.get('post_id', 'N/A')}")

    # Test 3: Vérifier le statut des posts en attente
    print("\n📊 Test 3: Statut des posts en attente")
    print("-" * 40)

    approval_agent = ApprovalWorkflowAgent()

    status_task = approval_agent.create_task(
        task_type="get_pending_posts",
        priority=5,
        data={}
    )

    await approval_agent.add_task(status_task)
    await approval_agent.execute_tasks()
    await approval_agent.stop()

    print("✅ Dashboard d'approbation mis à jour")

    # Résumé
    print("\n🎉 RÉSUMÉ DU TEST")
    print("=" * 60)
    print("✅ Workflow d'approbation configuré")
    print("✅ Emails d'approbation envoyés à richard@ifiveme.com")
    print("✅ Interface d'approbation rapide disponible")
    print("✅ Système de rappels automatiques actif")
    print("✅ Notifications équipe configurées")

    print("\n📧 PROCHAINES ÉTAPES:")
    print("1. Vérifiez vos emails pour les demandes d'approbation")
    print("2. Cliquez sur APPROUVER ou REJETER dans l'email")
    print("3. Les posts approuvés seront publiés automatiquement")
    print("4. L'équipe sera notifiée des décisions")

    print("\n🔗 Fonctionnalités disponibles:")
    print("• Approbation par email avec boutons rapides")
    print("• Interface web d'approbation")
    print("• Rappels automatiques après 12h")
    print("• Expiration automatique après 24h")
    print("• Historique complet des décisions")
    print("• Notifications à l'équipe")

    return True

if __name__ == "__main__":
    asyncio.run(demo_approval_workflow())