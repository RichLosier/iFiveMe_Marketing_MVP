# 🚀 iFiveMe Marketing MVP

**Système d'automatisation marketing complet avec subagents intelligents**

*Le plus grand créateur de cartes d'affaires virtuelles*

## 📋 Vue d'ensemble

Ce MVP fournit un système d'automatisation marketing complet pour iFiveMe, utilisant des agents spécialisés pour gérer tous les aspects du marketing digital.

### 🎯 Objectifs

- Automatiser les campagnes marketing multi-canaux
- Optimiser le ROI et les performances
- Fournir des insights et recommandations en temps réel
- Coordonner efficacement tous les canaux marketing

## 🏗️ Architecture

### 🤖 Agents Spécialisés

1. **Content Creator Agent** (`agents/content_creator_agent.py`)
   - Génération de contenu pour tous les canaux
   - Posts LinkedIn, Twitter, emails, blogs
   - Adaptation multi-plateforme intelligente

2. **Social Media Agent** (`agents/social_media_agent.py`)
   - Gestion multi-plateforme (LinkedIn, Twitter, Facebook, Instagram)
   - Engagement communautaire automatisé
   - Analytics et optimisation des performances

3. **Email Marketing Agent** (`agents/email_marketing_agent.py`)
   - Séquences d'emails automatisées
   - Segmentation avancée des contacts
   - A/B testing et optimisation

4. **Analytics Agent** (`agents/analytics_agent.py`)
   - Collecte et analyse des données
   - Attribution marketing multi-touch
   - Prévisions et recommandations

5. **Orchestrator Agent** (`agents/orchestrator_agent.py`)
   - Coordination de tous les agents
   - Gestion des campagnes complexes
   - Optimisation automatique des budgets

### 🛠️ Composants de base

- **BaseAgent** (`utils/base_agent.py`) - Classe de base pour tous les agents
- **Settings** (`config/settings.py`) - Configuration centralisée
- **Main** (`main.py`) - Point d'entrée et démonstrations

## 🚀 Installation et utilisation

### Prérequis

```bash
python 3.8+
pip install asyncio pandas openai (optionnel)
```

### Lancement

```bash
cd /Users/richardlosier/Desktop/iFiveMe_Marketing_MVP
python main.py
```

### Menu interactif

1. **Démonstration complète** - Campagne orchestrée complète
2. **Test agents individuels** - Test des agents spécialisés
3. **Dashboard analytics** - Visualisation des métriques
4. **Tests de performance** - Benchmark du système

## 🎯 Fonctionnalités clés

### 📈 Campaign Orchestration
- Création de campagnes multi-canaux
- Coordination automatique des contenus
- Optimisation en temps réel

### 🤖 Intelligence artificielle
- Génération de contenu adaptatif
- Prédictions de performance
- Recommandations automatiques

### 📊 Analytics avancées
- Tracking ROI en temps réel
- Attribution multi-touch
- Prévisions et tendances

### ⚡ Automation
- Workflows marketing automatisés
- Réponses aux crises en temps réel
- Optimisation budgétaire intelligente

## 🏢 Spécificités iFiveMe

### 🎨 Branding
- Tons professionnels mais accessibles
- Messages centrés sur l'innovation
- Ciblage entrepreneurs et professionnels

### 🎯 Marchés cibles
- Entrepreneurs québécois et canadiens
- Professionnels du networking
- PME en transformation digitale

### 💼 Propositions de valeur
- Cartes d'affaires virtuelles innovantes
- Networking digital facilité
- Analytics de networking avancées

## 📝 Configuration

### APIs (optionnelles)
```python
# config/settings.py
API_KEYS = {
    "openai": "your_openai_key",
    "linkedin": "your_linkedin_key",
    "mailchimp": "your_mailchimp_key",
    "firecrawl": "fc-9693fe7608a14ff7a988520c8ccd7020"  # Déjà configuré
}
```

### Personnalisation
- Modifier `COMPANY_INFO` dans `config/settings.py`
- Ajuster les templates de contenu
- Configurer les segments clients

## 🔍 Exemples d'utilisation

### Création d'une campagne
```python
from agents.orchestrator_agent import MarketingOrchestrator

orchestrator = MarketingOrchestrator()

campaign_task = orchestrator.create_task(
    task_type="create_campaign",
    priority=9,
    data={
        "type": "product_launch",
        "name": "Lancement iFiveMe 2.0",
        "budget": 5000.0,
        "channels": ["social_media", "email"],
        "objectives": ["Generate 1000 signups", "Achieve 4.0 ROI"]
    }
)

await orchestrator.add_task(campaign_task)
await orchestrator.execute_tasks()
```

### Génération de contenu
```python
from agents.content_creator_agent import ContentCreatorAgent

content_agent = ContentCreatorAgent()

task = content_agent.create_task(
    task_type="create_social_post",
    priority=8,
    data={
        "platform": "linkedin",
        "topic": "Innovation cartes virtuelles",
        "key_points": ["Networking facilité", "Analytics temps réel"]
    }
)

await content_agent.add_task(task)
await content_agent.execute_tasks()
```

## 📊 Métriques et KPIs

### KPIs principaux
- **CAC** (Customer Acquisition Cost)
- **LTV** (Lifetime Value)
- **ROI/ROAS** (Return on Investment/Ad Spend)
- **Taux de conversion**
- **Engagement rate**

### Alertes automatiques
- ROI en dessous du seuil (200%)
- CAC supérieur à 30% du LTV
- Baisse de conversion > 20%

## 🚨 Gestion de crise

Le système détecte et gère automatiquement:
- Sentiment négatif sur les réseaux sociaux
- Dépassement de budget
- Chute des performances
- Problèmes techniques

## 🔄 Workflows automatisés

### Séquence de bienvenue
1. Email immédiat de bienvenue
2. Conseils d'utilisation (J+3)
3. Statistiques personnalisées (J+7)
4. Upgrade premium (J+14)

### Optimisation continue
1. Monitoring des performances 24/7
2. Réallocation budgétaire automatique
3. A/B testing permanent
4. Rapports hebdomadaires automatisés

## 🤝 Support et contribution

### Structure des fichiers
```
iFiveMe_Marketing_MVP/
├── agents/                 # Agents spécialisés
├── config/                 # Configuration
├── data/                   # Données et résultats
├── logs/                   # Logs système
├── utils/                  # Utilitaires
├── main.py                 # Point d'entrée
└── README.md              # Documentation
```

### Logs et debugging
- Logs détaillés dans `/logs/marketing_mvp.log`
- Résultats des tâches sauvés dans `/data/`
- Health checks automatiques

## 🎉 Démo et test

Le système inclut des données simulées réalistes pour tester toutes les fonctionnalités sans APIs externes. Parfait pour:

- Démonstrations clients
- Tests de performance
- Développement et itération
- Formation des équipes

---

**🚀 iFiveMe - Révolutionner le networking professionnel avec l'IA marketing**