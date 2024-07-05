from entities.jogada import Jogada, jogadas
from entities.jogador import Jogador, jogadores
from entities.peca import Peca, pecas
from entities.situacao import Situacao


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
        jogador = Jogador(move["Jogador"])

    for peca in pecas:
        if peca.uid == int(move["UID"]):
            # lógica para atualizar peça
            peca = peca
    if not peca:
        # lógica para verificar vizinhança
        peca = Peca(int(move["UID"]))
        peca.set_cor(move["Cor"])

    peca.set_posicao_atual(int(move["PosX"]), int(move["PosY"]))
    peca.set_player(jogador)
    peca.set_vizinho()

    # definir jogada
    jogada = Jogada()
    jogada.set_peca(peca)
    jogada.set_tempo(int(move["Tempo"]))

    # definir situação
    situacao = Situacao(jogada)

    # atualizar listas
    if jogadores[jogador.nome]:
        jogadores[jogador.nome] = jogador
    else:
        jogadores.add(jogador)

    if pecas[peca.uid]:
        pecas[peca.uid] = peca
        print(
            f"Peca atualizada: "
            f"UID={peca.uid}, "
            f"Cor={peca.cor}, "
            f"Posição Antiga={peca.posicao_antiga}, "
            f"Posição Atual={peca.posicao_atual}, "
            f"Player={peca.jogador_peca}, "
            f"LastPlayer={peca.jogador_antigo}"
        )
    else:
        print(
            f"Peca criada: "
            f"UID={peca.uid}, "
            f"Cor={peca.cor}, "
            f"Posição Antiga={peca.posicao_antiga}, "
            f"Posição Atual={peca.posicao_atual}, "
            f"Player={peca.jogador_peca}, "
            f"LastPlayer={peca.jogador_antigo}"
        )

    print(f"Grupo: {jogada.grupo.id} - {jogada.grupo.qtd_pecas} peças")
    print(f"Jogador: {jogador.nome}")
    print(f"Tempo: {jogada.tempo} segundos")
    print(f"Situacao: {situacao.casos_id}")
    print("")
    jogadas[jogada.id] = [jogada, situacao]
