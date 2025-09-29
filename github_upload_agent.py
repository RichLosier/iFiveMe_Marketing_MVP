#!/usr/bin/env python3
"""
🚀 Agent Upload GitHub Automatique - iFiveMe
Upload intelligent par batches pour contourner limite 100 fichiers
"""

import asyncio
import os
import time
from playwright.async_api import async_playwright
from pathlib import Path
import glob

class GitHubUploadAgent:
    def __init__(self):
        self.page = None
        self.browser = None
        self.repo_url = "https://github.com/RichLosier/iFiveMe_Marketing_MVP"
        self.base_path = Path("/Users/richardlosier/Desktop/iFiveMe_Marketing_MVP")

    async def setup_browser(self):
        """Configure navigateur pour GitHub"""
        print("🔧 Configuration navigateur GitHub...")

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
        )

        context = await self.browser.new_context()
        self.page = await context.new_page()

    async def navigate_to_repo(self):
        """Navigue vers le dépôt GitHub"""
        print("🌐 Navigation vers dépôt GitHub...")
        await self.page.goto(self.repo_url)
        await self.page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

    async def create_folder_and_upload(self, folder_path, files_batch):
        """Crée un dossier et upload un batch de fichiers"""
        try:
            folder_name = folder_path.name
            print(f"📁 Upload du dossier: {folder_name} ({len(files_batch)} fichiers)")

            # Cliquer "Create new file"
            await self.page.click('text="Create new file"')
            await asyncio.sleep(2)

            # Taper le nom du dossier + fichier temporaire
            await self.page.fill('input[placeholder="Name your file..."]', f"{folder_name}/temp.md")
            await asyncio.sleep(1)

            # Ajouter contenu temporaire
            await self.page.fill('textarea[placeholder="Enter file contents here"]', "# Temporary file")

            # Commit
            await self.page.click('button:has-text("Commit changes")')
            await asyncio.sleep(3)

            # Maintenant uploader les vrais fichiers dans ce dossier
            await self.upload_files_to_folder(folder_name, files_batch)

            return True

        except Exception as e:
            print(f"❌ Erreur création dossier {folder_name}: {e}")
            return False

    async def upload_files_to_folder(self, folder_name, files_batch):
        """Upload fichiers dans un dossier existant"""
        try:
            # Naviguer vers le dossier
            await self.page.click(f'text="{folder_name}"')
            await asyncio.sleep(2)

            # Cliquer "Upload files"
            upload_button = await self.page.wait_for_selector('text="Upload files"', timeout=5000)
            await upload_button.click()
            await asyncio.sleep(2)

            # Upload par batch de 50 fichiers max
            for i in range(0, len(files_batch), 50):
                batch = files_batch[i:i+50]
                print(f"  📤 Upload batch {i//50 + 1}: {len(batch)} fichiers")

                # Sélectionner les fichiers
                file_input = await self.page.wait_for_selector('input[type="file"]')
                await file_input.set_input_files([str(f) for f in batch])
                await asyncio.sleep(3)

                # Commit si c'est le dernier batch
                if i + 50 >= len(files_batch):
                    await self.page.fill('input[placeholder="Add files via upload"]', f"📁 Upload {folder_name}")
                    await self.page.click('button:has-text("Commit changes")')
                    await asyncio.sleep(5)

        except Exception as e:
            print(f"❌ Erreur upload fichiers: {e}")

    async def upload_root_files(self):
        """Upload fichiers à la racine"""
        try:
            print("📄 Upload fichiers racine...")

            # Fichiers importants à la racine
            root_files = [
                "ifiveme_control_tower.py",
                "requirements.txt",
                "package.json",
                "Dockerfile",
                "render.yaml",
                "README.md",
                ".gitignore"
            ]

            existing_files = []
            for filename in root_files:
                file_path = self.base_path / filename
                if file_path.exists():
                    existing_files.append(file_path)

            if existing_files:
                # Cliquer "Upload files"
                await self.page.click('text="Upload files"')
                await asyncio.sleep(2)

                # Upload files
                file_input = await self.page.wait_for_selector('input[type="file"]')
                await file_input.set_input_files([str(f) for f in existing_files])
                await asyncio.sleep(3)

                # Commit
                await self.page.fill('input[placeholder="Add files via upload"]', "🚀 Upload fichiers racine iFiveMe")
                await self.page.click('button:has-text("Commit changes")')
                await asyncio.sleep(5)

            return True

        except Exception as e:
            print(f"❌ Erreur upload racine: {e}")
            return False

    async def organize_and_upload(self):
        """Organisation intelligente et upload par dossiers"""
        try:
            print("📊 Analyse structure projet...")

            # Dossiers principaux à uploader
            folders_to_upload = [
                ("agents", "*.py"),
                ("config", "*.py"),
                ("data", "*"),
                ("web_approval", "*"),
                ("utils", "*.py")
            ]

            # Upload fichiers racine d'abord
            await self.upload_root_files()
            await asyncio.sleep(3)

            # Upload chaque dossier
            for folder_name, pattern in folders_to_upload:
                folder_path = self.base_path / folder_name
                if folder_path.exists():
                    # Trouver tous les fichiers
                    files = list(folder_path.rglob(pattern))
                    if files:
                        await self.create_folder_and_upload(folder_path, files)
                        await asyncio.sleep(5)

            print("✅ Upload complet terminé!")
            return True

        except Exception as e:
            print(f"❌ Erreur organisation upload: {e}")
            return False

    async def run(self):
        """Processus principal"""
        try:
            print("🚀 DÉMARRAGE AGENT UPLOAD GITHUB")
            print("="*50)

            await self.setup_browser()
            await self.navigate_to_repo()
            await self.organize_and_upload()

            print("🎉 UPLOAD GITHUB TERMINÉ AVEC SUCCÈS!")
            input("Appuyez sur ENTRÉE pour fermer...")

        except Exception as e:
            print(f"❌ Erreur agent upload: {e}")
        finally:
            if self.browser:
                await self.browser.close()

async def main():
    agent = GitHubUploadAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())