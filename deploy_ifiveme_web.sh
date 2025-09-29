#!/bin/bash

# 🚀 Script de déploiement iFiveMe Interface Web
# Déploie votre interface d'approbation 24/7 en ligne

echo "🚀 iFiveMe - Déploiement Interface Web d'Approbation"
echo "=================================================="

cd /Users/richardlosier/Desktop/iFiveMe_Marketing_MVP/web_approval/

echo ""
echo "📁 Préparation des fichiers de déploiement..."
echo "✅ Flask app prête"
echo "✅ Requirements.txt généré"
echo "✅ Configuration Vercel créée"
echo "✅ Configuration Railway/Heroku prête"

echo ""
echo "🎯 OPTION 1: Déploiement Vercel (Recommandé)"
echo "============================================"
echo "1. Authentification Vercel:"
echo "   vercel login"
echo ""
echo "2. Déploiement:"
echo "   vercel --prod --yes"
echo ""
echo "✨ Votre interface sera disponible à: https://ifiveme-approval-[random].vercel.app"

echo ""
echo "🎯 OPTION 2: Déploiement Railway (Alternative)"
echo "=============================================="
echo "1. Authentification Railway:"
echo "   railway login"
echo ""
echo "2. Initialisation:"
echo "   railway init"
echo ""
echo "3. Déploiement:"
echo "   railway up"
echo ""
echo "✨ Votre interface sera disponible à: https://ifiveme-approval.up.railway.app"

echo ""
echo "🔧 APRÈS DÉPLOIEMENT:"
echo "====================="
echo "1. Récupérez votre URL finale"
echo "2. Modifiez config/deployment_config.py avec votre vraie URL"
echo "3. Relancez vos tests avec:"
echo "   python test_web_approval.py"

echo ""
echo "📱 FONCTIONNALITÉS DISPONIBLES 24/7:"
echo "===================================="
echo "✅ Dashboard temps réel avec auto-refresh"
echo "✅ Approbation/Rejet en un clic"
echo "✅ Prévisualisation complète des posts"
echo "✅ Interface mobile responsive"
echo "✅ Notifications équipe automatiques"
echo "✅ Statistiques et historique"
echo "✅ Expiration automatique 24h"
echo ""
echo "🎉 VOTRE ÉQUIPE POURRA APPROUVER DEPUIS N'IMPORTE OÙ !"

echo ""
echo "Choisissez votre méthode de déploiement et suivez les étapes ci-dessus."