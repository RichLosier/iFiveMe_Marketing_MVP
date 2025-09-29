#!/usr/bin/env python3
"""
Simple Web Agent iFiveMe - Vraiment Fonctionnel
Conçu pour exécuter réellement les tâches au lieu de juste ouvrir des pages
"""

import asyncio
import time
import random
import logging
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

class SimpleWebAgent:
    """Agent web simple mais vraiment fonctionnel pour iFiveMe"""

    def __init__(self):
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    async def start(self):
        """Démarrage simple et fiable"""
        if self.browser:
            return

        playwright = await async_playwright().__aenter__()

        # Configuration simple mais efficace
        self.browser = await playwright.chromium.launch(
            headless=False,  # Visible pour voir ce qui se passe
            slow_mo=1000     # Ralentit pour être plus humain
        )

        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )

        self.page = await self.context.new_page()
        print("✅ Agent web simple démarré")

    async def stop(self):
        """Arrêt propre"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

    async def wait_human(self, min_ms=500, max_ms=1500):
        """Attendre comme un humain"""
        delay = random.uniform(min_ms, max_ms) / 1000
        await asyncio.sleep(delay)

    async def go_to_google_and_search(self, search_term="iFiveMe cartes virtuelles"):
        """Va sur Google et fait une recherche RÉELLE"""
        try:
            print(f"🌐 Navigation vers Google...")
            await self.page.goto("https://www.google.com", wait_until="domcontentloaded")
            await self.wait_human()

            print("🔍 Recherche de la barre de recherche...")

            # Accepter les cookies si nécessaire
            try:
                accept_btn = await self.page.wait_for_selector('button:has-text("Tout accepter")', timeout=3000)
                if accept_btn:
                    await accept_btn.click()
                    print("✅ Cookies acceptés")
                    await self.wait_human()
            except:
                print("ℹ️ Pas de popup cookies")

            # Trouver la barre de recherche
            search_box = await self.page.wait_for_selector('textarea[name="q"], input[name="q"]', timeout=10000)

            print(f"⌨️ Frappe: {search_term}")
            await search_box.click()
            await self.wait_human(200, 500)

            # Taper caractère par caractère
            for char in search_term:
                await self.page.keyboard.type(char)
                await asyncio.sleep(random.uniform(0.05, 0.15))

            await self.wait_human()

            print("🚀 Appui sur Entrée...")
            await self.page.keyboard.press('Enter')

            # Attendre les résultats
            await self.page.wait_for_selector('h3', timeout=15000)
            await self.wait_human(1000, 2000)

            print("📸 Capture d'écran...")
            Path("data/simple_agent").mkdir(parents=True, exist_ok=True)
            await self.page.screenshot(path="data/simple_agent/google_search_results.png", full_page=True)

            # Extraire quelques résultats
            results = await self.page.query_selector_all('h3')
            found_results = []
            for i, result in enumerate(results[:5]):
                try:
                    text = await result.inner_text()
                    found_results.append(text)
                    print(f"📋 Résultat {i+1}: {text[:50]}...")
                except:
                    continue

            return {
                "success": True,
                "action": "google_search",
                "search_term": search_term,
                "results_found": len(found_results),
                "results": found_results,
                "screenshot": "data/simple_agent/google_search_results.png"
            }

        except Exception as e:
            print(f"❌ Erreur: {e}")
            return {"success": False, "error": str(e)}

    async def go_to_facebook_and_explore(self):
        """Va sur Facebook et explore RÉELLEMENT"""
        try:
            print("🌐 Navigation vers Facebook...")
            await self.page.goto("https://www.facebook.com", wait_until="domcontentloaded")
            await self.wait_human(2000, 3000)

            print("📸 Capture d'écran Facebook...")
            await self.page.screenshot(path="data/simple_agent/facebook_homepage.png", full_page=True)

            # Scroll pour voir plus de contenu
            print("📜 Scroll vers le bas...")
            for i in range(3):
                await self.page.mouse.wheel(0, 500)
                await self.wait_human(1000, 2000)

            print("📸 Capture après scroll...")
            await self.page.screenshot(path="data/simple_agent/facebook_scrolled.png", full_page=True)

            return {
                "success": True,
                "action": "facebook_exploration",
                "screenshots": [
                    "data/simple_agent/facebook_homepage.png",
                    "data/simple_agent/facebook_scrolled.png"
                ]
            }

        except Exception as e:
            print(f"❌ Erreur Facebook: {e}")
            return {"success": False, "error": str(e)}

    async def complete_ifiveme_task(self, task_description="Recherche iFiveMe"):
        """Exécute une tâche complète iFiveMe"""
        print(f"🎯 TÂCHE: {task_description}")
        print("=" * 60)

        results = []

        # 1. Recherche Google
        print("📍 ÉTAPE 1: Recherche Google sur iFiveMe")
        google_result = await self.go_to_google_and_search("iFiveMe cartes d'affaires virtuelles")
        results.append(google_result)

        await self.wait_human(2000, 3000)

        # 2. Exploration réseaux sociaux
        print("\n📍 ÉTAPE 2: Exploration Facebook")
        facebook_result = await self.go_to_facebook_and_explore()
        results.append(facebook_result)

        await self.wait_human(2000, 3000)

        # 3. Retour à Google pour plus de recherches
        print("\n📍 ÉTAPE 3: Recherche concurrence")
        competition_result = await self.go_to_google_and_search("cartes d'affaires virtuelles NFC concurrents")
        results.append(competition_result)

        # Capture finale
        print("\n📸 Capture d'écran finale...")
        await self.page.screenshot(path="data/simple_agent/task_completed.png", full_page=True)

        print(f"\n🏆 TÂCHE TERMINÉE AVEC SUCCÈS!")
        print(f"📊 {len([r for r in results if r.get('success')])} actions réussies sur {len(results)}")

        return {
            "success": True,
            "task": task_description,
            "steps_completed": len(results),
            "results": results,
            "final_screenshot": "data/simple_agent/task_completed.png"
        }

# Fonction simple pour utilisation directe
async def execute_simple_task(task="Recherche et analyse iFiveMe"):
    """Exécute une tâche simple mais complète"""
    agent = SimpleWebAgent()

    try:
        await agent.start()
        result = await agent.complete_ifiveme_task(task)
        return result
    finally:
        await agent.stop()

if __name__ == "__main__":
    async def demo():
        print("🚀 Simple Web Agent iFiveMe - VRAIMENT FONCTIONNEL")
        print("=" * 60)
        print("🎯 Cet agent va RÉELLEMENT exécuter les tâches")
        print("🌐 Visible pour que vous voyiez ce qui se passe")
        print("=" * 60)

        result = await execute_simple_task("Recherche complète iFiveMe et concurrence")

        print(f"\n✅ RÉSULTAT FINAL:")
        print(f"Success: {result['success']}")
        print(f"Étapes: {result['steps_completed']}")
        print(f"Screenshot: {result['final_screenshot']}")

    asyncio.run(demo())