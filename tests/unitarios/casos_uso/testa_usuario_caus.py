import pytest

from src.casos_uso.usuario_caus import (AlteraUsuarioParam, GerenciadorUsuario,
                                        InsereUsuarioParam, ObjectId, Usuario)
from src.repositorios.repo_usuario import RepoUsuarioMemoria


@pytest.fixture
def gerenciador_usuario():
    return GerenciadorUsuario(repo=RepoUsuarioMemoria())


def testa_insere_usuario(gerenciador_usuario: GerenciadorUsuario):
    params = InsereUsuarioParam(nome='ff', email='ff@ff', celular='91234')
    ret = gerenciador_usuario.insere_usuario(
        params=params, criado_por=ObjectId())
    assert isinstance(ret, Usuario)
    assert gerenciador_usuario.busca_usuario(_id=ret.id) == ret


def testa_busca_usuario(gerenciador_usuario: GerenciadorUsuario):
    params = InsereUsuarioParam(nome='ff', email='ff@ff', celular='91234')
    ret = gerenciador_usuario.insere_usuario(
        params=params, criado_por=ObjectId())
    ret2 = gerenciador_usuario.busca_usuario(_id=ret.id)
    assert ret2 == ret


def testa_lista_usuario(gerenciador_usuario: GerenciadorUsuario):
    params = InsereUsuarioParam(nome='ff', email='ff@ff', celular='91234')
    ret = gerenciador_usuario.insere_usuario(
        params=params, criado_por=ObjectId())

    ret2 = gerenciador_usuario.lista_usuario()
    assert len(ret2) == 1
    assert ret == ret2[0]


def testa_altera_usuario(gerenciador_usuario: GerenciadorUsuario):
    params = InsereUsuarioParam(nome='ff', email='ff@ff', celular='91234')
    ret = gerenciador_usuario.insere_usuario(
        params=params, criado_por=ObjectId())
    alteracao = AlteraUsuarioParam(nome='alterado')
    alterador = ObjectId()
    ret2 = gerenciador_usuario.altera_usuario(
        _id=ret.id, params=alteracao, alterado_por=alterador)
    assert ret2.nome == alteracao.nome
    assert ret.alterado_em is None
    assert ret2.alterado_em is not None
    assert ret.alterado_por is None
    assert ret2.alterado_por == alterador


def testa_remove_usuario(gerenciador_usuario: GerenciadorUsuario):
    params = InsereUsuarioParam(nome='ff', email='ff@ff', celular='91234')
    ret = gerenciador_usuario.insere_usuario(
        params=params, criado_por=ObjectId())
    ret2 = gerenciador_usuario.remove_usuario(_id=ret.id)
    assert ret == ret2
    assert gerenciador_usuario.lista_usuario() == []
