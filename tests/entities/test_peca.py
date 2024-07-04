from entities.peca import *


def rodar_testes_peca():
    # Função de Teste para contar_vizinhos_peca
    def teste_contar_vizinhos_peca():
        print("Teste contar_vizinhos_peca")
        pecas.clear()
        peca1 = Peca()
        peca1.set_uid(1)
        peca1.set_posicao_atual(123, 74)
        peca2 = Peca()
        peca2.set_uid(2)
        peca2.set_posicao_atual(200, 74)
        pecas.extend([peca1, peca2])
        assert contar_vizinhos_peca(peca1) == 1
        assert contar_vizinhos_peca(peca2) == 1
        print("Teste contar_vizinhos_peca passou\n")

    teste_contar_vizinhos_peca()


rodar_testes_peca()
