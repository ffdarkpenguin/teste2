from src.repositorios.repo_usuario import RepoUsuarioMemoria, Usuario, Usuarios


def testa_modelo_definido_corretamente():
    repo = RepoUsuarioMemoria()
    assert repo.modelo() == Usuario


def testa_lista_modelo_definido_corretamente():
    repo = RepoUsuarioMemoria()
    assert repo.lista_modelo() == Usuarios
