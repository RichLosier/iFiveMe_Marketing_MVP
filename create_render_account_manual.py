#!/usr/bin/env python3
"""
🚀 Guide Manuel Création Compte Render.com - iFiveMe
Ouvre navigateur et guide étape par étape
"""

import subprocess
import time
import os

def create_render_account_guide():
    """Guide manuel complet pour création compte Render.com"""

    print("🚀 GUIDE CRÉATION COMPTE RENDER.COM - IFIVEME")
    print("="*60)

    # Ouvrir Render.com dans le navigateur
    print("🌐 Ouverture de Render.com...")
    subprocess.run(['open', 'https://render.com'], check=False)
    time.sleep(2)

    print("\n📋 INFORMATIONS POUR VOTRE COMPTE RENDER:")
    print("="*50)
    print("📧 Email: richard@ifiveme.com")
    print("👤 Nom complet: Richard Losier")
    print("🏢 Entreprise: iFiveMe")
    print("💼 Type: Business/Company")
    print("🔑 Mot de passe: [Choisissez un mot de passe fort]")

    print("\n🎯 ÉTAPES À SUIVRE DANS VOTRE NAVIGATEUR:")
    print("="*50)
    print("1. Sur render.com, cliquez 'Get Started' ou 'Sign Up'")
    print("2. Choisissez 'Sign up with Email' (pas GitHub/Google)")
    print("3. Remplissez le formulaire avec vos infos:")
    print("   - Email: richard@ifiveme.com")
    print("   - Password: [mot de passe sécurisé]")
    print("   - Full Name: Richard Losier")
    print("4. Cochez les cases d'acceptation si nécessaire")
    print("5. Cliquez 'Create Account' ou 'Sign Up'")
    print("6. Vérifiez votre email et confirmez si requis")
    print("7. Revenez ici quand vous êtes connecté au dashboard")

    print("\n💡 CONSEILS:")
    print("- Utilisez un mot de passe avec majuscules, chiffres, symboles")
    print("- Gardez vos identifiants en sécurité")
    print("- Render peut demander vérification email ou téléphone")

    # Attendre confirmation utilisateur
    input("\n⏳ Appuyez sur ENTRÉE quand votre compte est créé et vous êtes connecté...")

    # Vérification post-création
    print("\n✅ VÉRIFICATION POST-CRÉATION:")
    print("="*40)
    print("Dans votre navigateur, vous devriez voir:")
    print("- Dashboard Render avec menu de navigation")
    print("- Bouton 'New +' pour créer services")
    print("- Votre nom/email en haut à droite")
    print("- URL comme: https://dashboard.render.com")

    confirm = input("\n🔍 Voyez-vous le dashboard Render? (o/n): ").lower().strip()

    if confirm == 'o' or confirm == 'oui' or confirm == 'y' or confirm == 'yes':
        print("\n🎉 PARFAIT! COMPTE RENDER.COM CRÉÉ AVEC SUCCÈS!")
        print("="*50)

        # Instructions prochaines étapes
        print("\n🚀 PROCHAINES ÉTAPES - DÉPLOIEMENT IFIVEME:")
        print("="*45)
        print("1. Cliquez 'New +' puis 'Web Service'")
        print("2. Connectez votre repository GitHub")
        print("3. Utilisez les paramètres du fichier DEPLOYMENT_RENDER_GUIDE.md")

        # Ouvrir le guide de déploiement
        print("\n📖 Ouverture du guide de déploiement...")
        subprocess.run(['open', 'DEPLOYMENT_RENDER_GUIDE.md'], check=False)

        return True

    else:
        print("\n⚠️ Il semble y avoir un problème...")
        print("Vérifiez ces points:")
        print("- Avez-vous cliqué sur le lien de confirmation email?")
        print("- Êtes-vous sur https://dashboard.render.com?")
        print("- Y a-t-il des messages d'erreur affichés?")

        retry = input("\nVoulez-vous réessayer? (o/n): ").lower().strip()
        if retry == 'o' or retry == 'oui' or retry == 'y' or retry == 'yes':
            # Relancer le processus
            subprocess.run(['open', 'https://render.com/signup'], check=False)
            input("⏳ Réessayez la création de compte, puis appuyez ENTRÉE...")

        return False

def main():
    """Point d'entrée principal"""
    os.makedirs('data/render_setup', exist_ok=True)

    print("🎯 ASSISTANT CRÉATION COMPTE RENDER.COM")
    print("Cet outil va vous guider pas à pas pour créer votre compte")

    success = create_render_account_guide()

    if success:
        print("\n✅ MISSION ACCOMPLIE!")
        print("Votre compte Render.com est prêt pour déployer iFiveMe!")
    else:
        print("\n⚠️ Besoin d'aide? Contactez support Render.com")
        print("Ou réessayez ce script: python3 create_render_account_manual.py")

if __name__ == "__main__":
    main()