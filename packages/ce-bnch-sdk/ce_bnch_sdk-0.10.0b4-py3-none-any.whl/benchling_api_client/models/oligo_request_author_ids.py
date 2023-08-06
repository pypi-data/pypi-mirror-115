from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="OligoRequestAuthorIds")


@attr.s(auto_attribs=True)
class OligoRequestAuthorIds:
    """  """

    _author_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        author_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._author_ids, Unset):
            author_ids = self._author_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        author_ids = cast(List[str], d.pop("authorIds", UNSET))

        oligo_request_author_ids = cls(
            author_ids=author_ids,
        )

        return oligo_request_author_ids

    @property
    def author_ids(self) -> List[str]:
        if isinstance(self._author_ids, Unset):
            raise NotPresentError(self, "author_ids")
        return self._author_ids

    @author_ids.setter
    def author_ids(self, value: List[str]) -> None:
        self._author_ids = value

    @author_ids.deleter
    def author_ids(self) -> None:
        self._author_ids = UNSET
