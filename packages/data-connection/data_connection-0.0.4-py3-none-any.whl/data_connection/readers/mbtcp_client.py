"""Modbus TCP клиент для чтения / записи данных с Modbus TCP сервера."""

from ipaddress import IPv4Address
from typing import Any, Generic, Iterable


from ..field import Field as FieldComm, TField


class Field(Generic[TField]):
    """Один регистр для чтения / записи."""

    __field: FieldComm[TField]

    def __init__(
        self,
        field: FieldComm[TField],
        byte_offset: int,
        bit_offset: int | None = None,
    ) -> None:
        """Один регистр для чтения / записи.

        Parameters
        ----------
        field: FieldComm[TField],
            Ссылка на поле из модели данных
        """
        self.__field = field


class FieldGroup(object):
    """Группа региситров для запроса."""

    def __init__(
        self,
        fields: Iterable[Field[Any]] | None = None,
    ) -> None:
        """Группа региситров для запроса.

        Parameters
        ----------
        fields: Iterable[Field[Any]]
            Перечень полей
        """


class Reader(object):
    """Подключение к Modbus TCP серверу."""

    def __init__(
        self,
        host: IPv4Address,
        port: int = 502,
        field_groups: Iterable[FieldGroup] | None = None,
    ) -> None:
        """Подключение к Modbus TCP серверу.

        Parameters
        ----------
        host: IPv4Address
            Адрес
        port: int
            Порт
        field_groups: Iterable[FieldGroup]
            Перечень групп запросов
        """
