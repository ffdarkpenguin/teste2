
from src.casos_uso.usuario_proto import ProtoRepoUsuario
from src.dominio.usuario.usuario_modelo import (AlteraUsuario,
                                                AlteraUsuarioParam,
                                                InsereUsuarioParam, ObjectId,
                                                Usuario, Usuarios)


class GerenciadorUsuario():
    def __init__(self, repo: ProtoRepoUsuario) -> None:
        self.repo = repo

    def insere_usuario(
            self,
            params: InsereUsuarioParam,
            criado_por: ObjectId) -> Usuario:
        usuario = Usuario(**params.model_dump(), criado_por=criado_por)
        self.repo.insere(usuario)
        return usuario

    def busca_usuario(self, _id) -> Usuario:
        return self.repo.busca_id(_id)

    def lista_usuario(self) -> Usuarios:
        return self.repo.lista()

    def altera_usuario(
            self,
            _id,
            params: AlteraUsuarioParam,
            alterado_por: ObjectId) -> Usuario:
        alteracao_dic = params.model_dump(by_alias=True)
        alteracao = AlteraUsuario(
            _id=_id,
            alterado_por=alterado_por,
            **alteracao_dic,)
        ret = self.repo.altera(params=alteracao)
        return ret

    def remove_usuario(self, _id) -> Usuario:
        return self.repo.remove(_id)
