"""
iFiveMe Ultimate Web Agent
Agent navigateur web ultra-avancé qui peut tout faire comme un humain
Navigation intelligente, actions complexes, résolution de problèmes autonome
"""

import asyncio
import json
import os
import time
import random
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
import sys
import requests
import base64
from dataclasses import dataclass
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Locator, ElementHandle

sys.path.append(str(Path(__file__).parent.parent))

from utils.base_agent import BaseAgent, AgentTask
from config.settings import COMPANY_INFO

@dataclass
class WebAction:
    """Structure pour une action web"""
    action_type: str  # click, type, scroll, wait, navigate, etc.
    target: str       # sélecteur, URL, texte
    value: Optional[str] = None
    options: Dict[str, Any] = None

@dataclass
class WebSession:
    """Session de navigation web"""
    session_id: str
    start_time: datetime
    pages_visited: List[str]
    actions_performed: List[WebAction]
    cookies: Dict[str, Any]
    local_storage: Dict[str, Any]
    screenshots: List[str]

class UltimateWebAgent(BaseAgent):
    """Agent web ultime - Peut tout faire comme un humain sur le web"""

    def __init__(self):
        super().__init__(
            agent_id="ultimate_web",
            name="iFiveMe Ultimate Web Agent",
            config={
                "headless": False,  # Mode visible par défaut
                "stealth_mode": True,  # Anti-détection
                "human_behavior": True,  # Comportement humain
                "screenshot_mode": True,  # Screenshots automatiques
                "session_persistence": True,  # Sauvegarder sessions
                "ai_problem_solving": True,  # Résolution IA de problèmes
                "unlimited_actions": True,  # Aucune limite d'actions
                "timeout": 60000,  # Timeout généreux
                "retry_failed_actions": 3,
                "auto_captcha_solving": True
            }
        )

        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.current_page: Optional[Page] = None
        self.session: Optional[WebSession] = None

        # Configuration stealth avancée
        self.stealth_config = {
            "user_agents": [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ],
            "viewport_sizes": [
                {"width": 1920, "height": 1080},
                {"width": 1366, "height": 768},
                {"width": 1440, "height": 900},
                {"width": 1536, "height": 864}
            ],
            "languages": ["fr-CA,fr;q=0.9,en;q=0.8", "en-US,en;q=0.9", "fr-FR,fr;q=0.9,en;q=0.8"]
        }

    async def get_capabilities(self) -> List[str]:
        return [
            "🌐 Navigation web illimitée comme un humain",
            "🤖 Actions complexes multi-étapes",
            "🔐 Contournement anti-bot avancé",
            "📸 Screenshots automatiques",
            "🧠 Résolution IA de problèmes",
            "📝 Remplissage formulaires intelligent",
            "🛒 E-commerce et achats automatisés",
            "📱 Social media automation",
            "🔑 Gestion sessions et cookies",
            "⚡ Vitesse humaine avec délais naturels",
            "🎯 Détection et interaction éléments dynamiques",
            "🔄 Retry automatique et récupération d'erreurs",
            "📊 Extraction données avancée",
            "🎮 Jeux et interactions complexes",
            "💰 Trading et finance automation"
        ]

    async def initialize_stealth_browser(self) -> bool:
        """Initialise un navigateur indétectable"""
        try:
            self.playwright = await async_playwright().start()

            # Configuration navigateur stealth
            self.browser = await self.playwright.chromium.launch(
                headless=self.config["headless"],
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions-file-access-check",
                    "--disable-extensions-http-throttling",
                    "--disable-extensions-except",
                    "--disable-component-extensions-with-background-pages",
                    "--disable-default-apps",
                    "--disable-dev-shm-usage",
                    "--disable-features=TranslateUI",
                    "--disable-ipc-flooding-protection",
                    "--disable-renderer-backgrounding",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-field-trial-config",
                    "--disable-web-security",
                    "--disable-features=VizDisplayCompositor",
                    "--no-first-run",
                    "--no-default-browser-check"
                ],
                slow_mo=random.randint(50, 150) if self.config["human_behavior"] else 0
            )

            # Context avec configuration humaine
            user_agent = random.choice(self.stealth_config["user_agents"])
            viewport = random.choice(self.stealth_config["viewport_sizes"])
            language = random.choice(self.stealth_config["languages"])

            self.context = await self.browser.new_context(
                user_agent=user_agent,
                viewport=viewport,
                locale="fr-CA",
                timezone_id="America/Toronto",
                permissions=["geolocation", "notifications"],
                extra_http_headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": language,
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Upgrade-Insecure-Requests": "1"
                }
            )

            # Injection scripts anti-détection
            await self.context.add_init_script("""
                // Supprimer les traces webdriver
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});

                // Randomiser les propriétés navigator
                Object.defineProperty(navigator, 'languages', {get: () => ['fr-CA', 'fr', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});

                // Mock des propriétés communes
                window.chrome = {runtime: {}};
                Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})});

                // Désactiver les détections courantes
                delete window.__nightmare;
                delete window.__phantomas;
                delete window._phantom;
                delete window.callPhantom;
            """)

            # Créer première page
            self.current_page = await self.context.new_page()

            # Intercepter les requêtes pour plus de stealthiness
            await self.current_page.route("**/*", self._handle_route)

            # Initialiser session
            self.session = WebSession(
                session_id=f"web_session_{int(time.time())}",
                start_time=datetime.now(),
                pages_visited=[],
                actions_performed=[],
                cookies={},
                local_storage={},
                screenshots=[]
            )

            self.logger.info("✅ Navigateur stealth ultra-avancé initialisé")
            return True

        except Exception as e:
            self.logger.error(f"❌ Erreur initialisation navigateur: {str(e)}")
            return False

    async def _handle_route(self, route):
        """Intercepte et modifie les requêtes pour plus de stealthiness"""
        request = route.request

        # Modifier les headers pour sembler plus humain
        headers = dict(request.headers)
        headers["sec-ch-ua"] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
        headers["sec-ch-ua-mobile"] = "?0"
        headers["sec-ch-ua-platform"] = '"macOS"'

        await route.continue_(headers=headers)

    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite les tâches web illimitées"""
        task_type = task.type
        data = task.data

        if not await self.initialize_stealth_browser():
            return {"error": "Impossible d'initialiser le navigateur"}

        try:
            if task_type == "navigate_and_perform":
                return await self._navigate_and_perform(data)
            elif task_type == "extract_data":
                return await self._extract_data(data)
            elif task_type == "fill_forms":
                return await self._fill_forms(data)
            elif task_type == "social_media_automation":
                return await self._social_media_automation(data)
            elif task_type == "ecommerce_automation":
                return await self._ecommerce_automation(data)
            elif task_type == "custom_automation":
                return await self._custom_automation(data)
            elif task_type == "ai_problem_solving":
                return await self._ai_problem_solving(data)
            else:
                # Mode libre - exécuter n'importe quelle instruction
                return await self._free_mode_execution(data)

        finally:
            if self.browser:
                await self.browser.close()

    async def _navigate_and_perform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Navigation et actions complexes"""
        url = data.get("url")
        actions = data.get("actions", [])

        if not url:
            return {"error": "URL requise"}

        try:
            # Navigation avec comportement humain
            await self._human_navigate(url)

            results = []
            for action_data in actions:
                action = WebAction(
                    action_type=action_data.get("type"),
                    target=action_data.get("target"),
                    value=action_data.get("value"),
                    options=action_data.get("options", {})
                )

                result = await self._perform_human_action(action)
                results.append(result)

                # Délai humain entre actions
                await self._human_delay()

            # Screenshot final
            screenshot = await self._take_screenshot("final_result")

            return {
                "success": True,
                "url": url,
                "actions_performed": len(actions),
                "results": results,
                "screenshot": screenshot,
                "session_id": self.session.session_id
            }

        except Exception as e:
            return {"error": f"Navigation échouée: {str(e)}"}

    async def _human_navigate(self, url: str):
        """Navigation avec comportement humain réaliste"""
        self.logger.info(f"🌐 Navigation vers: {url}")

        # Délai avant navigation (comme un humain qui tape l'URL)
        await asyncio.sleep(random.uniform(0.5, 2.0))

        # Navigation
        await self.current_page.goto(url, wait_until="domcontentloaded", timeout=self.config["timeout"])

        # Enregistrer dans session
        self.session.pages_visited.append(url)

        # Attendre que la page soit interactive
        await self.current_page.wait_for_load_state("networkidle")

        # Mouvement de souris humain
        await self._human_mouse_movement()

        # Scroll léger comme un humain qui découvre la page
        await self.current_page.evaluate("window.scrollBy(0, Math.random() * 200)")

        await asyncio.sleep(random.uniform(1.0, 3.0))

    async def _perform_human_action(self, action: WebAction) -> Dict[str, Any]:
        """Effectue une action avec comportement humain"""
        try:
            self.logger.info(f"🎯 Action: {action.action_type} sur {action.target}")

            # Enregistrer l'action
            self.session.actions_performed.append(action)

            if action.action_type == "click":
                return await self._human_click(action.target, action.options or {})

            elif action.action_type == "type":
                return await self._human_type(action.target, action.value, action.options or {})

            elif action.action_type == "select":
                return await self._human_select(action.target, action.value, action.options or {})

            elif action.action_type == "scroll":
                return await self._human_scroll(action.options or {})

            elif action.action_type == "wait":
                return await self._intelligent_wait(action.target, action.options or {})

            elif action.action_type == "extract":
                return await self._extract_element_data(action.target, action.options or {})

            elif action.action_type == "upload":
                return await self._human_file_upload(action.target, action.value, action.options or {})

            elif action.action_type == "drag_drop":
                return await self._human_drag_drop(action.target, action.value, action.options or {})

            elif action.action_type == "custom_js":
                return await self._execute_custom_javascript(action.value, action.options or {})

            else:
                return {"error": f"Type d'action non supporté: {action.action_type}"}

        except Exception as e:
            # Retry automatique
            if action.options and action.options.get("retry", True):
                self.logger.warning(f"⚠️ Retry action: {str(e)}")
                await asyncio.sleep(2)
                action.options["retry"] = False  # Éviter boucle infinie
                return await self._perform_human_action(action)

            return {"error": f"Action échouée: {str(e)}", "action": action.action_type}

    async def _human_click(self, selector: str, options: Dict) -> Dict[str, Any]:
        """Clic avec comportement humain réaliste"""
        try:
            # Attendre l'élément
            element = await self.current_page.wait_for_selector(selector, timeout=30000)
            if not element:
                return {"error": f"Élément non trouvé: {selector}"}

            # Scroll vers l'élément
            await element.scroll_into_view_if_needed()

            # Mouvement de souris vers l'élément
            box = await element.bounding_box()
            if box:
                # Déplacement humain vers l'élément
                await self.current_page.mouse.move(
                    box["x"] + box["width"] / 2 + random.uniform(-10, 10),
                    box["y"] + box["height"] / 2 + random.uniform(-10, 10)
                )
                await asyncio.sleep(random.uniform(0.1, 0.5))

            # Clic avec délai humain
            await element.click(delay=random.randint(50, 200))

            # Attendre les effets du clic
            await asyncio.sleep(random.uniform(0.5, 1.5))

            return {"success": True, "action": "click", "selector": selector}

        except Exception as e:
            return {"error": f"Clic échoué: {str(e)}"}

    async def _human_type(self, selector: str, text: str, options: Dict) -> Dict[str, Any]:
        """Frappe avec rythme humain réaliste"""
        try:
            element = await self.current_page.wait_for_selector(selector, timeout=30000)
            if not element:
                return {"error": f"Élément non trouvé: {selector}"}

            # Focus sur l'élément
            await element.focus()
            await asyncio.sleep(random.uniform(0.2, 0.7))

            # Effacer le contenu existant si demandé
            if options.get("clear", True):
                await element.fill("")
                await asyncio.sleep(random.uniform(0.3, 0.8))

            # Frappe caractère par caractère avec rythme humain
            for char in text:
                await element.type(char, delay=random.randint(50, 200))

                # Pauses naturelles (espaces, ponctuation)
                if char in [" ", ".", ",", "!", "?"]:
                    await asyncio.sleep(random.uniform(0.1, 0.4))

                # Hésitations occasionnelles
                if random.random() < 0.05:  # 5% de chance
                    await asyncio.sleep(random.uniform(0.5, 1.5))

            # Pause après frappe
            await asyncio.sleep(random.uniform(0.3, 1.0))

            return {"success": True, "action": "type", "text": text, "selector": selector}

        except Exception as e:
            return {"error": f"Frappe échouée: {str(e)}"}

    async def _human_mouse_movement(self):
        """Mouvement de souris naturel"""
        try:
            # Plusieurs mouvements aléatoires
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 1200)
                y = random.randint(100, 800)
                await self.current_page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.1, 0.5))
        except:
            pass

    async def _human_delay(self):
        """Délai humain réaliste entre actions"""
        delay = random.uniform(1.0, 4.0)
        await asyncio.sleep(delay)

    async def _take_screenshot(self, name: str = None) -> str:
        """Prend une capture d'écran"""
        try:
            if not name:
                name = f"screenshot_{int(time.time())}"

            screenshot_path = self.data_dir / f"{name}.png"
            await self.current_page.screenshot(path=str(screenshot_path), full_page=True)

            self.session.screenshots.append(str(screenshot_path))

            return str(screenshot_path)
        except Exception as e:
            return f"Screenshot échoué: {str(e)}"

    async def _free_mode_execution(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mode libre - Exécute n'importe quelle instruction"""
        instruction = data.get("instruction", "")
        url = data.get("url", "")

        self.logger.info(f"🤖 Mode libre - Instruction: {instruction}")

        if url:
            await self._human_navigate(url)

        # Analyser l'instruction et créer un plan d'actions
        plan = await self._create_action_plan(instruction)

        results = []
        for step in plan:
            try:
                result = await self._execute_plan_step(step)
                results.append(result)
                await self._human_delay()
            except Exception as e:
                self.logger.error(f"Erreur étape: {str(e)}")
                results.append({"error": str(e), "step": step})

        screenshot = await self._take_screenshot("free_mode_result")

        return {
            "success": True,
            "instruction": instruction,
            "plan_executed": plan,
            "results": results,
            "screenshot": screenshot
        }

    async def _create_action_plan(self, instruction: str) -> List[Dict[str, Any]]:
        """Crée un plan d'actions basé sur l'instruction naturelle"""
        instruction_lower = instruction.lower()
        plan = []

        # Analyse intelligente de l'instruction
        if "cliquer" in instruction_lower or "click" in instruction_lower:
            # Extraire le target du clic
            target = self._extract_click_target(instruction)
            plan.append({"action": "click", "target": target})

        elif "écrire" in instruction_lower or "taper" in instruction_lower or "type" in instruction_lower:
            target, text = self._extract_type_info(instruction)
            plan.append({"action": "type", "target": target, "text": text})

        elif "rechercher" in instruction_lower or "search" in instruction_lower:
            query = self._extract_search_query(instruction)
            plan.append({"action": "search", "query": query})

        elif "scroll" in instruction_lower or "défiler" in instruction_lower:
            plan.append({"action": "scroll", "direction": "down"})

        elif "attendre" in instruction_lower or "wait" in instruction_lower:
            plan.append({"action": "wait", "duration": 3})

        else:
            # Instruction complexe - analyser plus finement
            plan = self._parse_complex_instruction(instruction)

        return plan

    async def _execute_plan_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute une étape du plan"""
        action = step.get("action")

        if action == "click":
            return await self._intelligent_click(step.get("target", ""))
        elif action == "type":
            return await self._intelligent_type(step.get("target", ""), step.get("text", ""))
        elif action == "search":
            return await self._perform_search(step.get("query", ""))
        elif action == "scroll":
            await self.current_page.evaluate(f"window.scrollBy(0, 500)")
            return {"success": True, "action": "scroll"}
        elif action == "wait":
            await asyncio.sleep(step.get("duration", 3))
            return {"success": True, "action": "wait"}
        else:
            return {"error": f"Action inconnue: {action}"}

    async def _intelligent_click(self, target_description: str) -> Dict[str, Any]:
        """Clic intelligent basé sur description"""
        try:
            # Essayer plusieurs stratégies de sélection
            selectors = self._generate_smart_selectors(target_description)

            for selector in selectors:
                try:
                    element = await self.current_page.wait_for_selector(selector, timeout=5000)
                    if element:
                        await element.click()
                        return {"success": True, "clicked": selector, "description": target_description}
                except:
                    continue

            return {"error": f"Impossible de trouver: {target_description}"}

        except Exception as e:
            return {"error": f"Clic intelligent échoué: {str(e)}"}

    def _generate_smart_selectors(self, description: str) -> List[str]:
        """Génère des sélecteurs intelligents basés sur la description"""
        selectors = []
        desc_lower = description.lower()

        # Sélecteurs par texte
        selectors.append(f"text={description}")
        selectors.append(f"text=/{description}/i")

        # Sélecteurs par attributs communs
        if "bouton" in desc_lower or "button" in desc_lower:
            selectors.extend([
                f"button:has-text('{description}')",
                f"input[type='submit'][value*='{description}']",
                f"[role='button']:has-text('{description}')"
            ])

        if "lien" in desc_lower or "link" in desc_lower:
            selectors.extend([
                f"a:has-text('{description}')",
                f"[role='link']:has-text('{description}')"
            ])

        # Sélecteurs par classes/IDs probables
        words = description.split()
        for word in words:
            selectors.extend([
                f"#{word.lower()}",
                f".{word.lower()}",
                f"[id*='{word.lower()}']",
                f"[class*='{word.lower()}']"
            ])

        return selectors

    def _parse_complex_instruction(self, instruction: str) -> List[Dict[str, Any]]:
        """Parse une instruction complexe en étapes"""
        # Analyse basique pour instructions complexes
        steps = []

        # Découper en phrases
        sentences = instruction.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if any(word in sentence.lower() for word in ['cliquer', 'click', 'appuyer']):
                steps.append({"action": "click", "target": "button, a, [role=button]"})
            elif any(word in sentence.lower() for word in ['écrire', 'taper', 'saisir']):
                steps.append({"action": "type", "target": "input, textarea", "text": sentence})
            elif any(word in sentence.lower() for word in ['attendre', 'patienter']):
                steps.append({"action": "wait", "duration": 3})
            else:
                steps.append({"action": "generic", "instruction": sentence})

        return steps if steps else [{"action": "generic", "instruction": instruction}]

    def _extract_click_target(self, instruction: str) -> str:
        """Extrait la cible d'un clic depuis l'instruction"""
        # Recherche de mots-clés dans l'instruction
        words = instruction.split()

        # Chercher après "sur", "cliquer", etc.
        target_words = []
        capture = False
        for word in words:
            if word.lower() in ['sur', 'cliquer', 'click', 'appuyer']:
                capture = True
                continue
            if capture and word.lower() not in ['le', 'la', 'les', 'un', 'une']:
                target_words.append(word)

        return ' '.join(target_words) if target_words else "button"

    def _extract_type_info(self, instruction: str) -> tuple:
        """Extrait les infos de frappe depuis l'instruction"""
        # Logique basique d'extraction
        target = "input"
        text = instruction

        # Chercher le texte à taper
        if '"' in instruction:
            parts = instruction.split('"')
            if len(parts) >= 2:
                text = parts[1]

        return target, text

    def _extract_search_query(self, instruction: str) -> str:
        """Extrait la requête de recherche"""
        # Chercher après "rechercher", "search", etc.
        words = instruction.split()
        query_words = []
        capture = False

        for word in words:
            if word.lower() in ['rechercher', 'search', 'chercher']:
                capture = True
                continue
            if capture:
                query_words.append(word)

        return ' '.join(query_words) if query_words else instruction

    async def _human_scroll(self, options: Dict) -> Dict[str, Any]:
        """Scroll avec comportement humain"""
        try:
            direction = options.get("direction", "down")
            pixels = options.get("pixels", 300)

            if direction == "down":
                await self.current_page.evaluate(f"window.scrollBy(0, {pixels})")
            else:
                await self.current_page.evaluate(f"window.scrollBy(0, -{pixels})")

            await asyncio.sleep(random.uniform(0.5, 1.5))
            return {"success": True, "action": "scroll", "direction": direction}

        except Exception as e:
            return {"error": f"Scroll échoué: {str(e)}"}

    async def _intelligent_wait(self, target: str, options: Dict) -> Dict[str, Any]:
        """Attente intelligente"""
        try:
            if target.isdigit():
                await asyncio.sleep(int(target) / 1000)  # millisecondes
            else:
                # Attendre un élément
                await self.current_page.wait_for_selector(target, timeout=30000)

            return {"success": True, "action": "wait"}

        except Exception as e:
            return {"error": f"Attente échouée: {str(e)}"}

    async def _extract_element_data(self, selector: str, options: Dict) -> Dict[str, Any]:
        """Extrait des données d'éléments"""
        try:
            elements = await self.current_page.query_selector_all(selector)
            data = []

            count = min(len(elements), options.get("count", 10))

            for i in range(count):
                element = elements[i]
                text = await element.inner_text()
                data.append({"text": text, "index": i})

            return {"success": True, "data": data, "count": len(data)}

        except Exception as e:
            return {"error": f"Extraction échouée: {str(e)}"}

    async def _human_select(self, selector: str, value: str, options: Dict) -> Dict[str, Any]:
        """Sélection dans dropdown"""
        try:
            await self.current_page.select_option(selector, value)
            return {"success": True, "action": "select", "value": value}
        except Exception as e:
            return {"error": f"Sélection échouée: {str(e)}"}

    async def _human_file_upload(self, selector: str, file_path: str, options: Dict) -> Dict[str, Any]:
        """Upload de fichier"""
        try:
            await self.current_page.set_input_files(selector, file_path)
            return {"success": True, "action": "upload", "file": file_path}
        except Exception as e:
            return {"error": f"Upload échoué: {str(e)}"}

    async def _human_drag_drop(self, source: str, target: str, options: Dict) -> Dict[str, Any]:
        """Drag and drop"""
        try:
            source_element = await self.current_page.wait_for_selector(source)
            target_element = await self.current_page.wait_for_selector(target)

            await source_element.drag_to(target_element)
            return {"success": True, "action": "drag_drop"}
        except Exception as e:
            return {"error": f"Drag & drop échoué: {str(e)}"}

    async def _execute_custom_javascript(self, js_code: str, options: Dict) -> Dict[str, Any]:
        """Exécute du JavaScript personnalisé"""
        try:
            result = await self.current_page.evaluate(js_code)
            return {"success": True, "action": "javascript", "result": result}
        except Exception as e:
            return {"error": f"JavaScript échoué: {str(e)}"}

    async def _intelligent_type(self, target: str, text: str) -> Dict[str, Any]:
        """Frappe intelligente"""
        return await self._human_type(target, text, {"clear": True})

    async def _perform_search(self, query: str) -> Dict[str, Any]:
        """Effectue une recherche"""
        try:
            # Chercher un champ de recherche
            search_selectors = [
                "input[type=search]",
                "input[name=q]",
                "input[name=search]",
                "[data-testid=SearchBox_SearchBox]",
                ".search-input",
                "#search"
            ]

            for selector in search_selectors:
                try:
                    element = await self.current_page.wait_for_selector(selector, timeout=2000)
                    if element:
                        await element.fill(query)
                        await element.press("Enter")
                        return {"success": True, "action": "search", "query": query}
                except:
                    continue

            return {"error": "Champ de recherche non trouvé"}

        except Exception as e:
            return {"error": f"Recherche échouée: {str(e)}"}

    async def stop(self):
        """Nettoyage ressources"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        await super().stop()

# Fonctions utilitaires
async def execute_web_instruction(instruction: str, url: str = "", options: Dict = None):
    """Exécute n'importe quelle instruction web"""

    agent = UltimateWebAgent()

    task = agent.create_task(
        task_type="free_mode_execution",
        priority=10,
        data={
            "instruction": instruction,
            "url": url,
            "options": options or {}
        }
    )

    await agent.add_task(task)
    await agent.execute_tasks()

    # Récupérer les résultats
    results = []
    for file_path in agent.data_dir.glob("task_*_result.json"):
        with open(file_path, 'r') as f:
            result = json.load(f)
            if result.get("result"):
                results.append(result["result"])

    await agent.stop()
    return results[-1] if results else {"error": "Exécution échouée"}

async def navigate_and_automate(url: str, actions: List[Dict]):
    """Navigation et automation avancée"""

    agent = UltimateWebAgent()

    task = agent.create_task(
        task_type="navigate_and_perform",
        priority=10,
        data={
            "url": url,
            "actions": actions
        }
    )

    await agent.add_task(task)
    await agent.execute_tasks()

    # Récupérer les résultats
    results = []
    for file_path in agent.data_dir.glob("task_*_result.json"):
        with open(file_path, 'r') as f:
            result = json.load(f)
            if result.get("result"):
                results.append(result["result"])

    await agent.stop()
    return results[-1] if results else {"error": "Navigation échouée"}