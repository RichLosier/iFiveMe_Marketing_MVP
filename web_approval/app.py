"""
iFiveMe Web Approval Interface
Interface web pour approuver les posts marketing en ligne 24/7
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import os
import sys
import asyncio
import requests

# Configuration simplifiée pour déploiement cloud
# sys.path.append(str(Path(__file__).parent.parent))
# from config.email_config import GmailService

app = Flask(__name__)
app.secret_key = 'ifiveme_approval_secret_key_2024'  # À changer en production

# Configuration
APPROVAL_DB = Path(__file__).parent / "approvals.db"
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@ifiveme.com")
APPROVAL_EMAIL = os.getenv("APPROVAL_EMAIL", "richard@ifiveme.com")

def init_database():
    """Initialize the approval database"""
    conn = sqlite3.connect(APPROVAL_DB)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS approvals (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            platform TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            scheduled_time DATETIME,
            status TEXT DEFAULT 'pending',
            approval_token TEXT NOT NULL,
            approved_at DATETIME,
            approved_by TEXT,
            rejection_reason TEXT,
            expires_at DATETIME NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    """Dashboard principal des approbations"""
    conn = sqlite3.connect(APPROVAL_DB)
    cursor = conn.cursor()

    # Récupérer tous les posts en attente
    cursor.execute('''
        SELECT * FROM approvals
        WHERE status = 'pending' AND expires_at > datetime('now')
        ORDER BY created_at DESC
    ''')

    pending_posts = cursor.fetchall()

    # Récupérer l'historique récent
    cursor.execute('''
        SELECT * FROM approvals
        WHERE status != 'pending'
        ORDER BY created_at DESC
        LIMIT 10
    ''')

    recent_posts = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html',
                         pending_posts=pending_posts,
                         recent_posts=recent_posts)

@app.route('/generate_instant_post', methods=['GET', 'POST'])
def generate_instant_post():
    """Génère instantanément un post iFiveMe"""
    if request.method == 'POST':
        platform = request.form.get('platform', 'Facebook')
        topic = request.form.get('topic', 'Innovation iFiveMe')

        try:
            # Appeler l'agent de génération
            result = asyncio.run(generate_instant_post_content(platform, topic))

            if result.get("success"):
                flash("✅ Post instantané généré et soumis pour approbation!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash(f"❌ Erreur: {result.get('error', 'Génération échouée')}", "error")
        except Exception as e:
            flash(f"❌ Erreur génération: {str(e)}", "error")

    return render_template('generate_post.html')

@app.route('/setup_social_platforms')
def setup_social_platforms():
    """Configure automatiquement les plateformes sociales"""
    try:
        # Lancer la configuration en arrière-plan
        result = asyncio.run(setup_all_social_credentials())

        if result.get("success"):
            flash("✅ Configuration des plateformes sociales lancée! Vérifiez le navigateur.", "success")
        else:
            flash(f"❌ Erreur configuration: {result.get('error', 'Configuration échouée')}", "error")

    except Exception as e:
        flash(f"❌ Erreur: {str(e)}", "error")

    return redirect(url_for('dashboard'))

@app.route('/publish_approved/<post_id>')
def publish_approved(post_id):
    """Publie automatiquement un post approuvé"""
    try:
        conn = sqlite3.connect(APPROVAL_DB)
        cursor = conn.cursor()

        # Récupérer le post approuvé
        cursor.execute('SELECT * FROM approvals WHERE id = ? AND status = "approved"', (post_id,))
        post = cursor.fetchone()

        if not post:
            flash("Post non trouvé ou non approuvé", "error")
            return redirect(url_for('dashboard'))

        # Préparer les données pour publication
        post_data = {
            "content": post[2],  # content
            "platform": post[3],  # platform
            "title": post[1],     # title
            "post_id": post[0]    # id
        }

        # Publier automatiquement
        result = asyncio.run(publish_to_social_media(post_data))

        if result.get("success"):
            # Mettre à jour le statut
            cursor.execute('''
                UPDATE approvals
                SET status = 'published', approved_at = datetime('now')
                WHERE id = ?
            ''', (post_id,))
            conn.commit()

            flash(f"🚀 Post publié avec succès sur {post_data['platform']}!", "success")
        else:
            flash(f"❌ Erreur publication: {result.get('error', 'Publication échouée')}", "error")

        conn.close()

    except Exception as e:
        flash(f"❌ Erreur: {str(e)}", "error")

    return redirect(url_for('dashboard'))

@app.route('/approve/<post_id>/<token>')
def approve_post(post_id, token):
    """Approuve un post"""
    try:
        conn = sqlite3.connect(APPROVAL_DB)
        cursor = conn.cursor()

        # Vérifier le post et le token
        cursor.execute('''
            SELECT * FROM approvals
            WHERE id = ? AND approval_token = ? AND status = 'pending'
        ''', (post_id, token))

        post = cursor.fetchone()

        if not post:
            flash("Post non trouvé ou déjà traité", "error")
            return redirect(url_for('dashboard'))

        # Vérifier si pas expiré
        expires_at = datetime.fromisoformat(post[12])  # expires_at
        if datetime.now() > expires_at:
            flash("Cette demande d'approbation a expiré", "error")
            return redirect(url_for('dashboard'))

        # Approuver le post
        cursor.execute('''
            UPDATE approvals
            SET status = 'approved', approved_at = datetime('now'), approved_by = 'Richard Losier'
            WHERE id = ?
        ''', (post_id,))

        conn.commit()
        conn.close()

        # Notifier l'équipe
        notify_team_approval(post, "approved")

        # Déclencher la publication (simulation)
        trigger_publication(post)

        flash(f"✅ Post '{post[1]}' approuvé avec succès !", "success")

    except Exception as e:
        flash(f"Erreur lors de l'approbation: {str(e)}", "error")

    return redirect(url_for('dashboard'))

@app.route('/reject/<post_id>/<token>', methods=['GET', 'POST'])
def reject_post(post_id, token):
    """Rejette un post avec raison"""

    if request.method == 'GET':
        # Afficher le formulaire de rejet
        conn = sqlite3.connect(APPROVAL_DB)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM approvals
            WHERE id = ? AND approval_token = ? AND status = 'pending'
        ''', (post_id, token))

        post = cursor.fetchone()
        conn.close()

        if not post:
            flash("Post non trouvé", "error")
            return redirect(url_for('dashboard'))

        return render_template('reject_form.html', post=post)

    # Traitement du rejet
    try:
        reason = request.form.get('reason', 'Aucune raison spécifiée')

        conn = sqlite3.connect(APPROVAL_DB)
        cursor = conn.cursor()

        # Récupérer le post
        cursor.execute('''
            SELECT * FROM approvals
            WHERE id = ? AND approval_token = ? AND status = 'pending'
        ''', (post_id, token))

        post = cursor.fetchone()

        if not post:
            flash("Post non trouvé", "error")
            return redirect(url_for('dashboard'))

        # Rejeter le post
        cursor.execute('''
            UPDATE approvals
            SET status = 'rejected', rejection_reason = ?
            WHERE id = ?
        ''', (reason, post_id))

        conn.commit()
        conn.close()

        # Notifier l'équipe
        notify_team_approval(post, "rejected", reason)

        flash(f"❌ Post '{post[1]}' rejeté. L'équipe sera notifiée.", "warning")

    except Exception as e:
        flash(f"Erreur lors du rejet: {str(e)}", "error")

    return redirect(url_for('dashboard'))

@app.route('/preview/<post_id>/<token>')
def preview_post(post_id, token):
    """Prévisualise un post"""
    conn = sqlite3.connect(APPROVAL_DB)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM approvals
        WHERE id = ? AND approval_token = ?
    ''', (post_id, token))

    post = cursor.fetchone()
    conn.close()

    if not post:
        flash("Post non trouvé", "error")
        return redirect(url_for('dashboard'))

    return render_template('preview.html', post=post)

@app.route('/api/submit_post', methods=['POST'])
def api_submit_post():
    """API pour soumettre un nouveau post"""
    try:
        data = request.get_json()

        post_id = data.get('post_id')
        title = data.get('title')
        content = data.get('content')
        platform = data.get('platform')
        created_by = data.get('created_by')
        scheduled_time = data.get('scheduled_time')
        approval_token = data.get('approval_token')

        # Calculer expiration (24h)
        expires_at = datetime.now() + timedelta(hours=24)

        # Insérer dans la base
        conn = sqlite3.connect(APPROVAL_DB)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO approvals
            (id, title, content, platform, created_by, created_at, scheduled_time, approval_token, expires_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'), ?, ?, ?)
        ''', (post_id, title, content, platform, created_by, scheduled_time, approval_token, expires_at))

        conn.commit()
        conn.close()

        # Envoyer email d'approbation si configuré
        if GMAIL_APP_PASSWORD:
            send_approval_email(post_id, title, content, platform, created_by, scheduled_time, approval_token)

        return jsonify({
            "success": True,
            "post_id": post_id,
            "approval_url": f"https://approve.ifiveme.com/approve/{post_id}/{approval_token}",
            "message": "Post soumis pour approbation"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

def send_approval_email(post_id, title, content, platform, created_by, scheduled_time, token):
    """Envoie l'email d'approbation via Gmail"""

    gmail_service = GmailService()

    # URLs d'approbation (remplacer par votre domaine)
    base_url = "https://approve.ifiveme.com"  # À configurer
    approval_url = f"{base_url}/approve/{post_id}/{token}"
    rejection_url = f"{base_url}/reject/{post_id}/{token}"
    preview_url = f"{base_url}/preview/{post_id}/{token}"

    subject = f"🚀 iFiveMe - Nouveau post à approuver: {title}"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Approbation iFiveMe</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .content {{ padding: 30px; }}
        .post-preview {{ background: #f8f9fa; padding: 20px; margin: 20px 0; border-left: 4px solid #667eea; border-radius: 8px; }}
        .meta {{ background: #e9ecef; padding: 15px; margin: 15px 0; border-radius: 8px; }}
        .actions {{ text-align: center; margin: 30px 0; }}
        .btn {{ display: inline-block; padding: 15px 30px; margin: 10px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; }}
        .btn-approve {{ background: #28a745; color: white; }}
        .btn-reject {{ background: #dc3545; color: white; }}
        .btn-preview {{ background: #17a2b8; color: white; }}
        .footer {{ background: #333; color: white; padding: 20px; text-align: center; }}
        .content p {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 iFiveMe - Approbation Contenu</h1>
            <p>Nouveau post en attente de validation</p>
        </div>

        <div class="content">
            <div class="meta">
                <strong>📋 Détails du post:</strong><br>
                <strong>Titre:</strong> {title}<br>
                <strong>Plateforme:</strong> {platform}<br>
                <strong>Créé par:</strong> {created_by}<br>
                <strong>Publication prévue:</strong> {scheduled_time or 'Non programmée'}<br>
                <strong>Créé le:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>

            <div class="post-preview">
                <h3>📝 Aperçu du contenu:</h3>
                <div style="white-space: pre-wrap; font-family: Georgia, serif; line-height: 1.5;">{content[:500]}{'...' if len(content) > 500 else ''}</div>
            </div>

            <div class="actions">
                <h3>🎯 Actions disponibles:</h3>
                <a href="{approval_url}" class="btn btn-approve">✅ APPROUVER</a>
                <a href="{rejection_url}" class="btn btn-reject">❌ REJETER</a>
                <a href="{preview_url}" class="btn btn-preview">👀 PRÉVISUALISER</a>
            </div>

            <div class="meta">
                <strong>⏰ Important:</strong><br>
                • Ce post expirera automatiquement après 24h sans réponse<br>
                • Un rappel sera envoyé dans 12h si aucune action<br>
                • L'équipe sera notifiée de votre décision<br>
                • Post ID: {post_id}
            </div>
        </div>

        <div class="footer">
            <p><strong>iFiveMe Marketing System</strong></p>
            <p>Le plus grand créateur de cartes d'affaires virtuelles</p>
        </div>
    </div>
</body>
</html>
    """

    # Envoyer l'email
    gmail_service.send_approval_email(
        to_email=APPROVAL_EMAIL,
        subject=subject,
        html_content=html_content,
        app_password=GMAIL_APP_PASSWORD
    )

