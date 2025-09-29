#!/usr/bin/env python3
"""
Agent d'Action iFiveMe Admin
Exécute des actions spécifiques basées sur l'analyse du site
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

class iFiveMeActionAgent:
    """Agent pour exécuter des actions spécifiques sur admin.ifiveme.com"""

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.site_structure = None
        self.is_logged_in = False
        self.credentials = {
            "email": "richard@ifiveme.com",
            "password": "bonjour"
        }

    async def start(self):
        """Démarrage et connexion"""
        playwright = await async_playwright().__aenter__()

        self.browser = await playwright.chromium.launch(
            headless=False,
            slow_mo=300
        )

        self.context = await self.browser.new_context(
            viewport={"width": 1400, "height": 900}
        )

        self.page = await self.context.new_page()

        # Charger la structure du site si disponible
        await self._load_site_structure()

        print("🚀 Agent d'Action iFiveMe prêt")

    async def stop(self):
        """Arrêt propre"""
        if self.browser:
            await self.browser.close()

    async def _load_site_structure(self):
        """Charge la structure du site depuis l'analyse précédente"""
        try:
            structure_file = Path("data/ifiveme_admin/site_structure.json")
            if structure_file.exists():
                with open(structure_file, "r", encoding="utf-8") as f:
                    self.site_structure = json.load(f)
                print("✅ Structure du site chargée")
            else:
                print("ℹ️ Structure du site non disponible - Analyse requise")
        except:
            print("⚠️ Erreur chargement structure")

    async def login(self):
        """Connexion rapide à l'admin"""
        if self.is_logged_in:
            return True

        print("🔐 Connexion à admin.ifiveme.com...")

        try:
            await self.page.goto("https://admin.ifiveme.com")
            await asyncio.sleep(2)

            # Connexion rapide
            email_field = await self.page.wait_for_selector('input[type="email"], input[name="email"], input[name="username"]')
            password_field = await self.page.wait_for_selector('input[type="password"]')

            await email_field.fill(self.credentials["email"])
            await password_field.fill(self.credentials["password"])

            await self.page.keyboard.press('Enter')
            await asyncio.sleep(3)

            # Vérifier connexion
            if "login" not in self.page.url.lower():
                print("✅ Connexion réussie")
                self.is_logged_in = True
                return True
            else:
                print("❌ Connexion échouée")
                return False

        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            return False

    async def navigate_to_section(self, section_name):
        """Navigation vers une section spécifique"""
        await self.login()

        print(f"🧭 Navigation vers: {section_name}")

        if self.site_structure:
            # Chercher dans la navigation
            for nav_item in self.site_structure.get("navigation", []):
                if section_name.lower() in nav_item["text"].lower():
                    try:
                        href = nav_item["href"]
                        if href:
                            if href.startswith('http'):
                                await self.page.goto(href)
                            else:
                                base_url = "https://admin.ifiveme.com"
                                full_url = base_url + href
                                await self.page.goto(full_url)

                            await asyncio.sleep(2)
                            print(f"✅ Navigation vers {section_name} réussie")
                            return True
                    except Exception as e:
                        print(f"⚠️ Erreur navigation: {e}")

        # Fallback: chercher le lien sur la page
        try:
            link = await self.page.wait_for_selector(f'a:has-text("{section_name}")', timeout=5000)
            await link.click()
            await asyncio.sleep(2)
            print(f"✅ Navigation par lien réussie")
            return True
        except:
            print(f"❌ Section {section_name} non trouvée")
            return False

    async def extract_table_data(self, section_name=None):
        """Extrait les données d'un tableau"""
        if section_name:
            await self.navigate_to_section(section_name)

        print("📊 Extraction données tableau...")

        try:
            # Chercher le premier tableau visible
            table = await self.page.wait_for_selector('table', timeout=10000)

            # Extraire les headers
            headers = []
            header_elements = await table.query_selector_all('th')
            for header in header_elements:
                text = await header.inner_text()
                headers.append(text.strip())

            # Extraire les lignes
            rows_data = []
            row_elements = await table.query_selector_all('tbody tr, tr')

            for row in row_elements[:10]:  # Limiter à 10 premières lignes
                cells = await row.query_selector_all('td, th')
                row_data = []

                for cell in cells:
                    text = await cell.inner_text()
                    row_data.append(text.strip())

                if row_data and len(row_data) > 1:  # Éviter lignes vides
                    rows_data.append(row_data)

            extracted_data = {
                "headers": headers,
                "rows": rows_data,
                "total_rows": len(rows_data)
            }

            # Sauvegarder
            Path("data/ifiveme_admin/actions").mkdir(parents=True, exist_ok=True)
            timestamp = int(asyncio.get_event_loop().time())

            with open(f"data/ifiveme_admin/actions/table_data_{timestamp}.json", "w", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)

            await self.page.screenshot(path=f"data/ifiveme_admin/actions/table_screenshot_{timestamp}.png")

            print(f"✅ Données extraites: {len(headers)} colonnes, {len(rows_data)} lignes")
            return extracted_data

        except Exception as e:
            print(f"❌ Erreur extraction: {e}")
            return None

    async def fill_form(self, form_data, section_name=None):
        """Remplit un formulaire avec les données fournies"""
        if section_name:
            await self.navigate_to_section(section_name)

        print(f"📝 Remplissage formulaire...")

        try:
            # Trouver le formulaire
            form = await self.page.wait_for_selector('form', timeout=10000)

            filled_fields = 0

            for field_name, value in form_data.items():
                try:
                    # Différents types de sélecteurs
                    selectors = [
                        f'input[name="{field_name}"]',
                        f'select[name="{field_name}"]',
                        f'textarea[name="{field_name}"]',
                        f'#{field_name}',
                        f'input[placeholder*="{field_name}"]'
                    ]

                    field = None
                    for selector in selectors:
                        try:
                            field = await self.page.wait_for_selector(selector, timeout=2000)
                            if field:
                                break
                        except:
                            continue

                    if field:
                        element_type = await field.evaluate('el => el.tagName.toLowerCase()')

                        if element_type == 'select':
                            await field.select_option(value=str(value))
                        elif element_type in ['input', 'textarea']:
                            await field.fill(str(value))

                        filled_fields += 1
                        print(f"  ✅ {field_name}: {value}")

                except Exception as e:
                    print(f"  ⚠️ {field_name}: {e}")

            await self.page.screenshot(path=f"data/ifiveme_admin/actions/form_filled_{int(asyncio.get_event_loop().time())}.png")

            print(f"✅ Formulaire rempli: {filled_fields} champs")
            return {"success": True, "fields_filled": filled_fields}

        except Exception as e:
            print(f"❌ Erreur remplissage: {e}")
            return {"success": False, "error": str(e)}

    async def click_button(self, button_text, section_name=None):
        """Clique sur un bouton spécifique"""
        if section_name:
            await self.navigate_to_section(section_name)

        print(f"🔘 Recherche bouton: {button_text}")

        try:
            # Différents sélecteurs possibles
            selectors = [
                f'button:has-text("{button_text}")',
                f'input[value="{button_text}"]',
                f'a:has-text("{button_text}")',
                f'[role="button"]:has-text("{button_text}")',
                f'button[title="{button_text}"]'
            ]

            button = None
            for selector in selectors:
                try:
                    button = await self.page.wait_for_selector(selector, timeout=3000)
                    if button:
                        break
                except:
                    continue

            if button:
                await button.click()
                await asyncio.sleep(2)

                await self.page.screenshot(path=f"data/ifiveme_admin/actions/button_clicked_{int(asyncio.get_event_loop().time())}.png")

                print(f"✅ Bouton '{button_text}' cliqué")
                return {"success": True, "action": "click", "button": button_text}
            else:
                print(f"❌ Bouton '{button_text}' non trouvé")
                return {"success": False, "error": "Button not found"}

        except Exception as e:
            print(f"❌ Erreur clic: {e}")
            return {"success": False, "error": str(e)}

    async def export_data(self, section_name=None):
        """Cherche et déclenche un export de données"""
        if section_name:
            await self.navigate_to_section(section_name)

        print("📤 Recherche fonction d'export...")

        export_buttons = [
            "Export", "Exporter", "Download", "Télécharger",
            "CSV", "Excel", "PDF", "Export Data"
        ]

        for button_text in export_buttons:
            result = await self.click_button(button_text)
            if result.get("success"):
                print(f"✅ Export déclenché via: {button_text}")
                return result

        print("❌ Fonction d'export non trouvée")
        return {"success": False, "error": "No export function found"}

    async def monitor_statistics(self):
        """Surveille et extrait les statistiques/métriques"""
        await self.login()

        print("📈 Surveillance statistiques...")

        try:
            # Chercher des éléments de statistiques
            stat_selectors = [
                '.stat', '.kpi', '.metric', '.count', '.number',
                '[class*="stat"]', '[class*="kpi"]', '[class*="metric"]',
                '.dashboard-stat', '.widget-stat'
            ]

            all_stats = []

            for selector in stat_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        text = await element.inner_text()
                        if text.strip() and any(char.isdigit() for char in text):
                            all_stats.append({
                                "selector": selector,
                                "value": text.strip(),
                                "timestamp": asyncio.get_event_loop().time()
                            })
                except:
                    continue

            # Sauvegarder stats
            timestamp = int(asyncio.get_event_loop().time())
            with open(f"data/ifiveme_admin/actions/stats_{timestamp}.json", "w", encoding="utf-8") as f:
                json.dump(all_stats, f, indent=2, ensure_ascii=False)

            await self.page.screenshot(path=f"data/ifiveme_admin/actions/stats_screenshot_{timestamp}.png")

            print(f"✅ {len(all_stats)} statistiques extraites")
            return all_stats

        except Exception as e:
            print(f"❌ Erreur surveillance: {e}")
            return []

    async def execute_custom_action(self, action_description):
        """Exécute une action personnalisée basée sur la description"""
        await self.login()

        print(f"🎯 Action personnalisée: {action_description}")

        action_lower = action_description.lower()

        # Actions de données
        if "extract" in action_lower or "données" in action_lower:
            return await self.extract_table_data()

        # Actions d'export
        elif "export" in action_lower or "télécharger" in action_lower:
            return await self.export_data()

        # Actions de statistiques
        elif "stat" in action_lower or "métrique" in action_lower:
            return await self.monitor_statistics()

        # Actions de navigation
        elif "aller" in action_lower or "navigate" in action_lower:
            # Extraire le nom de section
            for nav_item in self.site_structure.get("navigation", []) if self.site_structure else []:
                if nav_item["text"].lower() in action_lower:
                    return await self.navigate_to_section(nav_item["text"])

        # Screenshot général
        else:
            timestamp = int(asyncio.get_event_loop().time())
            await self.page.screenshot(path=f"data/ifiveme_admin/actions/custom_action_{timestamp}.png", full_page=True)
            return {"success": True, "action": "screenshot", "description": action_description}

# Fonction d'utilisation simple
async def execute_ifiveme_action(action_description):
    """Exécute une action sur admin.ifiveme.com"""
    agent = iFiveMeActionAgent()

    try:
        await agent.start()
        result = await agent.execute_custom_action(action_description)
        return result
    finally:
        await agent.stop()

if __name__ == "__main__":
    # Test d'action
    action = "Extraire les données des utilisateurs"
    print(f"🧪 Test action: {action}")
    result = asyncio.run(execute_ifiveme_action(action))
    print(f"Résultat: {result}")