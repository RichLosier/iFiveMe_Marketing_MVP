#!/usr/bin/env python3
"""
🧠 Intelligent GitHub Sync - iFiveMe Marketing MVP
Upload intelligent automatique avec gestion d'erreurs et optimisation
"""

import os
import subprocess
import sys
from pathlib import Path
import time

class IntelligentGitHubSync:
    def __init__(self):
        self.project_path = Path("/Users/richardlosier/Desktop/iFiveMe_Marketing_MVP")
        self.repo_url = "https://github.com/RichLosier/iFiveMe_Marketing_MVP"

    def run_command(self, command, description=""):
        """Execute command with intelligent error handling"""
        try:
            print(f"🔄 {description}")
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print(f"✅ {description} - Succès")
                return True, result.stdout
            else:
                print(f"❌ {description} - Erreur: {result.stderr}")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            print(f"⏱️ {description} - Timeout")
            return False, "Command timeout"
        except Exception as e:
            print(f"💥 {description} - Exception: {e}")
            return False, str(e)

    def setup_git_credentials(self):
        """Configure git avec token GitHub intelligent"""
        print("🔑 Configuration authentification GitHub...")

        # Instructions pour obtenir token
        print("\n" + "="*60)
        print("📋 AUTHENTIFICATION GITHUB REQUISE:")
        print("1. Ouvrez: https://github.com/settings/tokens")
        print("2. Cliquez 'Generate new token (classic)'")
        print("3. Donnez un nom: 'iFiveMe Upload Token'")
        print("4. Cochez les scopes: 'repo', 'workflow'")
        print("5. Cliquez 'Generate token'")
        print("6. COPIEZ le token généré (il ne sera plus affiché)")
        print("="*60 + "\n")

        # Demander token de façon sécurisée
        import getpass
        token = getpass.getpass("🔐 Collez votre token GitHub (masqué): ").strip()

        if not token:
            print("❌ Token requis pour continuer")
            return False

        # Configurer remote avec token
        remote_url = f"https://{token}@github.com/RichLosier/iFiveMe_Marketing_MVP.git"

        success, _ = self.run_command(
            f"git remote set-url origin {remote_url}",
            "Configuration remote avec authentification"
        )

        return success

    def analyze_files_to_upload(self):
        """Analyse intelligente des fichiers à uploader"""
        print("🔍 Analyse structure projet...")

        # Fichiers critiques pour Render.com
        critical_files = [
            "ifiveme_control_tower.py",  # Application principale
            "requirements.txt",          # Dépendances Python
            "Dockerfile",               # Container Docker
            "render.yaml",              # Configuration Render
            "package.json",             # Dépendances Node.js
        ]

        # Dossiers essentiels
        essential_folders = [
            "agents/",          # Tous les agents AI
            "config/",          # Configuration système
            "web_approval/",    # Interface web
            "utils/",           # Utilitaires
        ]

        files_status = {}

        # Vérifier fichiers critiques
        for file in critical_files:
            file_path = self.project_path / file
            files_status[file] = {
                'exists': file_path.exists(),
                'size': file_path.stat().st_size if file_path.exists() else 0,
                'critical': True
            }

        # Analyser dossiers
        for folder in essential_folders:
            folder_path = self.project_path / folder
            if folder_path.exists():
                files_in_folder = list(folder_path.rglob("*.py"))
                files_status[folder] = {
                    'exists': True,
                    'file_count': len(files_in_folder),
                    'critical': True
                }

        return files_status

    def create_optimized_gitignore(self):
        """Crée un .gitignore optimisé pour éviter upload inutile"""
        gitignore_content = """
# iFiveMe - Fichiers à ignorer pour upload GitHub optimisé
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Node modules (si présent)
node_modules/

# Base de données locales
*.db
*.sqlite
*.sqlite3

# Secrets/Clés
.env
*.key
*.pem
config_secrets.py

# Temporary files
temp/
tmp/
*.tmp
*.temp
"""
        gitignore_path = self.project_path / ".gitignore"

        try:
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content.strip())
            print("✅ .gitignore optimisé créé")
            return True
        except Exception as e:
            print(f"⚠️ Erreur création .gitignore: {e}")
            return False

    def intelligent_upload_sequence(self):
        """Séquence d'upload intelligente par priorité"""
        print("🚀 Séquence upload intelligente...")

        # Étape 1: Fichiers critiques Render.com
        critical_commands = [
            ("git add ifiveme_control_tower.py", "Ajout application principale"),
            ("git add requirements.txt", "Ajout dépendances Python"),
            ("git add Dockerfile", "Ajout configuration Docker"),
            ("git add render.yaml", "Ajout configuration Render"),
            ("git add package.json", "Ajout dépendances Node"),
        ]

        for cmd, desc in critical_commands:
            success, _ = self.run_command(cmd, desc)
            if not success:
                print(f"⚠️ Échec {desc}, continue...")

        # Étape 2: Dossiers essentiels
        folder_commands = [
            ("git add agents/", "Ajout agents AI"),
            ("git add config/", "Ajout configuration"),
            ("git add web_approval/", "Ajout interface web"),
            ("git add utils/", "Ajout utilitaires"),
        ]

        for cmd, desc in folder_commands:
            success, _ = self.run_command(cmd, desc)
            if not success:
                print(f"⚠️ Échec {desc}, continue...")

        # Étape 3: Fichiers documentation
        doc_commands = [
            ("git add README.md", "Ajout documentation principale"),
            ("git add *.md", "Ajout autres documentations"),
        ]

        for cmd, desc in doc_commands:
            success, _ = self.run_command(cmd, desc)

        return True

    def create_deployment_ready_commit(self):
        """Crée un commit optimisé pour déploiement"""
        commit_message = """🚀 iFiveMe Marketing MVP - Production Ready

✨ Fonctionnalités principales:
- 🤖 Système agents AI complet (20+ agents)
- 📱 Interface web d'approbation
- 🔄 Orchestration automatique posts
- 📊 Analytics et reporting
- ⚡ Déploiement Render.com ready

🛠️ Infrastructure:
- 🐳 Docker containerisé
- 📦 Dépendances optimisées
- ⚙️ Configuration Render.com
- 🔧 Système modulaire

🎯 Prêt pour production sur Render.com!

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""

        success, _ = self.run_command(
            f'git commit -m "{commit_message}"',
            "Création commit déploiement"
        )

        return success

    def push_with_retry(self, max_retries=3):
        """Push avec retry intelligent"""
        for attempt in range(max_retries):
            print(f"📤 Tentative push {attempt + 1}/{max_retries}")

            success, output = self.run_command(
                "git push origin main",
                f"Push vers GitHub (tentative {attempt + 1})"
            )

            if success:
                print("🎉 Push réussi!")
                return True

            if attempt < max_retries - 1:
                print(f"⏱️ Attente avant retry...")
                time.sleep(5)

        print("❌ Échec push après toutes les tentatives")
        return False

    def run_intelligent_sync(self):
        """Processus complet de synchronisation intelligente"""
        print("🧠 DÉMARRAGE SYNC GITHUB INTELLIGENT")
        print("=" * 60)

        try:
            # Étape 1: Analyse du projet
            file_status = self.analyze_files_to_upload()
            print(f"📊 Analyse: {len(file_status)} éléments détectés")

            # Étape 2: Optimisation gitignore
            self.create_optimized_gitignore()

            # Étape 3: Configuration authentification
            if not self.setup_git_credentials():
                print("❌ Échec authentification")
                return False

            # Étape 4: Upload intelligent
            self.intelligent_upload_sequence()

            # Étape 5: Commit optimisé
            if not self.create_deployment_ready_commit():
                print("❌ Échec création commit")
                return False

            # Étape 6: Push avec retry
            if not self.push_with_retry():
                print("❌ Échec push final")
                return False

            # Succès !
            print("\n" + "🎉" * 20)
            print("✅ SYNC GITHUB RÉUSSI!")
            print(f"🔗 Dépôt: {self.repo_url}")
            print("🚀 Prêt pour déploiement Render.com!")
            print("🎉" * 20)

            return True

        except Exception as e:
            print(f"💥 Erreur critique: {e}")
            return False

def main():
    sync_agent = IntelligentGitHubSync()

    print("🧠 INTELLIGENT GITHUB SYNC - IFIVEME")
    print("Système automatique d'upload optimisé pour Render.com")
    print("-" * 60)

    success = sync_agent.run_intelligent_sync()

    if success:
        print("\n✅ MISSION ACCOMPLIE!")
        print("Votre projet iFiveMe est maintenant sur GitHub")
        print("Prochaine étape: Déploiement Render.com")
    else:
        print("\n❌ Échec synchronisation")
        print("Vérifiez votre token GitHub et réessayez")

    return success

if __name__ == "__main__":
    main()