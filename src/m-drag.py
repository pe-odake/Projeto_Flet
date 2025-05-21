import flet as ft
import requests

class truco:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0

def embaralhar():
    truco_cards = [
        'AS','2S','3S','4S','5S','6S','7S','QS','JS','KS',
        'AH','2H','3H','4H','5H','6H','7H','QH','JH','KH',
        'AD','2D','3D','4D','5D','6D','7D','QD','JD','KD',
        'AC','2C','3C','4C','5C','6C','7C','QC','JC','KC'
    ]

    cards_str = ",".join(truco_cards)
    url_create = f"https://deckofcardsapi.com/api/deck/new/shuffle/?cards={cards_str}"
    #print(url_create)
    response_create = requests.get(url_create).json()

    if response_create["success"]:
        deck_id = response_create["deck_id"]
        url_draw = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=7"
        #print(url_draw)
        response_draw = requests.get(url_draw).json()

        if response_draw["success"]:
            cartas = response_draw["cards"]
            jogador1 = cartas[:3] 
            jogador2 = cartas[3:6]
            manilha = cartas[6]
            return jogador1, jogador2, manilha
        
    return [], [], None


def main(page: ft.Page):
    page.title = "Truco"
    page.scroll = True

    jogador1_container = ft.Column()
    jogador2_container = ft.Column()
    manilha_container = ft.Column()
    
    # FUNÇÕES DE ARRASTAR
    
    def place(card, slot):
        """place card to the slot"""
        card.top = slot.top
        card.left = slot.left

    def bounce_back(game, card):
        """return card to its original position"""
        card.top = game.start_top
        card.left = game.start_left
    
    def start_drag(e: ft.DragStartEvent):
        truco.start_top = e.control.top
        truco.start_left = e.control.left

    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()
    
    def drop(e: ft.DragEndEvent):
        if (
            abs(e.control.top - slot.top) < 20
            and abs(e.control.left - slot.left) < 20
        ):
            place(e.control, slot)

        else:
            bounce_back(truco, e.control)

        e.control.update()

    
    # FIM DELAS

    def atualizar_cartas(e=None):
        j1, j2, manilha = embaralhar()

        jogador1_container.controls = [
            ft.Text("Jogador 1:"),
            ft.Row([ 
                ft.Column([
                    ft.Text(f"{c['value']} de {c['suit']}"),
                    ft.Image(src=c["image"], width=100)
                ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                for c in j1
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ]

        # jogador1_container.controls = [
        #     ft.Text('Jogador 1:'),
        #     ft.Row([
        #         ft.Column([
        #             ft.Text(f"{c['value']} de {c['suit']}"),
        #             ft.GestureDetector(
        #                 mouse_cursor=ft.MouseCursor.MOVE,
        #                 drag_interval=5,
        #                 on_pan_start=start_drag,
        #                 on_pan_update=drag,
        #                 on_pan_end=drop,
        #                 left=0,
        #                 top=0,
        #                 content=ft.Container(
        #                     ft.Image(src='coco.png', width=70),
        #                     width=70,
        #                     height=100
        #                 ),
        #             )
        #         ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        #         for c in j1
        #     ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        # ]   

        jogador2_container.controls = [
            ft.Text("Jogador 2:"),
            ft.Row([
                ft.Column([
                    ft.Text(f"{c['value']} de {c['suit']}"),
                    ft.Image(src=c['image'], width=100)
                ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                for c in j2
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ]

        manilha_container.controls = [
            ft.Text("Manilha:"),
            ft.Image(src='https://deckofcardsapi.com/static/img/QC.png', width=120) if manilha else ft.Text("Erro")
        ]

        page.update()

    btn_embaralhar = ft.IconButton(icon=ft.Icons.SHUFFLE, on_click=atualizar_cartas)
    slot = ft.Container(
        width=70, height=100, left=200, top=0, border=ft.border.all(1)
    )
    

    # ADICIONAR OS ELEMENTOS NA PAGINA
    
    page.add(
        jogador1_container,ft.Divider(),
        slot,
        jogador2_container,ft.Divider(),
        manilha_container,ft.Divider(),
        btn_embaralhar
    )
    atualizar_cartas()

ft.app(target=main, assets_dir="assets")