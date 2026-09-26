import threading
import flet as ft
from src.ui.theme import AppTheme


class ChatStreamComponent(ft.Column):
    def __init__(self, groq_service=None, prompt_engine=None, storage=None, on_state_updated=None):
        super().__init__()
        self.groq_service = groq_service
        self.prompt_engine = prompt_engine
        self.storage = storage
        self.on_state_updated = on_state_updated

        self.expand = True
        self.spacing = 14

        # Feed rolável de mensagens
        self.messages_list = ft.ListView(
            expand=True,
            spacing=12,
            auto_scroll=True,
            padding=ft.Padding(0, 0, 8, 0),
        )

        # Campo de texto limpo, sem argumentos conflitantes
        self.input_text = ft.TextField(
            hint_text="Digite sua mensagem e pressione Enter...",
            hint_style=ft.TextStyle(size=12, color=AppTheme.TEXT_MUTED),
            text_size=13,
            color=AppTheme.TEXT_MAIN,
            border=ft.InputBorder.NONE,
            content_padding=ft.Padding(18, 10, 18, 10),
            expand=True,
            on_submit=self._handle_send_click,
        )

        # Container que aplica o arredondamento e fundo suave com segurança
        self.input_field = ft.Container(
            content=self.input_text,
            bgcolor=AppTheme.CARD_TRANSLUCENT,
            border_radius=22,
            expand=True,
        )

        self.send_button = ft.IconButton(
            icon=ft.Icons.ARROW_UPWARD_ROUNDED,
            icon_color=ft.Colors.WHITE,
            bgcolor=AppTheme.PRIMARY_PINK,
            icon_size=18,
            on_click=self._handle_send_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=16),
            ),
        )

        self.controls = [
            self._build_action_chips(),
            self.messages_list,
            ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.input_field,
                    self.send_button,
                ],
            ),
        ]

        self._add_assistant_message(
            "Olá! Estou pronta para te acompanhar hoje. Como está o teu nível de energia e o teu plano de metas para hoje?"
        )

    def _build_action_chips(self) -> ft.Row:
        actions = [
            ("⚡ Rever modo do dia", "Hoje o dia foi bastante exigente e sinto um nível de cansaço elevado."),
            ("💰 Registar gasto", "Regista uma despesa não prevista de R$ "),
            ("🏋️ Registar treino", "Concluí o meu treino de pernas e cárdio com sucesso hoje!"),
        ]

        return ft.Row(
            spacing=8,
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                ft.Container(
                    on_click=lambda e, prompt=p: self._fill_and_send(prompt),
                    padding=ft.Padding(12, 6, 12, 6),
                    border_radius=14,
                    bgcolor=ft.Colors.with_opacity(0.1, AppTheme.PRIMARY_PINK),
                    content=ft.Text(
                        title,
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color=AppTheme.PRIMARY_HOVER,
                    ),
                )
                for title, p in actions
            ],
        )

    def _fill_and_send(self, prompt: str):
        self.input_text.value = prompt
        self.update()

    def _handle_send_click(self, e):
        text = (self.input_text.value or "").strip()
        if not text:
            return

        self.input_text.value = ""
        self.input_text.disabled = True
        self.send_button.disabled = True

        self._add_user_message(text)
        self.update()

        # Executa em segundo plano para não congelar o layout durante a inferência
        threading.Thread(target=self._process_ai_response, args=(text,), daemon=True).start()

    def _process_ai_response(self, user_text: str):
        try:
            if self.groq_service and self.prompt_engine:
                # 1. Carrega histórico e constrói o prompt adaptativo
                history = self.storage.load_chat_history(limit=8) if self.storage else []
                messages = self.prompt_engine.build_context_messages(user_text, history=history)

                # 2. Chama a Groq e extrai mutações de estado
                response_text, state_update = self.groq_service.chat_completion(messages)

                # 3. Ingestão e persistência atómica no disco
                if self.storage:
                    self.storage.append_chat_message("user", user_text)
                    self.storage.append_chat_message("assistant", response_text)

                    if state_update:
                        new_state = self.storage.ingest_information(state_update)
                        self.prompt_engine.update_internal_state(new_state)
                        if self.on_state_updated:
                            self.on_state_updated(new_state)

                self._add_assistant_message(response_text)
            else:
                self._add_assistant_message(f"Mensagem processada (Modo offline): '{user_text}'.")
        except Exception as ex:
            self._add_assistant_message(f"Ocorreu uma falha na resposta da IA: {str(ex)}")
        finally:
            self.input_field.disabled = False
            self.send_button.disabled = False
            self.update()

    def _add_user_message(self, text: str):
        bubble = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Container(
                    bgcolor=AppTheme.PRIMARY_PINK,
                    border_radius=ft.BorderRadius.only(
                        top_left=18, top_right=18, bottom_left=18, bottom_right=4
                    ),
                    padding=ft.Padding(16, 10, 16, 10),
                    content=ft.Text(
                        text,
                        size=13,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_400,
                        selectable=True,
                    ),
                )
            ],
        )
        self.messages_list.controls.append(bubble)

    def _add_assistant_message(self, text: str):
        bubble = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=8,
            controls=[
                ft.CircleAvatar(
                    radius=12,
                    bgcolor=ft.Colors.with_opacity(0.15, AppTheme.PRIMARY_PINK),
                    content=ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, size=12, color=AppTheme.PRIMARY_PINK),
                ),
                ft.Container(
                    bgcolor=AppTheme.CARD_TRANSLUCENT,
                    border_radius=ft.BorderRadius.only(
                        top_left=4, top_right=18, bottom_left=18, bottom_right=18
                    ),
                    padding=ft.Padding(16, 10, 16, 10),
                    expand=True,
                    content=ft.Text(
                        text,
                        size=13,
                        color=AppTheme.TEXT_MAIN,
                        weight=ft.FontWeight.W_400,
                        selectable=True,
                    ),
                ),
            ],
        )
        self.messages_list.controls.append(bubble)