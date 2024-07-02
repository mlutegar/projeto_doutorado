from entities.jogada import Jogada
from entities.peca import Peca
from entities.situacao import Situacao

pecas = []
jogadas = []


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
    Verifica se duas peças estão na mesma linha e são de colunas subsequentes.
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


def contar_vizinhos_peca(peca: Peca) -> int:
    """
    Conta a quantidade de peças vizinhas a uma determinada peça analisando as peças já adicionadas.
    """
    vizinhos = 0
    for outra_peca in pecas:
        if outra_peca.uid == peca.uid:
            continue
        if tem_lateral_vizinho(
                peca.posicao_atual, outra_peca.posicao_atual
        ) or tem_lateral_diagonal(
            peca.posicao_atual, outra_peca.posicao_atual
        ):
            vizinhos += 1
    return vizinhos


def contar_pecas_grupo(peca: Peca):
    """
    Conta a quantidade de peças pertencente ao mesmo grupo. Ela verifica todos os vizinhos da peça, adiciona as UIDs
    deles em uma lista e começa a verificar os vizinhos dos vizinhos. Até que não haja mais nenhuma UID para verificar.
    """
    pecas_grupo = [peca]
    pecas_analisadas = []

    while pecas_grupo:
        peca_analisada = pecas_grupo.pop()
        pecas_analisadas.append(peca_analisada.uid)
        for outra_peca in pecas:
            if outra_peca.uid in pecas_analisadas:
                continue
            if tem_lateral_vizinho(
                    peca_analisada.posicao_atual, outra_peca.posicao_atual
            ) or tem_lateral_diagonal(
                peca_analisada.posicao_atual, outra_peca.posicao_atual
            ):
                pecas_grupo.append(outra_peca)
    return len(pecas_analisadas)


def process_data(move: dict) -> None:
    """
    Processa os dados da jogada, atualizando a lista de movimentos.
    """
    required_keys = {"UID", "InicioX", "InicioY", "DestinoX", "DestinoY", "Tempo", "UltimoPlayer", "PenultimoPlayer"}
    if not required_keys.issubset(move.keys()):
        raise ValueError("Dados incompletos recebidos")

    peca = Peca()
    jogada = Jogada()

    peca.set_uid(int(move["UID"]))
    peca.set_cor("azul")  # Aqui você pode ajustar para definir a cor correta

    peca.set_posicao_antiga(int(move["InicioX"]), int(move["InicioY"]))
    peca.set_posicao_atual(int(move["DestinoX"]), int(move["DestinoY"]))

    peca.set_grupo(contar_pecas_grupo(peca))
    print(
        f"Peca criada: "
        f"UID={peca.uid}, "
        f"Cor={peca.cor}, "
        f"Posição Antiga={peca.posicao_antiga}, "
        f"Posição Atual={peca.posicao_atual}"
        f"Grupo={peca.grupo}"
    )

    peca.set_last_player(move["PenultimoPlayer"])
    peca.set_player(move["UltimoPlayer"])

    if verificar_peca_existe(peca.uid):
        substituir_peca(peca)
    else:
        pecas.append(peca)

    peca.set_vizinho(contar_vizinhos_peca(peca))
    print(f"Vizinhos da peça {peca.uid}: {peca.vizinho}")

    jogada.id = len(jogadas) + 1
    jogada.set_peca(peca)
    jogada.set_jogador(move["UltimoPlayer"])
    jogada.set_tempo(int(move["Tempo"]))
    print(f"Jogada criada: ID={jogada.id}, Jogador={jogada.jogador}, Tempo={jogada.tempo}")

    situacao = Situacao(jogada)
    print(f"Situação determinada: ID={situacao.id}, Descrição={situacao.descricao}")

    jogadas.append([jogada, situacao])
