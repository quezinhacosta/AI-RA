import json
import shutil
import sys
from pathlib import Path


class StorageService:
    def __init__(self, data_dir: str = None):
        if data_dir:
            self.base_data_path = Path(data_dir)
        else:
            if getattr(sys, "frozen", False):
                app_root = Path(sys.executable).parent
            else:
                app_root = Path(__file__).resolve().parent.parent

            self.base_data_path = app_root / "data"

        self.base_data_path.mkdir(parents=True, exist_ok=True)

        self.state_file = self.base_data_path / "user_state.json"
        self.history_file = self.base_data_path / "chat_history.json"

        self._ensure_files_exist()

    def _get_default_user_state(self) -> dict:
        """Estado inicial neutro à espera das informações voluntárias do utilizador."""
        return {
            "profile": {
                "name": "",
                "onboarding_completed": False,
            },
            "primary_goal": {
                "title": "Definir Meta Principal",
                "target_value": 0.0,
                "current_saved": 0.0,
                "monthly_target": 0.0,
                "deadline_horizon": "A definir",
            },
            "runtime_state": {
                "current_operational_mode": "MANUTENCAO",
                "energy_level": "normal",
                "weekly_habits_target": 0,
                "habits_completed_this_week": 0,
                "financial_logs": [],
                "user_notes": [],
            },
        }

    def _ensure_files_exist(self):
        """Garante a criação inicial dos ficheiros JSON."""
        if not self.state_file.exists():
            self.save_user_state(self._get_default_user_state())

        if not self.history_file.exists():
            self.save_chat_history([])

    def load_user_state(self) -> dict:
        """Lê o ficheiro user_state.json com fallback para o estado padrão."""
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            default_state = self._get_default_user_state()
            self.save_user_state(default_state)
            return default_state

    def save_user_state(self, state: dict):
        """Gravação atómica: grava num ficheiro temporário antes de substituir o original."""
        temp_file = self.state_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            shutil.move(temp_file, self.state_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise IOError(f"Falha ao gravar user_state.json: {e}")

    def save_chat_history(self, history: list):
        """Grava a lista completa de mensagens de conversa no disco."""
        temp_file = self.history_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            shutil.move(temp_file, self.history_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise IOError(f"Falha ao gravar chat_history.json: {e}")

    def load_chat_history(self, limit: int = 20) -> list:
        """Carrega as mensagens recentes da conversa."""
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
                return history[-limit:] if limit else history
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def append_chat_message(self, role: str, content: str):
        """Regista uma nova mensagem no histórico mantendo o teto recente."""
        history = self.load_chat_history(limit=100)
        history.append({"role": role, "content": content})
        self.save_chat_history(history)

    def ingest_information(self, incoming_data: dict) -> dict:
        """Ingere, consolida e persiste de forma atómica todas as mutações vindas do chatbot."""
        current_state = self.load_user_state()

        # 1. Atualizações de perfil (nome, onboarding, etc.)
        if "profile" in incoming_data and isinstance(incoming_data["profile"], dict):
            current_state["profile"].update(incoming_data["profile"])

        # 2. Definição ou ajustamento da meta primordial
        if "primary_goal" in incoming_data and isinstance(incoming_data["primary_goal"], dict):
            current_state["primary_goal"].update(incoming_data["primary_goal"])

        # 3. Mutações de estado de execução (modo ativo, energia, etc.)
        if "runtime_state" in incoming_data and isinstance(incoming_data["runtime_state"], dict):
            current_state["runtime_state"].update(incoming_data["runtime_state"])

        # 4. Registos financeiros (despesas e poupanças/aportes)
        if "financial_logs" in incoming_data and isinstance(incoming_data["financial_logs"], list):
            logs = current_state["runtime_state"].setdefault("financial_logs", [])
            for entry in incoming_data["financial_logs"]:
                logs.append(entry)
                # Se for aporte, incrementa diretamente o acumulado da meta primordial
                if entry.get("type") == "saving":
                    amount = float(entry.get("amount", 0.0))
                    current_saved = float(current_state["primary_goal"].get("current_saved", 0.0))
                    current_state["primary_goal"]["current_saved"] = current_saved + amount

        # 5. Conclusão de hábitos na semana (ex.: treinos)
        if "habits_completed" in incoming_data:
            habits = incoming_data["habits_completed"]
            if isinstance(habits, list):
                completed = current_state["runtime_state"].get("habits_completed_this_week", 0)
                current_state["runtime_state"]["habits_completed_this_week"] = completed + len(habits)

        # 6. Notas e preferências aprendidas sobre a rotina
        if "user_notes" in incoming_data:
            notes = current_state["runtime_state"].setdefault("user_notes", [])
            new_note = incoming_data["user_notes"]
            if isinstance(new_note, list):
                notes.extend(new_note)
            elif isinstance(new_note, str) and new_note not in notes:
                notes.append(new_note)

        # Gravação atómica final
        self.save_user_state(current_state)
        return current_state