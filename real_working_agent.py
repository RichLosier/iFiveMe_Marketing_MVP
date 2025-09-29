#!/usr/bin/env python3
"""
Agent qui fonctionne VRAIMENT - Upload GitHub direct API
Pas de mensonges, que des résultats réels
"""

import requests
import base64
import os
from pathlib import Path
import json

def upload_to_github_real(token, file_path, github_path):
    """Upload RÉEL vers GitHub API - aucune simulation"""

    try:
        with open(file_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode()

        url = f"https://api.github.com/repos/RichLosier/iFiveMe_Marketing_MVP/contents/{github_path}"

        data = {
            "message": f"📤 Upload {github_path}",
            "content": content
        }

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }

        response = requests.put(url, json=data, headers=headers)

        if response.status_code == 201:
            return True, f"✅ {github_path} uploadé"
        else:
            return False, f"❌ {github_path}: {response.status_code} - {response.text}"

    except Exception as e:
        return False, f"❌ Erreur {file_path}: {e}"

def main():
    print("🔧 AGENT RÉEL - UPLOAD GITHUB")
    print("="*50)

    token = input("🔐 Token GitHub: ").strip()

    if not token:
        print("❌ Token requis")
        return

    # Fichiers essentiels à uploader
    files_to_upload = [
        ("ifiveme_control_tower.py", "ifiveme_control_tower.py"),
        ("requirements.txt", "requirements.txt"),
        ("package.json", "package.json"),
        ("Dockerfile", "Dockerfile"),
        ("render.yaml", "render.yaml")
    ]

    success_count = 0

    for local_file, github_file in files_to_upload:
        if os.path.exists(local_file):
            success, message = upload_to_github_real(token, local_file, github_file)
            print(message)
            if success:
                success_count += 1
        else:
            print(f"⚠️ Fichier manquant: {local_file}")

    print(f"\n🎯 RÉSULTAT: {success_count}/{len(files_to_upload)} fichiers uploadés")

    if success_count > 0:
        print("✅ SUCCESS! Fichiers sur GitHub")
        print("🚀 Maintenant: Render.com → New Web Service → Connecter le repo")
    else:
        print("❌ Échec total")

if __name__ == "__main__":
    main()