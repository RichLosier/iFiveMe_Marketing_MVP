"""
iFiveMe Marketing MVP - Agent Créateur de Contenu
Génère du contenu marketing adapté aux différents canaux
"""

import openai
import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.base_agent import BaseAgent, AgentTask
from config.settings import COMPANY_INFO, CONTENT_TEMPLATES, API_KEYS

class ContentCreatorAgent(BaseAgent):
    """Agent spécialisé dans la création de contenu marketing pour iFiveMe"""

    def __init__(self):
        super().__init__(
            agent_id="content_creator",
            name="Agent Créateur de Contenu iFiveMe",
            config={
                "max_tokens": 2000,
                "temperature": 0.7,
                "content_types": ["social_post", "email", "blog_article", "video_script", "ad_copy"]
            }
        )

        # Configuration OpenAI
        if API_KEYS.get("openai"):
            openai.api_key = API_KEYS["openai"]

        # Templates de contenu spécialisés iFiveMe
        self.ifiveme_templates = {
            "social_post_linkedin": """
Créez un post LinkedIn professionnel pour iFiveMe qui :
- Met en avant notre expertise en cartes d'affaires virtuelles
- Utilise un ton professionnel mais accessible
- Inclut un appel à l'action engageant
- Utilise des hashtags pertinents (#networking #digitalbusiness #virtualcards)
- Maximum 1300 caractères

Sujet: {topic}
Points clés: {key_points}
""",
            "social_post_twitter": """
Créez un tweet accrocheur pour iFiveMe qui :
- Capture l'attention en maximum 280 caractères
- Met en avant un avantage clé des cartes virtuelles
- Utilise 2-3 hashtags pertinents
- Inclut un appel à l'action

Sujet: {topic}
Message clé: {key_message}
""",
            "email_welcome": """
Rédigez un email de bienvenue pour les nouveaux utilisateurs iFiveMe :
- Ton chaleureux et professionnel
- Présentation des fonctionnalités clés
- Guide de démarrage rapide
- Support et ressources disponibles
- Appel à l'action pour créer leur première carte

Personnalisation: {user_name}
Fonctionnalités à mettre en avant: {features}
""",
            "blog_article": """
Rédigez un article de blog pour iFiveMe sur le sujet : {topic}
- Structure : Introduction, 3-4 sections principales, conclusion
- Ton expert mais accessible
- Inclure des exemples concrets d'usage
- SEO optimisé avec mots-clés : {keywords}
- 800-1200 mots
- Call-to-action vers iFiveMe

Points à couvrir: {points}
""",
            "ad_copy": """
Créez une publicité persuasive pour iFiveMe :
- Accroche puissante
- Bénéfices clairs pour l'utilisateur
- Preuve sociale ou statistiques
- Appel à l'action irrésistible
- Format : {format} (Facebook/Google/LinkedIn)

Audience cible: {target_audience}
Objectif: {objective}
""",
            "video_script": """
Écrivez un script vidéo pour iFiveMe :
- Durée cible: {duration}
- Ton: {tone}
- Hook dans les 3 premières secondes
- Démonstration claire du produit
- Bénéfices utilisateurs
- Call-to-action final

Sujet: {topic}
Messages clés: {key_messages}
"""
        }

    def get_capabilities(self) -> List[str]:
        return [
            "Génération de posts LinkedIn professionnels",
            "Création de tweets engageants",
            "Rédaction d'emails marketing personnalisés",
            "Écriture d'articles de blog SEO",
            "Création de copies publicitaires",
            "Écriture de scripts vidéo",
            "Adaptation de contenu multi-plateforme",
            "Optimisation pour différentes audiences"
        ]

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite les tâches de création de contenu"""
        task_type = task.type
        data = task.data

        if task_type == "create_social_post":
            return await self._create_social_post(data)
        elif task_type == "create_email_content":
            return await self._create_email_content(data)
        elif task_type == "create_blog_article":
            return await self._create_blog_article(data)
        elif task_type == "create_ad_copy":
            return await self._create_ad_copy(data)
        elif task_type == "create_video_script":
            return await self._create_video_script(data)
        elif task_type == "adapt_content":
            return await self._adapt_content(data)
        else:
            raise ValueError(f"Type de tâche non supporté: {task_type}")

    async def _create_social_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un post pour les réseaux sociaux"""
        platform = data.get("platform", "linkedin")
        topic = data.get("topic", "Innovation en cartes d'affaires virtuelles")
        key_points = data.get("key_points", [
            "Networking facilité",
            "Suivi en temps réel",
            "Intégration CRM"
        ])

        if platform == "linkedin":
            template = self.ifiveme_templates["social_post_linkedin"]
            prompt = template.format(
                topic=topic,
                key_points=", ".join(key_points)
            )
        elif platform == "twitter":
            template = self.ifiveme_templates["social_post_twitter"]
            key_message = data.get("key_message", key_points[0] if key_points else "Révolutionnez votre networking")
            prompt = template.format(
                topic=topic,
                key_message=key_message
            )
        else:
            prompt = f"Créez un post {platform} pour iFiveMe sur le sujet: {topic}. Points clés: {', '.join(key_points)}"

        content = await self._generate_content(prompt)

        return {
            "platform": platform,
            "content": content,
            "topic": topic,
            "hashtags": self._extract_hashtags(content),
            "estimated_reach": self._estimate_reach(platform, content),
            "optimal_posting_time": self._get_optimal_posting_time(platform)
        }

    async def _create_email_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée le contenu d'un email marketing"""
        email_type = data.get("type", "welcome")
        user_name = data.get("user_name", "Cher utilisateur")
        features = data.get("features", [
            "Création rapide de cartes",
            "Partage instantané",
            "Analytics avancées"
        ])

        if email_type == "welcome":
            template = self.ifiveme_templates["email_welcome"]
            prompt = template.format(
                user_name=user_name,
                features=", ".join(features)
            )
        else:
            prompt = f"Créez un email {email_type} pour iFiveMe destiné à {user_name}"

        content = await self._generate_content(prompt)

        return {
            "type": email_type,
            "subject": self._generate_email_subject(email_type, content),
            "content": content,
            "personalization_fields": ["user_name", "company"],
            "cta_buttons": self._extract_cta_buttons(content),
            "estimated_open_rate": self._estimate_email_metrics(email_type)["open_rate"],
            "estimated_click_rate": self._estimate_email_metrics(email_type)["click_rate"]
        }

    async def _create_blog_article(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un article de blog"""
        topic = data.get("topic", "L'avenir du networking digital avec les cartes virtuelles")
        keywords = data.get("keywords", ["cartes virtuelles", "networking", "business digital"])
        points = data.get("points", [
            "Évolution du networking traditionnel",
            "Avantages des cartes virtuelles",
            "Impact sur les relations d'affaires"
        ])

        template = self.ifiveme_templates["blog_article"]
        prompt = template.format(
            topic=topic,
            keywords=", ".join(keywords),
            points=", ".join(points)
        )

        content = await self._generate_content(prompt)

        return {
            "title": topic,
            "content": content,
            "keywords": keywords,
            "meta_description": self._generate_meta_description(content),
            "reading_time": self._calculate_reading_time(content),
            "seo_score": self._calculate_seo_score(content, keywords)
        }

    async def _create_ad_copy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une copie publicitaire"""
        format_type = data.get("format", "facebook")
        target_audience = data.get("target_audience", "Entrepreneurs et professionnels")
        objective = data.get("objective", "Générer des inscriptions")

        template = self.ifiveme_templates["ad_copy"]
        prompt = template.format(
            format=format_type,
            target_audience=target_audience,
            objective=objective
        )

        content = await self._generate_content(prompt)

        return {
            "format": format_type,
            "headline": self._extract_headline(content),
            "body": content,
            "cta": self._extract_cta(content),
            "target_audience": target_audience,
            "estimated_ctr": self._estimate_ad_ctr(format_type),
            "budget_recommendation": self._recommend_budget(format_type, objective)
        }

    async def _create_video_script(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un script vidéo"""
        duration = data.get("duration", "60 secondes")
        tone = data.get("tone", "professionnel et énergique")
        topic = data.get("topic", "Démonstration iFiveMe")
        key_messages = data.get("key_messages", [
            "Simplicité d'utilisation",
            "Fonctionnalités innovantes",
            "ROI mesurable"
        ])

        template = self.ifiveme_templates["video_script"]
        prompt = template.format(
            duration=duration,
            tone=tone,
            topic=topic,
            key_messages=", ".join(key_messages)
        )

        content = await self._generate_content(prompt)

        return {
            "title": topic,
            "script": content,
            "duration": duration,
            "tone": tone,
            "scenes": self._extract_scenes(content),
            "production_notes": self._generate_production_notes(content)
        }

    async def _adapt_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Adapte du contenu existant pour différentes plateformes"""
        original_content = data.get("content", "")
        target_platform = data.get("target_platform", "linkedin")
        source_platform = data.get("source_platform", "blog")

        prompt = f"""
Adaptez ce contenu iFiveMe du format {source_platform} vers {target_platform}:

Contenu original:
{original_content}

Instructions:
- Gardez le message principal
- Adaptez le ton et la longueur pour {target_platform}
- Ajoutez les hashtags appropriés
- Incluez un call-to-action adapté
"""

        adapted_content = await self._generate_content(prompt)

        return {
            "original_platform": source_platform,
            "target_platform": target_platform,
            "adapted_content": adapted_content,
            "changes_made": self._analyze_adaptations(original_content, adapted_content),
            "optimization_score": self._score_adaptation(target_platform, adapted_content)
        }

    async def _generate_content(self, prompt: str) -> str:
        """Génère le contenu via OpenAI"""
        try:
            if not API_KEYS.get("openai"):
                # Mode simulation si pas d'API key
                return self._generate_mock_content(prompt)

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"Vous êtes un expert en marketing digital spécialisé dans iFiveMe, {COMPANY_INFO['tagline']}. Créez du contenu professionnel, engageant et aligné avec la marque iFiveMe."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.config["max_tokens"],
                    temperature=self.config["temperature"]
                )
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Erreur génération contenu: {str(e)}")
            return self._generate_mock_content(prompt)

    def _generate_mock_content(self, prompt: str) -> str:
        """Génère du contenu mock pour les tests"""
        if "linkedin" in prompt.lower():
            return """🚀 Révolutionnez votre networking avec iFiveMe !

Les cartes d'affaires traditionnelles appartiennent au passé. Avec iFiveMe, créez des cartes virtuelles interactives qui :

✅ Se partagent instantanément
✅ Incluent vos réseaux sociaux et portfolio
✅ Offrent des analytics détaillées
✅ S'intègrent à votre CRM

Rejoignez les milliers de professionnels qui ont déjà modernisé leur networking !

👉 Créez votre première carte gratuite : iFiveMe.com

#Networking #CartesVirtuelles #DigitalBusiness #Innovation #iFiveMe"""

        elif "twitter" in prompt.lower():
            return """🔥 Plus besoin de cartes papier ! Avec iFiveMe, partagez votre profil professionnel d'un simple clic 📱✨

✅ Cartes virtuelles interactives
✅ Analytics en temps réel
✅ Intégration CRM

Essayez gratuitement : iFiveMe.com

#Networking #Digital #Innovation"""

        elif "email" in prompt.lower():
            return """Objet : Bienvenue dans l'avenir du networking ! 🚀

Bonjour [Prénom],

Félicitations ! Vous venez de rejoindre iFiveMe, la plateforme qui révolutionne les cartes d'affaires.

Voici ce que vous pouvez faire dès maintenant :

🎯 Créer votre première carte virtuelle en 3 minutes
📊 Suivre vos interactions en temps réel
🔗 Intégrer vos réseaux sociaux et portfolio
📈 Analyser l'efficacité de votre networking

Pour commencer, cliquez simplement sur "Créer ma carte" dans votre tableau de bord.

Besoin d'aide ? Notre équipe support est là pour vous : support@ifiveme.com

Excellente journée,
L'équipe iFiveMe

P.S. : Suivez nos conseils networking sur LinkedIn @iFiveMe"""

        else:
            return """Contenu iFiveMe généré automatiquement.

iFiveMe révolutionne le networking professionnel avec des cartes d'affaires virtuelles innovantes.

Notre plateforme permet aux professionnels de créer, partager et analyser leurs interactions de networking de manière moderne et efficace.

Rejoignez la révolution digitale du networking avec iFiveMe !"""

    # Méthodes utilitaires
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extrait les hashtags du contenu"""
        import re
        return re.findall(r'#\w+', content)

    def _estimate_reach(self, platform: str, content: str) -> Dict[str, int]:
        """Estime la portée du contenu"""
        base_reach = {
            "linkedin": 500,
            "twitter": 300,
            "facebook": 200,
            "instagram": 400
        }

        # Facteurs d'engagement
        engagement_boost = len(self._extract_hashtags(content)) * 10

        return {
            "estimated_reach": base_reach.get(platform, 250) + engagement_boost,
            "potential_impressions": (base_reach.get(platform, 250) + engagement_boost) * 3
        }

    def _get_optimal_posting_time(self, platform: str) -> str:
        """Retourne le meilleur moment pour poster"""
        optimal_times = {
            "linkedin": "09:00 - 10:00 en semaine",
            "twitter": "12:00 - 15:00",
            "facebook": "13:00 - 16:00",
            "instagram": "11:00 - 13:00 et 17:00 - 19:00"
        }
        return optimal_times.get(platform, "10:00 - 14:00")

    def _generate_email_subject(self, email_type: str, content: str) -> str:
        """Génère un objet d'email"""
        subjects = {
            "welcome": "Bienvenue chez iFiveMe ! Créez votre première carte 🚀",
            "product_update": "Nouvelles fonctionnalités iFiveMe disponibles !",
            "engagement": "Votre carte iFiveMe vous attend...",
            "promotion": "Offre exclusive iFiveMe - 48h seulement !"
        }
        return subjects.get(email_type, "Actualités iFiveMe")

    def _extract_cta_buttons(self, content: str) -> List[str]:
        """Extrait les boutons d'appel à l'action"""
        cta_patterns = [
            "Créer ma carte",
            "Essayer gratuitement",
            "En savoir plus",
            "Commencer maintenant",
            "Découvrir iFiveMe"
        ]
        found_ctas = []
        for cta in cta_patterns:
            if cta.lower() in content.lower():
                found_ctas.append(cta)
        return found_ctas if found_ctas else ["Découvrir iFiveMe"]

    def _estimate_email_metrics(self, email_type: str) -> Dict[str, float]:
        """Estime les métriques email"""
        metrics = {
            "welcome": {"open_rate": 45.0, "click_rate": 12.0},
            "product_update": {"open_rate": 35.0, "click_rate": 8.0},
            "engagement": {"open_rate": 25.0, "click_rate": 6.0},
            "promotion": {"open_rate": 40.0, "click_rate": 15.0}
        }
        return metrics.get(email_type, {"open_rate": 30.0, "click_rate": 8.0})

    def _generate_meta_description(self, content: str) -> str:
        """Génère une méta-description"""
        # Prendre les 150 premiers caractères du contenu nettoyé
        clean_content = content.replace('\n', ' ').strip()
        return clean_content[:147] + "..." if len(clean_content) > 150 else clean_content

    def _calculate_reading_time(self, content: str) -> str:
        """Calcule le temps de lecture"""
        word_count = len(content.split())
        minutes = max(1, round(word_count / 200))  # 200 mots par minute
        return f"{minutes} minute{'s' if minutes > 1 else ''}"

    def _calculate_seo_score(self, content: str, keywords: List[str]) -> int:
        """Calcule un score SEO basique"""
        score = 70  # Score de base

        content_lower = content.lower()
        for keyword in keywords:
            if keyword.lower() in content_lower:
                score += 5

        # Bonus si bon nombre de mots
        word_count = len(content.split())
        if 800 <= word_count <= 1200:
            score += 10

        return min(100, score)

    def _extract_headline(self, content: str) -> str:
        """Extrait le titre principal"""
        lines = content.split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) > 10:
                return line.strip()
        return "Découvrez iFiveMe"

    def _extract_cta(self, content: str) -> str:
        """Extrait le call-to-action principal"""
        cta_indicators = ["cliquez", "découvrez", "essayez", "créez", "commencez"]
        lines = content.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in cta_indicators):
                return line.strip()
        return "Découvrir iFiveMe"

    def _estimate_ad_ctr(self, format_type: str) -> float:
        """Estime le taux de clic publicitaire"""
        ctrs = {
            "facebook": 1.2,
            "google": 2.1,
            "linkedin": 0.8,
            "instagram": 1.0
        }
        return ctrs.get(format_type, 1.0)

    def _recommend_budget(self, format_type: str, objective: str) -> Dict[str, Any]:
        """Recommande un budget publicitaire"""
        base_budgets = {
            "facebook": {"min": 50, "recommended": 150, "max": 500},
            "google": {"min": 100, "recommended": 300, "max": 1000},
            "linkedin": {"min": 100, "recommended": 250, "max": 800}
        }

        budget = base_budgets.get(format_type, {"min": 50, "recommended": 150, "max": 500})

        if "inscription" in objective.lower():
            # Augmenter le budget pour les conversions
            budget = {k: int(v * 1.5) for k, v in budget.items()}

        return budget

    def _extract_scenes(self, script: str) -> List[Dict[str, str]]:
        """Extrait les scènes du script vidéo"""
        scenes = []
        lines = script.split('\n')
        current_scene = {"timestamp": "0:00", "action": "", "dialogue": ""}

        for line in lines:
            if "scène" in line.lower() or ":" in line:
                if current_scene["action"] or current_scene["dialogue"]:
                    scenes.append(current_scene.copy())
                current_scene = {"timestamp": "0:00", "action": line.strip(), "dialogue": ""}
            else:
                current_scene["dialogue"] += line.strip() + " "

        if current_scene["action"] or current_scene["dialogue"]:
            scenes.append(current_scene)

        return scenes[:5]  # Limiter à 5 scènes

    def _generate_production_notes(self, script: str) -> List[str]:
        """Génère des notes de production"""
        return [
            "Utiliser l'identité visuelle iFiveMe",
            "Inclure des démonstrations écran",
            "Musique de fond professionnelle",
            "Call-to-action visible à l'écran",
            "Logo iFiveMe en filigrane"
        ]

    def _analyze_adaptations(self, original: str, adapted: str) -> List[str]:
        """Analyse les changements apportés lors de l'adaptation"""
        changes = []

        if len(adapted) < len(original) * 0.7:
            changes.append("Contenu raccourci pour la plateforme")
        if "#" in adapted and "#" not in original:
            changes.append("Hashtags ajoutés")
        if "👉" in adapted or "🚀" in adapted:
            changes.append("Émojis ajoutés pour l'engagement")

        return changes

    def _score_adaptation(self, platform: str, content: str) -> int:
        """Score l'adaptation pour une plateforme"""
        score = 70

        if platform == "linkedin":
            if len(content) < 1300:
                score += 10
            if "#" in content:
                score += 10
        elif platform == "twitter":
            if len(content) <= 280:
                score += 15
            if content.count("#") <= 3:
                score += 10

        return min(100, score)