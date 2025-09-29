from playwright.sync_api import sync_playwright
import time

def deploy_to_render():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("🚀 Navigation vers Render.com...")
        page.goto("https://render.com")

        # Attendre chargement
        page.wait_for_selector("body")
        time.sleep(3)

        print("🔍 Recherche bouton New+...")

        # Chercher différents sélecteurs pour "New" ou "Create"
        selectors = [
            'button:has-text("New")',
            'a:has-text("New")',
            '[data-testid*="new"]',
            'button:has-text("Create")',
            '.new-button',
            '[aria-label*="New"]'
        ]

        for selector in selectors:
            try:
                button = page.query_selector(selector)
                if button:
                    print(f"✅ Bouton trouvé: {selector}")
                    button.click()
                    time.sleep(2)
                    break
            except:
                continue
        else:
            print("⚠️ Bouton New non trouvé automatiquement")
            input("Cliquez manuellement sur 'New +' puis appuyez ENTRÉE...")

        print("🔍 Recherche 'Web Service'...")

        # Chercher "Web Service"
        web_service_selectors = [
            'text="Web Service"',
            'a:has-text("Web Service")',
            'button:has-text("Web Service")',
            '[data-testid*="web-service"]'
        ]

        for selector in web_service_selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    print(f"✅ Web Service trouvé: {selector}")
                    element.click()
                    time.sleep(2)
                    break
            except:
                continue
        else:
            print("⚠️ Web Service non trouvé")
            input("Cliquez sur 'Web Service' puis appuyez ENTRÉE...")

        print("🔗 Recherche connexion GitHub...")

        # Chercher connexion repo
        github_selectors = [
            'text="Connect a repository"',
            'button:has-text("Connect")',
            'a:has-text("GitHub")',
            '[data-testid*="connect"]'
        ]

        for selector in github_selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    print(f"✅ Connexion GitHub trouvée: {selector}")
                    element.click()
                    time.sleep(3)
                    break
            except:
                continue
        else:
            print("⚠️ Connexion GitHub non trouvée")
            input("Connectez votre repo GitHub puis appuyez ENTRÉE...")

        print("📂 Recherche du repo iFiveMe_Marketing_MVP...")

        # Chercher le repo
        repo_selectors = [
            'text="iFiveMe_Marketing_MVP"',
            '[data-testid*="ifiveme"]',
            'a:has-text("iFiveMe")'
        ]

        for selector in repo_selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    print(f"✅ Repo trouvé: {selector}")
                    element.click()
                    time.sleep(2)
                    break
            except:
                continue
        else:
            print("⚠️ Repo iFiveMe non trouvé")
            input("Sélectionnez 'iFiveMe_Marketing_MVP' puis appuyez ENTRÉE...")

        print("⚙️ Configuration des paramètres...")
        input("Configurez manuellement:\nBuild: pip install -r requirements.txt\nStart: python ifiveme_control_tower.py\nPuis appuyez ENTRÉE...")

        print("🚀 Recherche bouton Deploy/Create...")

        deploy_selectors = [
            'button:has-text("Create Web Service")',
            'button:has-text("Deploy")',
            'input[type="submit"]',
            '[data-testid*="create"]'
        ]

        for selector in deploy_selectors:
            try:
                button = page.query_selector(selector)
                if button:
                    print(f"✅ Bouton deploy trouvé: {selector}")
                    button.click()
                    print("🎉 DÉPLOIEMENT LANCÉ!")
                    time.sleep(5)
                    break
            except:
                continue
        else:
            print("⚠️ Bouton deploy non trouvé")
            input("Cliquez sur 'Create Web Service' puis appuyez ENTRÉE...")

        print("✅ PROCESSUS TERMINÉ!")
        print("🌐 Votre application iFiveMe sera disponible dans quelques minutes!")

        input("Appuyez ENTRÉE pour fermer...")
        browser.close()

if __name__ == "__main__":
    deploy_to_render()