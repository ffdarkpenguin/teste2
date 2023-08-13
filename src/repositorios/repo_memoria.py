from abc import abstractmethod
from typing import Any, Generic, Type, TypeVar, Iterator, Iterable

from pydantic import BaseModel

from src.erros import Duplicado, NaoEncontrado

Modelo = TypeVar('Modelo', bound=BaseModel)
ParamsAlteracao = TypeVar('ParamsAlteracao', bound=BaseModel)
ListaModelo = TypeVar('ListaModelo', bound=list)


class RepoMemoria(list, Generic[Modelo, ParamsAlteracao, ListaModelo]):

    @abstractmethod
    def modelo(self) -> Type:
        ...

    @abstractmethod
    def lista_modelo(self) -> Type:
        ...

    def _converte_modelo(self, dados: dict) -> Modelo:
        return self.modelo()(**dados)

    def _converte_lista_modela(self, dados: Iterable[dict]) -> ListaModelo:
        return self.lista_modelo()(self.modelo()(**x) for x in dados)

    @property
    def qtd_registros(self) -> int:
        return len(self)

    def insere(self, params: Modelo):
        dados = params.model_dump(by_alias=True)
        try:
            self.busca_id(dados['_id'])
            raise Duplicado(
                f'Já existe um registro com ID: {dados["_id"]}')
        except NaoEncontrado:
            self.append(dados)

    def lista(self, **filtro) -> ListaModelo:
        if not filtro:
            return self._converte_lista_modela(self)
        campo, valor = self._pega_campo_valor_filtro(filtro)
        return self._converte_lista_modela(self._filtra(campo, valor))

    def busca(self, **filtro) -> Modelo:
        ret = self._busca(**filtro)
        return self._converte_modelo(ret)

    def _busca(self, **filtro) -> dict:
        campo, valor = self._pega_campo_valor_filtro(filtro)
        ret = self._filtra(campo, valor)
        try:
            return next(ret)
        except StopIteration:
            raise NaoEncontrado(f'Registro não encontrado filtro: {filtro}')

    def busca_id(self, _id) -> Modelo:
        return self.busca(_id=_id)

    def altera(self, params: ParamsAlteracao) -> Modelo:
        alteracao = params.model_dump(by_alias=True, exclude_none=True)
        _id = alteracao.pop('_id')
        dados = self._busca(_id=_id)
        dados.update(alteracao)
        return self._converte_modelo(dados)

    def remove(self, _id) -> Modelo:
        ret = self._busca(_id=_id)
        super().remove(ret)
        return self._converte_modelo(ret)

    def _filtra(self, campo, valor) -> Iterator[dict]:
        return (x for x in self if x[campo] == valor)

    def _pega_campo_valor_filtro(self, filtro: dict) -> tuple[str, Any]:
        return next((k, v) for k, v in filtro.items())
