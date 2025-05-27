import random
from game_logic import TrucoGame

class Bot:
    def __init__(self, cartas, manilha_base, modo="aleatorio"):
        self.cartas = cartas  # lista de cartas
        self.manilha_base = manilha_base
        self.modo = modo  # "agressivo", "leve", "aleatorio"

    def escolher_carta(self, carta_adversario=None, j1_tem_ponto=False):
        if j1_tem_ponto and carta_adversario:
            # Modo defensivo: tentar vencer a carta do adversário
            for carta in self.cartas:
                v = TrucoGame.comparar_cartas(carta, carta_adversario, self.manilha_base)
                if v == 2:  # bot vence
                    self.cartas.remove(carta)
                    return carta

        if self.modo == "agressivo":
            return self.jogar_agressivo()
        elif self.modo == "leve":
            return self.jogar_leve()
        else:  # aleatório
            return self.jogar_aleatorio()

    def jogar_agressivo(self):
        # Prioriza manilhas e cartas mais fortes
        def valor_forca(carta):
            return TrucoGame.ordem_cartas.index(carta['code'][:-1])
        self.cartas.sort(key=valor_forca, reverse=True)
        return self.cartas.pop(0)

    def jogar_leve(self):
        # Prioriza cartas mais fracas
        def valor_forca(carta):
            return TrucoGame.ordem_cartas.index(carta['code'][:-1])
        self.cartas.sort(key=valor_forca)
        return self.cartas.pop(0)

    def jogar_aleatorio(self):
        carta = random.choice(self.cartas)
        self.cartas.remove(carta)
        return carta
    
    