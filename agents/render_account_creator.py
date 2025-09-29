#!/usr/bin/env python3
"""
🚀 Agent Création Compte Render.com pour iFiveMe
Automatise la création de compte sur Render.com avec interaction guidée
"""

import asyncio
import os
from playwright.async_api import async_playwright
import time
import random

class RenderAccountCreator:
    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None

    async def setup_browser(self):
        """Configure un navigateur avec comportement humain"""
        print("🔧 Configuration navigateur...")

        self.playwright = await async_playwright().start()

        # Configuration navigateur réaliste
        self.browser = await self.playwright.chromium.launch(
            headless=False,  # Mode visible pour interaction
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--no-sandbox',
                '--disable-web-security',
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        )

        # Context avec permissions réalistes
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            extra_http_headers={
                'Accept-Language': 'fr-CA,fr;q=0.9,en;q=0.8',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
        )

        self.page = await self.context.new_page()

        # Supprimer détection webdriver
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });

            // Masquer playwright
            delete window.playwright;
            delete window.__playwright;

            // Ajouter propriétés manquantes
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """)

    async def human_delay(self, min_ms=500, max_ms=2000):
        """Délai humain aléatoire"""
        delay = random.randint(min_ms, max_ms) / 1000
        await asyncio.sleep(delay)

    async def navigate_to_render(self):
        """Navigue vers Render.com avec gestion d'erreurs"""
        try:
            print("🌐 Navigation vers Render.com...")
            await self.page.goto('https://render.com', timeout=30000)

            # Attendre chargement complet
            await self.page.wait_for_load_state('networkidle')
            await self.human_delay(1000, 3000)

            # Screenshot documentation
            os.makedirs('data/render_setup', exist_ok=True)
            await self.page.screenshot(path='data/render_setup/01_homepage.png')

            print("✅ Page Render.com chargée")
            return True

        except Exception as e:
            print(f"❌ Erreur navigation: {e}")
            return False

    async def find_and_click_signup(self):
        """Trouve et clique sur le bouton d'inscription"""
        try:
            print("🔍 Recherche bouton d'inscription...")

            # Attendre que la page soit entièrement chargée
            await self.human_delay(2000, 4000)

            # Multiples sélecteurs pour Sign Up
            signup_selectors = [
                'text=Sign up',
                'text=Get Started',
                'a[href*="signup"]',
                'button:has-text("Sign up")',
                'a:has-text("Sign up")',
                '[data-testid*="signup"]',
                '.signup',
                '#signup'
            ]

            for selector in signup_selectors:
                try:
                    print(f"  🔍 Tentative: {selector}")
                    element = await self.page.wait_for_selector(selector, timeout=3000)

                    if element:
                        # Scroll vers l'élément
                        await element.scroll_into_view_if_needed()
                        await self.human_delay(500, 1500)

                        # Clic avec comportement humain
                        await element.click()
                        print(f"✅ Bouton cliqué: {selector}")

                        # Attendre navigation
                        await self.page.wait_for_load_state('networkidle')
                        await self.human_delay(1000, 2000)

                        await self.page.screenshot(path='data/render_setup/02_after_signup_click.png')
                        return True

                except:
                    continue

            # Si aucun bouton trouvé, analyser la page
            print("⚠️ Aucun bouton d'inscription automatique trouvé")
            await self.analyze_current_page()
            return False

        except Exception as e:
            print(f"❌ Erreur recherche bouton: {e}")
            return False

    async def analyze_current_page(self):
        """Analyse la page actuelle et guide l'utilisateur"""
        try:
            print("\n" + "="*60)
            print("🔍 ANALYSE DE LA PAGE ACTUELLE")
            print("="*60)

            # Titre et URL
            title = await self.page.title()
            url = self.page.url
            print(f"📄 Titre: {title}")
            print(f"🌐 URL: {url}")

            # Chercher tous les liens et boutons
            links = await self.page.query_selector_all('a')
            buttons = await self.page.query_selector_all('button')

            print(f"\n🔗 {len(links)} liens trouvés:")
            for i, link in enumerate(links[:10]):  # Limiter à 10
                try:
                    text = await link.text_content()
                    href = await link.get_attribute('href')
                    if text and text.strip():
                        print(f"  {i+1}. {text.strip()[:50]} → {href}")
                except:
                    continue

            print(f"\n🔘 {len(buttons)} boutons trouvés:")
            for i, button in enumerate(buttons[:10]):
                try:
                    text = await button.text_content()
                    if text and text.strip():
                        print(f"  {i+1}. {text.strip()[:50]}")
                except:
                    continue

            # Screenshot final
            await self.page.screenshot(path='data/render_setup/03_page_analysis.png')

            return True

        except Exception as e:
            print(f"❌ Erreur analyse: {e}")
            return False

    async def wait_for_signup_form(self):
        """Détecte et analyse le formulaire d'inscription"""
        try:
            print("📋 Recherche formulaire d'inscription...")

            # Sélecteurs de formulaires
            form_selectors = [
                'input[type="email"]',
                'input[name*="email"]',
                'input[placeholder*="email"]',
                'input[placeholder*="Email"]',
                'form'
            ]

            for selector in form_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=3000)
                    print(f"✅ Élément formulaire trouvé: {selector}")

                    # Screenshot du formulaire
                    await self.page.screenshot(path='data/render_setup/04_signup_form.png')
                    return True
                except:
                    continue

            return False

        except Exception as e:
            print(f"❌ Erreur détection formulaire: {e}")
            return False

    async def guide_manual_signup(self):
        """Guide l'utilisateur pour l'inscription manuelle"""
        print("\n" + "="*70)
        print("🎯 GUIDE D'INSCRIPTION MANUELLE RENDER.COM")
        print("="*70)
        print("📋 INFORMATIONS À UTILISER:")
        print("   📧 Email: richard@ifiveme.com")
        print("   👤 Nom: Richard Losier")
        print("   🏢 Entreprise: iFiveMe")
        print("   🔑 Mot de passe: [Choisissez un mot de passe sécurisé]")
        print("\n🔍 ÉTAPES À SUIVRE DANS LE NAVIGATEUR:")
        print("1. Cherchez un bouton 'Sign Up', 'Get Started' ou similaire")
        print("2. Cliquez dessus pour accéder au formulaire")
        print("3. Remplissez avec les informations ci-dessus")
        print("4. Confirmez votre email si requis")
        print("5. Une fois connecté, revenez ici")
        print("="*70)

        # Garder navigateur ouvert
        input("⏳ Appuyez sur ENTRÉE quand vous avez terminé l'inscription...")

        # Vérifier si on est connecté
        await self.check_if_logged_in()

    async def check_if_logged_in(self):
        """Vérifie si l'utilisateur est maintenant connecté"""
        try:
            print("🔍 Vérification connexion...")

            # Actualiser la page
            await self.page.reload()
            await self.page.wait_for_load_state('networkidle')

            # Chercher indicateurs de connexion
            logged_in_selectors = [
                'text=Dashboard',
                'text=New',
                'text=Services',
                'text=Account',
                'text=Profile',
                '[data-testid*="dashboard"]',
                'button:has-text("New")'
            ]

            for selector in logged_in_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=2000)
                    print(f"✅ Connexion détectée: {selector}")

                    await self.page.screenshot(path='data/render_setup/05_logged_in.png')
                    print("🎉 COMPTE RENDER.COM CRÉÉ ET CONNECTÉ !")
                    return True
                except:
                    continue

            print("⚠️ Connexion non détectée, l'inscription pourrait ne pas être terminée")
            await self.page.screenshot(path='data/render_setup/06_login_check.png')
            return False

        except Exception as e:
            print(f"❌ Erreur vérification connexion: {e}")
            return False

    async def run(self):
        """Processus principal de création de compte"""
        try:
            print("🚀 DÉMARRAGE AGENT CRÉATION COMPTE RENDER.COM")
            print("="*55)

            # Setup navigateur
            await self.setup_browser()

            # Navigation vers Render
            if not await self.navigate_to_render():
                print("❌ Impossible d'accéder à Render.com")
                return False

            # Tentative clic automatique
            if not await self.find_and_click_signup():
                print("⚠️ Clic automatique échoué, passage en mode manuel")

            # Attendre formulaire
            await self.wait_for_signup_form()

            # Guide manuel
            await self.guide_manual_signup()

            print("✅ PROCESSUS TERMINÉ")
            return True

        except Exception as e:
            print(f"❌ Erreur agent création compte: {e}")
            return False
        finally:
            # Laisser navigateur ouvert pour utilisation
            print("🌐 Navigateur laissé ouvert pour utilisation continue...")

async def main():
    """Point d'entrée"""
    agent = RenderAccountCreator()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())