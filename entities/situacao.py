from entities.jogada import Jogada


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
        self.id = self.definir_situacao()
        self.descricao = self.situacoes.get(self.id, "Situação desconhecida")

    def definir_situacao(self) -> int:
        """
        Analisa a jogada e define a situação com base em critérios específicos.
        """
        if self.jogada.peca.grupo == 0:
            return 1  # Pegou a peça e largou em algum lugar Aleatório
        if self.jogada.peca.grupo == 1:
            return 2  # Fez, sozinho, um agrupamento com 2 peças
        if 2 <= self.jogada.peca.grupo <= 6:
            return 3  # Fez, sozinho, um agrupamento com 3 a 6 peças
        if self.jogada.peca.grupo > 6:
            return 4  # Fez, sozinho, um agrupamento com mais de 6 peças
        if self.jogada.tempo > 6:
            return 7  # Segurou uma peça por mais de 6 segundos por exemplo
        if self.jogada.tempo < 3:
            return 9  # Realizou uma ação rápida, menos de 3 segundos
        if self.jogada.jogador.fez_varias_vezes:
            return 5  # Adicionou uma peça no agrupamento de outro integrante, fez várias vezes
        if self.jogada.jogador.fez_uma_vez_curto_periodo:
            return 6  # Adicionou uma peça no agrupamento de outro integrante, faz somente uma vez num período curto
        # Adicione mais critérios conforme necessário
        return 0  # Situação padrão

    def to_dict(self) -> dict:
        return {
            "situacao_id": self.id,
            "situacao_descricao": self.descricao,
        }
