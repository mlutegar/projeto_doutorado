from datetime import timedelta

from entities.finalizacao import Finalizacao
from util.methods_game import *


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

    def __init__(self, game: Game, jogada: Jogada = None, finalizacao: Finalizacao = None) -> None:
        """
        Inicializa a classe Situacao.

        :param jogada: Jogada que será analisada.
        :param game: Game que contém a jogada.
        """
        self.game: Game = game
        self.jogada: Jogada = jogada
        self.finalizacao: Finalizacao = finalizacao
        self.casos_id: set[int] = self.definir_situacao()
        self.casos_descricao: set[str] | None = None

    def definir_situacao(self) -> set:
        """
        Analisa a jogada e define todos os casos que se encaixam.
        """
        casos: set[int] = set()

        if self.jogada:
            if self.jogada.peca.jogador.tabulacao:
                for caso in self.jogada.peca.jogador.tabulacao:
                    casos.add(caso)
                self.jogada.peca.jogador.tabulacao = []
            self.registrar_caso1(casos)
            self.registrar_caso2(casos)
            self.registrar_caso3(casos)
            self.registrar_caso4(casos)
            self.registrar_caso5(casos)
            self.registrar_caso6(casos)
            self.registrar_caso7(casos)
            self.registrar_caso8(casos)
            self.registrar_caso9(casos)
            self.registrar_caso10(casos)
            self.registrar_caso11(casos)
            self.registrar_caso12(casos)
            self.registrar_caso13(casos)
            self.registrar_caso14(casos)
            self.registrar_caso15(casos)
            self.registrar_caso16(casos)
            self.registrar_caso17(casos)
            self.registrar_caso18(casos)
            self.registrar_caso19(casos)
            self.registrar_caso20(casos)
            self.registrar_caso21(casos)
            self.registrar_caso22(casos)
            self.registrar_caso23(casos)
            self.registrar_caso24(casos)
            self.registrar_caso25(casos)
            self.registrar_caso26(casos)
            self.registrar_caso27(casos)
            self.registrar_caso36(casos)
            self.registrar_caso37(casos)
            self.registrar_caso38(casos)
        elif self.finalizacao:
            if self.finalizacao.descricao == "Desistiu":
                for jogador in self.game.players_desistiu:
                    if jogador.tabulacao:
                        for caso in jogador.tabulacao:
                            casos.add(caso)
                        jogador.tabulacao = []
                self.registrar_caso28(casos)
                self.registrar_caso29(casos)
                self.registrar_caso30(casos)
                self.registrar_caso31(casos)
            elif self.finalizacao.descricao == "Finalizou":
                for jogador in self.game.players_finalizou:
                    if jogador.tabulacao:
                        for caso in jogador.tabulacao:
                            casos.add(caso)
                        jogador.tabulacao = []
                self.registrar_caso32(casos)
                self.registrar_caso33(casos)
                self.registrar_caso34(casos)
                self.registrar_caso35(casos)
        else:
            # unir as listas players_desistiu e players_finalizou
            lista_jogadores = self.game.players_desistiu + self.game.players_finalizou

            for jogador in lista_jogadores:
                if jogador.tabulacao:
                    for caso in jogador.tabulacao:
                        casos.add(caso)
                    jogador.tabulacao = []

        self.casos_descricao = [self.situacoes[caso] for caso in casos]
        return casos

    def registrar_caso1(self, casos):
        """
        1: "Pegou a peça e largou em algum lugar Aleatório",
        """
        if self.jogada.grupo is None and self.jogada.peca.local == "tabuleiro":
            casos.add(1)

    def registrar_caso2(self, casos):
        """
        2: "Fez, sozinho, um agrupamento com 2 peças",
        """
        if self.jogada.grupo is not None and self.jogada.grupo.qtd_pecas == 2:
            casos.add(2)

    def registrar_caso3(self, casos):
        """
        3: "Fez, sozinho, um agrupamento com 3 a 6 peças",
        """
        if self.jogada.grupo is not None and 3 <= self.jogada.grupo.qtd_pecas <= 6:
            casos.add(3)

    def registrar_caso4(self, casos):
        """
        4: "Fez, sozinho, um agrupamento com mais de 6 peças",
        """
        if self.jogada.grupo is not None and self.jogada.grupo.qtd_pecas > 6:
            casos.add(4)

    def registrar_caso5(self, casos):
        """
        5: "Adicionou uma peça no agrupamento de outro integrante, fez várias vezes",
        """
        jogada_anterior = pegar_jogada_do_jogador(jogador=self.jogada.peca.jogador, game=self.game, indice=1)
        jogada_antes_da_anterior = pegar_jogada_do_jogador(jogador=self.jogada.peca.jogador, game=self.game, indice=2)

        # Verifica se houve pelo menos duas jogadas anteriores
        if jogada_anterior is None or jogada_antes_da_anterior is None:
            return

        grupo_anterior = jogada_anterior.grupo
        grupo_antes_da_anterior = jogada_antes_da_anterior.grupo

        # Verifica se as duas últimas jogadas e a jogada atual adicionaram peças em grupos diferentes do jogador atual
        if (grupo_anterior and grupo_antes_da_anterior and
                grupo_anterior.criador != self.jogada.peca.jogador and
                grupo_antes_da_anterior.criador != self.jogada.peca.jogador and
                self.jogada.grupo and self.jogada.grupo.criador != self.jogada.peca.jogador):
            casos.add(5)

    def registrar_caso6(self, casos):
        """
        6: "Adicionou uma peça no agrupamento de outro integrante, faz somente uma vez num período curto",
        """
        # vai analisar o player que adicionou a peça no grupo do outro jogador e tabular o jogador que sofreu a ação do
        # player observado

        # a peça precisa ter um grupo
        if self.jogada.grupo is not None:
            # o criador do grupo atual tem que ser diferente do jogador atual
            if self.jogada.grupo.criador != self.jogada.peca.jogador:
                self.jogada.grupo.criador.tabulacao.append(6)

    def registrar_caso7(self, casos):
        """
        7: "Segurou uma peça por mais de 6 segundos por exemplo",
        """
        if self.jogada.tempo > timedelta(seconds=6):
            casos.add(7)  # Segurou uma peça por mais de 6 segundos por exemplo

    def registrar_caso8(self, casos):
        """
        8: "Colocou uma peça no tabuleiro de forma aleatória ou no próprio agrupamento e depois colocou a mesma peça
        no agrupamento do outro",
        """
        jogada_anterior_do_jogador: Jogada = pegar_jogada_do_jogador(
            game=self.game,
            jogador=self.jogada.peca.jogador,
            indice=1
        )

        if jogada_anterior_do_jogador is None:
            return

        if self.jogada.grupo is None:
            return

        if jogada_anterior_do_jogador.grupo is None or (
                jogada_anterior_do_jogador.grupo.criador == self.jogada.peca.jogador):
            if self.jogada.grupo.criador != self.jogada.peca.jogador:
                casos.add(8)

    def registrar_caso9(self, casos):
        """
        9: "Realizou uma ação rápida, menos de 3 segundos",
        """
        if self.jogada.tempo < timedelta(seconds=3):
            casos.add(9)  # Realizou uma ação rápida, menos de 3 segundos

    def registrar_caso10(self, casos):
        """
        10: "Adicionou uma peça no agrupamento do outro, que a remove, mas continua a repetir a ação",
        """
        # Pega as jogadas mais recentes da peça
        jogada_anterior_da_peca = pegar_jogada_da_peca(
            game=self.game,
            peca=self.jogada.peca,
            indice=1
        )
        jogada_antes_da_anterior_da_peca = pegar_jogada_da_peca(
            game=self.game,
            peca=self.jogada.peca,
            indice=2
        )

        if jogada_anterior_da_peca is None or jogada_antes_da_anterior_da_peca is None:
            return

        # Verifica se a jogada antes da anterior foi em um grupo de outro jogador
        if (jogada_antes_da_anterior_da_peca.grupo is None or jogada_antes_da_anterior_da_peca.grupo.criador ==
                jogada_antes_da_anterior_da_peca.peca.jogador):
            return

        # Verifica se a jogada anterior foi em um grupo diferente do grupo da jogada antes da anterior
        if (jogada_anterior_da_peca.grupo is not None and jogada_anterior_da_peca.grupo.criador ==
                jogada_antes_da_anterior_da_peca.grupo.criador):
            return

        # Verifica se a jogada atual foi feita no grupo de outro jogador e é a repetição da ação
        if (self.jogada.grupo is not None and
                self.jogada.peca.jogador != self.jogada.grupo.criador and
                self.jogada.grupo.criador == jogada_antes_da_anterior_da_peca.grupo.criador):
            casos.add(10)

    def registrar_caso11(self, casos):
        """
        11: "Agrupou peças de cor igual",
        """
        if self.jogada.grupo is None:
            return  # Não agrupou peças

        if self.jogada.grupo.qtd_cores == 1:
            casos.add(11)  # Agrupou peças de cor igual

    def registrar_caso12(self, casos):
        """
        12: "Criou um agrupamento contendo peças iguais e diferentes. Exemplo: Duas amarelas e duas pretas",
        """
        if self.jogada.grupo is None:
            return  # Não agrupou peças

        if self.jogada.grupo.qtd_cores == 2:
            casos.add(12)  # Criou um agrupamento contendo peças iguais e diferentes

    def registrar_caso13(self, casos):
        """
        13: "Agrupou peças de cores diferentes",
        """
        if self.jogada.grupo is None:
            return  # Não agrupou peças

        if self.jogada.grupo.qtd_cores > 2:
            casos.add(13)  # Agrupou peças de cores diferentes

    def registrar_caso14(self, casos):
        """
        14: "Retirou peças do Agrupamento do outro integrante e devolveu para o monte",
        """
        # Verifica o histórico de grupos da peça
        grupo_anterior = None
        for grupo in self.game.historico_grupos.get(self.jogada.peca.uid, []):
            if grupo.criador and grupo.criador != self.jogada.peca.jogador:
                grupo_anterior = grupo
                break

        if grupo_anterior is None or grupo_anterior.criador is None:
            return

        # Verifica se a peça foi colocada no monte na jogada atual
        if self.jogada.peca.local == "monte":
            casos.add(14)

    def registrar_caso15(self, casos):
        """
        15: "Retirou peças do Agrupamento do outro integrante e colocou no seu próprio agrupamento",
        """
        # Verifica o histórico de grupos da peça
        grupo_anterior = None
        for grupo in self.game.historico_grupos.get(self.jogada.peca.uid, []):
            if grupo.criador and grupo.criador != self.jogada.peca.jogador:
                grupo_anterior = grupo
                break

        if grupo_anterior is None or grupo_anterior.criador is None:
            return

        # Verifica se o jogador da jogada atual é o criador do grupo da jogada atual
        if self.jogada.grupo is not None and self.jogada.grupo.criador == self.jogada.peca.jogador:
            casos.add(15)

    def registrar_caso16(self, casos):
        """
        16: "Retirou peças do Agrupamento do outro integrante e colocou em um lugar aleatório",
        """
        # Verifica o histórico de grupos da peça
        grupo_anterior = None
        for grupo in self.game.historico_grupos.get(self.jogada.peca.uid, []):
            if grupo.criador and grupo.criador != self.jogada.peca.jogador:
                grupo_anterior = grupo
                break

        if grupo_anterior is None or grupo_anterior.criador is None:
            return

        # Verifica se a peça foi colocada em um lugar aleatório na jogada atual
        if self.jogada.grupo is None:
            casos.add(16)

    def registrar_caso17(self, casos):
        """
        17: "Trocou a posição da própria peça",
        """
        jogada_antiga_da_peca = pegar_jogada_da_peca(
            game=self.game,
            peca=self.jogada.peca,
            indice=1
        )

        if jogada_antiga_da_peca is None:
            return

        # Verifica se o jogador da jogada atual é o mesmo da última jogada da peça
        if jogada_antiga_da_peca.peca.jogador == self.jogada.peca.jogador:
            casos.add(17)

    def registrar_caso18(self, casos):
        """
        18: "Retirou peças do próprio Agrupamento e devolveu para o monte",
        """
        # Verifica o histórico de grupos da peça
        grupo_anterior = None
        for grupo in self.game.historico_grupos.get(self.jogada.peca.uid, []):
            if grupo.criador == self.jogada.peca.jogador:
                grupo_anterior = grupo
                break

        if grupo_anterior is None or grupo_anterior.criador is None:
            return

        # Verifica se a peça foi colocada no monte na jogada atual
        if self.jogada.peca.local == "monte":
            casos.add(18)

    def registrar_caso19(self, casos):
        """
        19: "Retirou peças do próprio agrupamento e colocou em algum lugar aleatório",
        """

        grupo_anterior = None
        for grupo in self.game.historico_grupos.get(self.jogada.peca.uid, []):
            if grupo.criador == self.jogada.peca.jogador:
                grupo_anterior = grupo
                break

        if grupo_anterior is None or grupo_anterior.criador is None:
            return

        # Verifica se a peça foi colocada em um lugar aleatório na jogada atual
        if self.jogada.grupo is None:
            casos.add(19)

    def registrar_caso20(self, casos):
        """
        20: "Retirou peças dos outros integrantes que adicionaram no agrupamento feito por ele",
        """
        # Última jogada da peça
        jogada_anterior_da_peca = pegar_jogada_da_peca(
            game=self.game,
            peca=self.jogada.peca,
            indice=1
        )

        # precisa ter uma jogada anterior, que seria a jogada que adicionaram a peça no meu grupo
        if jogada_anterior_da_peca is None:
            return

        # a pessoa que fez a jogada anterior precisa ser diferente de mim
        if jogada_anterior_da_peca.peca.jogador == self.jogada.peca.jogador:
            return

        # a pessoa que fez a jogada anterior precisa ter adicionado a peça no meu grupo
        if jogada_anterior_da_peca.grupo is None or jogada_anterior_da_peca.grupo.criador != self.jogada.peca.jogador:
            return

        # eu preciso ter colocado a peça em um grupo diferente do grupo que estava antes
        if self.jogada.grupo is None or self.jogada.grupo.id != jogada_anterior_da_peca.grupo.id:
            casos.add(20)

    def registrar_caso21(self, casos):
        """
        21: "Criou mais de um agrupamento",
        """
        qtd_grupos = 0

        for _, grupo in self.game.grupos.items():
            if grupo.criador == self.jogada.peca.jogador:
                qtd_grupos += 1

        if qtd_grupos > 1:
            casos.add(21)

    def registrar_caso22(self, casos):
        """
        22: "Conecta dois ou mais agrupamentos com outros participantes",
        """
        if self.jogada.peca.eh_ponte:
            if self.jogada.peca.ponte_qtd_lideres > 1:
                casos.add(22)

    def registrar_caso23(self, casos):
        """
        23: "Conecta dois ou mais agrupamentos consigo mesmo
        """
        if self.jogada.peca.eh_ponte:
            if self.jogada.peca.ponte_qtd_lideres == 1:
                casos.add(23)

    def registrar_caso24(self, casos):
        """
        24: "Forma um agrupamento de 2 peças com outro integrante",
        """
        if self.jogada.grupo is None:
            return

        if self.jogada.grupo.qtd_jogadores == 1:
            return
        if self.jogada.grupo.qtd_pecas == 2:
            casos.add(24)

    def registrar_caso25(self, casos):
        """
        25: "Forma um agrupamento de 3 a 6 peças com outro integrante",
        """
        if self.jogada.grupo is None:
            return

        if self.jogada.grupo.qtd_jogadores == 1:
            return
        if 3 <= self.jogada.grupo.qtd_pecas <= 6:
            casos.add(25)

    def registrar_caso26(self, casos):
        """
        26: "Forma um agrupamento de mais de 6 peças com outro integrante",
        """
        if self.jogada.grupo is None:
            return
        if self.jogada.grupo.qtd_jogadores == 1:
            return
        if self.jogada.grupo.qtd_pecas > 6:
            casos.add(26)

    def registrar_caso27(self, casos):
        """
        27: "Desenvolveu um agrupamento e outro integrante resolveu adicionar peças",
        """
        # jogador da jogada atual precisa adiciona a peça em um grupo de outro jogador

        # a peça precisa ter um grupo e o criador do grupo precisa ser diferente do jogador da jogada
        if self.jogada.grupo is not None:
            if self.jogada.grupo.criador != self.jogada.peca.jogador:
                self.jogada.grupo.criador.tabulacao.append(27)

    def registrar_caso28(self, casos):
        """
        28: "Desistiu Sozinho",
        """
        if self.finalizacao is not None and self.finalizacao.descricao == "Desistiu":
            casos.add(28)

    def registrar_caso29(self, casos):
        """
        29: "Desistiu Sozinho com pouco tempo de jogo",
        """
        if (self.finalizacao is not None and
                self.finalizacao.descricao == "Desistiu" and
                self.finalizacao.jogador.tempo_em_jogo < timedelta(seconds=300)):
            casos.add(29)

    def registrar_caso30(self, casos):
        """
        30: "Desistiu Sozinho e pouco tempo depois outro integrante desistiu",
        """
        # verificar se alguem desistiu antes de mim
        if len(self.game.players_desistiu) > 1:
            # verificar se a última pessoa a desistir faz pouco tempo
            if self.game.players_desistiu[-1].tempo_em_jogo - self.finalizacao.jogador.tempo_em_jogo < timedelta(seconds=300):
                self.game.players_desistiu[-1].tabulacao.append(30)

    def registrar_caso31(self, casos):
        """
        31: "Desistiu depois de outro integrante Desistir
        """
        if len(self.game.players_desistiu) > 1:
            # verificar se a última pessoa a desistir faz pouco tempo
            if self.game.players_desistiu[-1].tempo_em_jogo - self.finalizacao.jogador.tempo_em_jogo < timedelta(seconds=300):
                if self.finalizacao is not None and self.finalizacao.descricao == "Desistiu":
                    casos.add(31)

    def registrar_caso32(self, casos):
        """
        32: "Finalizou sozinho",
        """
        if self.finalizacao is not None and self.finalizacao.descricao == "Finalizou":
            casos.add(32)

    def registrar_caso33(self, casos):
        """
        33: "Finalizou sozinho com pouco tempo de jogo",
        """
        if (self.finalizacao is not None and
                self.finalizacao.descricao == "Finalizou" and
                self.finalizacao.jogador.tempo_em_jogo < timedelta(seconds=300)):
            casos.add(33)

    def registrar_caso34(self, casos):
        """
        34: "Finalizou depois de outro integrante Finalizar",
        """
        if len(self.game.players_finalizou) > 1:
            if self.game.players_finalizou[-1].tempo_em_jogo - self.finalizacao.jogador.tempo_em_jogo < timedelta(seconds=300):
                if self.finalizacao is not None and self.finalizacao.descricao == "Finalizou":
                    casos.add(34)

    def registrar_caso35(self, casos):
        """
        35: "Finalizou Sozinho e pouco tempo depois outro integrante finalizou também
        """
        if len(self.game.players_finalizou) > 1:
            if self.game.players_finalizou[-1].tempo_em_jogo - self.finalizacao.jogador.tempo_em_jogo < timedelta(seconds=300):
                if self.finalizacao is not None and self.finalizacao.descricao == "Finalizou":
                    self.game.players_finalizou[-1].tabulacao.append(35)

    def registrar_caso36(self, casos):
        """
        36: "Imitou a forma do mesmo agrupamento do outro (fez depois que outro integrante realizou a ação)",
        """
        if self.jogada.grupo is None:
            print("Jogada atual não tem grupo.")
            return

        # Configuração do agrupamento atual
        configuracao_atual = {
            'qtd_pecas': self.jogada.grupo.qtd_pecas,
            'cores': set(peca.cor for peca in self.jogada.grupo.pecas.values())
        }

        print("Configuração atual:", configuracao_atual)

        # Itera sobre todas as jogadas anteriores para encontrar uma jogada que corresponda à configuração
        for jogada in self.game.jogadas.values():
            if jogada.peca.jogador != self.jogada.peca.jogador and jogada.grupo is not None:
                configuracao_anterior = {
                    'qtd_pecas': jogada.grupo.qtd_pecas,
                    'cores': set(peca.cor for peca in jogada.grupo.pecas.values())
                }

                print("Comparando com configuração anterior:", configuracao_anterior)

                if configuracao_atual == configuracao_anterior:
                    print("Encontrou uma configuração anterior correspondente.")
                    casos.add(36)
                    break

    def registrar_caso37(self, casos):
        """
        37: "É imitado por alguém",
        """
        if self.jogada.grupo is None:
            return

        # Configuração do agrupamento atual
        configuracao_atual = {
            'qtd_pecas': self.jogada.grupo.qtd_pecas,
            'cores': set(peca.cor for peca in self.jogada.grupo.pecas.values())
        }

        print(f"Configuração atual: {configuracao_atual}")

        # Itera sobre todas as jogadas anteriores para encontrar uma jogada que corresponda à configuração
        for jogada in self.game.jogadas.values():
            if jogada.peca.jogador != self.jogada.peca.jogador and jogada.grupo is not None:
                configuracao_anterior = {
                    'qtd_pecas': jogada.grupo.qtd_pecas,
                    'cores': set(peca.cor for peca in jogada.grupo.pecas.values())
                }

                print(f"Comparando com configuração anterior: {configuracao_anterior}")

                if configuracao_atual == configuracao_anterior:
                    print(
                        f"Jogador {self.jogada.peca.jogador.nome} foi imitado pelo jogador {jogada.peca.jogador.nome}")
                    jogada.peca.jogador.tabulacao.append(37)
                    break

    def registrar_caso38(self, casos):
        """
        38: "Não realizou ações"
        """
        # Verifica se o tempo desde o último movimento do jogador atual é maior que 10 segundos
        if self.jogada.tempo_desde_ultimo_movimento.total_seconds() > 10:
            casos.add(38)

    def to_dict(self) -> dict:
        return {
            "id": self.jogada.id,
            "casos_id": self.casos_id,
            "casos_descricao": self.casos_descricao
        }
