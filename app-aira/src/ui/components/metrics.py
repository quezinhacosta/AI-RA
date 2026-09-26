import flet as ft
from src.ui.theme import AppTheme


class MetricsVisualizerComponent(ft.Container):
    def __init__(self, state: dict = None):
        super().__init__()
        self.state = state or {}

        self.width = 280
        self.height = 230
        self.bgcolor = AppTheme.CARD_BG
        self.border_radius = 28
        self.padding = 22  # Valor numérico direto
        self.shadow = AppTheme.SOFT_SHADOW

        self.content = self._build_content()

    def _build_content(self) -> ft.Column:
        finances = self.state.get("primary_goals", {}).get("financial", {})
        saved = finances.get("current_saved", 5000)
        target = finances.get("target_value", 60000)
        progress_ratio = min(max(saved / target, 0.0), 1.0) if target > 0 else 0.0
        percentage_text = f"{int(progress_ratio * 100)}%"

        current_mode = self.state.get("current_state", {}).get(
            "current_operational_mode", "FOCO_TOTAL"
        )

        return ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Evolução Real",
                            size=14,
                            weight=ft.FontWeight.W_700,
                            color=AppTheme.TEXT_MAIN,
                        ),
                        ft.Container(
                            padding=ft.Padding(8, 3, 8, 3),
                            border_radius=10,
                            bgcolor=ft.Colors.with_opacity(0.12, AppTheme.PRIMARY_PINK),
                            content=ft.Text(
                                percentage_text,
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.PRIMARY_HOVER,
                            ),
                        ),
                    ],
                ),
                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "Reserva Imóvel",
                                    size=11,
                                    weight=ft.FontWeight.W_500,
                                    color=AppTheme.TEXT_MUTED,
                                ),
                                ft.Text(
                                    f"R$ {saved:,.0f} / {target:,.0f}".replace(",", "."),
                                    size=11,
                                    weight=ft.FontWeight.W_600,
                                    color=AppTheme.TEXT_MAIN,
                                ),
                            ],
                        ),
                        ft.ProgressBar(
                            value=progress_ratio,
                            color=AppTheme.PRIMARY_PINK,
                            bgcolor=ft.Colors.with_opacity(0.1, AppTheme.PRIMARY_PINK),
                            height=8,
                            border_radius=8,
                        ),
                    ],
                ),
                ft.Container(
                    padding=12,
                    border_radius=16,
                    bgcolor=AppTheme.CARD_TRANSLUCENT,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=2,
                                controls=[
                                    ft.Row(
                                        spacing=4,
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.FITNESS_CENTER_ROUNDED,
                                                size=14,
                                                color=AppTheme.PRIMARY_PINK,
                                            ),
                                            ft.Text(
                                                "4/5",
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                                color=AppTheme.TEXT_MAIN,
                                            ),
                                        ],
                                    ),
                                    ft.Text(
                                        "Treinos sem.",
                                        size=9,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                            ),
                            ft.VerticalDivider(width=1, color=ft.Colors.with_opacity(0.1, AppTheme.TEXT_MUTED)),
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=2,
                                controls=[
                                    ft.Row(
                                        spacing=4,
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.BOLT_ROUNDED,
                                                size=15,
                                                color=ft.Colors.AMBER_600,
                                            ),
                                            ft.Text(
                                                current_mode.replace("_", " ").title(),
                                                size=11,
                                                weight=ft.FontWeight.BOLD,
                                                color=AppTheme.TEXT_MAIN,
                                            ),
                                        ],
                                    ),
                                    ft.Text(
                                        "Estado Geral",
                                        size=9,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        )

    def update_metrics(self, new_state: dict):
        self.state = new_state
        self.content = self._build_content()
        self.update()