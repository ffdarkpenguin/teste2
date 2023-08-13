from datetime import datetime

import pytest
from bson import ObjectId
from pydantic import ValidationError

from src.dominio.usuario.usuario_modelo import (AlteraUsuario,
                                                AlteraUsuarioParam,
                                                InsereUsuarioParam, Usuario)


# USUARIO
def testa_modelo_usuario_tem_todos_campos():
    dados = {
        '_id': ObjectId(),
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'email_validado': True,
        'celular_validado': True,
        'criado_por': ObjectId(),
        'criado_em': datetime.now(),
        'alterado_por': ObjectId(),
        'alterado_em': datetime.now(),
    }

    usuario = Usuario(**dados)
    for c, v in dados.items():
        if c == '_id':
            assert usuario.id == v
        else:
            assert getattr(usuario, c) == v


def testa_modelo_gera_id_automaticamente():
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'email_validado': True,
        'celular_validado': True,
        'criado_por': ObjectId(),
        'criado_em': datetime.now(),
        'alterado_por': ObjectId(),
        'alterado_em': datetime.now(),
    }
    usuario = Usuario(**dados)
    assert isinstance(usuario.id, ObjectId)


def testa_modelo_gera_criado_em_automaticamente():
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'criado_por': ObjectId(),
    }
    usuario = Usuario(**dados)
    assert isinstance(usuario.criado_em, datetime)


def testa_modelo_seta_email_validado_false_por_padrao():
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'criado_por': ObjectId(),
    }
    usuario = Usuario(**dados)
    assert usuario.email_validado is False


def testa_modelo_seta_celular_validado_false_por_padrao():
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'criado_por': ObjectId(),
    }

    usuario = Usuario(**dados)
    assert usuario.celular_validado is False


@pytest.mark.parametrize(
        'nome_campo', ['nome', 'email', 'celular', 'criado_por'])
def testa_campos_obrigatorios(nome_campo):
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'criado_por': ObjectId(),
    }
    dados.pop(nome_campo)
    with pytest.raises(ValidationError):
        Usuario(**dados)


# INSERE USUARIO PARAM

def testa_modelo_insere_usuario_param_tem_todos_campos():
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'email_validado': True,
        'celular_validado': True,
    }

    usuario = InsereUsuarioParam(**dados)
    for c, v in dados.items():
        assert getattr(usuario, c) == v


def testa_insere_usuario_param_seta_email_validado_false_por_padrao():
    usuario = InsereUsuarioParam(nome='ff', email='ff@ff', celular='3491234')
    assert usuario.email_validado is False


def testa_insere_usuario_param_seta_celular_validado_false_por_padrao():
    usuario = InsereUsuarioParam(nome='ff', email='ff@ff', celular='3491234')
    assert usuario.celular_validado is False


# ALTERA USUARIO PARAM
def testa_modelo_altera_usuario_param_tem_todos_campos():
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
    }

    usuario = AlteraUsuarioParam(**dados)
    for c, v in dados.items():
        assert getattr(usuario, c) == v


@pytest.mark.parametrize('nome_campo', ['nome', 'email', 'celular'])
def testa_altera_usuario_param_todos_os_campos_sao_opcionais(nome_campo):
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234'
    }
    dados.pop(nome_campo)
    usuario = AlteraUsuarioParam(**dados)
    assert getattr(usuario, nome_campo) is None


def testa_altera_usuario_param_nao_aceita_tudo_nulo():
    with pytest.raises(ValidationError):
        AlteraUsuarioParam()


# ALTERA USUARIO

def testa_altera_usuario_todos_campos():
    dados = {
        '_id': ObjectId(),
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'alterado_por': ObjectId(),
        'alterado_em': datetime.now()

    }
    alteracao = AlteraUsuario(**dados)
    for c, v in dados.items():
        if c == '_id':
            assert alteracao.id == v
        else:
            assert getattr(alteracao, c) == v


def testa_altera_usuario_requer_id():
    dados = {
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'alterado_por': ObjectId(),
        'alterado_em': datetime.now()

    }
    with pytest.raises(ValidationError):
        AlteraUsuario(**dados)


def testa_altera_usuario_requer_alterado_por():
    dados = {
        '_id': ObjectId(),
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'alterado_em': datetime.now()

    }
    with pytest.raises(ValidationError):
        AlteraUsuario(**dados)


def testa_altera_usuario_gera_alterado_em():
    dados = {
        '_id': ObjectId(),
        'nome': 'ff',
        'email': 'ff@ff',
        'celular': '3491234',
        'alterado_por': ObjectId()
    }
    alteracao = AlteraUsuario(**dados)
    assert alteracao.alterado_em is not None


# LISTA USUARIOS
