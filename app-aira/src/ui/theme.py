# Paleta de cores rosa, fontes e espaçamentos

import flet as ft

class AppTheme:
    # Gradiente de fundo suave
    BG_GRADIENT_START = "#FDF2F4"  # Rosa pálido aconchegante
    BG_GRADIENT_END = "#F5F3FF"    # Toque sutil de lavanda

    # Cores de cartões e superfícies
    CARD_BG = "#FFFFFF"            # Branco limpo para os cards
    CARD_TRANSLUCENT = "#FAFAFA"   # Superfície suave
    
    # Cores de destaque (Rosa AI-RA)
    PRIMARY_PINK = "#FB7185"       # Rosa vibrante suave
    PRIMARY_HOVER = "#F43F5E"      # Rosa escuro para hover/clique
    TEXT_MAIN = "#1E1B4B"          # Índigo escuro para leitura perfeita
    TEXT_MUTED = "#6B7280"         # Cinza suave para legendas

    # Sombra suave para o estilo flutuante
    SOFT_SHADOW = ft.BoxShadow(
        spread_radius=0,
        blur_radius=20,
        color=ft.Colors.with_opacity(0.06, "#E11D48"),
        offset=ft.Offset(0, 8),
    )