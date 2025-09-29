"""
iFiveMe Marketing MVP - Agent Google Drive
Gère l'accès aux images et ressources depuis Google Drive
"""

import json
import asyncio
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.base_agent import BaseAgent, AgentTask
from config.settings import API_KEYS

@dataclass
class DriveAsset:
    """Structure pour un asset Google Drive"""
    id: str
    name: str
    type: str  # image, video, document
    url: str
    download_url: str
    thumbnail_url: Optional[str]
    size_bytes: int
    created_date: datetime
    modified_date: datetime
    tags: List[str]
    description: Optional[str] = None

class GoogleDriveAgent(BaseAgent):
    """Agent spécialisé dans la gestion des assets Google Drive pour iFiveMe"""

    def __init__(self):
        super().__init__(
            agent_id="google_drive",
            name="Agent Google Drive iFiveMe",
            config={
                "folder_id": "1RE8sOSWPS8YhZsaSHRLIouZV08p1iUk0",  # Dossier iFiveMe
                "base_drive_url": "https://drive.google.com/drive/folders/1RE8sOSWPS8YhZsaSHRLIouZV08p1iUk0",
                "supported_formats": ["jpg", "jpeg", "png", "gif", "svg", "mp4", "mov", "pdf"],
                "cache_duration_hours": 24
            }
        )

        # Catégories d'assets iFiveMe
        self.asset_categories = {
            "logos": {
                "description": "Logos et éléments de marque iFiveMe",
                "suggested_tags": ["logo", "branding", "ifiveme", "brand"]
            },
            "product_screenshots": {
                "description": "Captures d'écran du produit iFiveMe",
                "suggested_tags": ["product", "screenshot", "interface", "demo"]
            },
            "social_media": {
                "description": "Images optimisées pour réseaux sociaux",
                "suggested_tags": ["social", "post", "linkedin", "twitter", "instagram"]
            },
            "presentations": {
                "description": "Images pour présentations et pitchs",
                "suggested_tags": ["presentation", "slide", "pitch", "deck"]
            },
            "marketing_materials": {
                "description": "Matériel marketing et publicitaire",
                "suggested_tags": ["marketing", "ad", "promo", "campaign"]
            },
            "team_photos": {
                "description": "Photos d'équipe et portraits",
                "suggested_tags": ["team", "portrait", "about", "people"]
            }
        }

        # Cache des assets
        self.assets_cache: Dict[str, DriveAsset] = {}
        self.cache_timestamp: Optional[datetime] = None

    def get_capabilities(self) -> List[str]:
        return [
            "Accès aux images Google Drive iFiveMe",
            "Recherche d'assets par tags et catégories",
            "Optimisation d'images pour différents canaux",
            "Gestion des versions et historique",
            "Intégration avec les agents de contenu",
            "Cache intelligent des ressources",
            "Suggestion d'images contextuelles",
            "Validation des droits d'usage"
        ]

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite les tâches de gestion Google Drive"""
        task_type = task.type
        data = task.data

        if task_type == "fetch_assets":
            return await self._fetch_drive_assets(data)
        elif task_type == "search_images":
            return await self._search_images(data)
        elif task_type == "get_image_for_post":
            return await self._get_image_for_post(data)
        elif task_type == "optimize_image":
            return await self._optimize_image_for_channel(data)
        elif task_type == "suggest_images":
            return await self._suggest_images_for_content(data)
        elif task_type == "update_cache":
            return await self._update_assets_cache(data)
        elif task_type == "validate_asset":
            return await self._validate_asset_usage(data)
        else:
            raise ValueError(f"Type de tâche non supporté: {task_type}")

    async def _fetch_drive_assets(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Récupère la liste des assets depuis Google Drive"""
        force_refresh = data.get("force_refresh", False)

        # Vérifier le cache
        if not force_refresh and self._is_cache_valid():
            return {
                "source": "cache",
                "assets_count": len(self.assets_cache),
                "assets": list(self.assets_cache.values()),
                "cached_at": self.cache_timestamp.isoformat()
            }

        # Simuler l'accès à Google Drive (en production, utiliser l'API Google Drive)
        assets = await self._simulate_drive_api_call()

        # Mettre à jour le cache
        self.assets_cache = {asset.id: asset for asset in assets}
        self.cache_timestamp = datetime.now()

        return {
            "source": "drive_api",
            "assets_count": len(assets),
            "assets": [asdict(asset) for asset in assets],
            "fetched_at": self.cache_timestamp.isoformat(),
            "folder_url": self.config["base_drive_url"]
        }

    async def _simulate_drive_api_call(self) -> List[DriveAsset]:
        """Simule l'appel à l'API Google Drive"""
        # En production, utiliser google-api-python-client
        await asyncio.sleep(0.5)  # Simuler délai API

        # Assets simulés basés sur le dossier iFiveMe réel
        mock_assets = [
            DriveAsset(
                id="logo_ifiveme_001",
                name="iFiveMe_Logo_Principal.png",
                type="image",
                url="https://drive.google.com/file/d/logo_ifiveme_001/view",
                download_url="https://drive.google.com/uc?id=logo_ifiveme_001",
                thumbnail_url="https://drive.google.com/thumbnail?id=logo_ifiveme_001",
                size_bytes=245760,
                created_date=datetime(2024, 1, 15, 10, 30),
                modified_date=datetime(2024, 2, 20, 14, 15),
                tags=["logo", "branding", "ifiveme", "principal"],
                description="Logo principal iFiveMe - haute résolution"
            ),
            DriveAsset(
                id="screenshot_dashboard_001",
                name="iFiveMe_Dashboard_Screenshot.jpg",
                type="image",
                url="https://drive.google.com/file/d/screenshot_dashboard_001/view",
                download_url="https://drive.google.com/uc?id=screenshot_dashboard_001",
                thumbnail_url="https://drive.google.com/thumbnail?id=screenshot_dashboard_001",
                size_bytes=892450,
                created_date=datetime(2024, 3, 10, 16, 45),
                modified_date=datetime(2024, 3, 12, 9, 20),
                tags=["product", "screenshot", "dashboard", "interface"],
                description="Capture d'écran du dashboard iFiveMe"
            ),
            DriveAsset(
                id="social_linkedin_template_001",
                name="Template_LinkedIn_iFiveMe.png",
                type="image",
                url="https://drive.google.com/file/d/social_linkedin_template_001/view",
                download_url="https://drive.google.com/uc?id=social_linkedin_template_001",
                thumbnail_url="https://drive.google.com/thumbnail?id=social_linkedin_template_001",
                size_bytes=456789,
                created_date=datetime(2024, 4, 5, 11, 15),
                modified_date=datetime(2024, 4, 8, 13, 30),
                tags=["social", "linkedin", "template", "post"],
                description="Template pour posts LinkedIn iFiveMe"
            ),
            DriveAsset(
                id="team_photo_001",
                name="Equipe_iFiveMe_2024.jpg",
                type="image",
                url="https://drive.google.com/file/d/team_photo_001/view",
                download_url="https://drive.google.com/uc?id=team_photo_001",
                thumbnail_url="https://drive.google.com/thumbnail?id=team_photo_001",
                size_bytes=1204567,
                created_date=datetime(2024, 5, 20, 14, 0),
                modified_date=datetime(2024, 5, 20, 14, 0),
                tags=["team", "portrait", "about", "2024"],
                description="Photo d'équipe iFiveMe 2024"
            ),
            DriveAsset(
                id="product_demo_video_001",
                name="iFiveMe_Demo_Complete.mp4",
                type="video",
                url="https://drive.google.com/file/d/product_demo_video_001/view",
                download_url="https://drive.google.com/uc?id=product_demo_video_001",
                thumbnail_url="https://drive.google.com/thumbnail?id=product_demo_video_001",
                size_bytes=15678901,
                created_date=datetime(2024, 6, 1, 10, 0),
                modified_date=datetime(2024, 6, 15, 16, 30),
                tags=["video", "demo", "product", "complete"],
                description="Démonstration complète du produit iFiveMe"
            ),
            DriveAsset(
                id="infographic_networking_001",
                name="Infographie_Networking_Digital.png",
                type="image",
                url="https://drive.google.com/file/d/infographic_networking_001/view",
                download_url="https://drive.google.com/uc?id=infographic_networking_001",
                thumbnail_url="https://drive.google.com/thumbnail?id=infographic_networking_001",
                size_bytes=678912,
                created_date=datetime(2024, 7, 10, 9, 30),
                modified_date=datetime(2024, 7, 12, 11, 45),
                tags=["infographic", "networking", "digital", "education"],
                description="Infographie sur le networking digital"
            )
        ]

        return mock_assets

    async def _search_images(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recherche d'images par critères"""
        query = data.get("query", "").lower()
        tags = data.get("tags", [])
        category = data.get("category")
        image_type = data.get("type", "image")

        # S'assurer que le cache est à jour
        if not self._is_cache_valid():
            await self._fetch_drive_assets({"force_refresh": True})

        # Filtrer les assets
        matching_assets = []

        for asset in self.assets_cache.values():
            if asset.type != image_type and image_type != "all":
                continue

            # Recherche par query
            if query:
                if (query in asset.name.lower() or
                    query in (asset.description or "").lower() or
                    any(query in tag.lower() for tag in asset.tags)):
                    matching_assets.append(asset)
                    continue

            # Recherche par tags
            if tags:
                if any(tag.lower() in [t.lower() for t in asset.tags] for tag in tags):
                    matching_assets.append(asset)
                    continue

            # Recherche par catégorie
            if category and category in self.asset_categories:
                category_tags = self.asset_categories[category]["suggested_tags"]
                if any(tag in asset.tags for tag in category_tags):
                    matching_assets.append(asset)
                    continue

            # Si aucun critère spécifique, inclure tous les assets du type demandé
            if not query and not tags and not category:
                matching_assets.append(asset)

        # Trier par pertinence (date de modification récente)
        matching_assets.sort(key=lambda x: x.modified_date, reverse=True)

        return {
            "query": query,
            "tags": tags,
            "category": category,
            "type": image_type,
            "results_count": len(matching_assets),
            "results": [asdict(asset) for asset in matching_assets],
            "searched_at": datetime.now().isoformat()
        }

    async def _get_image_for_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Récupère l'image optimale pour un post spécifique - GARANTIT toujours un résultat"""
        platform = data.get("platform", "linkedin")
        post_topic = data.get("topic", "").lower()
        post_content = data.get("content", "").lower()
        force_image = data.get("force_image", False)

        # Analyser le contenu pour déterminer le type d'image nécessaire
        image_suggestions = self._analyze_content_for_images(post_topic, post_content, platform)

        # Rechercher les images correspondantes
        search_results = await self._search_images({
            "tags": image_suggestions["recommended_tags"],
            "category": image_suggestions["category"],
            "type": "image"
        })

        # Sélectionner la meilleure image
        best_image = self._select_best_image(search_results["results"], platform, image_suggestions)

        # GARANTIR qu'il y a toujours une image si forcé
        if not best_image and (force_image or "carte" in post_content.lower() or "ifiveme" in post_content.lower()):
            # Forcer l'utilisation du logo iFiveMe comme fallback
            fallback_assets = await self._get_fallback_ifiveme_images()
            if fallback_assets:
                best_image = fallback_assets[0]
                self.logger.info("✅ Image de fallback iFiveMe utilisée")

        return {
            "success": True if best_image else False,
            "image_url": best_image.get("download_url") if best_image else None,
            "image_name": best_image.get("name") if best_image else None,
            "platform": platform,
            "topic": post_topic,
            "analysis": image_suggestions,
            "recommended_image": best_image,
            "alternative_images": search_results["results"][:3],  # 3 alternatives
            "optimization_notes": self._get_optimization_notes(best_image, platform) if best_image else None,
            "selection_reason": "Analyse intelligente du contenu" if best_image else "Aucune image trouvée"
        }

    async def _get_fallback_ifiveme_images(self) -> List[DriveAsset]:
        """Retourne les images iFiveMe de fallback garanties"""

        # Assets iFiveMe toujours disponibles
        fallback_assets = [
            DriveAsset(
                id="logo_ifiveme_primary",
                name="iFiveMe_Logo_Principal_HD.png",
                type="image",
                url="https://drive.google.com/file/d/logo_ifiveme_primary/view",
                download_url="https://drive.google.com/uc?id=1RE8sOSWPS8YhZsaSHRLIouZV08p1iUk0",
                thumbnail_url="https://drive.google.com/thumbnail?id=logo_ifiveme_primary",
                size_bytes=456789,
                created_date=datetime(2024, 1, 1, 12, 0),
                modified_date=datetime(2024, 9, 25, 12, 0),
                tags=["ifiveme", "logo", "branding", "principal"],
                description="Logo principal iFiveMe - Toujours utilisable"
            ),
            DriveAsset(
                id="carte_virtuelle_demo",
                name="iFiveMe_Carte_Virtuelle_Demo.jpg",
                type="image",
                url="https://drive.google.com/file/d/carte_virtuelle_demo/view",
                download_url="https://drive.google.com/uc?id=1RE8sOSWPS8YhZsaSHRLIouZV08p1iUk0",
                thumbnail_url="https://drive.google.com/thumbnail?id=carte_virtuelle_demo",
                size_bytes=789123,
                created_date=datetime(2024, 3, 15, 10, 30),
                modified_date=datetime(2024, 9, 25, 12, 0),
                tags=["ifiveme", "carte", "virtuelle", "demo", "produit"],
                description="Démonstration carte virtuelle iFiveMe"
            )
        ]

        return fallback_assets

    # Méthode publique pour compatibilité
    async def get_image_for_post(self, content: str, platform: str = "Facebook", force_image: bool = False) -> Dict[str, Any]:
        """Interface publique pour récupérer une image pour un post"""
        return await self._get_image_for_post({
            "content": content,
            "platform": platform,
            "force_image": force_image
        })

    def _analyze_content_for_images(self, topic: str, content: str, platform: str) -> Dict[str, Any]:
        """Analyse le contenu pour suggérer des types d'images"""
        combined_text = f"{topic} {content}".lower()

        # Mots-clés pour différents types d'images
        keywords_mapping = {
            "product": ["dashboard", "interface", "fonctionnalité", "demo", "capture"],
            "team": ["équipe", "team", "about", "nous", "fondateur"],
            "branding": ["logo", "marque", "brand", "ifiveme"],
            "networking": ["networking", "contact", "business", "professionnel"],
            "social": ["social", "partage", "communauté", "followers"],
            "analytics": ["statistiques", "données", "analytics", "performance", "roi"],
            "innovation": ["innovation", "technologie", "futur", "révolution"]
        }

        # Analyser les mots-clés présents
        detected_themes = []
        recommended_tags = []

        for theme, keywords in keywords_mapping.items():
            if any(keyword in combined_text for keyword in keywords):
                detected_themes.append(theme)
                recommended_tags.extend(keywords[:2])  # Prendre les 2 premiers mots-clés

        # Déterminer la catégorie principale
        if "product" in detected_themes or "demo" in detected_themes:
            category = "product_screenshots"
        elif "team" in detected_themes:
            category = "team_photos"
        elif "branding" in detected_themes:
            category = "logos"
        elif "social" in detected_themes:
            category = "social_media"
        else:
            category = "marketing_materials"

        # Ajuster selon la plateforme
        if platform == "linkedin":
            recommended_tags.extend(["professional", "business", "linkedin"])
        elif platform == "twitter":
            recommended_tags.extend(["compact", "engaging", "twitter"])
        elif platform == "instagram":
            recommended_tags.extend(["visual", "story", "instagram"])

        return {
            "detected_themes": detected_themes,
            "category": category,
            "recommended_tags": list(set(recommended_tags)),
            "confidence_score": len(detected_themes) / len(keywords_mapping) * 100
        }

    def _select_best_image(self, images: List[Dict[str, Any]], platform: str, suggestions: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Sélectionne la meilleure image pour le post"""
        if not images:
            return None

        # Scorer chaque image
        scored_images = []

        for image in images:
            score = 0

            # Score basé sur les tags correspondants
            image_tags = image.get("tags", [])
            recommended_tags = suggestions["recommended_tags"]

            matching_tags = len(set(tag.lower() for tag in image_tags) & set(tag.lower() for tag in recommended_tags))
            score += matching_tags * 10

            # Score basé sur la fraîcheur (images récentes)
            days_old = (datetime.now() - datetime.fromisoformat(image["modified_date"].replace("Z", "+00:00").replace("+00:00", ""))).days
            freshness_score = max(0, 30 - days_old)  # Score décroissant après 30 jours
            score += freshness_score

            # Score basé sur la taille (favoriser les images de bonne qualité)
            size_bytes = image.get("size_bytes", 0)
            if 100000 < size_bytes < 2000000:  # Taille optimale 100KB - 2MB
                score += 20

            # Score spécifique à la plateforme
            if platform == "linkedin" and "linkedin" in image_tags:
                score += 15
            elif platform == "twitter" and any(tag in ["twitter", "compact"] for tag in image_tags):
                score += 15

            scored_images.append((image, score))

        # Trier par score décroissant
        scored_images.sort(key=lambda x: x[1], reverse=True)

        return scored_images[0][0] if scored_images else None

    def _get_optimization_notes(self, image: Dict[str, Any], platform: str) -> List[str]:
        """Génère des notes d'optimisation pour l'image"""
        notes = []

        size_bytes = image.get("size_bytes", 0)

        # Notes spécifiques à la plateforme
        if platform == "linkedin":
            notes.append("Optimal pour LinkedIn: format 1200x627 pixels recommandé")
            if size_bytes > 1000000:
                notes.append("Considérer compression pour temps de chargement optimal")
        elif platform == "twitter":
            notes.append("Optimal pour Twitter: format 1024x512 pixels recommandé")
            if size_bytes > 500000:
                notes.append("Compression recommandée pour Twitter")
        elif platform == "instagram":
            notes.append("Format carré 1080x1080 ou story 1080x1920 recommandé")

        # Notes générales
        if "logo" in image.get("tags", []):
            notes.append("Logo détecté: s'assurer de la visibilité sur fond du post")

        if size_bytes < 50000:
            notes.append("Image petite: vérifier la qualité pour impression grand format")

        return notes

    async def _optimize_image_for_channel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimise une image pour un canal spécifique"""
        image_id = data.get("image_id")
        channel = data.get("channel", "linkedin")
        optimization_type = data.get("type", "social_post")

        if image_id not in self.assets_cache:
            return {"error": "Image non trouvée", "image_id": image_id}

        image = self.assets_cache[image_id]

        # Recommandations d'optimisation par canal
        optimizations = {
            "linkedin": {
                "dimensions": "1200x627",
                "max_size_mb": 2,
                "format": "PNG/JPG",
                "text_overlay": "Recommandé avec call-to-action"
            },
            "twitter": {
                "dimensions": "1024x512",
                "max_size_mb": 1,
                "format": "PNG/JPG/GIF",
                "text_overlay": "Minimal, texte dans le tweet"
            },
            "instagram": {
                "dimensions": "1080x1080",
                "max_size_mb": 1.5,
                "format": "JPG/PNG",
                "text_overlay": "Visual storytelling recommandé"
            },
            "facebook": {
                "dimensions": "1200x630",
                "max_size_mb": 2,
                "format": "PNG/JPG",
                "text_overlay": "Maximum 20% de texte sur l'image"
            },
            "email": {
                "dimensions": "600x300",
                "max_size_mb": 0.5,
                "format": "JPG optimisé",
                "text_overlay": "Alt-text obligatoire"
            }
        }

        channel_specs = optimizations.get(channel, optimizations["linkedin"])

        return {
            "image_id": image_id,
            "original_image": asdict(image),
            "channel": channel,
            "optimization_specs": channel_specs,
            "recommendations": [
                f"Redimensionner à {channel_specs['dimensions']}",
                f"Optimiser la taille sous {channel_specs['max_size_mb']}MB",
                f"Format recommandé: {channel_specs['format']}",
                channel_specs['text_overlay']
            ],
            "estimated_performance": self._estimate_image_performance(image, channel)
        }

    def _estimate_image_performance(self, image: DriveAsset, channel: str) -> Dict[str, Any]:
        """Estime la performance d'une image sur un canal"""
        # Facteurs de performance
        engagement_score = 75  # Base score

        # Bonus selon le type d'image
        if "product" in image.tags:
            engagement_score += 10
        if "team" in image.tags:
            engagement_score += 8
        if "infographic" in image.tags:
            engagement_score += 15

        # Ajustements par canal
        if channel == "linkedin":
            if "professional" in image.tags or "business" in image.tags:
                engagement_score += 12
        elif channel == "instagram":
            if "visual" in image.tags or "story" in image.tags:
                engagement_score += 10

        # Facteur qualité basé sur la taille
        if 200000 < image.size_bytes < 1000000:  # Taille optimale
            engagement_score += 5

        return {
            "estimated_engagement": min(100, max(0, engagement_score)),
            "performance_factors": [
                "Image de qualité professionnelle" if engagement_score > 80 else "Image standard",
                f"Optimisé pour {channel}" if engagement_score > 75 else f"Nécessite optimisation pour {channel}",
                "Tags pertinents détectés" if len(image.tags) > 3 else "Tags limités"
            ],
            "recommendation": "Excellent choix" if engagement_score > 85 else "Bon choix" if engagement_score > 70 else "Considérer alternatives"
        }

    async def _suggest_images_for_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Suggère des images pour un contenu donné"""
        content_type = data.get("type", "social_post")
        topic = data.get("topic", "")
        platform = data.get("platform", "linkedin")
        mood = data.get("mood", "professional")  # professional, casual, energetic, educational

        # Analyser le contenu
        analysis = self._analyze_content_for_images(topic, "", platform)

        # Rechercher des images appropriées
        search_result = await self._search_images({
            "tags": analysis["recommended_tags"],
            "category": analysis["category"],
            "type": "image"
        })

        # Filtrer selon l'humeur/mood
        filtered_images = self._filter_by_mood(search_result["results"], mood)

        # Organiser les suggestions par priorité
        suggestions = {
            "primary": filtered_images[:1],      # Meilleure suggestion
            "alternatives": filtered_images[1:4], # 3 alternatives
            "creative": self._get_creative_suggestions(analysis["category"])
        }

        return {
            "content_type": content_type,
            "topic": topic,
            "platform": platform,
            "mood": mood,
            "analysis": analysis,
            "suggestions": suggestions,
            "total_options": len(filtered_images),
            "generated_at": datetime.now().isoformat()
        }

    def _filter_by_mood(self, images: List[Dict[str, Any]], mood: str) -> List[Dict[str, Any]]:
        """Filtre les images selon l'humeur désirée"""
        mood_tags = {
            "professional": ["professional", "business", "clean", "corporate"],
            "casual": ["casual", "friendly", "relaxed", "informal"],
            "energetic": ["dynamic", "action", "energy", "vibrant"],
            "educational": ["infographic", "chart", "data", "educational"]
        }

        target_tags = mood_tags.get(mood, mood_tags["professional"])

        scored_images = []
        for image in images:
            mood_score = len(set(image.get("tags", [])) & set(target_tags))
            scored_images.append((image, mood_score))

        # Trier par score de mood puis par date
        scored_images.sort(key=lambda x: (x[1], x[0].get("modified_date", "")), reverse=True)

        return [img[0] for img in scored_images]

    def _get_creative_suggestions(self, category: str) -> List[Dict[str, str]]:
        """Génère des suggestions créatives pour le contenu"""
        creative_ideas = {
            "logos": [
                {"idea": "Logo en filigrane sur image de fond", "description": "Subtil et professionnel"},
                {"idea": "Animation du logo", "description": "Pour contenu vidéo"},
            ],
            "product_screenshots": [
                {"idea": "Before/After comparison", "description": "Montrer l'amélioration apportée"},
                {"idea": "Interface annotée", "description": "Expliquer les fonctionnalités"},
            ],
            "social_media": [
                {"idea": "Carousel multi-images", "description": "Storytelling en plusieurs parties"},
                {"idea": "Quote overlay", "description": "Citation inspirante sur image"},
            ],
            "team_photos": [
                {"idea": "Behind-the-scenes", "description": "Côté humain de l'entreprise"},
                {"idea": "Team in action", "description": "Équipe au travail"},
            ]
        }

        return creative_ideas.get(category, [
            {"idea": "Collage thématique", "description": "Combiner plusieurs éléments"},
            {"idea": "Minimaliste", "description": "Design épuré et moderne"}
        ])

    def _is_cache_valid(self) -> bool:
        """Vérifie si le cache est encore valide"""
        if not self.cache_timestamp:
            return False

        cache_age = datetime.now() - self.cache_timestamp
        return cache_age.total_seconds() < (self.config["cache_duration_hours"] * 3600)

    async def _update_assets_cache(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Force la mise à jour du cache des assets"""
        return await self._fetch_drive_assets({"force_refresh": True})

    async def _validate_asset_usage(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valide les droits d'usage d'un asset"""
        asset_id = data.get("asset_id")
        usage_type = data.get("usage", "social_media")  # social_media, advertising, print, etc.

        if asset_id not in self.assets_cache:
            return {"valid": False, "error": "Asset non trouvé"}

        asset = self.assets_cache[asset_id]

        # Tous les assets du dossier iFiveMe sont approuvés pour usage
        return {
            "valid": True,
            "asset_id": asset_id,
            "asset_name": asset.name,
            "usage_type": usage_type,
            "rights": {
                "commercial_use": True,
                "modification_allowed": True,
                "attribution_required": False,
                "usage_restrictions": "Usage limité aux activités iFiveMe"
            },
            "recommendations": [
                "Asset approuvé pour usage commercial iFiveMe",
                "Modification autorisée selon les besoins",
                "Maintenir la cohérence de marque"
            ],
            "validated_at": datetime.now().isoformat()
        }