def notify_team_approval(post, decision, reason=None):
    """Notifie l'équipe de la décision d'approbation"""
    # Simulation - en production, envoyer un vrai email à l'équipe
    print(f"📧 NOTIFICATION ÉQUIPE: Post '{post[1]}' {decision.upper()}")
    if reason:
        print(f"💬 Raison: {reason}")

def trigger_publication(post):
    """Déclenche la publication du post approuvé"""
    try:
        # Appeler l'agent de publication automatique
        post_data = {
            "content": post[2],  # content
            "platform": post[3],  # platform
            "title": post[1],     # title
            "post_id": post[0]    # id
        }

        result = asyncio.run(publish_to_social_media(post_data))
        print(f"🚀 PUBLICATION AUTOMATIQUE: {post[3]} - {result.get('success', False)}")
        return result
    except Exception as e:
        print(f"❌ ERREUR PUBLICATION: {str(e)}")
        return {"error": str(e)}

# Fonctions utilitaires pour intégration agents
async def generate_instant_post_content(platform: str, topic: str) -> dict:
    """Génère un post instantané via l'agent"""
    try:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))

        from agents.social_media_publisher_agent import SocialMediaPublisherAgent

        publisher = SocialMediaPublisherAgent()

        task = publisher.create_task(
            task_type="generate_instant_post",
            priority=10,
            data={
                "platform": platform,
                "topic": topic,
                "urgent": True
            }
        )

        await publisher.add_task(task)
        await publisher.execute_tasks()

        # Récupérer les résultats
        results = []
        for file_path in publisher.data_dir.glob("task_*_result.json"):
            with open(file_path, 'r') as f:
                result = json.load(f)
                if result.get("result"):
                    results.append(result["result"])

        await publisher.stop()
        return results[-1] if results else {"error": "Génération échouée"}

    except Exception as e:
        return {"error": f"Erreur génération: {str(e)}"}

async def setup_all_social_credentials() -> dict:
    """Configure toutes les plateformes sociales"""
    try:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))

        from agents.social_media_publisher_agent import setup_all_social_platforms
        return await setup_all_social_platforms()

    except Exception as e:
        return {"error": f"Erreur configuration: {str(e)}"}

async def publish_to_social_media(post_data: dict) -> dict:
    """Publie automatiquement sur les réseaux sociaux"""
    try:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))

        from agents.social_media_publisher_agent import publish_approved_post
        return await publish_approved_post(post_data)

    except Exception as e:
        return {"error": f"Erreur publication: {str(e)}"}

# Initialize database on import for cloud deployment
init_database()

if __name__ == '__main__':
    # Local development
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
else:
    # Production deployment
    init_database()