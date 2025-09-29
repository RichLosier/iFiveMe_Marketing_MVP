#!/usr/bin/env python3
"""
🚀 Agent de Configuration Render.com pour iFiveMe
Navigue sur Render.com et aide à créer un compte pour déployer le système iFiveMe
"""

import asyncio
import os
from playwright.async_api import async_playwright
import time

class RenderSetupAgent:
    def __init__(self):
        self.page = None
        self.browser = None

    async def setup_browser(self, headless=False):
        """Configure le navigateur avec paramètres optimaux"""
        self.playwright = await async_playwright().start()

        # Lanceur Chrome avec paramètres humains
        self.browser = await self.playwright.chromium.launch(
            headless=headless,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',  # Plus rapide
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        )

        # Context avec permissions
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        self.page = await context.new_page()

        # Remove webdriver detection
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

    async def navigate_to_render(self):
        """Navigue vers Render.com"""
        try:
            print("🌐 Navigation vers Render.com...")
            await self.page.goto('https://render.com', wait_until='networkidle')

            # Attendre que la page soit chargée
            await self.page.wait_for_selector('h1, .hero, [data-testid="hero"]', timeout=10000)

            # Screenshot pour documenter
            await self.page.screenshot(path='data/render_setup/render_homepage.png')
            print("✅ Page d'accueil Render.com chargée")

            return True

        except Exception as e:
            print(f"❌ Erreur navigation Render.com: {e}")
            return False

    async def find_signup_button(self):
        """Trouve et clique sur le bouton d'inscription"""
        try:
            print("🔍 Recherche du bouton d'inscription...")

            # Plusieurs sélecteurs possibles pour "Sign Up"
            signup_selectors = [
                'a:has-text("Sign up")',
                'button:has-text("Sign up")',
                'a:has-text("Get started")',
                'button:has-text("Get started")',
                '[data-testid="signup"]',
                '.signup-button',
                'a[href*="signup"]',
                'a[href*="register"]'
            ]

            for selector in signup_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=2000)
                    print(f"✅ Bouton d'inscription trouvé: {selector}")
                    await self.page.click(selector)
                    await self.page.wait_for_load_state('networkidle')
                    return True
                except:
                    continue

            print("⚠️ Bouton d'inscription non trouvé automatiquement")
            return False

        except Exception as e:
            print(f"❌ Erreur recherche bouton inscription: {e}")
            return False

    async def wait_for_signup_form(self):
        """Attend et identifie le formulaire d'inscription"""
        try:
            print("⏳ Attente du formulaire d'inscription...")

            # Sélecteurs pour formulaire d'inscription
            form_selectors = [
                'form[action*="signup"]',
                'form[action*="register"]',
                'input[type="email"]',
                'input[name="email"]',
                '[data-testid="email-input"]'
            ]

            for selector in form_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=3000)
                    print(f"✅ Formulaire d'inscription détecté: {selector}")

                    # Screenshot du formulaire
                    await self.page.screenshot(path='data/render_setup/signup_form.png')
                    return True
                except:
                    continue

            print("⚠️ Formulaire d'inscription non détecté")
            return False

        except Exception as e:
            print(f"❌ Erreur attente formulaire: {e}")
            return False

    async def analyze_page(self):
        """Analyse la page actuelle et donne des instructions"""
        try:
            print("🔍 Analyse de la page actuelle...")

            # Obtenir le titre et l'URL
            title = await self.page.title()
            url = self.page.url

            print(f"📄 Titre: {title}")
            print(f"🌐 URL: {url}")

            # Chercher les éléments d'inscription
            signup_elements = await self.page.query_selector_all('a:has-text("Sign up"), button:has-text("Sign up"), a:has-text("Get started")')

            if signup_elements:
                print(f"✅ {len(signup_elements)} éléments d'inscription trouvés")
                for i, element in enumerate(signup_elements):
                    text = await element.text_content()
                    print(f"  {i+1}. {text}")
            else:
                print("⚠️ Aucun élément d'inscription évident trouvé")

            # Chercher les champs de formulaire
            email_inputs = await self.page.query_selector_all('input[type="email"], input[name="email"]')
            if email_inputs:
                print(f"📧 {len(email_inputs)} champs email trouvés")

            # Screenshot final
            await self.page.screenshot(path='data/render_setup/current_page.png')

            return True

        except Exception as e:
            print(f"❌ Erreur analyse page: {e}")
            return False

    async def interactive_mode(self):
        """Mode interactif pour laisser l'utilisateur continuer"""
        print("\n" + "="*60)
        print("🎯 RENDER.COM OUVERT - PRÊT POUR INSCRIPTION MANUELLE")
        print("="*60)
        print("📋 ÉTAPES SUIVANTES À FAIRE MANUELLEMENT:")
        print("1. Cliquez sur 'Sign Up' ou 'Get Started'")
        print("2. Remplissez le formulaire avec:")
        print("   - Email: richard@ifiveme.com")
        print("   - Nom: Richard Losier")
        print("   - Mot de passe sécurisé")
        print("3. Confirmez la création du compte")
        print("4. Une fois connecté, revenez ici")
        print("="*60)

        # Garder le navigateur ouvert
        input("⏳ Appuyez sur ENTRÉE quand vous avez terminé l'inscription...")

    async def run(self):
        """Processus principal de configuration Render"""
        try:
            # Créer répertoire de données
            os.makedirs('data/render_setup', exist_ok=True)

            print("🚀 Démarrage Agent Configuration Render.com")
            print("="*50)

            # Setup navigateur (visible pour interaction)
            await self.setup_browser(headless=False)

            # Navigation vers Render
            if await self.navigate_to_render():
                await self.analyze_page()

                # Tentative automatique de trouver inscription
                if not await self.find_signup_button():
                    print("⚠️ Navigation automatique impossible")

                # Mode interactif
                await self.interactive_mode()

            print("✅ Session Render.com terminée")

        except Exception as e:
            print(f"❌ Erreur agent Render: {e}")
        finally:
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Point d'entrée principal"""
    agent = RenderSetupAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())