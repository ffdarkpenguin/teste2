from datetime import datetime
from typing import Self

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, model_validator


class InsereUsuarioParam(BaseModel):
    nome: str
    email: str
    celular: str
    email_validado: bool = False
    celular_validado: bool = False


class AlteraUsuarioParam(BaseModel):
    nome: str | None = None
    email: str | None = None
    celular: str | None = None

    @model_validator(mode='after')
    def verifica_todos_nao_vazios(self) -> Self:
        if self.nome is None and self.email is None and self.celular is None:
            raise ValueError(
                'Todos os campos não podem ser nulos. Informe pelo menos um '
                'campo')
        return self


class AlteraUsuario(AlteraUsuarioParam):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ObjectId = Field(alias='_id')
    alterado_por: ObjectId
    alterado_em: datetime = Field(default_factory=datetime.now)


class Usuario(InsereUsuarioParam):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ObjectId = Field(default_factory=ObjectId, alias='_id')
    criado_em: datetime = Field(default_factory=datetime.now)
    criado_por: ObjectId
    alterado_em: datetime | None = None
    alterado_por: ObjectId | None = None


class Usuarios(list[Usuario]):
    ...


# restrições
# não pode ter email repetido (so verificável no banco de dados)
# nao pode ter celular repetido (so verificável no banco de daos)
# email deve ser validado (operação externa)
# celular deve ser validado (operação externa)
# funcionalidades
# precisa crude
# precisa autenticar
# precisa alterar senha (com autenticação da senha antiga)
