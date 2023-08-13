from typing import Protocol

from src.dominio.usuario.usuario_modelo import AlteraUsuario, Usuario, Usuarios


class ProtoRepoUsuario(Protocol):
    @property
    def qtd_registros(self) -> int:
        ...  # pragma: not covered

    def insere(self, params: Usuario):
        ...  # pragma: not covered

    def lista(self, **filtro) -> Usuarios:
        ...  # pragma: not covered

    def busca_id(self, _id) -> Usuario:
        ...  # pragma: not covered

    def altera(self, params: AlteraUsuario) -> Usuario:
        ...  # pragma: not covered

    def remove(self, _id) -> Usuario:
        ...  # pragma: not covered
