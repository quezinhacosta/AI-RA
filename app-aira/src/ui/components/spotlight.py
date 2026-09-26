import flet as ft
from src.ui.theme import AppTheme


class GoalSpotlightComponent(ft.Container):
    def __init__(self, primary_goal: dict = None, on_adjust_goal=None):
        super().__init__()
        self.primary_goal = primary_goal or {}
        self.on_adjust_goal = on_adjust_goal

        # Dimensões e acabamento
        self.expand = True
        self.height = 230
        self.bgcolor = AppTheme.CARD_BG
        self.border_radius = 28
        self.padding = 24
        self.shadow = AppTheme.SOFT_SHADOW

        # Montagem do layout interno
        self.content = self._build_layout()

    def _build_layout(self) -> ft.Column:
        target_name = self.primary_goal.get("target", "Aquisição do Primeiro Apartamento")
        target_value = self.primary_goal.get("target_value", 60000)
        monthly_target = self.primary_goal.get("monthly_target_savings", 1500)

        return ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(
                            target_name,
                            size=20,
                            weight=ft.FontWeight.W_800,
                            color=AppTheme.TEXT_MAIN,
                        ),
                        ft.Text(
                            "Meta Primordial • Construção de Património & Independência",
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=AppTheme.TEXT_MUTED,
                        ),
                    ],
                ),
                ft.Row(
                    spacing=8,
                    controls=[
                        self._build_pill_badge("Horizonte: Médio Prazo"),
                        self._build_pill_badge("Prioridade Máxima", is_highlight=True),
                        self._build_pill_badge("Liquidez / Selic"),
                    ],
                ),
                ft.Text(
                    f"Foco operacional do trimestre: assegurar a retenção do aporte regular de "
                    f"R$ {monthly_target:,.0f}/mês, protegendo o orçamento de imprevistos e acelerando o valor de entrada.".replace(",", "."),
                    size=11,
                    weight=ft.FontWeight.W_400,
                    color=AppTheme.TEXT_MUTED,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(
                            padding=ft.Padding(16, 8, 16, 8),
                            border_radius=20,
                            bgcolor=ft.Colors.with_opacity(0.12, AppTheme.PRIMARY_PINK),
                            content=ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.SAVINGS_OUTLINED, size=15, color=AppTheme.PRIMARY_HOVER),
                                    ft.Text(
                                        f"Alvo: R$ {target_value:,.0f}".replace(",", "."),
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.PRIMARY_HOVER,
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            on_click=self._handle_adjust_click,
                            padding=ft.Padding(14, 8, 14, 8),
                            border_radius=20,
                            bgcolor=AppTheme.CARD_TRANSLUCENT,
                            border=ft.Border.all(width=1, color=ft.Colors.with_opacity(0.1, AppTheme.TEXT_MUTED)),
                            content=ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.TUNE_ROUNDED, size=14, color=AppTheme.TEXT_MAIN),
                                    ft.Text(
                                        "Ajustar Meta",
                                        size=11,
                                        weight=ft.FontWeight.W_600,
                                        color=AppTheme.TEXT_MAIN,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        )

    def _build_pill_badge(self, text: str, is_highlight: bool = False) -> ft.Container:
        bg = (
            ft.Colors.with_opacity(0.15, AppTheme.PRIMARY_PINK)
            if is_highlight
            else AppTheme.CARD_TRANSLUCENT
        )
        border_col = (
            ft.Colors.TRANSPARENT
            if is_highlight
            else ft.Colors.with_opacity(0.08, AppTheme.TEXT_MUTED)
        )
        txt_col = AppTheme.PRIMARY_HOVER if is_highlight else AppTheme.TEXT_MUTED

        return ft.Container(
            padding=ft.Padding(12, 4, 12, 4),
            border_radius=14,
            bgcolor=bg,
            border=ft.Border.all(width=1, color=border_col),
            content=ft.Text(
                text,
                size=10,
                weight=ft.FontWeight.W_600 if is_highlight else ft.FontWeight.W_500,
                color=txt_col,
            ),
        )

    def _handle_adjust_click(self, e):
        if self.on_adjust_goal:
            self.on_adjust_goal()

    def update_goal_data(self, new_goal: dict):
        self.primary_goal = new_goal
        self.content = self._build_layout()
        self.update()