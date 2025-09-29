"""
iFiveMe Marketing MVP - Base Agent Class
Classe de base pour tous les agents marketing
"""

import logging
import json
import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class AgentTask:
    """Structure pour définir une tâche d'agent"""
    id: str
    type: str
    priority: int
    data: Dict[str, Any]
    created_at: datetime
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class AgentMetrics:
    """Métriques de performance des agents"""
    tasks_completed: int = 0
    tasks_failed: int = 0
    average_response_time: float = 0.0
    last_activity: Optional[datetime] = None
    success_rate: float = 0.0

class BaseAgent(ABC):
    """Classe de base pour tous les agents marketing iFiveMe"""

    def __init__(self, agent_id: str, name: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.metrics = AgentMetrics()
        self.task_queue: List[AgentTask] = []
        self.is_active = False

        # Initialiser les répertoires de données
        self.data_dir = Path("data") / agent_id
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Agent {self.name} initialisé")

    @abstractmethod
    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Traite une tâche spécifique - à implémenter par chaque agent"""
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Retourne la liste des capacités de l'agent"""
        pass

    async def add_task(self, task: AgentTask) -> bool:
        """Ajoute une tâche à la queue"""
        try:
            self.task_queue.append(task)
            self.task_queue.sort(key=lambda x: x.priority, reverse=True)
            self.logger.info(f"Tâche {task.id} ajoutée à la queue")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout de la tâche {task.id}: {str(e)}")
            return False

    async def execute_tasks(self):
        """Execute toutes les tâches en queue"""
        self.is_active = True
        self.logger.info(f"Début d'exécution des tâches pour {self.name}")

        while self.task_queue and self.is_active:
            task = self.task_queue.pop(0)
            await self._execute_single_task(task)

        self.is_active = False
        self.logger.info(f"Fin d'exécution des tâches pour {self.name}")

    async def _execute_single_task(self, task: AgentTask):
        """Exécute une tâche unique avec gestion des erreurs et métriques"""
        start_time = datetime.now()

        try:
            self.logger.info(f"Début traitement tâche {task.id} de type {task.type}")
            task.status = "processing"

            # Traiter la tâche
            result = await self.process_task(task)

            # Mettre à jour le résultat
            task.result = result
            task.status = "completed"

            # Mettre à jour les métriques
            self.metrics.tasks_completed += 1
            self._update_metrics(start_time)

            self.logger.info(f"Tâche {task.id} complétée avec succès")

            # Sauvegarder le résultat
            await self._save_task_result(task)

        except Exception as e:
            task.error = str(e)
            task.status = "failed"
            self.metrics.tasks_failed += 1
            self.logger.error(f"Erreur lors du traitement de la tâche {task.id}: {str(e)}")

    def _update_metrics(self, start_time: datetime):
        """Met à jour les métriques de performance"""
        execution_time = (datetime.now() - start_time).total_seconds()

        # Calcul temps de réponse moyen
        total_tasks = self.metrics.tasks_completed + self.metrics.tasks_failed
        if total_tasks > 0:
            current_avg = self.metrics.average_response_time
            self.metrics.average_response_time = (
                (current_avg * (total_tasks - 1) + execution_time) / total_tasks
            )

        # Calcul taux de succès
        if total_tasks > 0:
            self.metrics.success_rate = (
                self.metrics.tasks_completed / total_tasks * 100
            )

        self.metrics.last_activity = datetime.now()

    async def _save_task_result(self, task: AgentTask):
        """Sauvegarde le résultat d'une tâche"""
        try:
            result_file = self.data_dir / f"task_{task.id}_result.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(task), f, indent=2, default=str, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du résultat: {str(e)}")

    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel de l'agent"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "is_active": self.is_active,
            "tasks_in_queue": len(self.task_queue),
            "metrics": asdict(self.metrics),
            "capabilities": self.get_capabilities()
        }

    async def stop(self):
        """Arrête l'agent proprement"""
        self.is_active = False
        self.logger.info(f"Agent {self.name} arrêté")

    def create_task(self, task_type: str, priority: int, data: Dict[str, Any]) -> AgentTask:
        """Crée une nouvelle tâche"""
        task_id = f"{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        return AgentTask(
            id=task_id,
            type=task_type,
            priority=priority,
            data=data,
            created_at=datetime.now()
        )

    async def health_check(self) -> bool:
        """Vérifie la santé de l'agent"""
        try:
            # Vérifications de base
            if not self.data_dir.exists():
                self.data_dir.mkdir(parents=True, exist_ok=True)

            # Test d'écriture
            test_file = self.data_dir / "health_check.txt"
            with open(test_file, 'w') as f:
                f.write(f"Health check at {datetime.now()}")
            test_file.unlink()

            self.logger.info(f"Health check passed for {self.name}")
            return True
        except Exception as e:
            self.logger.error(f"Health check failed for {self.name}: {str(e)}")
            return False