"""
Templates de contenu iFiveMe authentiques
Basés sur les cartes d'affaires virtuelles et le style iFiveMe
"""

# Thèmes principaux iFiveMe
IFIVEME_CORE_THEMES = {
    "cartes_virtuelles": {
        "description": "Focus sur les cartes d'affaires virtuelles innovantes",
        "keywords": ["carte virtuelle", "digital business card", "NFC", "QR code", "contact instantané"]
    },
    "networking_moderne": {
        "description": "Révolution du networking traditionnel",
        "keywords": ["networking", "connexions", "réseautage", "contacts professionnels"]
    },
    "technologie_nfc": {
        "description": "Innovation technologique NFC et partage instantané",
        "keywords": ["NFC", "technologie", "innovation", "partage instantané", "sans contact"]
    },
    "professionnels_modernes": {
        "description": "Solutions pour professionnels et entrepreneurs",
        "keywords": ["entrepreneurs", "professionnels", "business", "efficacité", "modernité"]
    },
    "ecologie_papier": {
        "description": "Alternative écologique aux cartes papier",
        "keywords": ["écologique", "sans papier", "environnement", "durable", "vert"]
    }
}

# Templates par plateforme avec focus cartes virtuelles
PLATFORM_TEMPLATES = {
    "Facebook": {
        "style": "Engageant, visuel, stories personnelles",
        "tone": "Amical mais professionnel",
        "templates": [
            {
                "theme": "cartes_virtuelles",
                "template": """🚀 {title}

{hook}

🔥 **Découvrez les cartes d'affaires iFiveMe :**
{main_benefits}

💡 **Comment ça marche ?**
{how_it_works}

📊 **Résultats clients :**
{testimonials_or_stats}

{call_to_action}

{hashtags}""",
                "hooks": [
                    "Fini les cartes d'affaires perdues ! 📇",
                    "La révolution du networking est arrivée ! ⚡",
                    "Plus jamais de cartes froissées dans votre portefeuille ! 💳",
                    "Comment partager vos infos en 1 seconde ? 🤔"
                ],
                "benefits": [
                    "✅ Partage instantané par NFC ou QR code",
                    "✅ Mise à jour en temps réel de vos infos",
                    "✅ Design personnalisé à votre image",
                    "✅ Statistiques de vos interactions",
                    "✅ Écologique - zéro papier gaspillé"
                ]
            }
        ]
    },
    "LinkedIn": {
        "style": "Professionnel, expertise, leadership",
        "tone": "Expert et crédible",
        "templates": [
            {
                "theme": "networking_moderne",
                "template": """💼 {title}

{professional_insight}

🎯 **L'évolution du networking professionnel :**
{industry_analysis}

📈 **Impact mesuré avec iFiveMe :**
{business_metrics}

💡 **Notre approche innovante :**
{solution_details}

**Question à ma communauté :** {engagement_question}

{professional_hashtags}""",
                "insights": [
                    "Le networking traditionnel montre ses limites en 2024.",
                    "Les professionnels perdent 67% des cartes reçues en moins de 7 jours.",
                    "L'efficacité relationnelle devient un avantage concurrentiel majeur.",
                    "La digitalisation du networking n'est plus une option, c'est une nécessité."
                ]
            }
        ]
    },
    "Twitter": {
        "style": "Concis, percutant, viral",
        "tone": "Direct et impactant",
        "templates": [
            {
                "theme": "technologie_nfc",
                "template": """{hook} 🔥

{key_benefit}

{quick_stats}

{mini_demo}

{strong_cta}

{trending_hashtags}""",
                "hooks": [
                    "FINI les cartes d'affaires perdues !",
                    "1 seconde pour partager vos infos ⚡",
                    "La carte qui ne se perd jamais 📱",
                    "NFC + Design = Networking révolutionné"
                ]
            }
        ]
    }
}

