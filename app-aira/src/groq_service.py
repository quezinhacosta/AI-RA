import json
import re
from typing import Tuple, Optional
from groq import Groq


class GroqService:
    def __init__(self, api_key: Optional[str] = None, model: str = "openai/gpt-oss-120b"):
        self.api_key = api_key
        self.model = model
        self.client = None

        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def is_configured(self) -> bool:
        return self.client is not None

    def chat_completion(self, messages: list) -> Tuple[str, Optional[dict]]:
        if not self.client:
            raise ValueError("A chave GROQ_API_KEY não foi configurada.")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.6,
                max_tokens=2048,  # Aumentado para evitar corte de JSON
            )

            raw_content = response.choices[0].message.content or ""
            return self._extract_state_update(raw_content)

        except Exception as error:
            raise RuntimeError(f"Erro na comunicação com a API Groq: {str(error)}")

    def _extract_state_update(self, raw_text: str) -> Tuple[str, Optional[dict]]:
        state_update = None
        clean_text = raw_text

        # 1. Procura bloco fechado
        pattern_closed = r"```json_update\s*([\s\S]*?)\s*```"
        match = re.search(pattern_closed, raw_text)

        if match:
            json_str = match.group(1).strip()
            clean_text = re.sub(pattern_closed, "", raw_text).strip()
            try:
                state_update = json.loads(json_str)
            except json.JSONDecodeError:
                state_update = None
        else:
            # 2. Tolerância a corte: bloco aberto mas não finalizado
            pattern_open = r"```json_update\s*([\s\S]*)"
            match_open = re.search(pattern_open, raw_text)
            if match_open:
                json_str = match_open.group(1).strip()
                clean_text = re.sub(pattern_open, "", raw_text).strip()
                # Tenta reparar chaves não fechadas
                for suffix in ["\n}", "\n}\n}", "\n}\n}\n}"]:
                    try:
                        state_update = json.loads(json_str + suffix)
                        break
                    except json.JSONDecodeError:
                        continue

        return clean_text, state_update