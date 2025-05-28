import requests

class TrucoGame:
    # Ordem das cartas normais (sem manilhas)
    ordem_cartas = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']

    # Ordem de força dos naipes das manilhas
    ordem_naipes = ['D', 'S', 'H', 'C']  # Ouros < Espadas < Copas < Paus

    @staticmethod
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
    

    @staticmethod
    def proxima_carta(valor):
        ordem = TrucoGame.ordem_cartas
        idx = ordem.index(valor)
        return ordem[(idx + 1) % len(ordem)]  # circular (3 -> 4)

    @staticmethod
    def comparar_cartas(carta1, carta2, manilha_base):
        def valor(c):
            return c['code'][:-1]  # 4C TIRA A ULTIMO CARACTERE = 4

        def naipe(c):
            return c['code'][-1]  # MESMA COISA MAS TIRA O 1° CARACTERE

        v1, v2 = valor(carta1), valor(carta2)
        n1, n2 = naipe(carta1), naipe(carta2)

        valor_manilha = TrucoGame.proxima_carta(valor(manilha_base))

        # Verifica se as cartas são manilhas
        # 1 para j1, e 2 para j2
        e1_manilha = v1 == valor_manilha
        e2_manilha = v2 == valor_manilha

        if e1_manilha and not e2_manilha:
            return 1
        if e2_manilha and not e1_manilha:
            return 2
        if e1_manilha and e2_manilha:
            # desempate por naipe
            i1 = TrucoGame.ordem_naipes.index(n1)
            i2 = TrucoGame.ordem_naipes.index(n2)
            if i1 > i2:
                return 1
            elif i2 > i1:
                return 2
            else:
                return 0  # mesmo valor e mesmo naipe - impossivel

        # Comparação normal se nenhuma for manilha
        i1 = TrucoGame.ordem_cartas.index(v1)
        i2 = TrucoGame.ordem_cartas.index(v2)
        if i1 > i2:
            return 1
        elif i2 > i1:
            return 2
        else:
            return 0