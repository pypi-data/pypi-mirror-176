from typing import Any, Dict, List, Type, TypeVar, Union
import datetime

from dateutil.parser import isoparse
import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Filter")


@attr.s(auto_attribs=True)
class Filter:
    """
    Attributes:
        metric_name (Union[Unset, str]): Name of the metric to filter on Example: cluster.bytes.in.
        instance_id (Union[Unset, str]): The Nile instance id to filter on Example: inst_02qwn8bovgrXdNx8XlVzbU.
        entity_type (Union[Unset, str]): The Nile entity type to filter on. This is ignored if entity_type is on a URL
            param. Example: cluster.
        organization_id (Union[Unset, str]): The Nile organization id to filter on Example: org_02qwn8bovgrXdNx8XlVzbU.
        start_time (Union[Unset, datetime.datetime]): The ISO-8601 formatted timestamp used to begin searching for
            matching metrics, i.e., 2018-11-13T20:20:39+00:00. If not provided the range will start from the epoch. Results
            returned are inclusive of this timestamp. Example: 2021-01-01 00:00:00+00:00.
        duration (Union[Unset, int]): The duration is added to from_timestamp to limit the time range of the query.
            i.e., the query will be restricted to metric.timestamp >= from_timestamp AND metric.timestamp < from_timestamp +
            duration.  If not provided or the duration is <=0 then the end timestamp is set to now Example: 600000.
    """

    metric_name: Union[Unset, str] = UNSET
    instance_id: Union[Unset, str] = UNSET
    entity_type: Union[Unset, str] = UNSET
    organization_id: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    duration: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metric_name = self.metric_name
        instance_id = self.instance_id
        entity_type = self.entity_type
        organization_id = self.organization_id
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        duration = self.duration

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metric_name is not UNSET:
            field_dict["metric_name"] = metric_name
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if entity_type is not UNSET:
            field_dict["entity_type"] = entity_type
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if duration is not UNSET:
            field_dict["duration"] = duration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metric_name = d.pop("metric_name", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        entity_type = d.pop("entity_type", UNSET)

        organization_id = d.pop("organization_id", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        duration = d.pop("duration", UNSET)

        filter_ = cls(
            metric_name=metric_name,
            instance_id=instance_id,
            entity_type=entity_type,
            organization_id=organization_id,
            start_time=start_time,
            duration=duration,
        )

        filter_.additional_properties = d
        return filter_

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
