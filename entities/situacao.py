from entities.grupo import grupos
from entities.jogada import Jogada
from entities.peca import Peca, pecas


class Situacao:
    situacoes = {
        1: "Pegou a peça e largou em algum lugar Aleatório",
        2: "Fez, sozinho, um agrupamento com 2 peças",
        3: "Fez, sozinho, um agrupamento com 3 a 6 peças",
        4: "Fez, sozinho, um agrupamento com mais de 6 peças",
        5: "Adicionou uma peça no agrupamento de outro integrante, fez várias vezes",
        6: "Adicionou uma peça no agrupamento de outro integrante, faz somente uma vez num período curto",
        7: "Segurou uma peça por mais de 6 segundos por exemplo",
        8: "Colocou uma peça no tabuleiro de forma aleatória ou no próprio agrupamento e depois colocou a mesma peça "
           "no agrupamento do outro",
        9: "Realizou uma ação rápida, menos de 3 segundos",
        10: "Adicionou uma peça no agrupamento do outro, que a remove, mas continua a repetir a ação",
        11: "Agrupou peças de cor igual",
        12: "Criou um agrupamento contendo peças iguais e diferentes. Exemplo: Duas amarelas e duas pretas",
        13: "Agrupou peças de cores diferentes",
        14: "Retirou peças do Agrupamento do outro integrante e devolveu para o monte",
        15: "Retirou peças do Agrupamento do outro integrante e colocou no seu próprio agrupamento",
        16: "Retirou peças do Agrupamento do outro integrante e colocou em um lugar aleatório",
        17: "Trocou a posição da própria peça",
        18: "Retirou peças do próprio Agrupamento e devolveu para o monte",
        19: "Retirou peças do próprio agrupamento e colocou em algum lugar aleatório",
        20: "Retirou peças dos outros integrantes que adicionaram no agrupamento feito por ele",
        21: "Criou mais de um agrupamento",
        22: "Conecta dois ou mais agrupamentos com outros participantes",
        23: "Conecta dois ou mais agrupamentos consigo mesmo",
        24: "Forma um agrupamento de 2 peças com outro integrante",
        25: "Forma um agrupamento de 3 a 6 peças com outro integrante",
        26: "Forma um agrupamento de mais de 6 peças com outro integrante",
        27: "Desenvolveu um agrupamento e outro integrante resolveu adicionar peças",
        28: "Desistiu Sozinho",
        29: "Desistiu Sozinho com pouco tempo de jogo",
        30: "Desistiu Sozinho e pouco tempo depois outro integrante desistiu",
        31: "Desistiu depois de outro integrante Desistir",
        32: "Finalizou sozinho",
        33: "Finalizou sozinho com pouco tempo de jogo",
        34: "Finalizou depois de outro integrante Finalizar",
        35: "Finalizou Sozinho e pouco tempo depois outro integrante finalizou também",
        36: "Imitou a forma do mesmo agrupamento do outro (fez depois que outro integrante realizou a ação)",
        37: "É imitado por alguém",
        38: "Não realizou ações"
    }

    def __init__(self, jogada: Jogada):
        self.jogada = jogada
        self.casos_id = self.definir_situacao()
        self.casos_descricao = None

    def definir_situacao(self) -> set:
        """
        Analisa a jogada e define todos os casos que se encaixam.
        """
        casos = set()
        peca_antiga = Peca(999)
        peca_antiga.set_cor(self.jogada.peca.cor)
        peca_antiga.set_posicao(self.jogada.peca.posicao_antiga)
        peca_antiga.set_player(self.jogada.peca.jogador_antigo)
        jogada_antiga = Jogada()
        jogada_antiga.set_peca(peca_antiga)
        jogada_antiga.set_tempo(5)

        self.registrar_caso1a4(casos)
        self.registrar_caso5e6(casos)
        self.registrar_caso7(casos)
        # CASO 8 - é preciso analisar 3 jogadas seguidas
        self.registrar_caso9(casos)
        # CASO 10 - analisar 3 jogadas seguidas
        self.registrar_caso11a13(casos)
        self.registrar_caso14a16(casos, jogada_antiga)
        self.registrar_caso18a19(casos, jogada_antiga)

        self.casos_descricao = [self.situacoes[caso] for caso in casos]
        pecas.pop(999)
        grupos.pop((jogada_antiga.grupo.criador.nome, jogada_antiga.grupo.peca_pai.uid))
        return casos

    def registrar_caso18a19(self, casos, jogada_antiga):
        if jogada_antiga.grupo.criador is None:
            return
        if self.jogada.peca.jogador_peca == jogada_antiga.grupo.criador:
            if self.jogada.peca.local == "monte":
                casos.add(18)  # Retirou peças do próprio Agrupamento e devolveu para o monte
            elif self.jogada.peca.vizinho != 0:
                casos.add(19)  # Retirou peças do próprio agrupamento e colocou em algum lugar aleatório

    def registrar_caso14a16(self, casos, jogada_antiga):
        if jogada_antiga.grupo.criador is None:
            return
        if self.jogada.peca.jogador_peca != jogada_antiga.grupo.criador:
            if self.jogada.peca.local == "monte":
                casos.add(14)  # Retirou peças do Agrupamento do outro integrante e devolveu para o monte
            elif self.jogada.grupo.criador == self.jogada.peca.jogador_peca:
                casos.add(15)  # Retirou peças do Agrupamento do outro integrante e colocou no seu próprio agrupamento
            elif self.jogada.peca.vizinho != 0:
                casos.add(16)  # Retirou peças do Agrupamento do outro integrante e colocou em um lugar aleatório

    def registrar_caso11a13(self, casos):
        if self.jogada.grupo.qtd_cores == 1:
            casos.add(11)  # Agrupou peças de cor igual
        elif self.jogada.grupo.qtd_cores == 1:
            casos.add(12)  # Criou um agrupamento contendo peças iguais e diferentes. Exemplo: Duas amarelas e duas
        elif self.jogada.grupo.qtd_cores > 1:
            casos.add(13)  # Agrupou peças de cores diferentes

    def registrar_caso9(self, casos):
        if self.jogada.tempo < 3:
            casos.add(9)  # Realizou uma ação rápida, menos de 3 segundos

    def registrar_caso7(self, casos):
        if self.jogada.tempo > 6:
            casos.add(7)  # Segurou uma peça por mais de 6 segundos por exemplo

    def registrar_caso5e6(self, casos):
        if self.jogada.grupo.qtd_jogadores > 1:
            if self.jogada.jogador_jogada == self.jogada.grupo.criador:
                if self.jogada.jogador_jogada.infracoes > 1:
                    casos.add(5)  # Adicionou uma peça no agrupamento de outro integrante, fez várias vezes
                else:
                    casos.add(6)  # Adicionou uma peça no agrupamento de outro integrante, faz somente uma vez num
                    # período curto

    def registrar_caso1a4(self, casos):
        if self.jogada.grupo.criador is None and self.jogada.peca.linha_atual < 99:
            casos.add(1)  # Pegou a peça e largou em algum lugar Aleatório
        elif self.jogada.grupo.qtd_pecas == 2:
            casos.add(2)  # Fez, sozinho, um agrupamento com 2 peças
        elif 3 <= self.jogada.grupo.qtd_pecas <= 6:
            casos.add(3)  # Fez, sozinho, um agrupamento com 3 a 6 peças
        elif self.jogada.grupo.qtd_pecas > 6:
            casos.add(4)  # Fez, sozinho, um agrupamento com mais de 6 peças

    def to_dict(self) -> dict:
        return {
            "id": self.jogada.id,
            "casos_id": self.casos_id,
            "casos_descricao": self.casos_descricao
        }
