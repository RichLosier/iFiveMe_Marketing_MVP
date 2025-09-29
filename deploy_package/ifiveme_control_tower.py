#!/usr/bin/env python3
"""
iFiveMe Control Tower - Tour de Contrôle pour tous nos Agents
Interface WebSocket temps réel pour piloter le système marketing complet
"""

import os
import sys
import subprocess
import threading
import asyncio
import json
import base64
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Ajouter le répertoire parent au path pour imports
sys.path.append(str(Path(__file__).parent))

# Configuration iFiveMe
app = Flask(__name__)
CORS(app, origins=["*"])  # Autoriser toutes origines pour développement
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Configuration pour Render.com
PORT = int(os.environ.get('PORT', 5001))
HOST = os.environ.get('HOST', '0.0.0.0')
DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

# Configuration agents iFiveMe
IFIVEME_AGENTS = {
    "marketing": {
        "name": "Agent Marketing iFiveMe",
        "script": "agents/social_media_publisher_agent.py",
        "description": "Posts authentiques iFiveMe avec approbation web"
    },
    "admin": {
        "name": "Agent Admin iFiveMe",
        "script": "agents/ifiveme_action_agent.py",
        "description": "Actions automatisées sur admin.ifiveme.com"
    },
    "ultimate_web": {
        "name": "Ultimate Web Agent",
        "script": "agents/ultimate_web_agent.py",
        "description": "Navigation web illimitée avec comportement humain"
    },
    "super_ai": {
        "name": "Super iFiveMe Web Agent + IA",
        "script": "agents/super_ifiveme_web_agent.py",
        "description": "Agent IA avec planification intelligente"
    },
    "observe_think_act": {
        "name": "Observer-Penser-Agir Agent",
        "script": "agents/observe_think_act_agent.py",
        "description": "Apprentissage continu avec cycles d'amélioration"
    },
    "analyzer": {
        "name": "Ultimate Admin Analyzer",
        "script": "agents/ultimate_admin_analyzer.py",
        "description": "Analyse complète admin.ifiveme.com"
    },
    "quick_web": {
        "name": "Quick Web Agent",
        "script": "agents/quick_web_agent.py",
        "description": "Agent web rapide pour tests et actions simples"
    }
}

# Variables globales pour suivi des processus
active_processes = {}
agent_logs = {}

