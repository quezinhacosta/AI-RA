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

        self.messages_list = ft.ListView(
            expand=True,
            spacing=12,
            auto_scroll=True,
            padding=ft.Padding(0, 0, 8, 0),
        )

        self.input_field = ft.TextField(
            hint_text="Conta-me o teu dia, regista gastos ou pede conselhos de foco...",
            hint_style=ft.TextStyle(size=12, color=AppTheme.TEXT_MUTED),
            text_size=13,
            color=AppTheme.TEXT_MAIN,
            bgcolor=AppTheme.CARD_TRANSLUCENT,
            border_radius=22,
            border_color=ft.Colors.TRANSPARENT,
            focused_border_color=AppTheme.PRIMARY_PINK,
            content_padding=ft.Padding(18, 12, 18, 12),
            expand=True,
            on_submit=self._handle_send_click,
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
            "Olá! Estou pronta para alinhar a tua rotina, rever o orçamento da semana ou proteger o teu descanso. Por onde queres começar hoje?"
        )

    def _build_action_chips(self) -> ft.Row:
        actions = [
            ("⚡ Rever modo do dia", "Quero rever as minhas prioridades de hoje conforme o meu nível de cansaço."),
            ("💰 Registar gasto", "Tive um gasto imprevisto de "),
            ("🏋️ Atualizar treinos", "Concluí mais um treino hoje com sucesso!"),
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
        self.input_field.value = prompt
        self.input_field.focus()
        self.update()

    def _handle_send_click(self, e):
        text = (self.input_field.value or "").strip()
        if not text:
            return

        self.input_field.value = ""
        self.input_field.disabled = True
        self.send_button.disabled = True

        self._add_user_message(text)
        self.update()

        threading.Thread(target=self._process_ai_response, args=(text,), daemon=True).start()

    def _process_ai_response(self, user_text: str):
        try:
            if self.groq_service and self.prompt_engine:
                messages = self.prompt_engine.build_context_messages(user_text)
                response_text, state_update = self.groq_service.chat_completion(messages)

                if state_update and self.storage:
                    new_state = self.storage.update_state_patch(state_update)
                    if self.on_state_updated:
                        self.on_state_updated(new_state)

                self._add_assistant_message(response_text)
            else:
                self._add_assistant_message(
                    f"Mensagem recebida: '{user_text}'. (Modo offline)."
                )
        except Exception as ex:
            self._add_assistant_message(f"Ocorreu um erro: {str(ex)}")
        finally:
            self.input_field.disabled = False
            self.send_button.disabled = False
            self.input_field.focus()
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
                    expand=True,  # Ocupa o espaço natural da linha sem quebrar o layout
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