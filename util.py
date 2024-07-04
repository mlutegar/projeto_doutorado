from entities.grupo import Grupo, grupos
from entities.jogada import Jogada, jogadas
from entities.jogador import Jogador, jogadores
from entities.peca import Peca, pecas
from entities.situacao import Situacao


def get_grupo_by_peca_pai(peca_pai: Peca):
    """
    Retorna um grupo pelo identificador da peça pai.
    """
    for grupo in grupos:
        if grupo.peca_pai == peca_pai:
            return grupo
    return


def get_peca_by_uid(uid: int):
    """
    Retorna uma peça pelo seu identificador.
    """
    for peca in pecas:
        if peca.uid == uid:
            return peca
    return None


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


def tem_lateral_vizinho(pos1: tuple, pos2: tuple) -> bool:
    """
    Verifica se duas peças estão na mesma linha e são de colunas duas unidades distantes.
    """
    linha1, coluna1 = pos1
    linha2, coluna2 = pos2
    return linha1 == linha2 and abs(coluna1 - coluna2) == 2


def tem_lateral_diagonal(pos1: tuple, pos2: tuple) -> bool:
    """
    Verifica se duas posições em colunas subsequentes estão em linhas subsequentes.
    """
    linha1, coluna1 = pos1
    linha2, coluna2 = pos2
    return abs(linha1 - linha2) == 1 and abs(coluna1 - coluna2) == 1


def get_pecas_from_grupo(peca):
    pecas_grupo = [peca]
    pecas_uid_analisadas = []
    while pecas_grupo:
        peca_analisada = pecas_grupo.pop()
        pecas_uid_analisadas.append(peca_analisada.uid)
        for outra_peca in pecas:
            if outra_peca.uid in pecas_uid_analisadas or outra_peca in pecas_grupo:
                continue
            if tem_lateral_vizinho(
                    peca_analisada.posicao_atual, outra_peca.posicao_atual
            ) or tem_lateral_diagonal(
                peca_analisada.posicao_atual, outra_peca.posicao_atual
            ):
                pecas_grupo.append(outra_peca)

    pecas_analisadas = []
    for peca_uid_analisada in pecas_uid_analisadas:
        peca_nova = get_peca_by_uid(peca_uid_analisada)
        pecas_analisadas.append(peca_nova)

    return pecas_analisadas


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


def substituir_grupo(grupo_novo):
    """
    Substitui um grupo existente.
    """
    for i, grupo in enumerate(grupos):
        if grupo_novo.peca_pai == grupo.peca_pai:
            grupos[i] = grupo_novo
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

    # definir grupo
    grupo = Grupo()
    if peca.vizinho == 1:
        grupo.set_id = len(grupos) + 1
        grupo.add_peca(peca)
        grupo.set_pecas(get_pecas_from_grupo(peca))
        grupos.append(grupo)
    elif peca.vizinho > 1:
        # verificar quem sao as pecas desse grupo que acabou de entrar
        pecas_grupo_novo = get_pecas_from_grupo(peca)
        # verificar quem é a peça pai desse grupo
        peca_pai = pecas_grupo_novo[0]
        # atualizar o grupo
        grupo = get_grupo_by_peca_pai(peca_pai)
        grupo.set_pecas(pecas_grupo_novo)
        substituir_grupo(grupo)

    # definir jogada
    jogada = Jogada()
    jogada.id = len(jogadas) + 1
    jogada.set_peca(peca)
    jogada.set_grupo(grupo)
    jogada.set_jogador(peca.jogador)
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

    print(f"Grupo: {grupo.id} - {grupo.qtd_pecas} peças")
    print(f"Jogador: {jogador.nome}")
    print(f"Tempo: {jogada.tempo} segundos")
    print(f"Situacao: {situacao.casos_id}")
    print("")
    jogadas.append([jogada, situacao])
