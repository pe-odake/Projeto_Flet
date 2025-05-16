import flet as ft
import requests

import requests

p1 = []
p2 = []

def embaralhar():
    # Cartas do Truco (40 cartas)
    truco_cards = [
        'AS','2S','3S','4S','5S','6S','7S','QS','JS','KS', # ESPADILHA 
        'AH','2H','3H','4H','5H','6H','7H','QH','JH','KH', # COPAS
        'AD','2D','3D','4D','5D','6D','7D','QD','JD','KD', # OUROS
        'AC','2C','3C','4C','5C','6C','7C','QC','JC','KC'  # ZAP
    ]

    # Junta as cartas em uma string separada por vírgula
    cards_str = ",".join(truco_cards)

    # 1. Criar baralho com as cartas de Truco
    url_create = f"https://deckofcardsapi.com/api/deck/new/shuffle/?cards={cards_str}"
    response_create = requests.get(url_create).json()

    if response_create["success"]:
        deck_id = response_create["deck_id"]
        print(f"Baralho criado com ID: {deck_id}")

        # 2. Comprar 6 cartas (3 para cada jogador)
        url_draw = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=7"
        response_draw = requests.get(url_draw).json()

        if response_draw["success"]:
            cartas = response_draw["cards"]
            
            # Distribuir 3 cartas para cada jogador
            jogador1 = cartas[:3]
            jogador2 = cartas[3:6]
            manilha = cartas[6]
            global imagem 
            imagem = manilha['image']
            
            global cartas_jogador1
            cartas_jogador1 = [ft.Text(f"Jogador 1:")] + [
                widget
                for c in jogador1
                for widget in (ft.Text(f"{c['value']} de {c['suit']}"), ft.Image(src=c['image'], width=100))
            ]

            global cartas_jogador2
            cartas_jogador2 = [ft.Text(f"Jogador 2:")] + [
                widget
                for c in jogador2
                for widget in (ft.Text(f"{c['value']} de {c['suit']}"), ft.Image(src=c['image'], width=100))
            ]
        else:
            print("Erro ao comprar cartas.")
    else:
        print("Erro ao criar baralho.")


def main(page: ft.Page):
    embaralhar()
    
    page.title = "Hello Flet!"
    page.scroll = True
    page.add(*cartas_jogador1, ft.Divider(), *cartas_jogador2)
    page.add(ft.Image(imagem))
    page.add(
        ft.CupertinoButton(
            content=ft.Text(
                "Embaralhar",
                color=ft.CupertinoColors.DESTRUCTIVE_RED,
            ),
            bgcolor=ft.CupertinoColors.LIGHT_BACKGROUND_GRAY,
            opacity_on_click=0.8,
            on_click=embaralhar,
        ),
    )

ft.app(target=main)
