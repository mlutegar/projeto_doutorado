from typing import List, Dict, Tuple

moves_data: List[Dict[str, int]] = []

def tem_lateral_vizinho(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
    """
    Verifica se duas posições estão lado a lado.
    """
    return abs(pos1[1] - pos2[1]) <= 5 and 82 >= abs(pos1[0] - pos2[0]) >= 72

def tem_lateral_diagonal(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
    """
    Verifica se duas posições estão lado a lado na diagonal.
    """
    return 74 >= abs(pos1[1] - pos2[1]) >= 64 and 44 >= abs(pos1[0] - pos2[0]) >= 34

def contar_vizinhos_peca(jogada: int, peca: int) -> int:
    """
    Conta a quantidade de peças vizinhas a uma determinada peça até uma jogada específica.
    """
    vizinhos = 0
    for i in range(jogada):
        if moves_data[i]["UID"] == peca:
            pos_atual = [moves_data[i]["DestinoX"], moves_data[i]["DestinoY"]]
            pos_peca = [moves_data[jogada]["DestinoX"], moves_data[jogada]["DestinoY"]]
            if tem_lateral_vizinho(pos_atual, pos_peca) or tem_lateral_diagonal(pos_atual, pos_peca):
                vizinhos += 1
    return vizinhos

def verificar_vizinhos(jogada: Dict[str, int]) -> Tuple[bool, bool]:
    """
    Verifica se a jogada atual tem vizinhos laterais ou diagonais em relação a jogadas anteriores.
    """
    pos_atual = [jogada["DestinoX"], jogada["DestinoY"]]
    vizinhos_laterais = False
    vizinhos_diagonais = False
    for outra_jogada in moves_data:
        pos_outra = [outra_jogada["DestinoX"], outra_jogada["DestinoY"]]
        if tem_lateral_vizinho(pos_atual, pos_outra):
            vizinhos_laterais = True
            outra_jogada["vizinhos_laterais"] = True
        if tem_lateral_diagonal(pos_atual, pos_outra):
            vizinhos_diagonais = True
            outra_jogada["vizinhos_diagonais"] = True
    return vizinhos_laterais, vizinhos_diagonais

def determinar_valor_jogada(vizinhos_peca: int, vizinhos_laterais: bool, vizinhos_diagonais: bool) -> int:
    """
    Determina o valor da jogada com base nos vizinhos laterais, diagonais e quantidade de vizinhos da peça.
    """
    if vizinhos_laterais or vizinhos_diagonais:
        return 2
    if 2 <= vizinhos_peca <= 5:
        return 3
    if vizinhos_peca > 5:
        return 4
    return 1

def process_data(move: Dict[str, Dict[str, int]]) -> None:
    """
    Processa os dados da jogada, atualizando a lista de movimentos.
    """
    global moves_data
    move = move['data']

    required_keys = {"UID", "InicioX", "InicioY", "DestinoX", "DestinoY", "Tempo", "UltimoPlayer", "PenultimoPlayer"}
    if not required_keys.issubset(move.keys()):
        raise ValueError("Dados incompletos recebidos")

    if move["DestinoX"] == 0 and move["DestinoY"] == 0:
        return

    jogada = {
        "id_jogada": len(moves_data) + 1,
        "UID": move["UID"],
        "InicioX": move["InicioX"],
        "InicioY": move["InicioY"],
        "DestinoX": move["DestinoX"],
        "DestinoY": move["DestinoY"],
        "Tempo": move["Tempo"],
        "UltimoPlayer": move["UltimoPlayer"],
        "PenultimoPlayer": move["PenultimoPlayer"],
        "vizinhos_laterais": False,
        "vizinhos_diagonais": False,
        "valor": 0
    }

    jogada["vizinhos_laterais"], jogada["vizinhos_diagonais"] = verificar_vizinhos(jogada)
    jogada["vizinhos_peca"] = contar_vizinhos_peca(len(moves_data), move["UID"])
    jogada["valor"] = determinar_valor_jogada(jogada["vizinhos_peca"], jogada["vizinhos_laterais"], jogada["vizinhos_diagonais"])

    moves_data.append(jogada)
