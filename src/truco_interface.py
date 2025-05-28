import flet as ft
from game_logic import TrucoGame
from bot import Bot  
import random
import asyncio


class truco_interface(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
        self.start_top = 0
        self.start_left = 0
        
        self.cartas_no_slot_jogada = []
        
        self.jogador1_container = ft.Column()
        self.jogador2_container = ft.Column()
        self.manilha_container = ft.Column()

        self.cartas_jogador1 = []
        self.cartas_jogador2 = []  
        
        self.pontos_j1 = 0
        self.pontos_j2 = 0
        self.win_rodadas_j1 = 0
        self.win_rodadas_j2 = 0

        self.vez_do_jogador = 1  

        self.manilha = ft.Container()  

        self.btn_embaralhar = ft.IconButton(icon=ft.Icons.SHUFFLE, on_click=self.atualizar_cartas)
        self.slot = ft.Container(
                width=70,
                height=100,
                left=200,
                top=170,
                border=ft.border.all(2),
                border_radius=5
        )

        self.slot_jogada = ft.Container(
                width=70,
                height=100,
                left=150,
                top=300,
                border=ft.border.all(2),
                border_radius=5
        )
        
        self.slot_jogada_bot = ft.Container(
            width=70,
            height=100,
            # left=350,
            # top=300,
            border=ft.border.all(2),
            border_radius=5,
            content=None 
        )
        
        self.btn_confirmar_jogada = ft.ElevatedButton(
            text="Confirmar Jogada",
            on_click=self.confirmar_jogada
        )
        
        self.valor_truco_atual = 1 
        self.btn_truco = ft.ElevatedButton(
            text="Pedir Truco",
            on_click=self.pedir_truco
        )
        #self.controls.insert(3, self.btn_truco)  
        
        self.placar_jogo = ft.Text(f"Jogador 1 - {self.pontos_j1} ----- Jogador 2 - {self.pontos_j2}", size=26, weight=ft.FontWeight.BOLD)
        self.placar_rodada = ft.Text(f"Jogador 1: {self.win_rodadas_j1}\nJogador 2: {self.win_rodadas_j2}", size=18)#, weight=ft.FontWeight.BOLD

        self.controls = [
            self.placar_jogo,
            self.placar_rodada,
            self.jogador1_container, ft.Divider(),
            self.btn_confirmar_jogada,
            self.btn_truco,
            self.slot_jogada_bot,
            self.jogador2_container, 
            ft.Divider(), 
            self.manilha_container,
            self.btn_embaralhar
        ]

        self.atualizar_cartas()

    def atualizar_cartas(self, e=None):

        self.valor_truco_atual = 1
        self.btn_truco.text = "Pedir Truco"
        j1, j2, manilha = TrucoGame.embaralhar()

        self.cartas_jogador2 = j2  

        self.cartas_no_slot_jogada.clear() 
        self.cartas_jogador1.clear()  # LIMPA OS SLOTS

        slots_cartas = [self.criar_carta(c, jogador=1, index=i) for i, c in enumerate(j1)]
        slots = [item[0] for item in slots_cartas]
        cartas = [item[1] for item in slots_cartas]

        # Salva as cartas do jogador 1
        self.cartas_jogador1 = cartas

        # Atualiza a interface do jogador 1 com Stack (slots + cartas + slot de jogada)
        self.jogador1_container.controls = [
            ft.Text("Jogador 1:"),
            ft.Stack(
                controls=[*slots, *cartas, self.slot_jogada],
                width=600,
                height=400
            )
        ]

        # Atualiza a interface do jogador 2
        self.jogador2_container.controls = [
            ft.Text("Jogador 2:"),
            ft.Row([
                self.criar_carta(c, jogador=2) for c in j2
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ]

        self.manilha_container.controls = [
            ft.Text("Vira:"),
            ft.Image(src=manilha['image'], width=120, data=manilha) if manilha else ft.Text("Erro")
        ]

        self.manilha.content = ft.Image(src=manilha['image'], width=120)
        self.manilha.data = manilha

        self.page.update()

    
    # FUNÇÕES DO DRAG
    
    # def place(card, slot):
    #     card.top = slot.top
    #     card.left = slot.left

    # def bounce_back(game, card):
    #     card.top = game.start_top
    #     card.left = game.start_left

    def start_drag(self, e: ft.DragStartEvent):
        self.start_top = e.control.top
        self.start_left = e.control.left

    def drag(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(self, e: ft.DragEndEvent):
        def is_in_slot(slot):
            return abs(e.control.top - slot.top) < 20 and abs(e.control.left - slot.left) < 20

        stack_cartas = self.jogador1_container.controls[1]  # O Stack com cartas + slots

        if is_in_slot(self.slot_jogada):
            # Remove carta anterior do slot se existir
            if self.cartas_no_slot_jogada:
                carta_antiga = self.cartas_no_slot_jogada.pop()
                slot_antigo = carta_antiga.data["slot"]
                slot_antigo.visible = True
                carta_antiga.top = carta_antiga.data["original_top"]
                carta_antiga.left = carta_antiga.data["original_left"]
                stack_cartas.controls.append(carta_antiga)
                self.cartas_jogador1.append(carta_antiga)

            e.control.top = self.slot_jogada.top
            e.control.left = self.slot_jogada.left

            slot_atual = e.control.data["slot"]
            slot_atual.visible = False

            if e.control not in stack_cartas.controls:
                stack_cartas.controls.append(e.control)

            self.cartas_no_slot_jogada.append(e.control)

            if e.control in self.cartas_jogador1:
                self.cartas_jogador1.remove(e.control)

        else:
            # Volta para posição original
            e.control.top = e.control.data["original_top"]
            e.control.left = e.control.data["original_left"]

            slot = e.control.data["slot"]
            slot.visible = True  # Reexibe o slot

            if e.control not in stack_cartas.controls:
                stack_cartas.controls.append(e.control)

            if e.control not in self.cartas_jogador1:
                self.cartas_jogador1.append(e.control)

        e.control.update()
        self.page.update()


    
    # FIM DELAS    
    
    def criar_carta(self, carta, jogador, index=0):
        imagem = 'back_cards.png' if jogador == 2 else carta['image']
        
        left_pos = 50 + index * 100  # ESPAÇAMENTO
        top_pos = 170

        if jogador == 1:
            slot = ft.Container(
                width=70,
                height=100,
                left=left_pos,
                top=top_pos,
                border=ft.border.all(2, ft.Colors.BLUE),
                border_radius=5
            )

            carta_widget = ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                drag_interval=5,
                on_pan_start=self.start_drag,
                on_pan_update=self.drag,
                on_pan_end=self.drop,
                left=left_pos,
                top=top_pos,
                data={"original_top": top_pos, "original_left": left_pos, "slot": slot},  
                content=ft.Container(
                    content=ft.Image(imagem),
                    width=70,
                    height=100,
                    border_radius=5
                ),
            )


            return (slot, carta_widget)

        
        else:
            return ft.Column([
                ft.Image(src=imagem, width=70)
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

# CONFIRMAR JOGADA

    def confirmar_jogada(self, e):
        if not self.cartas_no_slot_jogada:
            self.page.snack_bar = ft.SnackBar(ft.Text("Jogador 1 precisa jogar uma carta."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Carta jogada pelo jogador 1
        carta1 = self.get_card_info(self.cartas_no_slot_jogada[0])

        if self.cartas_jogador2:
            modo = random.choices(["agressivo", "leve", "aleatorio"], weights=[0.8, 0.1, 0.1])[0]

            bot = Bot(self.cartas_jogador2, self.manilha.data, modo=modo)
            carta_bot = bot.escolher_carta(carta_adversario=carta1, j1_tem_ponto=self.win_rodadas_j1 == 1)
            print(carta_bot['image'])
            self.cartas_jogador2 = bot.cartas 

            self.slot_jogada_bot.content = ft.Image(
                src=carta_bot['image'],
                width=70,
                data=carta_bot
            )
            
            nova_mao_j2 = []
            for i, c in enumerate(self.cartas_jogador2):
                nova_mao_j2.append(self.criar_carta(c, jogador=2))

            while len(nova_mao_j2) < 3:
                nova_mao_j2.append(ft.Container(width=70, height=100, border=ft.border.all(2, ft.Colors.GREY), border_radius=5))

            #self.jogador2_container.controls[1] = ft.Row(nova_mao_j2, spacing=20, alignment=ft.MainAxisAlignment.CENTER)
            self.jogador2_container.controls = [
                ft.Text("Jogador 2:"),
                ft.Row(nova_mao_j2, spacing=20, alignment=ft.MainAxisAlignment.CENTER)
            ]
    
        else:
            self.slot_jogada_bot.content = None
            print('TESTE QUE O SLOT DO BOT NÃO ESTA RECEBENDO NADA')

        self.page.update()

        # Carta jogada pelo bot para comparar
        carta2 = carta_bot

        manilha_base = self.manilha.data

        vencedor = TrucoGame.comparar_cartas(carta1, carta2, manilha_base)

        if vencedor == 1:
            resultado = "Jogador 1 venceu a rodada!"
            self.win_rodadas_j1 += 1
            self.vez_do_jogador = 1
        elif vencedor == 2:
            resultado = "Jogador 2 venceu a rodada!"
            self.win_rodadas_j2 += 1
            self.vez_do_jogador = 2
        else:
            resultado = "Empate na rodada!"
            self.win_rodadas_j1 += 1
            self.win_rodadas_j2 += 1

        self.placar_rodada.value = f"Jogador 1 - {self.win_rodadas_j1}\nJogador 2 - {self.win_rodadas_j2}"

        print(f"Resultado: {resultado}")
        print(f"Jogador 1 jogou: {carta1['value']}")
        print(f"Jogador 2 jogou: {carta2['value']}")
        print(f"Manilha: {manilha_base['value']}")

        if self.win_rodadas_j1 == 2 or self.win_rodadas_j2 == 2:
            if self.win_rodadas_j1 == 2:
                self.pontos_j1 += self.valor_truco_atual
            else:
                self.pontos_j2 += self.valor_truco_atual

            self.valor_truco_atual = 1
            self.btn_truco.text = "Pedir Truco"

            # Reseta rodadas
            self.win_rodadas_j1 = 0
            self.win_rodadas_j2 = 0

            # Atualiza placares
            self.placar_jogo.value = f"Jogador 1 - {self.pontos_j1} --- Jogador 2 - {self.pontos_j2}"
            self.placar_rodada.value = f"Jogador 1 - {self.win_rodadas_j1}\nJogador 2 - {self.win_rodadas_j2}"

            self.page.run_task(self.nova_rodada)


        self.page.snack_bar = ft.SnackBar(ft.Text(resultado))
        self.page.snack_bar.open = True

        # Remover carta jogada do slot do jogador 1
        carta_widget = self.cartas_no_slot_jogada.pop()
        stack_cartas = self.jogador1_container.controls[1]  # Stack
        if carta_widget in stack_cartas.controls:
            stack_cartas.controls.remove(carta_widget)

        self.page.update()

        if not self.cartas_jogador1 or not self.cartas_jogador2:
            self.page.update()
            self.page.run_task(self.nova_rodada)  # roda nova rodada com delay


    def get_card_info(self, carta_widget):
        image_src = carta_widget.content.content.src  # Acessa ft.Image.src
        nome_arquivo = image_src.split('/')[-1].split('.')[0]  # Ex: '4H'
        return {
            'code': nome_arquivo,
            'value': nome_arquivo[:-1],
            'suit': nome_arquivo[-1]
        }

    async def nova_rodada(self):
        import asyncio
        await asyncio.sleep(1)
        self.slot_jogada.content = None
        self.slot_jogada_bot.content = None
        self.atualizar_cartas()

        # Se for a vez do bot começar
        if self.vez_do_jogador == 2:
            carta1 = None
            modo = random.choices(["agressivo", "leve", "aleatorio"], weights=[0.9, 0.1, 0.0][0])
            bot = Bot(self.cartas_jogador2, self.manilha.data, modo=modo)
            carta_bot = bot.escolher_carta(carta_adversario=None, j1_tem_ponto=self.win_rodadas_j1 == 1)
            self.cartas_jogador2 = bot.cartas

            self.slot_jogada_bot.content = ft.Image(
                src=carta_bot['image'],
                width=70,
                data=carta_bot
            )
            self.page.update()
            self.slot_jogada_bot.content = None
            self.page.update()
    
    def pedir_truco(self, e):
        proximo_valor = {1: 3, 3: 6, 6: 9, 9: 12}
        if self.valor_truco_atual not in proximo_valor:
            self.page.snack_bar = ft.SnackBar(ft.Text("Já está no valor máximo de Truco!"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        novo_valor = proximo_valor[self.valor_truco_atual]

        # Bot decide se aceita
        aceitou = random.random() < 0.9  

        if aceitou:
            self.valor_truco_atual = novo_valor
            self.btn_truco.text = f"Pedir {proximo_valor.get(novo_valor, novo_valor)}"
            print(f"Bot aceitou! Truco agora vale {self.valor_truco_atual} pontos.")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Bot correu! Você ganhou a rodada."))
            self.pontos_j1 += self.valor_truco_atual

            self.placar_jogo.value = f"Jogador 1 - {self.pontos_j1} ----- Jogador 2 - {self.pontos_j2}"
            self.win_rodadas_j1 = 0
            self.win_rodadas_j2 = 0
            self.valor_truco_atual = 1
            self.btn_truco.text = "Pedir Truco"
            self.page.run_task(self.nova_rodada)

        self.page.snack_bar.open = True
        self.page.update()
    