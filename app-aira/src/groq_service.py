# Conexão com a API da Groq

import json
import re
from typing import Tuple, Optional
from groq import Groq


class GroqService:
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.client = None

        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def is_configured(self) -> bool:
        """Verifica se a chave da API está devidamente instanciada."""
        return self.client is not None

    def chat_completion(self, messages: list) -> Tuple[str, Optional[dict]]:
        """Envia as mensagens acumuladas para o modelo na Groq.

        Retorna:
            Uma tupla contendo:
            - str: O texto limpo e formatado para exibir no balão de chat.
            - dict | None: As mutações de estado extraídas do bloco json_update (ou None se não houver).
        """
        if not self.client:
            raise ValueError(
                "A chave GROQ_API_KEY não foi configurada. "
                "Certifica-te de que definiste a variável no teu ficheiro .env."
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            )

            raw_content = response.choices[0].message.content or ""
            return self._extract_state_update(raw_content)

        except Exception as error:
            # Propaga o erro com uma mensagem clara para tratamento na interface
            raise RuntimeError(f"Erro na comunicação com a API Groq: {str(error)}")

    def _extract_state_update(self, raw_text: str) -> Tuple[str, Optional[dict]]:
        """Procura o bloco delimitado ```json_update ... ``` gerado pelo modelo,

        converte-o num dicionário Python e remove-o do texto de resposta visual.
        """
        pattern = r"```json_update\s*([\s\S]*?)\s*```"
        match = re.search(pattern, raw_text)

        state_update = None
        clean_text = raw_text

        if match:
            json_str = match.group(1).strip()
            try:
                state_update = json.loads(json_str)
                # Remove o bloco de mutação JSON para que o utilizador apenas leia o texto acolhedor
                clean_text = re.sub(pattern, "", raw_text).strip()
            except json.JSONDecodeError:
                # Caso o modelo alucine a sintaxe do JSON, mantemos o texto e ignoramos o patch inválido
                state_update = None

        return clean_text, state_update