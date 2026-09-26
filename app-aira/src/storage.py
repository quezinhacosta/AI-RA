# Leitura e gravação atômica dos JSONs

import json
import os
import shutil
import sys
from pathlib import Path


class StorageService:
    def __init__(self, data_dir: str = None):
        # Determina a raiz real do projeto de forma compatível com dev e com o executável (.exe)
        if data_dir:
            self.base_data_path = Path(data_dir)
        else:
            if getattr(sys, "frozen", False):
                # Rodando via PyInstaller (.exe)
                app_root = Path(sys.executable).parent
            else:
                # Rodando em modo de desenvolvimento (Python puro)
                app_root = Path(__file__).resolve().parent.parent

            self.base_data_path = app_root / "data"

        # Garante que a pasta data/ existe
        self.base_data_path.mkdir(parents=True, exist_ok=True)

        self.state_file = self.base_data_path / "user_state.json"
        self.history_file = self.base_data_path / "chat_history.json"

        # Inicializa arquivos caso não existam
        self._ensure_files_exist()

    def _get_default_user_state(self) -> dict:
        """Estado padrão inicial do usuário caso o arquivo não exista."""
        return {
            "profile": {
                "name": "Quezia",
                "core_anchors": ["Treino regular", "Sono 7h+", "Foco em metas"],
            },
            "current_state": {
                "energy_level": "media",
                "financial_runway_status": "estavel",
                "current_operational_mode": "FOCO_TOTAL",
            },
            "primary_goals": {
                "financial": {
                    "target": "Entrada do Apartamento",
                    "target_value": 60000,
                    "current_saved": 5000,
                    "monthly_target_savings": 1500,
                },
                "career": {
                    "target": "Aceleração Profissional e Destaque",
                    "current_bottleneck": "Gestão de tempo entre entregas e projetos de impacto",
                },
            },
            "constraints": {
                "weekly_free_hours": 12,
                "non_negotiable_budget_ceiling": 400,
            },
        }

    def _ensure_files_exist(self):
        """Cria os arquivos iniciais se for a primeira execução."""
        if not self.state_file.exists():
            self.save_user_state(self._get_default_user_state())

        if not self.history_file.exists():
            self.save_chat_history([])

    def load_user_state(self) -> dict:
        """Carrega o arquivo user_state.json com tratamento de erros."""
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            default_state = self._get_default_user_state()
            self.save_user_state(default_state)
            return default_state

    def save_user_state(self, state: dict):
        """Gravação atômica: escreve em arquivo temporário antes de substituir o original."""
        temp_file = self.state_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            # Substituição atômica no sistema de arquivos
            shutil.move(temp_file, self.state_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise IOError(f"Falha ao salvar user_state.json: {e}")

    def save_chat_history(self, history: list):
        """Salva a lista completa de histórico no arquivo chat_history.json."""
        temp_file = self.history_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            shutil.move(temp_file, self.history_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise IOError(f"Falha ao salvar chat_history.json: {e}")

    def update_state_patch(self, patch: dict) -> dict:
        """Aplica alterações parciais (patch) no estado atual e salva automaticamente."""
        current_state = self.load_user_state()

        def deep_merge(source, destination):
            for key, value in source.items():
                if isinstance(value, dict) and key in destination and isinstance(destination[key], dict):
                    deep_merge(value, destination[key])
                else:
                    destination[key] = value
            return destination

        updated_state = deep_merge(patch, current_state)
        self.save_user_state(updated_state)
        return updated_state

    def load_chat_history(self, limit: int = 20) -> list:
        """Carrega as últimas mensagens registradas."""
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
                return history[-limit:] if limit else history
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def append_chat_message(self, role: str, content: str):
        """Registra uma nova mensagem no histórico local."""
        history = self.load_chat_history(limit=100)
        history.append({"role": role, "content": content})

        temp_file = self.history_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            shutil.move(temp_file, self.history_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise IOError(f"Falha ao salvar chat_history.json: {e}")