from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO


import attr

from ..types import UNSET, Unset

from typing import cast
from typing import cast, List
from ..models.metadata_creators_item import MetadataCreatorsItem
from typing import Dict
from ..models.metadata_resource_type import MetadataResourceType
from typing import Union
from ..types import UNSET, Unset




T = TypeVar("T", bound="Metadata")

@attr.s(auto_attribs=True)
class Metadata:
    """  """
    resource_type: Union[Unset, MetadataResourceType] = UNSET
    creators: Union[Unset, List[MetadataCreatorsItem]] = UNSET
    title: Union[Unset, str] = UNSET
    publication_date: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        resource_type: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resource_type, Unset):
            resource_type = self.resource_type.to_dict()

        creators: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.creators, Unset):
            creators = []
            for creators_item_data in self.creators:
                creators_item = creators_item_data.to_dict()

                creators.append(creators_item)




        title = self.title
        publication_date = self.publication_date

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type
        if creators is not UNSET:
            field_dict["creators"] = creators
        if title is not UNSET:
            field_dict["title"] = title
        if publication_date is not UNSET:
            field_dict["publication_date"] = publication_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _resource_type = d.pop("resource_type", UNSET)
        resource_type: Union[Unset, MetadataResourceType]
        if isinstance(_resource_type,  Unset):
            resource_type = UNSET
        else:
            resource_type = MetadataResourceType.from_dict(_resource_type)




        creators = []
        _creators = d.pop("creators", UNSET)
        for creators_item_data in (_creators or []):
            creators_item = MetadataCreatorsItem.from_dict(creators_item_data)



            creators.append(creators_item)


        title = d.pop("title", UNSET)

        publication_date = d.pop("publication_date", UNSET)

        metadata = cls(
            resource_type=resource_type,
            creators=creators,
            title=title,
            publication_date=publication_date,
        )

        return metadata

