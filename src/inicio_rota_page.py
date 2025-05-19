import flet as ft

def menu_view(page: ft.Page):
    return ft.View(
        route="/",
        controls=[
            ft.Text("Bem-vindo ao Truco!", size=30),
            ft.ElevatedButton("COCO", on_click=lambda e: page.go("/jogo")), # <--- ROTA PARA QUAL ENDEREÇO ESSE BOTÃO VAI LEVAR
            ft.Image(src='coco.png', width=120)
        ]
    )
