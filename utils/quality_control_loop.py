"""
iFiveMe Marketing MVP - Boucle de Contrôle Qualité
Système d'itération pour garantir l'excellence de chaque production
"""

import logging
import json
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class QualityStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    NEEDS_REVISION = "needs_revision"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPERT_LEVEL = "expert_level"

@dataclass
class QualityStandard:
    """Standard de qualité iFiveMe"""
    name: str
    description: str
    criteria: List[str]
    weight: float
    minimum_score: float

@dataclass
class QualityAssessment:
    """Évaluation qualité d'une production"""
    standard: str
    score: float
    max_score: float
    feedback: List[str]
    suggestions: List[str]
    passed: bool

@dataclass
class ProductionItem:
    """Item de production en cours de validation"""
    id: str
    type: str
    content: Any
    iteration: int
    status: QualityStatus
    quality_score: float
    assessments: List[QualityAssessment]
    created_at: datetime
    last_modified: datetime
    feedback_history: List[str]

class QualityControlLoop:
    """
    Boucle de contrôle qualité pour productions iFiveMe

    Flux: Demande → Production → Révision → Auto-approbation/Rejet
    Si rejet → Réflexion → Nouvelle production → Loop continue
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"quality_control.{agent_name}")

        # Standards de qualité iFiveMe - Niveau Expert Mondial
        self.quality_standards = {
            "content_excellence": QualityStandard(
                name="Excellence de Contenu",
                description="Le contenu doit être d'un niveau expert mondial",
                criteria=[
                    "Grammaire et orthographe parfaites (français/anglais)",
                    "Ton professionnel et engageant",
                    "Message clair et concis",
                    "Call-to-action optimisé",
                    "Alignement avec la marque iFiveMe",
                    "Valeur ajoutée pour l'audience"
                ],
                weight=0.35,
                minimum_score=0.90
            ),
            "brand_consistency": QualityStandard(
                name="Cohérence de Marque",
                description="Respect strict de l'identité iFiveMe",
                criteria=[
                    "Utilisation correcte du logo et couleurs",
                    "Ton de voix iFiveMe respecté",
                    "Positionnement marché cohérent",
                    "Valeurs d'entreprise reflétées",
                    "Différenciation concurrentielle claire"
                ],
                weight=0.25,
                minimum_score=0.95
            ),
            "strategic_alignment": QualityStandard(
                name="Alignement Stratégique",
                description="Contribution aux objectifs business",
                criteria=[
                    "Objectifs marketing clairs",
                    "Audience cible appropriée",
                    "ROI potentiel élevé",
                    "Timing optimal",
                    "Synergies cross-canal"
                ],
                weight=0.20,
                minimum_score=0.85
            ),
            "technical_excellence": QualityStandard(
                name="Excellence Technique",
                description="Qualité technique irréprochable",
                criteria=[
                    "Format optimisé pour la plateforme",
                    "Specifications respectées",
                    "Performance de chargement",
                    "Accessibilité assurée",
                    "SEO optimisé si applicable"
                ],
                weight=0.15,
                minimum_score=0.90
            ),
            "innovation_factor": QualityStandard(
                name="Facteur Innovation",
                description="Créativité et innovation",
                criteria=[
                    "Approche créative unique",
                    "Différenciation competitive",
                    "Tendances avant-gardistes",
                    "Engagement émotionnel",
                    "Mémorabilité élevée"
                ],
                weight=0.05,
                minimum_score=0.80
            )
        }

        self.max_iterations = 5
        self.expert_threshold = 0.93  # Score pour qualification "expert"

    async def process_with_quality_loop(self,
                                       production_func: callable,
                                       initial_request: Dict[str, Any],
                                       production_type: str) -> Dict[str, Any]:
        """
        Lance la boucle de contrôle qualité

        Args:
            production_func: Fonction qui produit le contenu
            initial_request: Demande initiale
            production_type: Type de production (social_post, email, etc.)
        """

        item_id = f"{production_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        production_item = ProductionItem(
            id=item_id,
            type=production_type,
            content=None,
            iteration=0,
            status=QualityStatus.PENDING,
            quality_score=0.0,
            assessments=[],
            created_at=datetime.now(),
            last_modified=datetime.now(),
            feedback_history=[]
        )

        self.logger.info(f"🔄 Début boucle qualité pour {item_id}")

        # Boucle principale d'amélioration
        while production_item.iteration < self.max_iterations:
            production_item.iteration += 1
            production_item.status = QualityStatus.IN_REVIEW

            self.logger.info(f"🔄 Itération {production_item.iteration}/{self.max_iterations}")

            # 1. PRODUCTION
            try:
                # Ajuster la demande selon les feedbacks précédents
                adjusted_request = self._adjust_request_from_feedback(
                    initial_request,
                    production_item.feedback_history
                )

                production_item.content = await production_func(adjusted_request)

            except Exception as e:
                self.logger.error(f"❌ Erreur production: {str(e)}")
                production_item.status = QualityStatus.REJECTED
                break

            # 2. RÉVISION QUALITÉ
            production_item.assessments = await self._conduct_quality_review(
                production_item.content,
                production_type
            )

            # 3. CALCUL SCORE GLOBAL
            production_item.quality_score = self._calculate_overall_score(
                production_item.assessments
            )

            # 4. DÉCISION AUTO-APPROBATION
            decision = self._make_approval_decision(production_item)

            if decision["approved"]:
                production_item.status = QualityStatus.EXPERT_LEVEL if production_item.quality_score >= self.expert_threshold else QualityStatus.APPROVED
                self.logger.info(f"✅ Production approuvée - Score: {production_item.quality_score:.2%}")
                break

            # 5. RÉFLEXION ET AMÉLIORATION
            production_item.status = QualityStatus.NEEDS_REVISION
            reflection_feedback = await self._conduct_reflection(
                production_item,
                decision["feedback"]
            )

            production_item.feedback_history.append(reflection_feedback)
            production_item.last_modified = datetime.now()

            self.logger.info(f"🔄 Révision nécessaire - Score: {production_item.quality_score:.2%}")

        # Résultat final
        if production_item.status in [QualityStatus.APPROVED, QualityStatus.EXPERT_LEVEL]:
            return {
                "success": True,
                "content": production_item.content,
                "quality_score": production_item.quality_score,
                "status": production_item.status.value,
                "iterations": production_item.iteration,
                "assessments": [asdict(a) for a in production_item.assessments],
                "final_feedback": self._generate_final_report(production_item)
            }
        else:
            return {
                "success": False,
                "reason": "Impossible d'atteindre le standard qualité requis",
                "quality_score": production_item.quality_score,
                "iterations": production_item.iteration,
                "final_assessments": [asdict(a) for a in production_item.assessments],
                "recommendations": self._generate_improvement_recommendations(production_item)
            }

    async def _conduct_quality_review(self, content: Any, production_type: str) -> List[QualityAssessment]:
        """Effectue la révision qualité selon tous les standards"""

        assessments = []

        for standard_name, standard in self.quality_standards.items():
            assessment = await self._assess_against_standard(
                content,
                standard,
                production_type
            )
            assessments.append(assessment)

        return assessments

    async def _assess_against_standard(self,
                                     content: Any,
                                     standard: QualityStandard,
                                     production_type: str) -> QualityAssessment:
        """Évalue le contenu contre un standard spécifique"""

        feedback = []
        suggestions = []
        total_score = 0.0
        criteria_count = len(standard.criteria)

        # Analyse par critère
        for criterion in standard.criteria:
            score = await self._evaluate_criterion(content, criterion, production_type)
            total_score += score

            if score < 0.8:  # Seuil pour feedback
                feedback.append(f"❌ {criterion}: Score {score:.1%}")
                suggestions.append(await self._generate_improvement_suggestion(criterion, content))
            elif score >= 0.9:
                feedback.append(f"✅ {criterion}: Excellent ({score:.1%})")

        final_score = total_score / criteria_count
        passed = final_score >= standard.minimum_score

        return QualityAssessment(
            standard=standard.name,
            score=final_score,
            max_score=1.0,
            feedback=feedback,
            suggestions=suggestions,
            passed=passed
        )

    async def _evaluate_criterion(self, content: Any, criterion: str, production_type: str) -> float:
        """Évalue un critère spécifique"""

        # Analyse contextuelle selon le critère
        if "grammaire" in criterion.lower() or "orthographe" in criterion.lower():
            return await self._check_grammar_quality(content)
        elif "ton professionnel" in criterion.lower():
            return await self._check_professional_tone(content)
        elif "logo" in criterion.lower() or "couleurs" in criterion.lower():
            return await self._check_brand_elements(content)
        elif "audience cible" in criterion.lower():
            return await self._check_target_audience_fit(content, production_type)
        elif "roi potentiel" in criterion.lower():
            return await self._check_roi_potential(content, production_type)
        elif "format optimisé" in criterion.lower():
            return await self._check_format_optimization(content, production_type)
        elif "créativité" in criterion.lower() or "innovation" in criterion.lower():
            return await self._check_innovation_factor(content)
        else:
            # Score par défaut basé sur des heuristiques
            return await self._generic_quality_check(content, criterion)

    async def _check_grammar_quality(self, content: Any) -> float:
        """Vérifie la qualité grammaticale"""
        if not isinstance(content, str):
            content_text = str(content.get("content", "")) if isinstance(content, dict) else str(content)
        else:
            content_text = content

        # Indicateurs de qualité grammaticale
        quality_indicators = {
            "length_appropriate": len(content_text.split()) > 10,
            "proper_punctuation": content_text.count(".") + content_text.count("!") + content_text.count("?") > 0,
            "no_double_spaces": "  " not in content_text,
            "proper_capitalization": content_text[0].isupper() if content_text else False,
            "no_obvious_typos": len([w for w in content_text.split() if w.lower() in ["teh", "adn", "form", "wiht"]]) == 0
        }

        score = sum(quality_indicators.values()) / len(quality_indicators)

        # Bonus pour contenu professionnel français/anglais
        if any(word in content_text.lower() for word in ["excellence", "professionnel", "innovation", "expertise"]):
            score += 0.1

        return min(1.0, score)

    async def _check_professional_tone(self, content: Any) -> float:
        """Vérifie le ton professionnel"""
        content_text = self._extract_text_content(content)

        # Mots/phrases professionnels
        professional_indicators = [
            "nous", "notre expertise", "solutions", "accompagner",
            "professionnel", "innovation", "performance", "résultats",
            "partenaire", "collaboration", "stratégie", "optimisation"
        ]

        # Mots à éviter
        unprofessional_words = [
            "super", "génial", "fou", "dingue", "awesome", "sick",
            "lol", "omg", "wtf"
        ]

        professional_count = sum(1 for word in professional_indicators if word in content_text.lower())
        unprofessional_count = sum(1 for word in unprofessional_words if word in content_text.lower())

        # Score basé sur la présence de vocabulaire professionnel
        score = 0.7  # Base
        score += min(0.2, professional_count * 0.05)  # Bonus mots professionnels
        score -= unprofessional_count * 0.1  # Pénalité mots non-professionnels

        return max(0.0, min(1.0, score))

    async def _check_brand_elements(self, content: Any) -> float:
        """Vérifie la cohérence avec la marque iFiveMe"""
        content_text = self._extract_text_content(content)

        # Éléments de marque iFiveMe
        brand_keywords = [
            "ifiveme", "cartes virtuelles", "networking", "digital",
            "professionnel", "business card", "innovation"
        ]

        brand_presence = sum(1 for keyword in brand_keywords if keyword in content_text.lower())

        # Vérifier le positionnement
        positioning_phrases = [
            "plus grand créateur", "révolution", "avenir du networking",
            "plateforme leader", "innovation"
        ]

        positioning_score = sum(1 for phrase in positioning_phrases if phrase in content_text.lower())

        # Score combiné
        score = 0.6  # Base
        score += min(0.3, brand_presence * 0.1)
        score += min(0.1, positioning_score * 0.05)

        return min(1.0, score)

    async def _check_target_audience_fit(self, content: Any, production_type: str) -> float:
        """Vérifie l'adéquation avec l'audience cible"""
        content_text = self._extract_text_content(content)

        # Audiences iFiveMe
        target_keywords = {
            "entrepreneurs": ["entrepreneur", "startup", "business", "entreprise"],
            "professionals": ["professionnel", "carrière", "networking", "contacts"],
            "marketers": ["marketing", "lead", "conversion", "roi", "performance"],
            "quebec_market": ["québec", "canada", "montreal", "francophone"]
        }

        audience_scores = {}
        for audience, keywords in target_keywords.items():
            audience_scores[audience] = sum(1 for kw in keywords if kw in content_text.lower())

        # Score basé sur la meilleure adéquation audience
        max_audience_score = max(audience_scores.values()) if audience_scores else 0

        # Ajustement selon le type de production
        if production_type == "linkedin_post" and audience_scores.get("professionals", 0) > 0:
            max_audience_score += 1
        elif production_type == "email" and audience_scores.get("entrepreneurs", 0) > 0:
            max_audience_score += 1

        return min(1.0, 0.7 + max_audience_score * 0.1)

    async def _check_roi_potential(self, content: Any, production_type: str) -> float:
        """Évalue le potentiel ROI"""
        content_text = self._extract_text_content(content)

        # Indicateurs de ROI potentiel
        roi_indicators = {
            "clear_cta": any(cta in content_text.lower() for cta in
                           ["cliquez", "découvrez", "essayez", "commencez", "inscrivez"]),
            "value_proposition": any(value in content_text.lower() for value in
                                   ["gratuit", "rapide", "simple", "efficace", "résultats"]),
            "urgency": any(urgency in content_text.lower() for urgency in
                          ["maintenant", "aujourd'hui", "limité", "exclusif"]),
            "social_proof": any(proof in content_text.lower() for proof in
                              ["milliers", "clients", "utilisateurs", "témoignage"])
        }

        base_score = sum(roi_indicators.values()) * 0.2

        # Bonus selon le type de production
        if production_type in ["email", "ad_copy"]:
            base_score += 0.2  # Productions orientées conversion

        return min(1.0, base_score + 0.2)  # Score minimum 0.2

    async def _check_format_optimization(self, content: Any, production_type: str) -> float:
        """Vérifie l'optimisation du format"""

        format_scores = {
            "social_post": self._check_social_format(content),
            "email": self._check_email_format(content),
            "ad_copy": self._check_ad_format(content),
            "blog_article": self._check_blog_format(content)
        }

        return format_scores.get(production_type, 0.8)  # Score par défaut

    def _check_social_format(self, content: Any) -> float:
        """Vérifie le format pour réseaux sociaux"""
        content_text = self._extract_text_content(content)

        score = 0.7  # Base

        # Longueur appropriée
        if 50 <= len(content_text) <= 300:  # LinkedIn optimal
            score += 0.1

        # Hashtags présents
        if "#" in content_text:
            hashtag_count = content_text.count("#")
            if 2 <= hashtag_count <= 5:  # Nombre optimal
                score += 0.1

        # Émojis (avec modération)
        emoji_indicators = ["🚀", "✅", "💼", "📱", "🔗", "💡"]
        emoji_count = sum(1 for emoji in emoji_indicators if emoji in content_text)
        if 1 <= emoji_count <= 3:
            score += 0.1

        return min(1.0, score)

    def _check_email_format(self, content: Any) -> float:
        """Vérifie le format email"""
        content_text = self._extract_text_content(content)

        score = 0.7

        # Structure email
        if "objet:" in content_text.lower() or "subject:" in content_text.lower():
            score += 0.1

        if "bonjour" in content_text.lower() or "hello" in content_text.lower():
            score += 0.1

        if "cordialement" in content_text.lower() or "signature" in content_text.lower():
            score += 0.1

        return min(1.0, score)

    def _check_ad_format(self, content: Any) -> float:
        """Vérifie le format publicitaire"""
        content_text = self._extract_text_content(content)

        score = 0.6

        # Titre accrocheur
        if any(hook in content_text.lower() for hook in
               ["découvrez", "révolution", "nouveau", "exclusif", "gratuit"]):
            score += 0.15

        # CTA fort
        if any(cta in content_text.lower() for cta in
               ["commencez maintenant", "essayez gratuitement", "cliquez ici"]):
            score += 0.15

        # Bénéfices clairs
        benefit_count = sum(1 for benefit in ["✅", "•", "-", "►"] if benefit in content_text)
        score += min(0.1, benefit_count * 0.03)

        return min(1.0, score)

    def _check_blog_format(self, content: Any) -> float:
        """Vérifie le format blog"""
        content_text = self._extract_text_content(content)

        score = 0.7

        # Structure blog
        if len(content_text.split()) >= 300:  # Longueur minimum
            score += 0.1

        # Sous-titres
        subtitle_indicators = ["##", "###", "h2", "h3"]
        if any(indicator in content_text.lower() for indicator in subtitle_indicators):
            score += 0.1

        # Conclusion
        if "conclusion" in content_text.lower() or "en résumé" in content_text.lower():
            score += 0.1

        return min(1.0, score)

    async def _check_innovation_factor(self, content: Any) -> float:
        """Évalue le facteur innovation"""
        content_text = self._extract_text_content(content)

        # Mots innovants
        innovation_words = [
            "révolution", "innovation", "avant-garde", "futur", "breakthrough",
            "disruptif", "pionnier", "nouvelle génération", "technologie"
        ]

        innovation_score = sum(1 for word in innovation_words if word in content_text.lower())

        # Approches créatives
        creative_elements = {
            "storytelling": any(story in content_text.lower() for story in
                              ["histoire", "imaginez", "il était", "journey"]),
            "metaphors": any(metaphor in content_text.lower() for metaphor in
                           ["comme", "tel que", "à l'image de", "semblable"]),
            "questions": "?" in content_text,
            "statistics": any(char.isdigit() and "%" in content_text for char in content_text)
        }

        creative_score = sum(creative_elements.values()) * 0.1

        return min(1.0, 0.6 + innovation_score * 0.05 + creative_score)

    async def _generic_quality_check(self, content: Any, criterion: str) -> float:
        """Vérification qualité générique"""
        content_text = self._extract_text_content(content)

        # Heuristiques générales
        base_score = 0.75

        # Longueur appropriée
        if 20 <= len(content_text.split()) <= 500:
            base_score += 0.1

        # Présence de mots-clés de qualité
        quality_words = ["excellence", "qualité", "professionnel", "expertise", "résultat"]
        if any(word in content_text.lower() for word in quality_words):
            base_score += 0.1

        # Structure cohérente
        if content_text.count(".") >= len(content_text.split()) // 15:  # Ponctuation appropriée
            base_score += 0.05

        return min(1.0, base_score)

    def _extract_text_content(self, content: Any) -> str:
        """Extrait le texte du contenu"""
        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            # Extraire de différents champs possibles
            text_fields = ["content", "text", "body", "message", "description"]
            for field in text_fields:
                if field in content and content[field]:
                    return str(content[field])
            return str(content)
        else:
            return str(content)

    def _calculate_overall_score(self, assessments: List[QualityAssessment]) -> float:
        """Calcule le score qualité global"""
        total_weighted_score = 0.0
        total_weight = 0.0

        for assessment in assessments:
            # Récupérer le poids du standard
            standard = next((s for s in self.quality_standards.values()
                           if s.name == assessment.standard), None)

            if standard:
                total_weighted_score += assessment.score * standard.weight
                total_weight += standard.weight

        return total_weighted_score / total_weight if total_weight > 0 else 0.0

    def _make_approval_decision(self, production_item: ProductionItem) -> Dict[str, Any]:
        """Prend la décision d'approbation"""

        # Vérifier si tous les standards minimums sont atteints
        failed_standards = []
        for assessment in production_item.assessments:
            if not assessment.passed:
                failed_standards.append(assessment)

        # Décision d'approbation
        if not failed_standards and production_item.quality_score >= 0.85:
            return {
                "approved": True,
                "reason": f"Excellent score qualité: {production_item.quality_score:.1%}",
                "level": "expert" if production_item.quality_score >= self.expert_threshold else "approved"
            }

        # Compilation des feedbacks pour révision
        feedback = []
        for failed in failed_standards:
            feedback.extend([f"❌ {failed.standard}: {fb}" for fb in failed.feedback])
            feedback.extend([f"💡 Suggestion: {sg}" for sg in failed.suggestions])

        return {
            "approved": False,
            "reason": f"Score insuffisant: {production_item.quality_score:.1%} (minimum: 85%)",
            "feedback": feedback,
            "failed_standards": [f.standard for f in failed_standards]
        }

    def _adjust_request_from_feedback(self,
                                    original_request: Dict[str, Any],
                                    feedback_history: List[str]) -> Dict[str, Any]:
        """Ajuste la demande selon les feedbacks précédents"""

        adjusted_request = original_request.copy()

        if not feedback_history:
            return adjusted_request

        # Analyser les feedbacks pour ajustements
        latest_feedback = feedback_history[-1] if feedback_history else ""

        # Ajustements contextuels
        if "grammaire" in latest_feedback.lower():
            adjusted_request["quality_focus"] = "grammar_excellence"
            adjusted_request["extra_instructions"] = "Porter une attention particulière à la grammaire et l'orthographe"

        if "ton professionnel" in latest_feedback.lower():
            adjusted_request["tone"] = "expert_professional"
            adjusted_request["vocabulary_level"] = "executive"

        if "marque" in latest_feedback.lower() or "brand" in latest_feedback.lower():
            adjusted_request["brand_emphasis"] = "high"
            adjusted_request["ifiveme_focus"] = True

        if "créativité" in latest_feedback.lower():
            adjusted_request["creativity_level"] = "high"
            adjusted_request["innovation_required"] = True

        # Augmenter le niveau d'exigence à chaque itération
        adjusted_request["iteration_number"] = len(feedback_history) + 1
        adjusted_request["quality_bar"] = "expert_level"

        return adjusted_request

    async def _conduct_reflection(self,
                                production_item: ProductionItem,
                                decision_feedback: List[str]) -> str:
        """Effectue la réflexion pour l'amélioration"""

        reflection_points = []

        # Analyser les points d'échec
        for feedback in decision_feedback:
            if "grammaire" in feedback.lower():
                reflection_points.append("Renforcer la révision grammaticale et orthographique")
            elif "ton" in feedback.lower():
                reflection_points.append("Ajuster le ton vers plus de professionnalisme executive")
            elif "marque" in feedback.lower():
                reflection_points.append("Intégrer plus fortement les éléments de marque iFiveMe")
            elif "audience" in feedback.lower():
                reflection_points.append("Mieux cibler l'audience entrepreneurs/professionnels")
            elif "format" in feedback.lower():
                reflection_points.append("Optimiser le format pour la plateforme cible")
            elif "innovation" in feedback.lower():
                reflection_points.append("Ajouter des éléments créatifs et innovants")

        # Stratégies d'amélioration spécifiques
        improvement_strategies = [
            f"Itération {production_item.iteration}: Focus sur l'excellence",
            "Viser le niveau expert mondial reconnu",
            "Intégrer les meilleures pratiques de l'industrie",
            "Assurer la cohérence avec l'identité iFiveMe premium"
        ]

        reflection_report = f"""
RÉFLEXION QUALITÉ - Itération {production_item.iteration}
Score actuel: {production_item.quality_score:.1%}

🎯 Points d'amélioration identifiés:
{chr(10).join('• ' + point for point in reflection_points)}

🚀 Stratégies pour la prochaine itération:
{chr(10).join('• ' + strategy for strategy in improvement_strategies)}

📊 Standards non atteints:
{chr(10).join('• ' + f.standard for f in production_item.assessments if not f.passed)}
        """

        return reflection_report

    async def _generate_improvement_suggestion(self, criterion: str, content: Any) -> str:
        """Génère une suggestion d'amélioration spécifique"""

        suggestions = {
            "grammaire": "Utiliser un outil de correction avancé comme Antidote ou Grammarly Premium",
            "ton professionnel": "Adopter un vocabulaire C-suite avec des termes comme 'stratégique', 'optimisation', 'excellence'",
            "logo": "Intégrer subtilement le logo iFiveMe ou mentionner la marque de manière naturelle",
            "audience cible": "Utiliser des références spécifiques aux défis des entrepreneurs (scaling, networking, efficacité)",
            "roi potentiel": "Ajouter des métriques concrètes ou des bénéfices quantifiables",
            "format optimisé": "Respecter les spécifications de format optimal pour chaque plateforme",
            "créativité": "Utiliser des analogies, du storytelling ou des approches visuelles innovantes"
        }

        for key, suggestion in suggestions.items():
            if key in criterion.lower():
                return suggestion

        return "Réviser selon les meilleures pratiques de l'industrie"

    def _generate_final_report(self, production_item: ProductionItem) -> Dict[str, Any]:
        """Génère le rapport final de qualité"""

        return {
            "quality_level": "Expert Mondial" if production_item.quality_score >= self.expert_threshold else "Professionnel",
            "final_score": f"{production_item.quality_score:.1%}",
            "iterations_required": production_item.iteration,
            "excellence_areas": [
                assessment.standard for assessment in production_item.assessments
                if assessment.score >= 0.90
            ],
            "certification": "✅ Validé selon les standards iFiveMe Excellence",
            "ready_for_publication": True,
            "quality_guarantee": "Production certifiée niveau expert mondial"
        }

    def _generate_improvement_recommendations(self, production_item: ProductionItem) -> List[str]:
        """Génère des recommandations d'amélioration"""

        recommendations = []

        for assessment in production_item.assessments:
            if not assessment.passed:
                recommendations.append(f"🔧 {assessment.standard}: Score {assessment.score:.1%} - Minimum requis {self.quality_standards[assessment.standard].minimum_score:.1%}")
                recommendations.extend(assessment.suggestions)

        # Recommandations générales
        if production_item.quality_score < 0.7:
            recommendations.append("📚 Formation recommandée sur les standards iFiveMe")
            recommendations.append("🎯 Révision complète de l'approche créative")

        return recommendations