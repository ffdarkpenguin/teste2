from typing import Type
from pytest import fixture, raises

from pydantic import BaseModel, Field

from src.erros import Duplicado, NaoEncontrado
from src.repositorios.repo_memoria import RepoMemoria


class ModeloTeste(BaseModel):
    id: int = Field(alias='_id')
    nome: str


class ListaModeloTeste(list[ModeloTeste]):
    ...


class RepoTeste(RepoMemoria[ModeloTeste, ModeloTeste, ListaModeloTeste]):
    def modelo(self) -> Type:
        return ModeloTeste

    def lista_modelo(self) -> Type:
        return ListaModeloTeste


@fixture
def repo():
    return RepoTeste()


@fixture
def alteracao():
    return ModeloTeste(_id=1, nome='alterado')


@fixture
def dado1():
    return ModeloTeste(_id=1, nome='t1')


@fixture
def dado2():
    return ModeloTeste(_id=2, nome='t2')


@fixture
def repo_2_registros(
        repo: RepoTeste,
        dado1: ModeloTeste,
        dado2: ModeloTeste):
    repo.insere(dado1)
    repo.insere(dado2)
    return repo


def testa_qtd_registros_inicial_zero(repo: RepoMemoria):
    assert repo.qtd_registros == 0


def testa_insere(repo: RepoMemoria, dado1: ModeloTeste):
    repo.insere(dado1)
    assert repo.busca_id(dado1.id) == dado1


def testa_insere_nao_permite_duplicado(repo: RepoMemoria, dado1: ModeloTeste):
    repo.insere(dado1)
    with raises(Duplicado):
        repo.insere(dado1)


def testa_lista_sem_dados_retorna_lista_vazia(repo: RepoMemoria):
    ret = repo.lista()
    assert isinstance(ret, list)
    assert ret == []


def testa_lista_sem_filtro_retorna_todos(repo_2_registros: RepoMemoria):
    ret = repo_2_registros.lista()
    assert isinstance(ret, list)
    assert len(ret) == 2


def testa_lista_com_filtro_retorna_registro_atende_filtro(
        repo_2_registros: RepoMemoria):
    ret = repo_2_registros.lista(_id=1)
    assert isinstance(ret, list)
    assert len(ret) == 1
    assert ret[0].id == 1


def testa_busca_com_filtro_retorna_registro_atende_filtro(
        repo_2_registros: RepoMemoria):
    ret = repo_2_registros.busca(_id=1)
    assert isinstance(ret, ModeloTeste)
    assert ret.id == 1


def testa_busca_com_filtro_nao_encontrado_gera_excessao(
        repo_2_registros: RepoMemoria):
    with raises(NaoEncontrado):
        repo_2_registros.busca(_id=10)


def testa_busca_por_id_retorna_registro_com_id_passado(
        repo_2_registros: RepoMemoria):
    ret = repo_2_registros.busca_id(1)
    assert isinstance(ret, ModeloTeste)
    assert ret.id == 1


def testa_busca_por_id_nao_existente_gera_excessao(
        repo_2_registros: RepoMemoria):
    with raises(NaoEncontrado):
        repo_2_registros.busca_id(10)


def testa_altera_id_nao_existe_gera_excessao(
        repo_2_registros: RepoMemoria,
        alteracao: ModeloTeste):
    alteracao.id = 10
    with raises(NaoEncontrado):
        repo_2_registros.altera(alteracao)


def testa_altera_muda_campos_passados(
        repo_2_registros: RepoMemoria,
        alteracao: ModeloTeste):
    ret = repo_2_registros.busca_id(alteracao.id)
    assert ret.nome == 't1'
    repo_2_registros.altera(alteracao)
    ret = repo_2_registros.busca_id(alteracao.id)
    assert ret.nome == 'alterado'


def testa_remove_exclui_registro_banco(
        repo_2_registros: RepoMemoria):
    ret = repo_2_registros.remove(1)
    assert ret.id == 1
    with raises(NaoEncontrado):
        repo_2_registros.busca_id(1)


def testa_remove_id_nao_existente_gera_excessao(
        repo_2_registros: RepoMemoria):
    with raises(NaoEncontrado):
        repo_2_registros.remove(10)
