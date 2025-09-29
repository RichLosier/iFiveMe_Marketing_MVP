#!/usr/bin/env python3
"""
⚡ Upload GitHub Ultra-Rapide - iFiveMe
Upload direct via API GitHub sans navigateur (10000x plus rapide)
"""

import os
import base64
import requests
import json
from pathlib import Path

class LightningGitHubUpload:
    def __init__(self):
        self.repo_owner = "RichLosier"
        self.repo_name = "iFiveMe_Marketing_MVP"
        self.base_path = Path("/Users/richardlosier/Desktop/iFiveMe_Marketing_MVP")

        # GitHub token - vous devez le créer
        self.token = None

    def setup_auth(self):
        """Configuration rapide authentification"""
        print("🔑 CONFIGURATION RAPIDE:")
        print("1. Allez sur: https://github.com/settings/tokens")
        print("2. 'Generate new token (classic)'")
        print("3. Cochez 'repo' scope")
        print("4. Copiez le token généré")

        self.token = input("\n🔐 Collez votre token GitHub: ").strip()
        return bool(self.token)

    def upload_file(self, file_path, github_path):
        """Upload un fichier via API GitHub"""
        try:
            with open(file_path, 'rb') as f:
                content = base64.b64encode(f.read()).decode()

            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{github_path}"

            data = {
                "message": f"📁 Upload {github_path}",
                "content": content
            }

            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }

            response = requests.put(url, json=data, headers=headers)

            if response.status_code == 201:
                print(f"✅ {github_path}")
                return True
            else:
                print(f"❌ {github_path}: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Erreur {file_path}: {e}")
            return False

    def get_important_files(self):
        """Sélectionne seulement les fichiers essentiels"""
        important_files = []

        # Fichiers racine critiques
        root_files = [
            "ifiveme_control_tower.py",
            "requirements.txt",
            "package.json",
            "Dockerfile",
            "render.yaml",
            "README.md"
        ]

        for filename in root_files:
            file_path = self.base_path / filename
            if file_path.exists():
                important_files.append((file_path, filename))

        # Agents (seulement les principaux)
        agents_dir = self.base_path / "agents"
        if agents_dir.exists():
            key_agents = [
                "ultimate_web_agent.py",
                "ifiveme_action_agent.py",
                "observe_think_act_agent.py",
                "social_media_publisher_agent.py"
            ]

            for agent_file in key_agents:
                agent_path = agents_dir / agent_file
                if agent_path.exists():
                    important_files.append((agent_path, f"agents/{agent_file}"))

        # Config essentiel
        config_dir = self.base_path / "config"
        if config_dir.exists():
            for config_file in config_dir.glob("*.py"):
                rel_path = f"config/{config_file.name}"
                important_files.append((config_file, rel_path))

        return important_files

    def ultra_fast_upload(self):
        """Upload ultra-rapide fichiers essentiels"""
        print("⚡ UPLOAD ULTRA-RAPIDE EN COURS...")

        files_to_upload = self.get_important_files()
        print(f"📁 {len(files_to_upload)} fichiers essentiels sélectionnés")

        success_count = 0
        for file_path, github_path in files_to_upload:
            if self.upload_file(file_path, github_path):
                success_count += 1

        print(f"\n🎉 {success_count}/{len(files_to_upload)} fichiers uploadés avec succès!")
        return success_count > 0

    def run(self):
        """Processus ultra-rapide"""
        print("⚡ LIGHTNING GITHUB UPLOAD - IFIVEME")
        print("="*50)

        if not self.setup_auth():
            print("❌ Token requis pour continuer")
            return False

        return self.ultra_fast_upload()

def main():
    uploader = LightningGitHubUpload()

    if uploader.run():
        print("\n✅ SUCCESS! Dépôt GitHub prêt pour Render.com")
        print("🚀 Prochaine étape: Configuration Render.com")
    else:
        print("\n❌ Erreur upload - réessayez")

if __name__ == "__main__":
    main()