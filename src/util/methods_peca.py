def encontrar_peca_vizinha(item, pecas, dict_pecas):
    """
    Encontra peças vizinhas conectadas à peça indicada.
    :param item: A peça a ser analisada.
    :param pecas: Todas as peças disponíveis para análise.
    :param dict_pecas: Dicionário de peças conectadas.
    """
    for _, peca_analisada in pecas.items():
        if verificar_vizinhos(item.posicao, peca_analisada.posicao):
            dict_pecas[peca_analisada.uid] = peca_analisada


def verificar_vizinhos(pos1: tuple, pos2: tuple) -> bool:
    """
    Verifica se a peça tem vizinhos.
    """
    if tem_lateral_vizinho(pos1, pos2):
        return True
    if tem_lateral_diagonal(pos1, pos2):
        return True
    return False


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


def verificar_adicionar_pecas_conectadas(peca, dicionario, pecas):
    """
    Verifica um dicionário e adiciona todas as peças conectadas à peça indicada.
    :param peca: A peça a ser analisada.
    :param pecas: Todas as peças disponíveis para análise.
    :param dicionario: Dicionário de peças conectadas.
    :return: Dicionário de peças conectadas.
    """
    pecas_verificadas = set()
    pecas_a_verificar = [peca]

    while pecas_a_verificar:
        peca_atual = pecas_a_verificar.pop()
        pecas_verificadas.add(peca_atual.uid)

        encontrar_peca_vizinha(peca_atual, pecas, dicionario)

        for uid, peca_conectada in dicionario.items():
            if uid not in pecas_verificadas:
                pecas_a_verificar.append(peca_conectada)

    return dicionario


def verificar_peca_em_grupo(grupos, pecas_conectadas):
    """
    Verifica se alguma peça conectada já está em um grupo.
    :param pecas_conectadas: Dicionário de peças conectadas.
    :param grupos: Dicionário de grupos.
    :return: Grupo encontrado ou None.
    """
    grupos_verificados = set()
    grupo = None
    lideres = set()

    for _, peca_analisada in pecas_conectadas.items():
        for grupo_analisado in grupos.values():
            if peca_analisada.uid in grupo_analisado.pecas:
                grupo = grupo_analisado
                grupos_verificados.add((grupo.criador.nome, grupo.peca_pai.uid))
                lideres.add(grupo.criador.nome)

    if len(grupos_verificados) > 1:
        if len(lideres) == 1:
            return -1
        return -2
    elif len(grupos_verificados) == 1:
        return grupo
    else:
        return 0
