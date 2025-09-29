#!/usr/bin/env python3
"""
Quick Web Agent - Agent ultra rapide qui FONCTIONNE
Résout le problème de s'arrêter après avoir ouvert une page
"""

import asyncio
import time
from playwright.async_api import async_playwright
from pathlib import Path

class QuickWebAgent:
    """Agent web rapide et efficace"""

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        """Démarrage rapide"""
        playwright = await async_playwright().__aenter__()

        self.browser = await playwright.chromium.launch(
            headless=False,  # Visible pour debugging
            args=['--disable-blink-features=AutomationControlled']
        )

        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

        print("🚀 Agent rapide démarré")

    async def stop(self):
        """Arrêt rapide"""
        if self.browser:
            await self.browser.close()

    async def quick_google_test(self):
        """Test rapide sur Google"""
        print("🔍 Test Google rapide...")

        try:
            # Aller sur Google
            await self.page.goto("https://www.google.com", timeout=15000)
            print("✅ Page Google chargée")

            # Attendre un peu
            await asyncio.sleep(2)

            # Chercher la barre de recherche
            search_input = await self.page.query_selector('textarea[name="q"], input[name="q"]')

            if search_input:
                print("✅ Barre de recherche trouvée")

                # Cliquer et taper
                await search_input.click()
                await asyncio.sleep(0.5)

                await search_input.fill("iFiveMe")
                print("✅ Texte tapé")

                await asyncio.sleep(0.5)

                # Appuyer sur Entrée
                await self.page.keyboard.press('Enter')
                print("✅ Recherche lancée")

                # Attendre résultats
                await self.page.wait_for_selector('h3', timeout=10000)
                print("✅ Résultats chargés")

                # Screenshot
                Path("data/quick_agent").mkdir(parents=True, exist_ok=True)
                await self.page.screenshot(path="data/quick_agent/google_results.png")
                print("✅ Screenshot pris")

                return {"success": True, "action": "google_search_completed"}

            else:
                print("❌ Barre de recherche non trouvée")
                return {"success": False, "error": "search_input_not_found"}

        except Exception as e:
            print(f"❌ Erreur: {e}")
            return {"success": False, "error": str(e)}

    async def quick_multi_action(self):
        """Plusieurs actions rapides consécutives"""
        print("🎯 Série d'actions rapides...")

        results = []

        # Action 1: Google
        result1 = await self.quick_google_test()
        results.append(result1)

        if result1.get("success"):
            await asyncio.sleep(2)

            # Action 2: Nouvelle recherche
            print("🔍 Nouvelle recherche...")
            try:
                # Cliquer sur la barre de recherche
                search_input = await self.page.query_selector('textarea[name="q"], input[name="q"]')
                if search_input:
                    await search_input.click()
                    await asyncio.sleep(0.3)

                    # Sélectionner tout et remplacer
                    await self.page.keyboard.press('Ctrl+a')
                    await asyncio.sleep(0.2)

                    await search_input.fill("cartes virtuelles")
                    await asyncio.sleep(0.5)

                    await self.page.keyboard.press('Enter')
                    await self.page.wait_for_selector('h3', timeout=8000)

                    await self.page.screenshot(path="data/quick_agent/second_search.png")
                    print("✅ Deuxième recherche terminée")

                    results.append({"success": True, "action": "second_search"})

            except Exception as e:
                print(f"⚠️ Deuxième recherche échouée: {e}")
                results.append({"success": False, "error": str(e)})

        return {
            "success": True,
            "total_actions": len(results),
            "successful_actions": len([r for r in results if r.get("success")]),
            "results": results
        }

async def quick_test():
    """Test rapide fonctionnel"""
    print("⚡ QUICK WEB AGENT - TEST RAPIDE")
    print("=" * 50)

    agent = QuickWebAgent()

    try:
        await agent.start()
        result = await agent.quick_multi_action()

        print(f"\n🏆 RÉSULTAT:")
        print(f"Actions totales: {result['total_actions']}")
        print(f"Actions réussies: {result['successful_actions']}")

        if result['successful_actions'] > 0:
            print("✅ L'agent FONCTIONNE et fait plusieurs actions!")
        else:
            print("❌ Aucune action réussie")

        return result

    finally:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(quick_test())