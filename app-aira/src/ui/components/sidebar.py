import flet as ft
from src.ui.theme import AppTheme


class SidebarComponent(ft.Container):
    def __init__(self, user_name: str = "Quezia", on_nav_change=None):
        super().__init__()
        self.user_name = user_name
        self.on_nav_change = on_nav_change
        self.current_selected = "Overview"

        # Configurações do cartão lateral
        self.width = 240
        self.bgcolor = AppTheme.CARD_BG
        self.border_radius = 28
        self.padding = 24  # Valor numérico direto compatível com todas as versões
        self.shadow = AppTheme.SOFT_SHADOW

        # Conteúdo interno
        self.content = self._build_layout()

    def _build_layout(self) -> ft.Column:
        return ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        # Logo
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                            controls=[
                                ft.Container(
                                    width=12,
                                    height=12,
                                    border_radius=4,
                                    bgcolor=AppTheme.PRIMARY_PINK,
                                ),
                                ft.Text(
                                    "AI-RA",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppTheme.TEXT_MAIN,
                                ),
                            ],
                        ),
                        # Avatar
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                ft.CircleAvatar(
                                    radius=34,
                                    bgcolor=ft.Colors.with_opacity(0.15, AppTheme.PRIMARY_PINK),
                                    content=ft.Icon(
                                        ft.Icons.PERSON_ROUNDED,
                                        size=34,
                                        color=AppTheme.PRIMARY_PINK,
                                    ),
                                ),
                                ft.Text(
                                    self.user_name,
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=AppTheme.TEXT_MAIN,
                                ),
                                ft.Container(
                                    padding=ft.Padding(10, 4, 10, 4),
                                    border_radius=12,
                                    bgcolor=ft.Colors.with_opacity(0.1, AppTheme.PRIMARY_PINK),
                                    content=ft.Text(
                                        "Online • Copiloto Ativo",
                                        size=10,
                                        weight=ft.FontWeight.W_500,
                                        color=AppTheme.PRIMARY_HOVER,
                                    ),
                                ),
                            ],
                        ),
                        ft.Divider(height=1, color=ft.Colors.with_opacity(0.08, AppTheme.TEXT_MUTED)),
                        self._build_nav_items(),
                    ],
                ),
                # Botões inferiores
                ft.Column(
                    spacing=6,
                    controls=[
                        self._nav_button(
                            icon=ft.Icons.SETTINGS_OUTLINED,
                            label="Definições",
                            item_id="Settings",
                        ),
                        self._nav_button(
                            icon=ft.Icons.LOGOUT_ROUNDED,
                            label="Sair",
                            item_id="Logout",
                            is_logout=True,
                        ),
                    ],
                ),
            ],
        )

    def _build_nav_items(self) -> ft.Column:
        items = [
            ("Visão Geral", ft.Icons.DASHBOARD_ROUNDED, "Overview"),
            ("Copiloto IA", ft.Icons.AUTO_AWESOME_ROUNDED, "Chat"),
            ("Objetivo: Casa", ft.Icons.HOME_WORK_ROUNDED, "PropertyGoal"),
            ("Rotina & Hábitos", ft.Icons.FAVORITE_BORDER_ROUNDED, "Habits"),
            ("Finanças", ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, "Finance"),
        ]

        return ft.Column(
            spacing=6,
            controls=[
                self._nav_button(label=label, icon=icon, item_id=item_id)
                for label, icon, item_id in items
            ],
        )

    def _nav_button(self, label: str, icon: str, item_id: str, is_logout: bool = False) -> ft.Container:
        is_active = self.current_selected == item_id

        bg_color = (
            ft.Colors.with_opacity(0.15, AppTheme.PRIMARY_PINK)
            if is_active
            else ft.Colors.TRANSPARENT
        )
        text_color = (
            AppTheme.PRIMARY_HOVER
            if is_active
            else (ft.Colors.RED_400 if is_logout else AppTheme.TEXT_MUTED)
        )

        def on_click(e):
            if not is_logout:
                self.current_selected = item_id
                self.content = self._build_layout()
                self.update()
                if self.on_nav_change:
                    self.on_nav_change(item_id)

        return ft.Container(
            on_click=on_click,
            border_radius=16,
            padding=ft.Padding(12, 10, 12, 10),
            bgcolor=bg_color,
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(icon, size=18, color=text_color),
                    ft.Text(
                        label,
                        size=13,
                        weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_500,
                        color=text_color,
                    ),
                ],
            ),
        )