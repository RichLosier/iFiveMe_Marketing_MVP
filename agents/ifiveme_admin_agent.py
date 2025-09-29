#!/usr/bin/env python3
"""
Agent Admin iFiveMe - Connexion et Analyse Complète
Se connecte à admin.ifiveme.com et analyse toute la structure
"""

import asyncio
import json
import time
from pathlib import Path
from playwright.async_api import async_playwright

class iFiveMeAdminAgent:
    """Agent spécialisé pour admin.ifiveme.com"""

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.site_structure = {}
        self.credentials = {
            "email": "richard@ifiveme.com",
            "password": "bonjour"
        }

    async def start(self):
        """Démarrage agent admin"""
        playwright = await async_playwright().__aenter__()

        self.browser = await playwright.chromium.launch(
            headless=False,  # Visible pour voir la connexion
            slow_mo=500
        )

        # Context avec session persistante
        self.context = await self.browser.new_context(
            viewport={"width": 1400, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )

        self.page = await self.context.new_page()
        print("🚀 Agent Admin iFiveMe démarré")

    async def stop(self):
        """Arrêt propre"""
        if self.browser:
            await self.browser.close()

    async def login_to_admin(self):
        """Connexion à l'admin iFiveMe"""
        print("🔐 CONNEXION À ADMIN.IFIVEME.COM")
        print("=" * 50)

        try:
            # Navigation vers admin
            print("🌐 Navigation vers admin.ifiveme.com...")
            await self.page.goto("https://admin.ifiveme.com", timeout=30000)
            await asyncio.sleep(2)

            # Screenshot page de connexion
            Path("data/ifiveme_admin").mkdir(parents=True, exist_ok=True)
            await self.page.screenshot(path="data/ifiveme_admin/01_login_page.png")
            print("✅ Page de connexion chargée")

            # Chercher le formulaire de connexion
            print("🔍 Recherche des champs de connexion...")

            # Différentes possibilités de sélecteurs
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[name="username"]',
                'input[placeholder*="email"]',
                '#email',
                '#username',
                '.email',
                '[data-testid="email"]'
            ]

            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                '#password',
                '.password',
                '[data-testid="password"]'
            ]

            # Trouver le champ email
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = await self.page.wait_for_selector(selector, timeout=3000)
                    if email_field:
                        print(f"✅ Champ email trouvé avec: {selector}")
                        break
                except:
                    continue

            if not email_field:
                print("❌ Champ email non trouvé, analyse de la page...")
                page_content = await self.page.content()
                print("Page HTML:", page_content[:500])
                return {"success": False, "error": "Champ email non trouvé"}

            # Trouver le champ password
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = await self.page.wait_for_selector(selector, timeout=3000)
                    if password_field:
                        print(f"✅ Champ password trouvé avec: {selector}")
                        break
                except:
                    continue

            if not password_field:
                print("❌ Champ password non trouvé")
                return {"success": False, "error": "Champ password non trouvé"}

            # Saisie des credentials
            print("⌨️ Saisie email...")
            await email_field.click()
            await asyncio.sleep(0.5)
            await email_field.fill(self.credentials["email"])
            print(f"✅ Email saisi: {self.credentials['email']}")

            print("⌨️ Saisie password...")
            await password_field.click()
            await asyncio.sleep(0.5)
            await password_field.fill(self.credentials["password"])
            print("✅ Password saisi")

            await asyncio.sleep(1)

            # Chercher le bouton de connexion
            print("🔍 Recherche bouton de connexion...")
            login_button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Connexion")',
                'button:has-text("Se connecter")',
                'button:has-text("Login")',
                'button:has-text("Sign in")',
                '.login-button',
                '#login-button',
                '[data-testid="login"]'
            ]

            login_button = None
            for selector in login_button_selectors:
                try:
                    login_button = await self.page.wait_for_selector(selector, timeout=2000)
                    if login_button:
                        print(f"✅ Bouton connexion trouvé: {selector}")
                        break
                except:
                    continue

            if login_button:
                print("🚀 Clic sur bouton de connexion...")
                await login_button.click()
            else:
                print("🚀 Tentative Enter sur password...")
                await self.page.keyboard.press('Enter')

            # Attendre redirection après login
            print("⏳ Attente redirection après connexion...")
            await asyncio.sleep(5)

            # Vérifier si connecté
            current_url = self.page.url
            print(f"📍 URL actuelle: {current_url}")

            await self.page.screenshot(path="data/ifiveme_admin/02_after_login.png")

            if "login" in current_url.lower() or "signin" in current_url.lower():
                print("❌ Connexion échouée - Toujours sur page login")

                # Vérifier s'il y a des messages d'erreur
                try:
                    error_elements = await self.page.query_selector_all('.error, .alert, .danger, [role="alert"]')
                    for error in error_elements:
                        error_text = await error.inner_text()
                        print(f"⚠️ Erreur détectée: {error_text}")
                except:
                    pass

                return {"success": False, "error": "Connexion échouée", "url": current_url}
            else:
                print("✅ CONNEXION RÉUSSIE!")
                return {"success": True, "url": current_url}

        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            await self.page.screenshot(path="data/ifiveme_admin/error_login.png")
            return {"success": False, "error": str(e)}

    async def analyze_site_structure(self):
        """Analyse complète de la structure du site admin"""
        print("\n🔍 ANALYSE STRUCTURE SITE ADMIN")
        print("=" * 50)

        structure = {
            "url": self.page.url,
            "title": await self.page.title(),
            "navigation": [],
            "main_sections": [],
            "forms": [],
            "buttons": [],
            "tables": [],
            "statistics": [],
            "user_info": {},
            "available_actions": []
        }

        try:
            # 1. Analyser la navigation
            print("📋 Analyse navigation...")
            nav_elements = await self.page.query_selector_all('nav a, .nav a, .menu a, .sidebar a, [role="navigation"] a')

            for nav in nav_elements:
                try:
                    text = await nav.inner_text()
                    href = await nav.get_attribute('href')
                    if text.strip():
                        structure["navigation"].append({
                            "text": text.strip(),
                            "href": href,
                            "type": "navigation"
                        })
                        print(f"  📌 Menu: {text.strip()} -> {href}")
                except:
                    continue

            # 2. Analyser les sections principales
            print("📋 Analyse sections principales...")
            sections = await self.page.query_selector_all('main, .main, .content, .dashboard, section, .panel, .card')

            for i, section in enumerate(sections[:10]):
                try:
                    text = await section.inner_text()
                    if len(text) > 20:  # Seulement sections avec du contenu
                        structure["main_sections"].append({
                            "index": i,
                            "content_preview": text[:100] + "..." if len(text) > 100 else text,
                            "element_count": len(await section.query_selector_all('*'))
                        })
                        print(f"  📑 Section {i}: {text[:50]}...")
                except:
                    continue

            # 3. Analyser les formulaires
            print("📋 Analyse formulaires...")
            forms = await self.page.query_selector_all('form')

            for i, form in enumerate(forms):
                try:
                    inputs = await form.query_selector_all('input, select, textarea')
                    action = await form.get_attribute('action')
                    method = await form.get_attribute('method')

                    form_data = {
                        "index": i,
                        "action": action,
                        "method": method,
                        "inputs": []
                    }

                    for input_elem in inputs:
                        input_type = await input_elem.get_attribute('type')
                        input_name = await input_elem.get_attribute('name')
                        input_placeholder = await input_elem.get_attribute('placeholder')

                        form_data["inputs"].append({
                            "type": input_type,
                            "name": input_name,
                            "placeholder": input_placeholder
                        })

                    structure["forms"].append(form_data)
                    print(f"  📝 Form {i}: {len(form_data['inputs'])} inputs, action: {action}")
                except:
                    continue

            # 4. Analyser les boutons d'action
            print("📋 Analyse boutons d'action...")
            buttons = await self.page.query_selector_all('button, .btn, input[type="button"], input[type="submit"]')

            for button in buttons:
                try:
                    text = await button.inner_text()
                    onclick = await button.get_attribute('onclick')
                    btn_type = await button.get_attribute('type')

                    if text.strip():
                        structure["buttons"].append({
                            "text": text.strip(),
                            "type": btn_type,
                            "onclick": onclick,
                            "action_type": self._classify_button_action(text)
                        })
                        print(f"  🔘 Button: {text.strip()} ({self._classify_button_action(text)})")
                except:
                    continue

            # 5. Analyser les tableaux de données
            print("📋 Analyse tableaux...")
            tables = await self.page.query_selector_all('table, .table, .data-table')

            for i, table in enumerate(tables):
                try:
                    headers = await table.query_selector_all('th')
                    rows = await table.query_selector_all('tr')

                    header_texts = []
                    for header in headers:
                        header_text = await header.inner_text()
                        header_texts.append(header_text.strip())

                    structure["tables"].append({
                        "index": i,
                        "headers": header_texts,
                        "row_count": len(rows),
                        "data_type": self._classify_table_type(header_texts)
                    })
                    print(f"  📊 Table {i}: {len(rows)} lignes, Type: {self._classify_table_type(header_texts)}")
                except:
                    continue

            # 6. Chercher des statistiques/KPI
            print("📋 Recherche statistiques...")
            stat_elements = await self.page.query_selector_all('.stat, .kpi, .metric, .count, .number, [class*="stat"]')

            for stat in stat_elements:
                try:
                    text = await stat.inner_text()
                    if any(char.isdigit() for char in text):
                        structure["statistics"].append({
                            "text": text.strip(),
                            "type": "metric"
                        })
                        print(f"  📈 Stat: {text.strip()}")
                except:
                    continue

            # 7. Informations utilisateur
            print("📋 Recherche info utilisateur...")
            user_elements = await self.page.query_selector_all('.user, .profile, .account, [class*="user"], [class*="profile"]')

            for user_elem in user_elements:
                try:
                    text = await user_elem.inner_text()
                    if "richard" in text.lower() or "@" in text:
                        structure["user_info"]["display"] = text.strip()
                        print(f"  👤 User info: {text.strip()}")
                except:
                    continue

            # Screenshot de l'analyse
            await self.page.screenshot(path="data/ifiveme_admin/03_structure_analysis.png", full_page=True)

            # Sauvegarder la structure
            with open("data/ifiveme_admin/site_structure.json", "w", encoding="utf-8") as f:
                json.dump(structure, f, indent=2, ensure_ascii=False)

            print(f"\n✅ ANALYSE TERMINÉE:")
            print(f"  📌 {len(structure['navigation'])} éléments de navigation")
            print(f"  📑 {len(structure['main_sections'])} sections principales")
            print(f"  📝 {len(structure['forms'])} formulaires")
            print(f"  🔘 {len(structure['buttons'])} boutons d'action")
            print(f"  📊 {len(structure['tables'])} tableaux")
            print(f"  📈 {len(structure['statistics'])} statistiques")

            self.site_structure = structure
            return structure

        except Exception as e:
            print(f"❌ Erreur analyse: {e}")
            return {"error": str(e)}

    def _classify_button_action(self, text):
        """Classifie le type d'action d'un bouton"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['save', 'sauvegarder', 'enregistrer']):
            return "save"
        elif any(word in text_lower for word in ['delete', 'supprimer', 'remove']):
            return "delete"
        elif any(word in text_lower for word in ['edit', 'modifier', 'update']):
            return "edit"
        elif any(word in text_lower for word in ['create', 'créer', 'nouveau', 'add']):
            return "create"
        elif any(word in text_lower for word in ['export', 'download', 'télécharger']):
            return "export"
        else:
            return "other"

    def _classify_table_type(self, headers):
        """Classifie le type de tableau selon ses headers"""
        headers_text = " ".join(headers).lower()
        if any(word in headers_text for word in ['user', 'utilisateur', 'client']):
            return "users"
        elif any(word in headers_text for word in ['card', 'carte', 'profile']):
            return "cards"
        elif any(word in headers_text for word in ['order', 'commande', 'transaction']):
            return "orders"
        elif any(word in headers_text for word in ['stat', 'analytics', 'metric']):
            return "analytics"
        else:
            return "data"

    async def explore_navigation(self):
        """Explore chaque section de navigation"""
        print("\n🗺️ EXPLORATION NAVIGATION")
        print("=" * 50)

        explored_sections = {}

        for i, nav_item in enumerate(self.site_structure.get("navigation", [])):
            try:
                print(f"\n📍 Exploration: {nav_item['text']}")

                if nav_item['href']:
                    # Navigation vers la section
                    if nav_item['href'].startswith('http'):
                        await self.page.goto(nav_item['href'])
                    else:
                        base_url = "https://admin.ifiveme.com"
                        full_url = base_url + nav_item['href'] if not nav_item['href'].startswith('/') else base_url + nav_item['href']
                        await self.page.goto(full_url)

                    await asyncio.sleep(2)

                    # Analyse de cette section
                    section_data = {
                        "url": self.page.url,
                        "title": await self.page.title(),
                        "content_preview": "",
                        "forms": [],
                        "tables": [],
                        "buttons": []
                    }

                    # Contenu principal
                    main_content = await self.page.query_selector('main, .main, .content, body')
                    if main_content:
                        content_text = await main_content.inner_text()
                        section_data["content_preview"] = content_text[:200] + "..." if len(content_text) > 200 else content_text

                    # Screenshot
                    await self.page.screenshot(path=f"data/ifiveme_admin/section_{i}_{nav_item['text'].replace(' ', '_')}.png")

                    explored_sections[nav_item['text']] = section_data
                    print(f"✅ Section explorée: {nav_item['text']}")

                if i >= 5:  # Limiter à 5 sections pour éviter trop long
                    break

            except Exception as e:
                print(f"⚠️ Erreur exploration {nav_item['text']}: {e}")
                continue

        return explored_sections

    async def complete_analysis(self):
        """Analyse complète du site admin"""
        print("🎯 ANALYSE COMPLÈTE ADMIN.IFIVEME.COM")
        print("=" * 60)

        # 1. Connexion
        login_result = await self.login_to_admin()
        if not login_result.get("success"):
            return login_result

        await asyncio.sleep(2)

        # 2. Analyse structure principale
        structure = await self.analyze_site_structure()

        await asyncio.sleep(2)

        # 3. Exploration navigation
        navigation_data = await self.explore_navigation()

        # 4. Rapport final
        final_report = {
            "login_success": True,
            "site_structure": structure,
            "navigation_explored": navigation_data,
            "capabilities": self._identify_capabilities(structure),
            "recommended_actions": self._suggest_actions(structure)
        }

        # Sauvegarder rapport complet
        with open("data/ifiveme_admin/complete_analysis.json", "w", encoding="utf-8") as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)

        print("\n" + "="*60)
        print("🏆 ANALYSE COMPLÈTE TERMINÉE")
        print("="*60)

        print(f"✅ Connexion réussie à admin.ifiveme.com")
        print(f"📊 Structure analysée: {len(structure.get('navigation', []))} sections")
        print(f"🗺️ Navigation explorée: {len(navigation_data)} pages")

        print(f"\n🎯 CAPACITÉS IDENTIFIÉES:")
        for capability in final_report["capabilities"]:
            print(f"  ✅ {capability}")

        print(f"\n💡 ACTIONS RECOMMANDÉES:")
        for action in final_report["recommended_actions"]:
            print(f"  🚀 {action}")

        print(f"\n📁 FICHIERS GÉNÉRÉS:")
        print(f"  📸 Screenshots dans data/ifiveme_admin/")
        print(f"  📋 site_structure.json - Structure complète")
        print(f"  📄 complete_analysis.json - Rapport final")

        return final_report

    def _identify_capabilities(self, structure):
        """Identifie les capacités disponibles"""
        capabilities = []

        # Basé sur la navigation
        nav_texts = [nav["text"].lower() for nav in structure.get("navigation", [])]

        if any("user" in text or "client" in text for text in nav_texts):
            capabilities.append("Gestion des utilisateurs/clients")

        if any("card" in text or "carte" in text for text in nav_texts):
            capabilities.append("Gestion des cartes virtuelles")

        if any("order" in text or "commande" in text for text in nav_texts):
            capabilities.append("Gestion des commandes")

        if any("stat" in text or "analyt" in text for text in nav_texts):
            capabilities.append("Analytics et statistiques")

        if any("setting" in text or "config" in text for text in nav_texts):
            capabilities.append("Configuration système")

        # Basé sur les boutons
        button_actions = set(btn["action_type"] for btn in structure.get("buttons", []))
        if "create" in button_actions:
            capabilities.append("Création d'éléments")
        if "edit" in button_actions:
            capabilities.append("Modification d'éléments")
        if "delete" in button_actions:
            capabilities.append("Suppression d'éléments")
        if "export" in button_actions:
            capabilities.append("Export de données")

        return capabilities

    def _suggest_actions(self, structure):
        """Suggère des actions possibles"""
        suggestions = []

        if len(structure.get("tables", [])) > 0:
            suggestions.append("Extraire données des tableaux")

        if len(structure.get("forms", [])) > 0:
            suggestions.append("Automatiser remplissage de formulaires")

        if any(btn["action_type"] == "export" for btn in structure.get("buttons", [])):
            suggestions.append("Automatiser les exports de données")

        if len(structure.get("statistics", [])) > 0:
            suggestions.append("Surveiller les métriques automatiquement")

        suggestions.append("Navigation automatique entre sections")
        suggestions.append("Screenshots périodiques pour monitoring")

        return suggestions

# Fonction d'utilisation simple
async def analyze_ifiveme_admin():
    """Lance l'analyse complète de admin.ifiveme.com"""
    agent = iFiveMeAdminAgent()

    try:
        await agent.start()
        result = await agent.complete_analysis()
        return result
    finally:
        await agent.stop()

if __name__ == "__main__":
    print("🚀 DÉMARRAGE ANALYSE ADMIN IFIVEME")
    result = asyncio.run(analyze_ifiveme_admin())

    if result.get("login_success"):
        print("\n🎉 MISSION ACCOMPLIE!")
        print("L'agent connaît maintenant parfaitement votre site admin.")
        print("Prêt à exécuter vos actions spécifiques ! 🚀")
    else:
        print(f"\n❌ Problème: {result.get('error')}")