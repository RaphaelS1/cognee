import inspect
import json
import re
import warnings
from typing import Any
from uuid import UUID

from cognee.infrastructure.databases.relational import get_relational_engine

from ..models.Metadata import Metadata


async def write_metadata(data_item: Any) -> UUID:
    metadata_dict = get_metadata_dict(data_item)
    db_engine = get_relational_engine()
    async with db_engine.get_async_session() as session:
        metadata = Metadata(
            metadata=json.dumps(metadata_dict),
            metadata_source=parse_type(type(data_item)),
        )
        session.add(metadata)
        await session.commit()

        return metadata.id


def parse_type(type_: Any) -> str:
    pattern = r".+'([\w_\.]+)'"
    match = re.search(pattern, str(type_))
    if match:
        return match.group(1)
    else:
        raise Exception(f"type: {type_} could not be parsed")


def get_metadata_dict(metadata: Any) -> dict[str, Any]:
    if hasattr(metadata, "dict") and inspect.ismethod(getattr(metadata, "dict")):
        return metadata.dict()
    else:
        warnings.warn(
            f"metadata of type {type(metadata)}: {str(metadata)[:20]}... does not have dict method. Defaulting to string method"
        )
        try:
            return {"content": str(metadata)}
        except Exception as e:
            raise Exception(f"Could not cast metadata to string: {e}")
