#!/usr/bin/env python3
"""
Agent iFiveMe avec Boucle Observer-Penser-Agir
Implémente le cycle complet d'amélioration continue
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from playwright.async_api import async_playwright

@dataclass
class Observation:
    """Une observation de l'état actuel"""
    timestamp: float
    page_url: str
    page_title: str
    page_state: Dict[str, Any]
    elements_detected: List[Dict[str, Any]]
    success_indicators: List[str]
    error_indicators: List[str]
    completion_percentage: float
    notes: str

@dataclass
class Thought:
    """Une réflexion basée sur les observations"""
    timestamp: float
    observations_analyzed: List[Observation]
    current_situation: str
    problems_identified: List[str]
    opportunities: List[str]
    next_action_plan: Dict[str, Any]
    confidence_level: float
    reasoning: str

@dataclass
class Action:
    """Une action à exécuter"""
    timestamp: float
    action_type: str
    target: Optional[str]
    parameters: Dict[str, Any]
    expected_outcome: str
    success_criteria: List[str]
    fallback_plan: Optional[Dict[str, Any]]
    executed: bool = False
    success: bool = False
    actual_outcome: str = ""

class ObserveThinkActAgent:
    """Agent iFiveMe avec boucle Observer-Penser-Agir complète"""

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.credentials = {
            "email": "richard@ifiveme.com",
            "password": "bonjour"
        }

        # Cycle Observer-Penser-Agir
        self.observations_history: List[Observation] = []
        self.thoughts_history: List[Thought] = []
        self.actions_history: List[Action] = []

        # Configuration apprentissage
        self.learning_enabled = True
        self.max_cycles = 10
        self.success_threshold = 0.95
        self.improvement_target = 0.05  # 5% d'amélioration par cycle

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """Démarrage agent avec cycle OTA"""
        playwright = await async_playwright().__aenter__()

        self.browser = await playwright.chromium.launch(
            headless=False,
            slow_mo=200
        )

        self.context = await self.browser.new_context(
            viewport={"width": 1600, "height": 1000}
        )

        self.page = await self.context.new_page()
        print("🧠 Agent Observer-Penser-Agir démarré")

    async def stop(self):
        """Arrêt avec sauvegarde de l'apprentissage"""
        await self._save_learning_data()
        if self.browser:
            await self.browser.close()

    async def observe(self) -> Observation:
        """OBSERVER: Analyse l'état actuel de façon exhaustive"""
        print("👁️ OBSERVER - Analyse de l'état actuel...")

        try:
            # État de base
            current_url = self.page.url
            page_title = await self.page.title()

            # Détection d'éléments
            elements_detected = []

            # Boutons
            buttons = await self.page.query_selector_all('button, .btn, input[type="submit"]')
            for i, button in enumerate(buttons[:10]):
                try:
                    text = await button.inner_text()
                    visible = await button.is_visible()
                    enabled = await button.is_enabled()

                    elements_detected.append({
                        "type": "button",
                        "index": i,
                        "text": text.strip(),
                        "visible": visible,
                        "enabled": enabled,
                        "actionable": visible and enabled
                    })
                except:
                    continue

            # Formulaires
            forms = await self.page.query_selector_all('form')
            for i, form in enumerate(forms):
                try:
                    action = await form.get_attribute('action')
                    method = await form.get_attribute('method')
                    inputs = await form.query_selector_all('input, select, textarea')

                    elements_detected.append({
                        "type": "form",
                        "index": i,
                        "action": action,
                        "method": method,
                        "input_count": len(inputs),
                        "completable": len(inputs) > 0
                    })
                except:
                    continue

            # Tables de données
            tables = await self.page.query_selector_all('table')
            for i, table in enumerate(tables):
                try:
                    rows = await table.query_selector_all('tr')
                    headers = await table.query_selector_all('th')

                    elements_detected.append({
                        "type": "table",
                        "index": i,
                        "rows": len(rows),
                        "headers": len(headers),
                        "has_data": len(rows) > 1
                    })
                except:
                    continue

            # Indicateurs de succès
            success_indicators = []

            # Messages de succès
            success_elements = await self.page.query_selector_all('.success, .alert-success, .notice')
            for element in success_elements:
                try:
                    text = await element.inner_text()
                    if text.strip():
                        success_indicators.append(f"Success message: {text.strip()}")
                except:
                    continue

            # URLs de succès
            if any(keyword in current_url.lower() for keyword in ['success', 'complete', 'done']):
                success_indicators.append(f"Success URL pattern: {current_url}")

            # Indicateurs d'erreur
            error_indicators = []

            # Messages d'erreur
            error_elements = await self.page.query_selector_all('.error, .alert-danger, .alert-error')
            for element in error_elements:
                try:
                    text = await element.inner_text()
                    if text.strip():
                        error_indicators.append(f"Error message: {text.strip()}")
                except:
                    continue

            # Erreurs dans l'URL
            if any(keyword in current_url.lower() for keyword in ['error', 'failed', 'invalid']):
                error_indicators.append(f"Error URL pattern: {current_url}")

            # Calcul du pourcentage de completion
            completion_percentage = self._calculate_completion_percentage(
                current_url, elements_detected, success_indicators, error_indicators
            )

            observation = Observation(
                timestamp=time.time(),
                page_url=current_url,
                page_title=page_title,
                page_state={
                    "button_count": len([e for e in elements_detected if e["type"] == "button"]),
                    "form_count": len([e for e in elements_detected if e["type"] == "form"]),
                    "table_count": len([e for e in elements_detected if e["type"] == "table"]),
                    "actionable_elements": len([e for e in elements_detected if e.get("actionable", False)])
                },
                elements_detected=elements_detected,
                success_indicators=success_indicators,
                error_indicators=error_indicators,
                completion_percentage=completion_percentage,
                notes=f"Observation at {current_url} - {len(elements_detected)} elements detected"
            )

            self.observations_history.append(observation)

            print(f"✅ OBSERVATION: {completion_percentage:.1f}% complete, {len(elements_detected)} elements")
            return observation

        except Exception as e:
            self.logger.error(f"Erreur observation: {e}")
            # Observation d'erreur
            return Observation(
                timestamp=time.time(),
                page_url=self.page.url if self.page else "unknown",
                page_title="Error",
                page_state={"error": True},
                elements_detected=[],
                success_indicators=[],
                error_indicators=[f"Observation error: {str(e)}"],
                completion_percentage=0.0,
                notes=f"Observation failed: {str(e)}"
            )

    def _calculate_completion_percentage(self, url: str, elements: List[Dict],
                                       success_indicators: List[str],
                                       error_indicators: List[str]) -> float:
        """Calcule le pourcentage de completion de la tâche"""

        # Si erreurs détectées, completion basse
        if error_indicators:
            return 0.1

        # Si indicateurs de succès, completion haute
        if success_indicators:
            return 0.9

        # Basé sur les éléments détectés
        actionable_count = len([e for e in elements if e.get("actionable", False)])

        # Basé sur l'URL
        if "login" in url.lower():
            return 0.2  # Début du processus
        elif "users" in url.lower() and "edit" not in url.lower():
            return 0.6  # Navigation réussie
        elif "edit" in url.lower():
            return 0.8  # Dans un processus d'édition

        return 0.5  # État neutre

    async def think(self, recent_observations: List[Observation]) -> Thought:
        """PENSER: Analyse les observations et planifie la prochaine action"""
        print("🤔 PENSER - Analyse et planification...")

        if not recent_observations:
            return self._create_default_thought()

        latest_observation = recent_observations[-1]

        # Analyser la situation actuelle
        current_situation = self._analyze_current_situation(latest_observation)

        # Identifier les problèmes
        problems_identified = self._identify_problems(recent_observations)

        # Identifier les opportunités
        opportunities = self._identify_opportunities(latest_observation)

        # Planifier la prochaine action
        next_action_plan = await self._plan_next_action(latest_observation, problems_identified, opportunities)

        # Calculer le niveau de confiance
        confidence_level = self._calculate_confidence(recent_observations, problems_identified)

        # Raisonnement
        reasoning = self._generate_reasoning(current_situation, problems_identified, opportunities, next_action_plan)

        thought = Thought(
            timestamp=time.time(),
            observations_analyzed=recent_observations,
            current_situation=current_situation,
            problems_identified=problems_identified,
            opportunities=opportunities,
            next_action_plan=next_action_plan,
            confidence_level=confidence_level,
            reasoning=reasoning
        )

        self.thoughts_history.append(thought)

        print(f"✅ PENSÉE: {current_situation}, Confiance: {confidence_level:.2f}")
        return thought

    def _analyze_current_situation(self, observation: Observation) -> str:
        """Analyse la situation actuelle"""

        if observation.error_indicators:
            return "ERROR_STATE"
        elif observation.success_indicators:
            return "SUCCESS_STATE"
        elif observation.completion_percentage > 0.8:
            return "NEAR_COMPLETION"
        elif observation.completion_percentage > 0.5:
            return "IN_PROGRESS"
        elif "login" in observation.page_url.lower():
            return "LOGIN_REQUIRED"
        elif observation.page_state.get("form_count", 0) > 0:
            return "FORM_AVAILABLE"
        elif observation.page_state.get("table_count", 0) > 0:
            return "DATA_DISPLAY"
        else:
            return "EXPLORING"

    def _identify_problems(self, observations: List[Observation]) -> List[str]:
        """Identifie les problèmes récurrents"""
        problems = []

        latest = observations[-1]

        # Erreurs explicites
        if latest.error_indicators:
            problems.extend([f"Error detected: {err}" for err in latest.error_indicators])

        # Pas de progression
        if len(observations) >= 3:
            recent_completions = [obs.completion_percentage for obs in observations[-3:]]
            if max(recent_completions) - min(recent_completions) < 0.1:
                problems.append("No progress in recent observations")

        # Éléments non actionnables
        actionable_count = len([e for e in latest.elements_detected if e.get("actionable", False)])
        if actionable_count == 0:
            problems.append("No actionable elements available")

        return problems

    def _identify_opportunities(self, observation: Observation) -> List[str]:
        """Identifie les opportunités d'action"""
        opportunities = []

        # Formulaires disponibles
        forms = [e for e in observation.elements_detected if e["type"] == "form"]
        if forms:
            opportunities.append(f"Can fill {len(forms)} form(s)")

        # Boutons actionnables
        buttons = [e for e in observation.elements_detected if e["type"] == "button" and e.get("actionable")]
        if buttons:
            opportunities.append(f"Can click {len(buttons)} button(s)")

        # Données extractibles
        tables = [e for e in observation.elements_detected if e["type"] == "table" and e.get("has_data")]
        if tables:
            opportunities.append(f"Can extract data from {len(tables)} table(s)")

        return opportunities

    async def _plan_next_action(self, observation: Observation, problems: List[str],
                               opportunities: List[str]) -> Dict[str, Any]:
        """Planifie la prochaine action basée sur l'analyse"""

        # Si erreurs, action de récupération
        if observation.error_indicators:
            return {
                "type": "recovery",
                "action": "navigate_back",
                "reason": "Error detected, attempting recovery"
            }

        # Si page de login
        if "login" in observation.page_url.lower():
            return {
                "type": "authentication",
                "action": "login",
                "credentials": self.credentials,
                "reason": "Login required"
            }

        # Si formulaires disponibles
        forms = [e for e in observation.elements_detected if e["type"] == "form"]
        if forms and "Can fill" in str(opportunities):
            return {
                "type": "form_interaction",
                "action": "fill_form",
                "target_form": forms[0],
                "reason": "Form available for interaction"
            }

        # Si boutons d'action disponibles
        actionable_buttons = [e for e in observation.elements_detected
                             if e["type"] == "button" and e.get("actionable")]
        if actionable_buttons:
            # Prioriser certains boutons
            priority_keywords = ["save", "submit", "create", "export", "download"]

            for button in actionable_buttons:
                button_text = button.get("text", "").lower()
                if any(keyword in button_text for keyword in priority_keywords):
                    return {
                        "type": "button_click",
                        "action": "click_button",
                        "target_button": button,
                        "reason": f"Priority button available: {button_text}"
                    }

            # Si pas de bouton prioritaire, prendre le premier
            return {
                "type": "button_click",
                "action": "click_button",
                "target_button": actionable_buttons[0],
                "reason": "Available button interaction"
            }

        # Si données extractibles
        tables = [e for e in observation.elements_detected if e["type"] == "table" and e.get("has_data")]
        if tables:
            return {
                "type": "data_extraction",
                "action": "extract_table_data",
                "target_table": tables[0],
                "reason": "Data available for extraction"
            }

        # Action par défaut - exploration
        return {
            "type": "exploration",
            "action": "take_screenshot",
            "reason": "Exploring current state"
        }

    def _calculate_confidence(self, observations: List[Observation], problems: List[str]) -> float:
        """Calcule le niveau de confiance pour l'action planifiée"""

        base_confidence = 0.7

        # Réduire si problèmes
        confidence = base_confidence - (len(problems) * 0.1)

        # Augmenter si observations récentes sont cohérentes
        if len(observations) >= 2:
            latest = observations[-1]
            previous = observations[-2]

            if latest.completion_percentage > previous.completion_percentage:
                confidence += 0.1  # Progression positive
            elif latest.completion_percentage < previous.completion_percentage:
                confidence -= 0.1  # Régression

        return max(0.1, min(1.0, confidence))

    def _generate_reasoning(self, situation: str, problems: List[str],
                          opportunities: List[str], action_plan: Dict[str, Any]) -> str:
        """Génère le raisonnement pour les décisions"""

        reasoning = f"Current situation: {situation}. "

        if problems:
            reasoning += f"Problems identified: {', '.join(problems)}. "

        if opportunities:
            reasoning += f"Opportunities available: {', '.join(opportunities)}. "

        reasoning += f"Planned action: {action_plan.get('action', 'unknown')} because {action_plan.get('reason', 'no reason provided')}."

        return reasoning

    def _create_default_thought(self) -> Thought:
        """Crée une pensée par défaut si pas d'observations"""
        return Thought(
            timestamp=time.time(),
            observations_analyzed=[],
            current_situation="NO_OBSERVATIONS",
            problems_identified=["No observations available"],
            opportunities=["Need to start observing"],
            next_action_plan={
                "type": "initialization",
                "action": "navigate_to_admin",
                "reason": "Start the process"
            },
            confidence_level=0.5,
            reasoning="No observations available, starting with basic navigation"
        )

    async def act(self, thought: Thought) -> Action:
        """AGIR: Execute l'action planifiée"""
        print("🚀 AGIR - Exécution de l'action planifiée...")

        action_plan = thought.next_action_plan
        action_type = action_plan.get("type", "unknown")
        action_name = action_plan.get("action", "unknown")

        action = Action(
            timestamp=time.time(),
            action_type=action_type,
            target=str(action_plan.get("target_button", action_plan.get("target_form", ""))),
            parameters=action_plan,
            expected_outcome=action_plan.get("reason", "Unknown outcome"),
            success_criteria=["No errors", "Page change or element interaction"],
            fallback_plan={"type": "screenshot", "action": "document_state"}
        )

        try:
            # Exécuter l'action selon le type
            if action_name == "login":
                success = await self._execute_login(action_plan)
            elif action_name == "click_button":
                success = await self._execute_button_click(action_plan)
            elif action_name == "fill_form":
                success = await self._execute_form_fill(action_plan)
            elif action_name == "extract_table_data":
                success = await self._execute_data_extraction(action_plan)
            elif action_name == "take_screenshot":
                success = await self._execute_screenshot(action_plan)
            elif action_name == "navigate_to_admin":
                success = await self._execute_navigation(action_plan)
            else:
                print(f"⚠️ Action non reconnue: {action_name}")
                success = await self._execute_screenshot({"reason": f"Unknown action: {action_name}"})

            action.executed = True
            action.success = success
            action.actual_outcome = "Action completed successfully" if success else "Action failed"

        except Exception as e:
            self.logger.error(f"Erreur exécution action: {e}")
            action.executed = True
            action.success = False
            action.actual_outcome = f"Error: {str(e)}"

            # Fallback
            await self._execute_screenshot({"reason": f"Fallback after error: {str(e)}"})

        self.actions_history.append(action)

        result_icon = "✅" if action.success else "❌"
        print(f"{result_icon} ACTION: {action_name} - {action.actual_outcome}")

        return action

    async def _execute_login(self, action_plan: Dict[str, Any]) -> bool:
        """Exécute la connexion"""
        try:
            await self.page.goto("https://admin.ifiveme.com")
            await asyncio.sleep(2)

            email_field = await self.page.wait_for_selector('input[type="email"]', timeout=10000)
            password_field = await self.page.wait_for_selector('input[type="password"]', timeout=5000)

            await email_field.fill(self.credentials["email"])
            await password_field.fill(self.credentials["password"])

            submit_btn = await self.page.wait_for_selector('input[type="submit"]', timeout=5000)
            await submit_btn.click()

            await asyncio.sleep(3)

            # Vérifier succès
            if "login" not in self.page.url.lower():
                return True

        except Exception as e:
            self.logger.error(f"Login error: {e}")

        return False

    async def _execute_button_click(self, action_plan: Dict[str, Any]) -> bool:
        """Exécute un clic de bouton"""
        try:
            target_button = action_plan.get("target_button", {})
            button_text = target_button.get("text", "")

            if button_text:
                # Chercher le bouton par son texte
                button = await self.page.wait_for_selector(f'button:has-text("{button_text}")', timeout=5000)
                await button.click()
                await asyncio.sleep(2)
                return True

        except Exception as e:
            self.logger.error(f"Button click error: {e}")

        return False

    async def _execute_form_fill(self, action_plan: Dict[str, Any]) -> bool:
        """Remplit un formulaire"""
        try:
            # Pour cette démo, on remplit avec des données de test
            inputs = await self.page.query_selector_all('input[type="text"], input[type="email"], textarea')

            test_data = {
                "name": "Test iFiveMe",
                "email": "test@ifiveme.com",
                "organization": "iFiveMe Test Org"
            }

            for i, input_field in enumerate(inputs[:3]):
                placeholder = await input_field.get_attribute('placeholder') or ""
                name = await input_field.get_attribute('name') or ""

                # Choisir la valeur selon le contexte
                if "email" in (placeholder + name).lower():
                    value = test_data["email"]
                elif "name" in (placeholder + name).lower():
                    value = test_data["name"]
                elif "org" in (placeholder + name).lower():
                    value = test_data["organization"]
                else:
                    value = f"Test Value {i+1}"

                await input_field.fill(value)
                await asyncio.sleep(0.5)

            return True

        except Exception as e:
            self.logger.error(f"Form fill error: {e}")

        return False

    async def _execute_data_extraction(self, action_plan: Dict[str, Any]) -> bool:
        """Extrait des données d'un tableau"""
        try:
            tables = await self.page.query_selector_all('table')
            if not tables:
                return False

            table = tables[0]  # Premier tableau

            # Extraire headers
            headers = []
            header_elements = await table.query_selector_all('th')
            for header in header_elements:
                text = await header.inner_text()
                headers.append(text.strip())

            # Extraire quelques lignes
            rows = await table.query_selector_all('tbody tr, tr')
            extracted_data = []

            for row in rows[:5]:  # 5 premières lignes
                cells = await row.query_selector_all('td, th')
                row_data = []
                for cell in cells:
                    text = await cell.inner_text()
                    row_data.append(text.strip())
                if row_data:
                    extracted_data.append(row_data)

            # Sauvegarder les données
            Path("data/observe_think_act").mkdir(parents=True, exist_ok=True)

            extraction_result = {
                "timestamp": time.time(),
                "headers": headers,
                "data": extracted_data,
                "total_rows": len(extracted_data)
            }

            with open(f"data/observe_think_act/extracted_data_{int(time.time())}.json", "w") as f:
                json.dump(extraction_result, f, indent=2)

            print(f"📊 Données extraites: {len(headers)} colonnes, {len(extracted_data)} lignes")
            return True

        except Exception as e:
            self.logger.error(f"Data extraction error: {e}")

        return False

    async def _execute_screenshot(self, action_plan: Dict[str, Any]) -> bool:
        """Prend une capture d'écran"""
        try:
            Path("data/observe_think_act").mkdir(parents=True, exist_ok=True)

            timestamp = int(time.time())
            screenshot_path = f"data/observe_think_act/screenshot_{timestamp}.png"

            await self.page.screenshot(path=screenshot_path, full_page=True)

            print(f"📸 Screenshot: {screenshot_path}")
            return True

        except Exception as e:
            self.logger.error(f"Screenshot error: {e}")

        return False

    async def _execute_navigation(self, action_plan: Dict[str, Any]) -> bool:
        """Navigue vers une page"""
        try:
            await self.page.goto("https://admin.ifiveme.com")
            await asyncio.sleep(2)
            return True

        except Exception as e:
            self.logger.error(f"Navigation error: {e}")

        return False

    async def _save_learning_data(self):
        """Sauvegarde les données d'apprentissage"""
        try:
            Path("data/observe_think_act").mkdir(parents=True, exist_ok=True)

            learning_data = {
                "timestamp": time.time(),
                "total_observations": len(self.observations_history),
                "total_thoughts": len(self.thoughts_history),
                "total_actions": len(self.actions_history),
                "success_rate": self._calculate_success_rate(),
                "observations": [obs.__dict__ for obs in self.observations_history],
                "thoughts": [thought.__dict__ for thought in self.thoughts_history],
                "actions": [action.__dict__ for action in self.actions_history]
            }

            with open("data/observe_think_act/learning_data.json", "w") as f:
                json.dump(learning_data, f, indent=2, default=str)

            print(f"📚 Données d'apprentissage sauvegardées")

        except Exception as e:
            self.logger.error(f"Save learning error: {e}")

    def _calculate_success_rate(self) -> float:
        """Calcule le taux de succès des actions"""
        if not self.actions_history:
            return 0.0

        successful_actions = len([a for a in self.actions_history if a.success])
        return successful_actions / len(self.actions_history)

    async def run_observe_think_act_cycle(self, task_description: str = "Complete admin task") -> Dict[str, Any]:
        """Exécute le cycle complet Observer-Penser-Agir"""

        print("🧠 DÉMARRAGE CYCLE OBSERVER-PENSER-AGIR")
        print("=" * 60)
        print(f"🎯 Tâche: {task_description}")
        print("🔄 Cycles maximum: {self.max_cycles}")
        print("=" * 60)

        cycle_count = 0
        task_completed = False

        while cycle_count < self.max_cycles and not task_completed:
            cycle_count += 1
            print(f"\n🔄 CYCLE {cycle_count}/{self.max_cycles}")
            print("-" * 40)

            # OBSERVER
            observation = await self.observe()
            await asyncio.sleep(1)

            # PENSER
            recent_observations = self.observations_history[-3:]  # 3 dernières observations
            thought = await self.think(recent_observations)
            await asyncio.sleep(1)

            # AGIR
            action = await self.act(thought)
            await asyncio.sleep(2)  # Laisser temps à l'action

            # Évaluer si la tâche est terminée
            if observation.completion_percentage >= self.success_threshold:
                task_completed = True
                print(f"\n✅ TÂCHE TERMINÉE - Seuil de succès atteint: {observation.completion_percentage:.2f}")
            elif observation.error_indicators:
                print(f"\n⚠️ ERREURS DÉTECTÉES - Continuons avec récupération")

            # Afficher résumé du cycle
            print(f"📊 Résumé cycle {cycle_count}:")
            print(f"  👁️ Observation: {observation.completion_percentage:.1f}% complete")
            print(f"  🤔 Pensée: {thought.confidence_level:.2f} confidence")
            print(f"  🚀 Action: {action.action_type} - {'✅' if action.success else '❌'}")

        # Résultats finaux
        success_rate = self._calculate_success_rate()

        final_results = {
            "task_completed": task_completed,
            "cycles_executed": cycle_count,
            "final_completion": self.observations_history[-1].completion_percentage if self.observations_history else 0,
            "success_rate": success_rate,
            "total_observations": len(self.observations_history),
            "total_thoughts": len(self.thoughts_history),
            "total_actions": len(self.actions_history),
            "learning_data_saved": True
        }

        print(f"\n" + "="*60)
        print("🏆 CYCLE OBSERVER-PENSER-AGIR TERMINÉ")
        print("="*60)
        print(f"✅ Tâche terminée: {'Oui' if task_completed else 'Non'}")
        print(f"🔄 Cycles exécutés: {cycle_count}")
        print(f"📊 Taux de succès: {success_rate:.2f}")
        print(f"🎯 Completion finale: {final_results['final_completion']:.1f}%")

        return final_results

# Fonction d'utilisation simple
async def run_ota_agent(task: str = "Admin task automation"):
    """Lance un agent avec cycle Observer-Penser-Agir"""
    agent = ObserveThinkActAgent()

    try:
        await agent.start()
        result = await agent.run_observe_think_act_cycle(task)
        return result
    finally:
        await agent.stop()

if __name__ == "__main__":
    print("🧠 AGENT OBSERVER-PENSER-AGIR POUR IFIVEME")
    result = asyncio.run(run_ota_agent("Automatisation admin iFiveMe avec apprentissage"))

    print(f"\n🎉 RÉSULTAT FINAL:")
    print(f"Succès: {'✅' if result['task_completed'] else '❌'}")
    print(f"Taux de réussite: {result['success_rate']:.2f}")
    print(f"Apprentissage continu activé ! 🚀")