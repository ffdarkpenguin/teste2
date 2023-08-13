from typing import Type
from src.dominio.usuario.usuario_modelo import Usuario, AlteraUsuario, Usuarios
from src.repositorios.repo_memoria import RepoMemoria


class RepoUsuarioMemoria(RepoMemoria[Usuario, AlteraUsuario, Usuarios]):
    def modelo(self) -> Type:
        return Usuario

    def lista_modelo(self) -> Type:
        return Usuarios
