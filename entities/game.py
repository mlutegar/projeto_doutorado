from datetime import timedelta, datetime
from typing import Dict, Set, Union

from entities.grupo import Grupo
from entities.jogada import Jogada
from entities.jogador import Jogador
from entities.peca import Peca
from util.methods_peca import verificar_adicionar_pecas_conectadas, verificar_peca_em_grupo


class Game:
    def __init__(self, name: str, host: str) -> None:
        """
        Inicializa um jogo.
        :param name: Nome da sala.
        :param host: Nome do anfitrião.
        """
        self.nome_da_sala: str = name
        self.host: str = host
        self.status: str = "Iniciado"

        self.tempo_de_jogo: timedelta = timedelta(seconds=0)
        self.tempo_inicio: datetime = datetime.now()
        self.tempo_fim: Union[datetime, None] = None

        self.players_desistiu: Set[Jogador] = set()
        self.players_finalizou: Set[Jogador] = set()

        self.jogadas: Dict[int, Jogada] = dict()
        self.jogadores: Dict[str, Jogador] = dict()
        self.grupos: Dict[tuple, Grupo] = dict()
        self.pecas: Dict[int, Peca] = dict()

    def add_jogador(self, nome: str) -> Jogador:
        """
        Adiciona um novo jogador ao jogo.
        :param nome: Nome do jogador.
        :return: Instância de Jogador criada.
        """
        jogador: Jogador = Jogador(nome)
        self.jogadores[jogador.nome] = jogador
        return jogador

    def add_jogada(self, peca: Peca, tempo: timedelta) -> Jogada:
        """
        Adiciona uma nova jogada ao jogo.
        :param peca: Peça utilizada na jogada.
        :param tempo: Tempo da jogada.
        :return: Instância de Jogada criada.
        """
        grupo: Grupo = self.add_grupo(peca)
        jogada: Jogada = Jogada(uid=len(self.jogadas) + 1, peca=peca, grupo=grupo, tempo=tempo)
        self.jogadas[jogada.id] = jogada
        return jogada

    def add_grupo(self, peca: Peca) -> Union[Grupo, None]:
        """
        Adiciona um grupo de peças conectadas à peça indicada.
        :param peca: A peça a ser adicionada ao grupo.
        :return: Grupo ao qual a peça foi adicionada ou novo grupo criado.
        """
        for grupo in self.grupos.values():
            if grupo.verificar_peca(peca):
                grupo.remover_peca(peca)

        pecas_conectadas: Dict[int, Peca] = {peca.uid: peca}
        pecas_conectadas = verificar_adicionar_pecas_conectadas(
            peca=peca,
            pecas=self.pecas,
            dicionario=pecas_conectadas
        )

        if len(pecas_conectadas) == 1:
            return None

        grupo_existente = verificar_peca_em_grupo(pecas_conectadas=pecas_conectadas, grupos=self.grupos)

        if isinstance(grupo_existente, Grupo):
            if grupo_existente.criador != peca.jogador:
                peca.jogador.adicionar_infracao()

            grupo_existente.add_peca(peca)
            self.grupos[(grupo_existente.criador.nome, grupo_existente.peca_pai.uid)] = grupo_existente
            return grupo_existente

        if grupo_existente == -1:
            peca.eh_ponte = True
            return None

        grupo: Grupo = Grupo(peca)

        for peca_conectada in pecas_conectadas.values():
            grupo.add_peca(peca_conectada)

        self.grupos[(grupo.criador.nome, grupo.peca_pai.uid)] = grupo
        return grupo

    def add_peca(self, uid: int, cor: str) -> Peca:
        """
        Adiciona uma nova peça ao jogo.
        :param uid: Identificador único da peça.
        :param cor: Cor da peça.
        :return: Instância de Peca criada.
        """
        peca: Peca = Peca(uid=uid, cor=cor)
        self.pecas[peca.uid] = peca
        return peca

    def desistir(self, player: Jogador) -> None:
        """
        Marca um jogador como desistente.
        :param player: Instância de Jogador que desistiu.
        """
        player.desistir()
        self.players_desistiu.add(player)
        self.jogadores.pop(player.nome)

        if len(self.jogadores) == 1:
            self.acabar_jogo()

    def finalizar(self, player: Jogador) -> None:
        """
        Marca um jogador como finalizado.
        :param player: Instância de Jogador que finalizou.
        """
        player.finalizar()
        self.players_finalizou.add(player)
        self.jogadores.pop(player.nome)

        if len(self.jogadores) == 1:
            self.acabar_jogo()

    def acabar_jogo(self) -> None:
        """
        Finaliza o jogo.
        """
        self.tempo_fim = datetime.now()
        self.tempo_de_jogo = self.tempo_fim - self.tempo_inicio
        self.status = "Finalizado"