# Exemples authentiques iFiveMe
AUTHENTIC_IFIVEME_POSTS = {
    "Facebook": [
        {
            "title": "💳 Révolution iFiveMe : La Carte qui Ne Se Perd Jamais !",
            "content": """🚀 Vous en avez marre de perdre vos cartes d'affaires ?

🔥 **Découvrez les cartes virtuelles iFiveMe :**
✅ Partage instantané par simple contact NFC
✅ Vos infos toujours à jour automatiquement
✅ Design personnalisé à votre image
✅ Statistiques de vos interactions en temps réel
✅ 100% écologique - zéro papier gaspillé

💡 **Comment ça marche ?**
1. Créez votre profil iFiveMe en 2 minutes
2. Recevez votre carte NFC personnalisée
3. Approchez votre carte du téléphone de votre contact
4. Magie ! Vos infos s'affichent instantanément

📊 **Nos clients témoignent :**
"Plus de cartes froissées ! Mes contacts sont maintenant tous dans mon CRM automatiquement." - Marie, Entrepreneure

🎯 **Offre spéciale** : -30% sur votre première carte iFiveMe !
👉 Commandez sur ifiveme.com

#iFiveMe #CartesVirtuelles #Networking #NFC #Innovation #Business #Écologique""",
            "image_context": "carte NFC élégante en action, partage de contact"
        },
        {
            "title": "📱 Client Success Story : +300% de Contacts Qualifiés !",
            "content": """🎉 Success Story iFiveMe !

👤 **Client :** Jean-François, Conseiller Financier
📈 **Résultat :** +300% de contacts qualifiés en 3 mois !

🔍 **Son défi :** "Je participais à 15 événements/mois mais mes cartes papier finissaient perdues ou oubliées..."

⚡ **La solution iFiveMe :**
✅ Carte NFC premium personnalisée
✅ Intégration CRM automatique
✅ Suivi des interactions en temps réel
✅ Landing page personnalisée intégrée

📊 **Résultats mesurés :**
• 300% plus de contacts dans son pipeline
• 89% de taux de récupération des infos
• 2h/semaine économisées en saisie manuelle
• ROI de 450% sur son investissement iFiveMe

💬 **Son témoignage :** "iFiveMe a transformé ma façon de faire du business. Je ne peux plus m'en passer !"

🚀 **Et vous ? Prêt à révolutionner votre networking ?**
👉 Découvrez iFiveMe sur ifiveme.com

#iFiveMe #SuccessStory #Networking #ROI #Business #Ventes""",
            "image_context": "graphiques de croissance, témoignage client professionnel"
        }
    ],
    "LinkedIn": [
        {
            "title": "💼 L'Évolution du Networking Professionnel en 2024",
            "content": """💼 Réflexion du jour : L'efficacité relationnelle comme avantage concurrentiel

En analysant les tendances networking 2024, une statistique m'interpelle : 67% des cartes d'affaires reçues sont perdues en moins de 7 jours.

🎯 **Le paradoxe moderne :**
Plus nous multiplions les interactions, moins nous créons de vraies connexions durables.

📈 **Notre approche iFiveMe :**
• Digitalisation intelligente du premier contact
• Suivi automatisé des interactions
• Intégration CRM native
• Analytics comportementaux

📊 **Impact mesuré chez nos clients B2B :**
• +340% d'efficacité dans la capture de leads
• 89% de taux de récupération des contacts
• ROI moyen 4:1 sur investissement networking
• 2.5h/semaine économisées par commercial

💡 **L'innovation qui fait la différence :**
Notre technologie NFC couplée à l'intelligence data transforme chaque interaction en opportunité business mesurable.

**Question à ma communauté :** Comment mesurez-vous actuellement l'efficacité de votre networking ?

#Networking #DigitalTransformation #B2B #iFiveMe #BusinessDevelopment #Innovation""",
            "image_context": "graphiques networking professionnels, statistiques B2B"
        }
    ],
    "Twitter": [
        {
            "title": "⚡ NFC + Networking = Révolution",
            "content": """FINI les cartes d'affaires perdues ! 🔥

1 contact NFC = Vos infos dans leur téléphone ⚡

📊 Stats iFiveMe :
• 89% taux de récupération
• 2 secondes de partage
• 0 carte perdue

La carte qui ne se perd jamais 📱

ifiveme.com

#NFC #Networking #iFiveMe #Innovation""",
            "image_context": "démonstration NFC rapide, cartes high-tech"
        }
    ]
}

# Générateur de hashtags iFiveMe
IFIVEME_HASHTAGS = {
    "core": ["#iFiveMe", "#CartesVirtuelles", "#Networking"],
    "tech": ["#NFC", "#QRCode", "#Innovation", "#DigitalCard"],
    "business": ["#Business", "#Entrepreneur", "#Professional", "#B2B"],
    "benefits": ["#Écologique", "#Efficace", "#Moderne", "#Intelligent"],
    "location": ["#Québec", "#Montréal", "#Canada", "#MadeInCanada"]
}

def get_ifiveme_hashtags(category="core", count=5):
    """Génère des hashtags iFiveMe appropriés"""
    import random

    hashtags = IFIVEME_HASHTAGS["core"].copy()

    if category in IFIVEME_HASHTAGS:
        hashtags.extend(IFIVEME_HASHTAGS[category])

    # Ajouter d'autres catégories
    for cat in ["tech", "business", "benefits"]:
        if cat != category:
            hashtags.extend(random.sample(IFIVEME_HASHTAGS[cat], min(2, len(IFIVEME_HASHTAGS[cat]))))

    return " ".join(random.sample(hashtags, min(count, len(hashtags))))