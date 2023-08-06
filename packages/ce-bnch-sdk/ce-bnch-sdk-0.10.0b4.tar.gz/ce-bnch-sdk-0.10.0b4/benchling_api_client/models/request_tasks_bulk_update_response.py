from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.request_task import RequestTask

T = TypeVar("T", bound="RequestTasksBulkUpdateResponse")


@attr.s(auto_attribs=True)
class RequestTasksBulkUpdateResponse:
    """  """

    _tasks: List[RequestTask]

    def to_dict(self) -> Dict[str, Any]:
        tasks = []
        for tasks_item_data in self._tasks:
            tasks_item = tasks_item_data.to_dict()

            tasks.append(tasks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "tasks": tasks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tasks = []
        _tasks = d.pop("tasks")
        for tasks_item_data in _tasks:
            tasks_item = RequestTask.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        request_tasks_bulk_update_response = cls(
            tasks=tasks,
        )

        return request_tasks_bulk_update_response

    @property
    def tasks(self) -> List[RequestTask]:
        return self._tasks

    @tasks.setter
    def tasks(self, value: List[RequestTask]) -> None:
        self._tasks = value
