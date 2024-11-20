import networkx as nx
import plotly.graph_objects as go

# Obtenha jogadores e layouts disponíveis
layouts = {
    "Spectral": nx.spectral_layout,
    "Circular": nx.circular_layout,
    "Shell": nx.shell_layout,
    "Kamada-Kawai": nx.kamada_kawai_layout,
    "Multipartite": nx.multipartite_layout
}

fases_disponiveis = list(range(1, 5))

def gerar_grafo(df_clusterizado, jogador, layout_name, jogada_inicial, jogada_final, mostrar_estados, fases_selecionadas):
    # Filtrar pelo jogador
    df_jogador = df_clusterizado[df_clusterizado["Nome do player"] == jogador]
    #printf"\nDados após filtrar pelo jogador ({jogador}):")
    #printdf_jogador)

    # Filtrar pelas fases selecionadas
    if fases_selecionadas:
        df_jogador = df_jogador[df_jogador["Fase da jogada"].isin(fases_selecionadas)]
        #printf"\nDados após filtrar pelas fases selecionadas ({fases_selecionadas}):")
        #printdf_jogador)

    # Criar um índice crescente de jogadas para cada jogador e fase
    df_jogador = df_jogador.copy()
    df_jogador["Jogada"] = df_jogador.groupby(["Nome do player"])["ID"].rank(method="dense").astype(int)
    #print"\nDados após calcular a coluna 'Jogada':")
    #printdf_jogador[["ID", "Nome do player", "Fase da jogada", "Jogada", "Descrição do Caso"]])

    # Filtrar pelas jogadas no intervalo especificado
    df_jogador = df_jogador[
        (df_jogador["Jogada"] >= jogada_inicial) & (df_jogador["Jogada"] <= jogada_final)
    ]
    #printf"\nDados após filtrar pelo intervalo de jogadas ({jogada_inicial} a {jogada_final}):")
    #printdf_jogador)

    # Lista de jogadas filtradas, reiniciando para cada fase
    jogadas_filtradas = (
        df_jogador.groupby("Fase da jogada")["Jogada"]
        .apply(lambda x: x.unique())
        .explode()
        .tolist()
    )
    #print"\nJogadas filtradas por fase:")
    #for fase, jogadas in df_jogador.groupby("Fase da jogada")["Jogada"].apply(lambda x: x.unique()).items():
        #printf"Fase {fase}: {jogadas}")

    #printf"Jogadas filtradas: {jogadas_filtradas}")

    # Criar o grafo
    G = nx.DiGraph()  # G: variável que armazena o grafo
    previous_jogada = None

    for jogada_id in jogadas_filtradas:
        #printf"Processando Jogada: {jogada_id}")
        # Dados da jogada atual
        df_fase_atual = df_jogador[df_jogador["Jogada"] == jogada_id]
        if df_fase_atual.empty:
            #printf"\nJogada {jogada_id} está vazia, ignorando.")
            continue

        fase_atual = df_fase_atual["Fase da jogada"].iloc[0]
        jogada = f"Jogada {jogada_id} - Fase {fase_atual}"
        #printf"\nCriando nó para {jogada}:")
        #printdf_fase_atual)

        G.add_node(jogada, label=jogada, color='blue', subset=0)

        if previous_jogada:
            G.add_edge(previous_jogada, jogada)
            #printf"Adicionando aresta entre {previous_jogada} -> {jogada}")

        # Iterar pelos IDs únicos associados à jogada
        jogada_ids = df_fase_atual["ID"].unique()
        #printf"\nIDs associados à jogada {jogada}: {jogada_ids}")

        for jogada_id in jogada_ids:
            df_id = df_jogador[df_jogador["ID"] == jogada_id]
            #printf"\nDados para ID {jogada_id}:")
            #printdf_id)

            for _, row in df_id.iterrows():
                caso_descricao = f"{row['Descrição do Caso']}"
                if caso_descricao not in G:
                    G.add_node(caso_descricao, label=caso_descricao, color='green', subset=1)
                    #printf"Adicionando nó para {caso_descricao}")
                G.add_edge(jogada, caso_descricao)
                #printf"Adicionando aresta entre {jogada} -> {caso_descricao}")

                # Adicionando operações
                for i in range(1, 9):
                    acao_coluna = f"Operação {i}"  # acao_coluna: variável que armazena o nome da coluna
                    operacao_descricao = row.get(
                        acao_coluna)  # operacao_descricao: variável que armazena o valor da coluna

                    # Certifique-se de que o valor é uma string antes de aplicar .strip()
                    if isinstance(operacao_descricao,
                                  str) and operacao_descricao.strip() and operacao_descricao not in G:
                        G.add_node(operacao_descricao, label=operacao_descricao, color='yellow', subset=2)

                    if isinstance(operacao_descricao, str) and operacao_descricao.strip():
                        G.add_edge(caso_descricao, operacao_descricao)

                    if mostrar_estados:
                        # Adicionando estados 1
                        for i in range(1, 9):
                            estado_coluna = f"Estado 1 {i}"
                            estado_descricao = row.get(estado_coluna)

                            # Validações robustas para 'estado_descricao'
                            if isinstance(estado_descricao, str) and estado_descricao.strip():
                                estado_descricao = estado_descricao.strip()  # Remove espaços extras

                                # Adiciona o nó apenas se ele não existe
                                if estado_descricao not in G:
                                    G.add_node(estado_descricao, label=estado_descricao, color='orange', subset=3)

                                # Valida 'operacao_descricao' antes de criar a aresta
                                if isinstance(operacao_descricao, str) and operacao_descricao.strip():
                                    G.add_edge(operacao_descricao.strip(), estado_descricao)

                        # Adicionando estados 2
                        for i in range(1, 9):
                            estado_coluna = f"Estado 2 {i}"
                            estado_descricao = row.get(estado_coluna)

                            # Validações robustas para 'estado_descricao'
                            if isinstance(estado_descricao, str) and estado_descricao.strip():
                                estado_descricao = estado_descricao.strip()  # Remove espaços extras

                                # Adiciona o nó apenas se ele não existe
                                if estado_descricao not in G:
                                    G.add_node(estado_descricao, label=estado_descricao, color='gray', subset=3)

                                # Valida 'operacao_descricao' antes de criar a aresta
                                if isinstance(operacao_descricao, str) and operacao_descricao.strip():
                                    operacao_descricao = operacao_descricao.strip()  # Remove espaços extras
                                    G.add_edge(operacao_descricao, estado_descricao)

        previous_jogada = jogada
    pos = layouts[layout_name](G)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x, node_y, node_color, node_text = [], [], [], []
    for node in G.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        node_color.append(node[1]['color'])
        node_text.append(node[1]['label'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=20, color=node_color, line=dict(width=2, color='black')),
        text=node_text,
        textposition='top center',
        textfont=dict(size=8),
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f"Grafo do Jogador: {jogador} ({layout_name} Layout) - Jogadas {jogada_inicial} a {jogada_final}",
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, visible=False),
                        yaxis=dict(showgrid=False, zeroline=False, visible=False)
                    ))
    return fig
