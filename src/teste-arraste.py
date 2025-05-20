import flet as ft
import requests


def embaralhar():
    truco_cards = [
        'AS','2S','3S','4S','5S','6S','7S','QS','JS','KS',
        'AH','2H','3H','4H','5H','6H','7H','QH','JH','KH',
        'AD','2D','3D','4D','5D','6D','7D','QD','JD','KD',
        'AC','2C','3C','4C','5C','6C','7C','QC','JC','KC'
    ]

    cards_str = ",".join(truco_cards)
    url_create = f"https://deckofcardsapi.com/api/deck/new/shuffle/?cards={cards_str}"
    response_create = requests.get(url_create).json()

    if response_create["success"]:
        deck_id = response_create["deck_id"]
        url_draw = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=7"
        response_draw = requests.get(url_draw).json()

        if response_draw["success"]:
            cartas = response_draw["cards"]
            jogador1 = cartas[:3]
            jogador2 = cartas[3:6]
            manilha = cartas[6]
            return jogador1, jogador2, manilha
        
    return [], [], None


def main(page: ft.Page):
    page.title = "Truco Drag & Drop"
    page.scroll = True

    jogador1_container = ft.Column()
    jogador2_container = ft.Column()
    manilha_container = ft.Column()

    slot_content = ft.Container(
        width=100,
        height=140,
        bgcolor=ft.Colors.GREY_200,
        border=ft.border.all(1),
        alignment=ft.alignment.center
    )

    def on_accept_drag(e: ft.DragTargetEvent):
        slot_content.content = ft.Image(src=e.data, width=100)
        page.update()

    slot_carta_j1 = ft.DragTarget(
        content=slot_content,
        on_accept=on_accept_drag
    )

    def atualizar_cartas(e=None):
        j1, j2, manilha = embaralhar()

        jogador1_cartas = []
        for c in j1:
            draggable = ft.Draggable(
                content=ft.Image(src=c['image'], width=100),
                data=c['image']
            )
            jogador1_cartas.append(draggable)

        jogador1_container.controls = [
            ft.Text("Jogador 1:"),
            ft.Row(jogador1_cartas, spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ]

        jogador2_container.controls = [
            ft.Text("Jogador 2:"),
            ft.Row([
                ft.Image(src=c['image'], width=100) for c in j2
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ]

        manilha_container.controls = [
            ft.Text("Manilha:"),
            ft.Image(src=manilha["image"], width=120) if manilha else ft.Text("Erro")
        ]
        
        page.update()

    btn_embaralhar = ft.IconButton(icon=ft.Icons.SHUFFLE, on_click=atualizar_cartas)

    page.add(
        jogador1_container,
        ft.Text("Slot de J1 (solte uma carta aqui):"),
        slot_carta_j1,
        ft.Divider(),
        jogador2_container,
        ft.Divider(),
        manilha_container,
        ft.Divider(),
        btn_embaralhar
    )

    atualizar_cartas()


ft.app(target=main, assets_dir="assets")
