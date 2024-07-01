moves_data = []


def tem_lateral_vizinho(pos1, pos2):
    """
    Verifica se duas posições estão lado a lado
    :param pos1:
    :param pos2:
    :return: True se as posições estiverem lado a lado, False caso contrário
    """
    return abs(pos1[1] - pos2[1]) <= 5 and 82 >= abs(pos1[0] - pos2[0]) >= 72


def tem_lateral_diagonal(pos1, pos2):
    return 74 >= abs(pos1[1] - pos2[1]) >= 64 and 44 >= abs(pos1[0] - pos2[0]) >= 34


def contar_vizinhos_peca(jogada, peca):
    """
    Dado o id da peça e o número da jogada, ele analisa a quantidade de peças vizinho a peça tem.
    Ele simula um tabuleiro com as peças dada até a jogada e faz a verificação.
    :param jogada: O número da jogada até o qual as peças devem ser simuladas
    :param peca: O id da peça que deve ser verificada
    :return: O número de peças vizinhas
    """
    vizinhos = 0
    for i in range(jogada):
        if moves_data[i]["UltimoPlayer"] == peca:
            pos_atual = [moves_data[i]["DestinoX"], moves_data[i]["DestinoY"]]
            pos_peca = [moves_data[jogada]["DestinoX"], moves_data[jogada]["DestinoY"]]

            if tem_lateral_vizinho(pos_atual, pos_peca) or tem_lateral_diagonal(pos_atual, pos_peca):
                vizinhos += 1

    return vizinhos


def process_data(move):
    global moves_data

    move = move['data']

    print(move)

    # Verifique se todas as chaves necessárias estão presentes
    if all(key in move for key in ("UID", "InicioX", "InicioY", "DestinoX", "DestinoY", "Tempo", "UltimoPlayer", "PenultimoPlayer")):
        uid, inicio_x, inicio_y, destino_x, destino_y, tempo, UltimoPlayer, PenultimoPlayer = move.values()
    else:
        raise ValueError("Dados incompletos recebidos")

    # Ignorar entradas com posições x e y iguais a 0
    if destino_x == 0 and destino_y == 0:
        return

    jogada = {
        "id_jogada": len(moves_data) + 1,  # Adiciona id_jogada incremental
        "UID": uid,
        "InicioX": inicio_x,
        "InicioY": inicio_y,
        "DestinoX": destino_x,
        "DestinoY": destino_y,
        "Tempo": tempo,
        "UltimoPlayer": UltimoPlayer,
        "PenultimoPlayer": PenultimoPlayer,
        "vizinhos_laterais": False,
        "vizinhos_diagonais": False,
        "valor": 0
    }

    # Verificar vizinhança nova jogada com jogadas anteriores
    pos_atual = [destino_x, destino_y]
    for outra_jogada in moves_data:
        pos_outra = [outra_jogada["DestinoX"], outra_jogada["DestinoY"]]

        if tem_lateral_vizinho(pos_atual, pos_outra):
            jogada["vizinhos_laterais"] = True
            outra_jogada["vizinhos_laterais"] = True
        if tem_lateral_diagonal(pos_atual, pos_outra):
            jogada["vizinhos_diagonais"] = True
            outra_jogada["vizinhos_diagonais"] = True

    # Determinar o valor da jogada
    if jogada["vizinhos_laterais"] or jogada["vizinhos_diagonais"]:
        jogada["valor"] = 1

    moves_data.append(jogada)
