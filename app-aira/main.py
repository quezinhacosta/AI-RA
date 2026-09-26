import os
import flet as ft
from dotenv import load_dotenv

load_dotenv()

from src.ui.theme import AppTheme
from src.ui.components.sidebar import SidebarComponent
from src.ui.components.spotlight import GoalSpotlightComponent
from src.ui.components.metrics import MetricsVisualizerComponent
from src.ui.components.chat import ChatStreamComponent
from src.storage import StorageService
from src.groq_service import GroqService
from src.prompt_engine import PromptEngine


def main(page: ft.Page):
    page.title = "AI-RA"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # Inicialização de Serviços
    storage = StorageService()
    user_state = storage.load_user_state()
    
    api_key = os.getenv("GROQ_API_KEY")
    groq_service = GroqService(api_key=api_key)
    prompt_engine = PromptEngine(user_state=user_state)

    # Componentes de UI
    sidebar = SidebarComponent(user_name=user_state.get("profile", {}).get("name") or "Visitante")
    spotlight = GoalSpotlightComponent(primary_goal=user_state.get("primary_goal", {}))
    metrics = MetricsVisualizerComponent(state=user_state)

    # Callback reativo: atualiza o dashboard quando o chatbot ingere novos dados
    def on_state_updated(new_state):
        metrics.update_metrics(new_state)
        spotlight.update_goal_data(new_state.get("primary_goal", {}))
        if new_state.get("profile", {}).get("name"):
            sidebar.user_name = new_state["profile"]["name"]
            sidebar.content = sidebar._build_layout()
            sidebar.update()

    chat = ChatStreamComponent(
        groq_service=groq_service,
        prompt_engine=prompt_engine,
        storage=storage,
        on_state_updated=on_state_updated,
    )

    main_dashboard = ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=16,
            controls=[
                ft.Row(
                    spacing=16,
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        spotlight,
                        metrics,
                    ],
                ),
                ft.Container(
                    expand=True,
                    bgcolor=AppTheme.CARD_BG,
                    border_radius=28,
                    padding=18,
                    shadow=AppTheme.SOFT_SHADOW,
                    content=chat,
                ),
            ],
        ),
    )

    app_layout = ft.Container(
        expand=True,
        border_radius=28,
        padding=14,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[AppTheme.BG_GRADIENT_START, AppTheme.BG_GRADIENT_END],
        ),
        content=ft.Row(
            expand=True,
            spacing=16,
            controls=[
                sidebar,
                main_dashboard,
            ],
        ),
    )

    page.add(app_layout)


if __name__ == "__main__":
    if hasattr(ft, "app"):
        ft.app(main)
    elif hasattr(ft, "run"):
        ft.run(main)