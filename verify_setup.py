#!/usr/bin/env python3
"""
Vérification Setup Complet - Playwright + Python + Node.js
"""

import asyncio
import subprocess
import sys
from pathlib import Path

async def verify_complete_setup():
    """Vérifie que tout le setup demandé est correct"""
    print("🔍 VÉRIFICATION SETUP COMPLET PLAYWRIGHT")
    print("=" * 60)

    checks = []

    # 1. Vérifier Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        node_version = result.stdout.strip()
        print(f"✅ Node.js: {node_version}")
        checks.append("✅ Node.js installé")
    except:
        print("❌ Node.js non trouvé")
        checks.append("❌ Node.js manquant")

    # 2. Vérifier npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        npm_version = result.stdout.strip()
        print(f"✅ npm: {npm_version}")
        checks.append("✅ npm installé")
    except:
        print("❌ npm non trouvé")
        checks.append("❌ npm manquant")

    # 3. Vérifier package.json
    package_json = Path("package.json")
    if package_json.exists():
        print("✅ package.json créé")
        checks.append("✅ package.json existe")

        import json
        with open(package_json, 'r') as f:
            pkg = json.load(f)
            if 'playwright' in pkg.get('devDependencies', {}):
                print(f"✅ Playwright dans devDependencies: {pkg['devDependencies']['playwright']}")
                checks.append("✅ Playwright installé")
            else:
                print("❌ Playwright manquant dans package.json")
                checks.append("❌ Playwright non installé")
    else:
        print("❌ package.json manquant")
        checks.append("❌ package.json manquant")

    # 4. Vérifier node_modules
    node_modules = Path("node_modules")
    if node_modules.exists():
        print("✅ node_modules créé")
        checks.append("✅ node_modules existe")

        playwright_dir = node_modules / "playwright"
        if playwright_dir.exists():
            print("✅ Playwright installé dans node_modules")
            checks.append("✅ Playwright dans node_modules")
        else:
            print("❌ Playwright manquant dans node_modules")
            checks.append("❌ Playwright non dans node_modules")
    else:
        print("❌ node_modules manquant")
        checks.append("❌ node_modules manquant")

    # 5. Vérifier Python
    python_version = sys.version
    print(f"✅ Python: {python_version.split()[0]}")
    checks.append(f"✅ Python {python_version.split()[0]}")

    # 6. Vérifier modules Python requis
    required_modules = ['playwright', 'asyncio', 'json', 'pathlib']

    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Module Python {module}")
            checks.append(f"✅ {module}")
        except ImportError:
            print(f"❌ Module Python {module} manquant")
            checks.append(f"❌ {module} manquant")

    # 7. Vérifier browsers Playwright
    try:
        from playwright.async_api import async_playwright

        print("🚀 Test Playwright...")
        playwright = await async_playwright().__aenter__()

        # Test browser launch
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.google.com")
        title = await page.title()

        await browser.close()

        print(f"✅ Playwright fonctionne - Test Google: {title[:20]}...")
        checks.append("✅ Playwright opérationnel")

    except Exception as e:
        print(f"❌ Erreur Playwright: {e}")
        checks.append(f"❌ Playwright erreur: {str(e)[:50]}")

    # 8. Vérifier structure directories
    expected_dirs = ["agents", "data", "config"]
    for dir_name in expected_dirs:
        if Path(dir_name).exists():
            print(f"✅ Directory {dir_name}")
            checks.append(f"✅ {dir_name}/")
        else:
            print(f"⚠️ Directory {dir_name} manquant")
            checks.append(f"⚠️ {dir_name}/ manquant")

    # 9. Vérifier .gitignore
    gitignore = Path(".gitignore")
    if gitignore.exists():
        with open(gitignore, 'r') as f:
            content = f.read()
            if 'node_modules/' in content:
                print("✅ .gitignore avec node_modules/")
                checks.append("✅ .gitignore correct")
            else:
                print("⚠️ .gitignore sans node_modules/")
                checks.append("⚠️ .gitignore incomplet")
    else:
        print("❌ .gitignore manquant")
        checks.append("❌ .gitignore manquant")

    # Résumé final
    print("\n" + "="*60)
    print("📋 RÉSUMÉ VÉRIFICATION SETUP")
    print("="*60)

    success_count = len([c for c in checks if c.startswith("✅")])
    total_count = len(checks)

    print(f"🎯 Score: {success_count}/{total_count} vérifications passées")
    print(f"📊 Taux de réussite: {(success_count/total_count)*100:.1f}%")

    if success_count == total_count:
        print("\n🏆 SETUP PARFAIT ! Tous les prérequis respectés !")
        setup_status = "perfect"
    elif success_count >= total_count * 0.8:
        print("\n✅ SETUP BON ! Quelques ajustements mineurs possibles")
        setup_status = "good"
    else:
        print("\n⚠️ SETUP À AMÉLIORER ! Plusieurs éléments manquants")
        setup_status = "needs_work"

    # Actions recommandées
    print(f"\n💡 ACTIONS RECOMMANDÉES:")

    missing_items = [c for c in checks if not c.startswith("✅")]
    if missing_items:
        for item in missing_items[:5]:  # Top 5
            print(f"  🔧 {item}")
    else:
        print("  🎉 Aucune action requise - Setup parfait !")

    return {
        "setup_status": setup_status,
        "score": f"{success_count}/{total_count}",
        "success_rate": (success_count/total_count)*100,
        "checks": checks,
        "playwright_working": "✅ Playwright opérationnel" in checks
    }

if __name__ == "__main__":
    result = asyncio.run(verify_complete_setup())

    if result["setup_status"] == "perfect":
        print("\n🚀 Prêt pour analyse ultra-complète du site admin !")
    else:
        print(f"\n🔧 Corrigez les éléments manquants puis relancez l'analyse")