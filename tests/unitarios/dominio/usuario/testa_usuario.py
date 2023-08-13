from bson import ObjectId
import pytest

from src.dominio.usuario.usuario_modelo import Usuario
from src.repositorios.repo_usuario import RepoUsuarioMemoria
from src.erros import NaoEncontrado

repo = RepoUsuarioMemoria()


def testa_quero_salvar_usuario():
    usuario = Usuario(
        nome='ff',
        email='ff@ff',
        celular='34912345678',
        criado_por=ObjectId())
    with pytest.raises(NaoEncontrado):
        print(repo.busca_id(_id=usuario.id))
    repo.insere(usuario)
    usuario_banco = repo.busca_id(_id=usuario.id)
    assert isinstance(usuario_banco, Usuario)