# --- Interface HTML embarquée ---
CONTROL_TOWER_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏗️ iFiveMe Control Tower</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }

        .header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .subtitle {
            opacity: 0.9;
            font-size: 1.1rem;
        }

        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
            height: calc(100vh - 140px);
        }

        .agents-panel, .logs-panel {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }

        .panel-title {
            font-size: 1.3rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }

        .agent-card {
            background: rgba(255,255,255,0.1);
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }

        .agent-card:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }

        .agent-name {
            font-weight: bold;
            font-size: 1.1rem;
            margin-bottom: 5px;
        }

        .agent-desc {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 10px;
        }

        .task-input {
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 5px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 0.9rem;
        }

        .task-input::placeholder {
            color: rgba(255,255,255,0.6);
        }

        .launch-btn {
            background: linear-gradient(45deg, #28a745, #20c997);
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .launch-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0,255,0,0.3);
        }

        .launch-btn:disabled {
            background: #6c757d;
            cursor: not-allowed;
            transform: none;
        }

        .logs-container {
            height: 70vh;
            overflow-y: auto;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }

        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-left: 3px solid #28a745;
            background: rgba(255,255,255,0.05);
            border-radius: 3px;
        }

        .log-error {
            border-left-color: #dc3545;
            background: rgba(220, 53, 69, 0.1);
        }

        .log-success {
            border-left-color: #28a745;
            background: rgba(40, 167, 69, 0.1);
        }

        .status-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.8);
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .connection-status {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #28a745;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        .quick-actions {
            display: flex;
            gap: 10px;
        }

        .quick-btn {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            padding: 5px 10px;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            font-size: 0.8rem;
        }

        .quick-btn:hover {
            background: rgba(255,255,255,0.3);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏗️ iFiveMe Control Tower</h1>
        <div class="subtitle">
            Tour de Contrôle - Pilotage des Agents Marketing & Admin
        </div>
    </div>

    <div class="container">
        <!-- Panel des Agents -->
        <div class="agents-panel">
            <div class="panel-title">🤖 Agents Disponibles</div>
            <div id="agents-list">
                <!-- Agents seront chargés dynamiquement -->
            </div>
        </div>

        <!-- Panel des Logs -->
        <div class="logs-panel">
            <div class="panel-title">📋 Logs en Temps Réel</div>
            <div class="logs-container" id="logs">
                <div class="log-entry">🔌 Connexion à la tour de contrôle...</div>
            </div>
        </div>
    </div>

    <div class="status-bar">
        <div class="connection-status">
            <div class="status-indicator" id="status-indicator"></div>
            <span id="connection-text">Connexion...</span>
        </div>

        <div class="quick-actions">
            <button class="quick-btn" onclick="clearLogs()">🗑️ Clear Logs</button>
            <button class="quick-btn" onclick="stopAllAgents()">⏹️ Stop All</button>
            <button class="quick-btn" onclick="refreshAgents()">🔄 Refresh</button>
        </div>
    </div>

    <script>
        // Connexion WebSocket
        const socket = io();
        let isConnected = false;

        // Événements de connexion
        socket.on('connect', function() {
            isConnected = true;
            document.getElementById('connection-text').textContent = 'Connecté à la Tour de Contrôle';
            document.getElementById('status-indicator').style.background = '#28a745';
            addLog('🔌 Tour de contrôle connectée', 'success');
            loadAgents();
        });

        socket.on('disconnect', function() {
            isConnected = false;
            document.getElementById('connection-text').textContent = 'Déconnecté';
            document.getElementById('status-indicator').style.background = '#dc3545';
            addLog('❌ Connexion perdue', 'error');
        });

        // Réception des logs des agents
        socket.on('agent_log', function(data) {
            addLog(data.data, 'info');
        });

        socket.on('agent_error', function(data) {
            addLog(`❌ ${data.error}`, 'error');
        });

        socket.on('agent_success', function(data) {
            addLog(`✅ ${data.message}`, 'success');
        });

        // Fonction pour ajouter un log
        function addLog(message, type = 'info') {
            const logsContainer = document.getElementById('logs');
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${type}`;

            const timestamp = new Date().toLocaleTimeString();
            logEntry.innerHTML = `<strong>[${timestamp}]</strong> ${message}`;

            logsContainer.appendChild(logEntry);
            logsContainer.scrollTop = logsContainer.scrollHeight;
        }

        // Charger la liste des agents
        function loadAgents() {
            fetch('/api/agents')
                .then(response => response.json())
                .then(agents => {
                    const agentsList = document.getElementById('agents-list');
                    agentsList.innerHTML = '';

                    Object.keys(agents).forEach(agentKey => {
                        const agent = agents[agentKey];
                        const agentCard = createAgentCard(agentKey, agent);
                        agentsList.appendChild(agentCard);
                    });
                })
                .catch(error => {
                    addLog(`Erreur chargement agents: ${error}`, 'error');
                });
        }

        // Créer une carte d'agent
        function createAgentCard(agentKey, agent) {
            const card = document.createElement('div');
            card.className = 'agent-card';

            card.innerHTML = `
                <div class="agent-name">${agent.name}</div>
                <div class="agent-desc">${agent.description}</div>
                <input type="text"
                       class="task-input"
                       id="task-${agentKey}"
                       placeholder="Description de la tâche pour cet agent...">
                <button class="launch-btn"
                        onclick="launchAgent('${agentKey}')">
                    🚀 Lancer Mission
                </button>
            `;

            return card;
        }

        // Lancer un agent
        function launchAgent(agentKey) {
            const taskInput = document.getElementById(`task-${agentKey}`);
            const task = taskInput.value.trim();

            if (!task) {
                addLog('⚠️ Veuillez spécifier une tâche', 'error');
                return;
            }

            addLog(`🚀 Lancement ${agentKey}: ${task}`, 'info');

            fetch('/api/start-agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    agent: agentKey,
                    task: task
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    addLog(`❌ Erreur: ${data.error}`, 'error');
                } else {
                    addLog(`✅ Agent lancé: ${data.status}`, 'success');
                    taskInput.value = ''; // Clear input
                }
            })
            .catch(error => {
                addLog(`❌ Erreur réseau: ${error}`, 'error');
            });
        }

        // Actions rapides
        function clearLogs() {
            document.getElementById('logs').innerHTML = '';
            addLog('🗑️ Logs effacés', 'info');
        }

        function stopAllAgents() {
            fetch('/api/stop-all', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    addLog('⏹️ Arrêt de tous les agents demandé', 'info');
                });
        }

        function refreshAgents() {
            loadAgents();
            addLog('🔄 Liste des agents actualisée', 'info');
        }

        // Raccourcis clavier
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'l') {
                e.preventDefault();
                clearLogs();
            }
        });
    </script>
</body>
</html>
"""

# --- Fonctions de gestion des agents iFiveMe ---

def stream_python_output(process, agent_key):
    """
    Lit la sortie stdout du processus Python de l'agent ligne par ligne
    et la transmet au frontend via WebSocket en temps réel.
    """
    try:
        for line in iter(process.stdout.readline, ''):
            if not line:
                break

            line = line.strip()

            if not line:
                continue

            # Formatage spécial pour les logs iFiveMe
            if '✅' in line or 'SUCCESS' in line.upper():
                socketio.emit('agent_success', {'message': line, 'agent': agent_key})
            elif '❌' in line or 'ERROR' in line.upper() or 'ERREUR' in line.upper():
                socketio.emit('agent_error', {'error': line, 'agent': agent_key})
            else:
                socketio.emit('agent_log', {'data': f'[{agent_key.upper()}] {line}'})

        # Nettoyage à la fin
        if agent_key in active_processes:
            del active_processes[agent_key]

        socketio.emit('agent_log', {'data': f'✅ --- Mission {agent_key} terminée ---'})

    except Exception as e:
        error_msg = f"❌ Erreur streaming {agent_key}: {str(e)}"
        print(error_msg)
        socketio.emit('agent_error', {'error': error_msg, 'agent': agent_key})

# --- Routes API ---

@app.route('/')
def control_tower_interface():
    """Interface principale de la tour de contrôle"""
    return render_template_string(CONTROL_TOWER_HTML)

@app.route('/api/agents')
def get_agents():
    """Retourne la liste des agents disponibles"""
    return jsonify(IFIVEME_AGENTS)

@app.route('/api/start-agent', methods=['POST'])
def start_ifiveme_agent():
    """
    Endpoint API pour démarrer un agent iFiveMe spécifique.
    """
    try:
        data = request.json
        agent_key = data.get('agent')
        task = data.get('task')

        if not agent_key or agent_key not in IFIVEME_AGENTS:
            return jsonify({"error": "Agent non reconnu. Agents disponibles: " + ", ".join(IFIVEME_AGENTS.keys())}), 400

        if not task:
            return jsonify({"error": "La description de la tâche est requise."}), 400

        agent_config = IFIVEME_AGENTS[agent_key]
        script_path = agent_config['script']

        # Vérifier que le script existe
        if not os.path.exists(script_path):
            return jsonify({"error": f"Script agent non trouvé: {script_path}"}), 404

        # Arrêter l'agent s'il est déjà en cours
        if agent_key in active_processes:
            try:
                active_processes[agent_key].terminate()
                del active_processes[agent_key]
            except:
                pass

        socketio.emit('agent_log', {'data': f'🚀 Lancement {agent_config["name"]}: {task}'})

        # Commande Python avec la tâche passée en variable d'environnement
        env = os.environ.copy()
        env['IFIVEME_TASK'] = task
        env['IFIVEME_AGENT_MODE'] = 'control_tower'

        command = ['python3', script_path]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line-buffered
            env=env
        )

        # Stocker le processus pour suivi
        active_processes[agent_key] = process

        # Créer un thread pour écouter la sortie sans bloquer
        thread = threading.Thread(
            target=stream_python_output,
            args=(process, agent_key),
            daemon=True
        )
        thread.start()

        return jsonify({
            "status": f"Agent {agent_config['name']} lancé avec succès",
            "task": task,
            "agent": agent_key
        })

    except Exception as e:
        error_message = f"❌ Erreur lancement agent: {str(e)}"
        print(error_message)
        socketio.emit('agent_error', {'error': error_message})
        return jsonify({"error": error_message}), 500

@app.route('/api/stop-all', methods=['POST'])
def stop_all_agents():
    """Arrête tous les agents en cours"""
    try:
        stopped_count = 0
        for agent_key, process in list(active_processes.items()):
            try:
                process.terminate()
                stopped_count += 1
            except:
                pass

        active_processes.clear()

        message = f"🛑 {stopped_count} agents arrêtés"
        socketio.emit('agent_log', {'data': message})

        return jsonify({"status": message, "stopped_count": stopped_count})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def get_status():
    """Retourne le statut des agents"""
    return jsonify({
        "active_agents": list(active_processes.keys()),
        "total_agents": len(IFIVEME_AGENTS),
        "server_status": "operational"
    })

# --- Événements WebSocket ---

@socketio.on('connect')
def handle_connect():
    print('🔌 Cockpit iFiveMe connecté à la tour de contrôle.')
    emit('agent_log', {'data': '🔌 Tour de contrôle iFiveMe opérationnelle.'})

@socketio.on('disconnect')
def handle_disconnect():
    print('📡 Cockpit déconnecté.')

@socketio.on('request_agents_list')
def handle_agents_request():
    """Envoie la liste des agents au client"""
    emit('agents_list', IFIVEME_AGENTS)

# --- Démarrage du serveur ---

if __name__ == '__main__':
    print("🏗️ iFiveMe Control Tower - Démarrage")
    print("=" * 60)
    print(f"🤖 {len(IFIVEME_AGENTS)} agents iFiveMe disponibles:")

    for key, agent in IFIVEME_AGENTS.items():
        print(f"  📋 {key}: {agent['name']}")

    print("=" * 60)
    print("🌐 Interface web: http://localhost:5001")
    print("📡 WebSocket: Temps réel activé")
    print("🚀 Prêt pour pilotage des missions iFiveMe !")

    # Utiliser socketio.run() pour support WebSocket complet
    try:
        socketio.run(
            app,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5001)),
            debug=False,  # Désactiver debug pour production
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de la tour de contrôle...")
        # Nettoyer les processus actifs
        for agent_key, process in active_processes.items():
            try:
                process.terminate()
            except:
                pass
        print("✅ Tour de contrôle arrêtée proprement.")