from util import *


def rodar_testes():
    def teste_substituir_grupo():
        print("Teste substituir_grupo")
        jogador1 = Jogador()
        jogador1.set_nome("Jogador1")

        peca1 = Peca()
        peca1.set_uid(1)
        peca1.cor = "vermelho"
        peca1.linha_atual = 1
        peca1.coluna_atual = 1
        peca1.set_player(jogador1)

        peca2 = Peca()
        peca2.set_uid(2)
        peca2.cor = "azul"
        peca2.linha_atual = 1
        peca2.coluna_atual = 3
        peca2.set_player(jogador1)

        grupos.clear()
        grupo1 = Grupo()
        grupo1.set_id(1)
        grupo1.add_peca(peca1)
        grupo2 = Grupo()
        grupo2.set_id(1)
        grupo2.add_peca(peca1)
        grupo2.add_peca(peca2)
        grupos.append(grupo1)
        substituir_grupo(grupo2)
        assert grupos[0].criador == jogador1
        assert grupos[0].qtd_cores == 2
        assert grupos[0].qtd_jogadores == 1
        assert grupos[0].qtd_pecas == 2
        print("Teste substituir_grupo passou\n")

    def teste_get_peca_by_uid():
        print("Teste get_peca_by_uid")
        pecas.clear()
        peca1 = Peca()
        peca1.set_uid(1)
        peca2 = Peca()
        peca2.set_uid(2)
        pecas.extend([peca1, peca2])
        assert get_peca_by_uid(1) == peca1
        assert get_peca_by_uid(2) == peca2
        print("Teste get_peca_by_uid passou\n")

    def teste_get_grupo_by_peca_pai():
        print("Teste get_grupo_by_peca_pai")
        grupos.clear()
        pecas.clear()
        grupo1 = Grupo()
        grupo1.set_id(1)
        peca1 = Peca()
        peca1.set_uid(1)
        peca2 = Peca()
        peca2.set_uid(2)
        grupo1.set_peca_pai(peca1)
        pecas.append(peca1)
        pecas.append(peca2)
        grupos.append(grupo1)
        assert get_grupo_by_peca_pai(peca1) == grupo1
        assert get_grupo_by_peca_pai(peca2) is None
        print("Teste get_grupo_by_peca_pai passou\n")

    # Função de Teste para verificar_peca_existe
    def teste_verificar_peca_existe():
        print("Teste verificar_peca_existe")
        pecas.clear()
        peca1 = Peca()
        peca1.set_uid(1)
        pecas.append(peca1)
        assert verificar_peca_existe(1).__eq__(True)
        assert verificar_peca_existe(2).__eq__(False)
        print("Teste verificar_peca_existe passou\n")

    def teste_verificar_jogador_existe():
        print("Teste verificar_jogador_existe")
        jogador1 = Jogador()
        jogador1.set_nome("Jogador1")
        jogadores.append(jogador1)
        assert verificar_jogador_existe("Jogador1").__eq__(True)
        assert verificar_jogador_existe("Jogador2").__eq__(False)
        print("Teste verificar_jogador_existe passou\n")

    # Função de Teste para substituir_peca
    def teste_substituir_peca():
        print("Teste substituir_peca")
        peca1 = Peca()
        peca1.set_uid(1)
        pecas.append(peca1)
        peca2 = Peca()
        peca2.set_uid(1)
        peca2.set_cor("vermelho")
        substituir_peca(peca2)
        assert pecas[0].cor == "vermelho"
        print("Teste substituir_peca passou\n")

    def teste_substituir_jogador():
        print("Teste substituir_jogador")
        jogador1 = Jogador()
        jogador1.set_nome("Jogador1")
        jogador1.incrementar_infracao()
        jogadores.append(jogador1)
        jogador2 = Jogador()
        jogador2.set_nome("Jogador1")
        jogador2.incrementar_infracao()
        jogador2.incrementar_infracao()
        substituir_jogador(jogador2)
        assert jogadores[0].infracoes == 2
        print("Teste substituir_jogador passou\n")

    # Função de Teste para tem_lateral_vizinho
    def teste_tem_lateral_vizinho():
        print("Teste tem_lateral_vizinho")
        pos1 = (1, 1)
        pos2 = (1, 3)
        assert tem_lateral_vizinho(pos1, pos2).__eq__(True)
        pos3 = (1, 4)
        assert tem_lateral_vizinho(pos1, pos3).__eq__(False)
        print("Teste tem_lateral_vizinho passou\n")

    # Função de Teste para tem_lateral_diagonal
    def teste_tem_lateral_diagonal():
        print("Teste tem_lateral_diagonal")
        pos1 = (1, 1)
        pos2 = (2, 2)
        assert tem_lateral_diagonal(pos1, pos2).__eq__(True)
        pos3 = (2, 3)
        assert tem_lateral_diagonal(pos1, pos3).__eq__(False)
        print("Teste tem_lateral_diagonal passou\n")

    # Função de Teste para process_data
    def teste_process_data():
        pecas.clear()
        print("Teste process_data")
        move = {
            "UID": 1,
            "PosX": 200,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "Jogador1",
            "Cor": "vermelho",
        }
        process_data(move)
        assert len(pecas) == 1
        assert len(jogadas) == 1
        assert pecas[0].uid == 1
        assert pecas[0].posicao_atual == [1, 4]
        print("Teste process_data passou\n")

    # Rodando todos os testes
    teste_verificar_peca_existe()
    teste_verificar_jogador_existe()
    teste_substituir_peca()
    teste_substituir_jogador()
    teste_tem_lateral_vizinho()
    teste_tem_lateral_diagonal()
    teste_get_grupo_by_peca_pai()
    teste_get_peca_by_uid()
    teste_substituir_grupo()
    teste_process_data()


rodar_testes()
