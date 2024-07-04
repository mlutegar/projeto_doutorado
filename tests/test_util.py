import unittest
from util import (
    substituir_grupo, get_peca_by_uid, get_grupo_by_peca_pai, verificar_peca_existe,
    verificar_jogador_existe, substituir_peca, substituir_jogador, tem_lateral_vizinho,
    tem_lateral_diagonal, process_data
)
from entities.jogador import Jogador, jogadores
from entities.peca import Peca, pecas
from entities.grupo import Grupo, grupos
from entities.jogada import jogadas


class TestUtil(unittest.TestCase):
    def setUp(self):
        # Resetar os estados globais antes de cada teste
        grupos.clear()
        pecas.clear()
        jogadores.clear()
        jogadas.clear()

    def test_substituir_grupo(self):
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

        grupo1 = Grupo()
        grupo1.set_id(1)
        grupo1.add_peca(peca1)

        grupo2 = Grupo()
        grupo2.set_id(1)
        grupo2.add_peca(peca1)
        grupo2.add_peca(peca2)

        grupos.append(grupo1)
        substituir_grupo(grupo2)

        self.assertEqual(grupos[0].criador, jogador1)
        self.assertEqual(grupos[0].qtd_cores, 2)
        self.assertEqual(grupos[0].qtd_jogadores, 1)
        self.assertEqual(grupos[0].qtd_pecas, 2)

    def test_get_peca_by_uid(self):
        peca1 = Peca()
        peca1.set_uid(1)
        peca2 = Peca()
        peca2.set_uid(2)
        pecas.extend([peca1, peca2])

        self.assertEqual(get_peca_by_uid(1), peca1)
        self.assertEqual(get_peca_by_uid(2), peca2)

    def test_get_grupo_by_peca_pai(self):
        grupo1 = Grupo()
        grupo1.set_id(1)
        peca1 = Peca()
        peca1.set_uid(1)
        peca2 = Peca()
        peca2.set_uid(2)
        grupo1.set_peca_pai(peca1)
        grupos.append(grupo1)

        self.assertEqual(get_grupo_by_peca_pai(peca1), grupo1)
        self.assertIsNone(get_grupo_by_peca_pai(peca2))

    def test_verificar_peca_existe(self):
        peca1 = Peca()
        peca1.set_uid(1)
        pecas.append(peca1)

        self.assertTrue(verificar_peca_existe(1))
        self.assertFalse(verificar_peca_existe(2))

    def test_verificar_jogador_existe(self):
        jogador1 = Jogador()
        jogador1.set_nome("Jogador1")
        jogadores.append(jogador1)

        self.assertTrue(verificar_jogador_existe("Jogador1"))
        self.assertFalse(verificar_jogador_existe("Jogador2"))

    def test_substituir_peca(self):
        peca1 = Peca()
        peca1.set_uid(1)
        pecas.append(peca1)

        peca2 = Peca()
        peca2.set_uid(1)
        peca2.set_cor("vermelho")
        substituir_peca(peca2)

        self.assertEqual(pecas[0].cor, "vermelho")

    def test_substituir_jogador(self):
        jogador1 = Jogador()
        jogador1.set_nome("Jogador1")
        jogador1.incrementar_infracao()
        jogadores.append(jogador1)

        jogador2 = Jogador()
        jogador2.set_nome("Jogador1")
        jogador2.incrementar_infracao()
        jogador2.incrementar_infracao()
        substituir_jogador(jogador2)

        self.assertEqual(jogadores[0].infracoes, 2)

    def test_tem_lateral_vizinho(self):
        pos1 = (1, 1)
        pos2 = (1, 3)
        self.assertTrue(tem_lateral_vizinho(pos1, pos2))

        pos3 = (1, 4)
        self.assertFalse(tem_lateral_vizinho(pos1, pos3))

    def test_tem_lateral_diagonal(self):
        pos1 = (1, 1)
        pos2 = (2, 2)
        self.assertTrue(tem_lateral_diagonal(pos1, pos2))

        pos3 = (2, 3)
        self.assertFalse(tem_lateral_diagonal(pos1, pos3))

    def test_process_data(self):
        move = {
            "UID": 1,
            "PosX": 200,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "Jogador1",
            "Cor": "vermelho",
        }
        process_data(move)

        self.assertEqual(len(pecas), 1)
        self.assertEqual(len(jogadas), 1)
        self.assertEqual(pecas[0].uid, 1)
        self.assertEqual(pecas[0].posicao_atual, [1, 4])
