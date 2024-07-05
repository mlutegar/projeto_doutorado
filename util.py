from entities.jogada import Jogada, jogadas
from entities.jogador import Jogador, jogadores
from entities.peca import Peca, pecas
from entities.situacao import Situacao


def verificar_peca_existe(uid: int) -> bool:
    """
    Verifica se uma peça já foi adicionada.
    """
    return any(peca.uid == uid for peca in pecas)


def substituir_peca(nova_peca: Peca) -> None:
    """
    Substitui uma peça existente.
    """
    for i, peca in enumerate(pecas):
        if peca.uid == nova_peca.uid:
            pecas[i] = nova_peca
            return


def verificar_jogador_existe(jogador_novo):
    """
    Verifica se um jogador já foi adicionado.
    """
    return any(jogador.nome == jogador_novo for jogador in jogadores)


def substituir_jogador(jogador_novo):
    """
    Substitui um jogador existente.
    """
    for i, jogador in enumerate(jogadores):
        if jogador_novo.nome == jogador.nome:
            jogadores[i] = jogador_novo
            return


def process_data(move: dict) -> None:
    """
    Processa os dados da jogada, atualizando a lista de movimentos.
    """
    required_keys = {"UID", "PosX", "PosY", "Tempo", "Jogador", "Cor"}
    if not required_keys.issubset(move.keys()):
        raise ValueError("Dados incompletos recebidos")

    jogador = None
    peca = None

    for jogador in jogadores:
        if jogador.nome == move["Jogador"]:
            # atualizar jogador
            jogador = jogador
    if not jogador:
        # definir jogador
        jogador = Jogador()
        jogador.set_nome(move["Jogador"])

    for peca in pecas:
        if peca.uid == int(move["UID"]):
            # lógica para atualizar peça
            peca = peca
    if not peca:
        # lógica para verificar vizinhança
        peca = Peca()
        peca.set_uid(int(move["UID"]))
        peca.set_cor(move["Cor"])

    peca.set_posicao_atual(int(move["PosX"]), int(move["PosY"]))
    peca.set_player(jogador)
    peca.set_vizinho()

    # definir jogada
    jogada = Jogada()
    jogada.id = len(jogadas) + 1
    jogada.set_peca(peca)
    jogada.set_tempo(int(move["Tempo"]))

    # definir situação
    situacao = Situacao(jogada)

    # atualizar listas
    if verificar_jogador_existe(jogador.nome):
        substituir_jogador(jogador)
    else:
        jogadores.append(jogador)

    if verificar_peca_existe(peca.uid):
        substituir_peca(peca)
        print(
            f"Peca atualizada: "
            f"UID={peca.uid}, "
            f"Cor={peca.cor}, "
            f"Posição Antiga={peca.posicao_antiga}, "
            f"Posição Atual={peca.posicao_atual}, "
            f"Player={peca.jogador}, "
            f"LastPlayer={peca.jogador_antigo}"
        )
    else:
        print(
            f"Peca criada: "
            f"UID={peca.uid}, "
            f"Cor={peca.cor}, "
            f"Posição Antiga={peca.posicao_antiga}, "
            f"Posição Atual={peca.posicao_atual}, "
            f"Player={peca.jogador}, "
            f"LastPlayer={peca.jogador_antigo}"
        )

    print(f"Grupo: {jogada.grupo.id} - {jogada.grupo.qtd_pecas} peças")
    print(f"Jogador: {jogador.nome}")
    print(f"Tempo: {jogada.tempo} segundos")
    print(f"Situacao: {situacao.casos_id}")
    print("")
    jogadas.append([jogada, situacao])
