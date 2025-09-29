"""
iFiveMe Marketing MVP - Configuration Settings
Configuration centrale pour tous les agents marketing
"""

import os
from pathlib import Path

# Chemins du projet
PROJECT_ROOT = Path(__file__).parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
UTILS_DIR = PROJECT_ROOT / "utils"

# Configuration iFiveMe
COMPANY_INFO = {
    "name": "iFiveMe",
    "tagline": "Le plus grand créateur de cartes d'affaires virtuelles",
    "description": "iFiveMe révolutionne le networking avec des cartes d'affaires virtuelles innovantes et interactives.",
    "target_audience": [
        "Entrepreneurs",
        "Professionnels du marketing",
        "Freelancers",
        "Entreprises modernes",
        "Consultants"
    ],
    "value_propositions": [
        "Cartes d'affaires virtuelles professionnelles",
        "Networking digital facilité",
        "Suivi des interactions en temps réel",
        "Intégration CRM avancée",
        "Analytics détaillées"
    ]
}

# Configuration des agents
AGENTS_CONFIG = {
    "content_creator": {
        "name": "Agent Créateur de Contenu",
        "description": "Génère du contenu marketing adapté aux différents canaux",
        "capabilities": [
            "Génération de posts sociaux",
            "Création d'emails marketing",
            "Rédaction d'articles de blog",
            "Création de scripts vidéo"
        ]
    },
    "social_media_manager": {
        "name": "Agent Gestionnaire Réseaux Sociaux",
        "description": "Gère la présence sur les réseaux sociaux",
        "platforms": ["LinkedIn", "Twitter", "Facebook", "Instagram", "TikTok"],
        "capabilities": [
            "Publication automatisée",
            "Engagement avec la communauté",
            "Monitoring des mentions",
            "Analyse des performances"
        ]
    },
    "email_marketer": {
        "name": "Agent Email Marketing",
        "description": "Gère les campagnes d'email marketing",
        "capabilities": [
            "Segmentation des listes",
            "Personnalisation des messages",
            "Optimisation A/B testing",
            "Automation des séquences"
        ]
    },
    "analytics_reporter": {
        "name": "Agent Analytique et Rapports",
        "description": "Collecte et analyse les données marketing",
        "capabilities": [
            "Tracking des KPIs",
            "Génération de rapports",
            "Analyse des tendances",
            "ROI calculation"
        ]
    },
    "orchestrator": {
        "name": "Agent Orchestrateur",
        "description": "Coordonne tous les agents marketing",
        "capabilities": [
            "Planification des campagnes",
            "Coordination inter-agents",
            "Optimisation des ressources",
            "Reporting global"
        ]
    }
}

# Configuration des APIs (à remplir par l'utilisateur)
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "linkedin": os.getenv("LINKEDIN_API_KEY", ""),
    "twitter": os.getenv("TWITTER_API_KEY", ""),
    "facebook": os.getenv("FACEBOOK_API_KEY", ""),
    "mailchimp": os.getenv("MAILCHIMP_API_KEY", ""),
    "google_analytics": os.getenv("GOOGLE_ANALYTICS_KEY", ""),
    "firecrawl": "fc-9693fe7608a14ff7a988520c8ccd7020"
}

# Configuration des contenus
CONTENT_TEMPLATES = {
    "social_posts": {
        "linkedin": "Post professionnel pour LinkedIn",
        "twitter": "Tweet engageant et concis",
        "facebook": "Post communautaire Facebook",
        "instagram": "Post visuel Instagram avec hashtags"
    },
    "email_campaigns": {
        "welcome": "Email de bienvenue nouveaux utilisateurs",
        "product_update": "Annonce de nouvelles fonctionnalités",
        "engagement": "Email d'engagement utilisateurs inactifs",
        "promotion": "Offre promotionnelle limitée"
    }
}

# Configuration de scheduling
SCHEDULING = {
    "social_media": {
        "linkedin": ["09:00", "12:00", "17:00"],
        "twitter": ["08:00", "12:00", "16:00", "20:00"],
        "facebook": ["10:00", "14:00", "19:00"],
        "instagram": ["11:00", "15:00", "21:00"]
    },
    "email_campaigns": {
        "optimal_times": ["10:00", "14:00", "16:00"],
        "days": ["tuesday", "wednesday", "thursday"]
    }
}

# Configuration des KPIs
MARKETING_KPIS = {
    "social_media": [
        "followers_growth",
        "engagement_rate",
        "reach",
        "impressions",
        "clicks",
        "shares"
    ],
    "email_marketing": [
        "open_rate",
        "click_through_rate",
        "conversion_rate",
        "bounce_rate",
        "unsubscribe_rate"
    ],
    "website": [
        "traffic",
        "conversion_rate",
        "bounce_rate",
        "time_on_page",
        "lead_generation"
    ]
}

# Configuration logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "marketing_mvp.log",
            "mode": "a",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}