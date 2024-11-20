from src.entities.peca import *


def rodar_testes_peca():
    # Função de Teste para contar_vizinhos_peca
    def teste_contar_vizinhos_peca():
        print("Teste contar_vizinhos_peca")
        pecas.clear()
        peca1 = Peca(1)
        peca1.set_posicao_atual_tabuleiro1(123, 74)
        peca2 = Peca(2)
        peca2.set_posicao_atual_tabuleiro1(200, 74)
        assert contar_vizinhos_peca(peca1) == 1
        assert contar_vizinhos_peca(peca2) == 1
        print("Teste contar_vizinhos_peca passou\n")

    teste_contar_vizinhos_peca()


rodar_testes_peca()
