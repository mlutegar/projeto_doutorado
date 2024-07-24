import ast
import unittest
from pathlib import Path

import pandas as pd

from process import Process
from util.situacoes import situacoes


class TestGameFunctions(unittest.TestCase):

    def setUp(self):
        self.processo = Process("teste_iniciar", "novo_host")

    def teste(self):
        def write_clustered() -> None:
            """
            Lê o CSV gerado e escreve os dados analisados em um arquivo clusterizado no caminho especificado.
            """
            # Caminho do CSV original
            csv_path = "../data/Sat_20_Jul_2024_01_39_45_GMT.csv"

            # Caminho do arquivo Excel a ser gerado
            excel_path = "../data/Sat_20_Jul_2024_01_39_45_GMT_clusterizado.xlsx"

            # Ler o CSV
            df = pd.read_csv(csv_path)

            # Lista para armazenar as novas linhas
            novas_linhas = []

            # Dicionário de exemplo para as descrições dos casos
            descricoes_casos = situacoes

            # Iterar sobre cada linha do DataFrame
            for index, row in df.iterrows():
                casos_id = ast.literal_eval(row["Casos ID"])

                # Para cada caso ID, criar uma nova linha com a descrição do caso
                for caso_id in casos_id:
                    nova_linha = row.copy()
                    nova_linha["Casos ID"] = caso_id
                    nova_linha["Descrição do Caso"] = descricoes_casos.get(caso_id, "Descrição não encontrada")
                    novas_linhas.append(nova_linha)

            # Criar um novo DataFrame com as novas linhas
            df_expandido = pd.DataFrame(novas_linhas)

            # Salvar o DataFrame expandido em um arquivo Excel
            df_expandido.to_excel(excel_path, index=False)

        write_clustered()

    def test_iniciar_jogo(self):
        self.assertEqual(self.processo.game.nome_da_sala, "teste_iniciar")
        self.assertEqual(self.processo.game.host, "novo_host")

    def test_process_data(self):
        move = {
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        }

        self.processo.process_data(move)

        self.assertIn(1, self.processo.game.pecas)
        self.assertIn("jogador1", self.processo.game.jogadores)
        self.assertEqual(self.processo.game.pecas[1].posicao, (1, 1))
        self.assertEqual(self.processo.game.pecas[1].jogador.nome, "jogador1")
        self.assertEqual(len(self.processo.game.jogadas), 1)

    def test_process_data_incomplete(self):
        move = {
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1"
            # "Cor" is missing
        }

        with self.assertRaises(ValueError):
            self.processo.process_data(move)

    def test_finalizar_jogo_desistiu(self):
        # Adiciona jogador para teste
        self.processo.process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        move = {"Jogador": "jogador1", "Acao": "Desistiu"}
        finalizacao = self.processo.finalizar_jogo(move)
        self.assertEqual(finalizacao.descricao, "Desistiu")
        self.assertEqual(finalizacao.jogador.nome, "jogador1")

    def test_finalizar_jogo_finalizou(self):
        # Adiciona jogador para teste
        self.processo.process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        move = {"Jogador": "jogador1", "Acao": "Finalizou"}
        finalizacao = self.processo.finalizar_jogo(move)
        self.assertEqual(finalizacao.descricao, "Finalizou")
        self.assertEqual(finalizacao.jogador.nome, "jogador1")

    def test_finalizar_jogo_invalid_action(self):
        self.processo.process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        move = {"Jogador": "jogador1", "Acao": "Invalid"}
        with self.assertRaises(ValueError):
            self.processo.finalizar_jogo(move)

    def test_finalizar_jogo_invalid_jogador(self):
        move = {"Jogador": "invalid_jogador", "Acao": "Desistiu"}
        with self.assertRaises(ValueError):
            self.processo.finalizar_jogo(move)

    def test_encerrar_jogo(self):
        # Adiciona jogadores e jogadas para teste
        self.processo.process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        self.processo.process_data({
            "UID": 2,
            "PosX": 211,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "azul"
        })
        self.processo.encerrar_jogo()
        self.assertTrue(Path('data.csv').is_file())

    def test_encerrar_jogo_no_data(self):
        self.processo.game = None  # Certifica que o jogo não foi iniciado
        with self.assertRaises(ValueError):
            self.processo.encerrar_jogo()


if __name__ == '__main__':
    unittest.main()
